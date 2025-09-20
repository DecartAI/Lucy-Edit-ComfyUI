from . import utils
import torch


class LucyEditProAPINode:
    """
    A ComfyUI node that edits video using the Decart API.

    This node takes video frames, a text prompt describing desired edits,
    and an API key, then returns the edited video using Decart's Lucy-Edit-Pro model.

    Input formats:
    - images: ComfyUI IMAGE tensor with shape [frames, height, width, channels=3]
              Expected dtype: float32 with values in range [0.0, 1.0]
              Color format: RGB
    - prompt: String describing the desired video edits
    - api_key: Valid Decart API key for authentication
    - fps: Frame rate (float, default: 24.0)

    Output formats:
    - images: Edited video as ComfyUI IMAGE tensor
              Shape: [frames, height, width, channels=3]
              dtype: float32 with values in range [0.0, 1.0]
              Color format: RGB
    - fps: Frame rate of the output video (may differ from input)
    """

    CATEGORY = "video/editing"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),  # ComfyUI uses IMAGE type for video frames
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "api_key": ("STRING", {"default": ""}),
                "fps": (
                    "FLOAT",
                    {"default": 24.0, "min": 0.01, "max": 1000.0, "step": 0.01},
                ),
            }
        }

    RETURN_TYPES = ("IMAGE", "FLOAT")
    RETURN_NAMES = ("images", "fps")
    FUNCTION = "process_video"

    def process_video(self, images, prompt, api_key, fps):
        """
        Edit video using the Decart API based on the provided prompt.

        Args:
            images: Input video tensor with shape [frames, height, width, channels=3]
                   Expected dtype: float32 with values in range [0.0, 1.0]
                   Color format: RGB
            prompt: Text description of desired video edits (e.g., "Change the shirt to blue")
            api_key: Valid Decart API key for authentication
            fps: Input frame rate (float)

        Returns:
            tuple: (output_images, output_fps)
                - output_images: Edited video tensor with same format as input
                                Shape: [frames, height, width, channels=3]
                                dtype: float32, range: [0.0, 1.0], RGB format
                - output_fps: Frame rate of the edited video (may differ from input)

        Raises:
            Exception: If API call fails or video processing encounters an error
        """
        output_images, output_fps = utils.generate_edited_video_tensor(images, prompt, api_key, fps)

        return (output_images, output_fps)


class LucyConditionConcatNode:
    """
    A ComfyUI node that concatenates additional latents to the input channels
    for conditioning during diffusion. The additional latents are concatenated
    via c_concat and properly handled during the diffusion process.

    This is designed for models with doubled input channels (like WAN2.2)
    where the extra channels are used for conditioning.
    """

    CATEGORY = "conditioning/latent"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "concat_latent": ("LATENT",),  # Additional latent to concatenate
            }
        }

    RETURN_NAMES = ("model", "latent")
    RETURN_TYPES = ("MODEL", "LATENT")
    FUNCTION = "apply_concat"

    def apply_concat(self, model, concat_latent):
        """
        Apply channel concatenation conditioning to the model.

        Args:
            model: The diffusion model (ModelPatcher)
            concat_latent: Dict with "samples" tensor to concatenate

        Returns:
            tuple: (modified_model, modified_conditioning)
        """
        # Clone model to avoid affecting other nodes
        model = model.clone()

        # Get the concatenation latent tensor
        concat_tensor = concat_latent["samples"].clone()

        # Normalize the concat_tensor with the same parameters as the main latent
        if hasattr(model.model, 'process_latent_in'):
            concat_tensor = model.model.process_latent_in(concat_tensor)

        # Store the concat latent in model options for proper handling
        # This will be used during the diffusion process
        model.model_options = model.model_options.copy()

        # Initialize the latent tensor
        latent = torch.zeros_like(concat_tensor)

        # Create a wrapper function that will handle the concatenation during the diffusion steps
        def concat_wrapper(model_function, params):
            nonlocal concat_tensor

            x = params["input"]
            t = params["timestep"]
            c = params["c"].copy()

            # Ensure concat_tensor matches batch size
            if x.shape[0] != concat_tensor.shape[0]:
                if concat_tensor.shape[0] == 1:
                    concat_tensor = concat_tensor.repeat(
                        (x.shape[0],) + (1,) * (concat_tensor.ndim - 1)
                    )
                else:
                    raise ValueError(
                        f"Batch size of concat_tensor and x do not match: {concat_tensor.shape[0]} != {x.shape[0]}"
                    )

            # Ensure spatial dimensions match
            if x.shape != concat_tensor.shape:
                raise ValueError(
                    f"Spatial dimensions of concat_tensor and x do not match: {x.shape} != {concat_tensor.shape}"
                )

            # Move to same device and dtype as input
            concat_tensor = concat_tensor.to(x.device, dtype=x.dtype)

            # Add c_concat to the conditioning dictionary
            c["c_concat"] = concat_tensor

            # Call the original model function with the modified conditioning
            return model_function(x, t, **c)

        # Set the wrapper function
        model.set_model_unet_function_wrapper(concat_wrapper)
        out_latent = {}
        out_latent["samples"] = latent

        return (model, out_latent)
