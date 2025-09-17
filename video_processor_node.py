from . import utils


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
                "fps": ("FLOAT", {"default": 24.0, "min": 0.01, "max": 1000.0, "step": 0.01}),
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