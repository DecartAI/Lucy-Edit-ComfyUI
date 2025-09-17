"""
Video processing utilities for ComfyUI custom node.

This module provides functions for video tensor manipulation, format conversion,
and API communication with the Decart video generation service.

Key data formats and conventions:
- Video tensors: torch.Tensor with shape [frames, height, width, channels]
- Color format: RGB (not BGR)
- Data type: float32 with values in range [0.0, 1.0] for tensors
- Frame rate: float (typically 24.0 fps)
- Video codec: MP4V for temporary files
"""

import io
import tempfile
from typing import Tuple

import cv2
import numpy as np
import requests
import torch

API_URL = "https://api3.decart.ai/v1/generate/lucy-pro-v2v"

def save_video(video: torch.Tensor, output_path: str, fps: float=24.0) -> None:
    """
    Save a video tensor to a file.

    Args:
        video: Video tensor with shape [frames, height, width, channels=3]
               Expected dtype: float32 with values in range [0.0, 1.0] or torch.uint8 with values in range [0, 255]
               Color format: RGB
        output_path: Path where the video file will be saved
        fps: Frame rate for the output video (default: 24.0)

    Note:
        - Uses MP4V codec for broad compatibility
    """
    np_video = video.detach().cpu().numpy()

    # Convert from float32 to uint8 if needed
    if np_video.dtype != np.uint8:
        # Assuming the video is in range [0, 1], scale to [0, 255]
        np_video = (np_video * 255).astype(np.uint8)

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # pyright: ignore[reportAttributeAccessIssue]
    height, width = np_video.shape[1:3]
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    for frame in np_video:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) # pyright: ignore[reportCallIssue,reportArgumentType]
        writer.write(frame)
    writer.release()

def get_video_bytes_from_tensor(frames: torch.Tensor, fps: float) -> bytes:
    """
    Convert a video tensor to MP4 bytes.

    Args:
        frames: Video tensor with shape [frames, height, width, channels=3]
               Expected dtype: float32 with values in range [0.0, 1.0] or torch.uint8 with values in range [0, 255]
               Color format: RGB
        fps: Frame rate for the video encoding

    Returns:
        bytes: MP4 video data as bytes

    Note:
        Uses a temporary file for conversion.
    """
    with tempfile.NamedTemporaryFile(suffix=".mp4") as f:
        save_video(frames, f.name, fps)
        video_bytes = f.read()
    return video_bytes

def get_tensor_from_video_bytes(video_bytes: bytes) -> Tuple[torch.Tensor, float]:
    """
    Convert MP4 video bytes to a video tensor.

    Args:
        video_bytes: MP4 video data as bytes

    Returns:
        Tuple containing:
        - video_tensor: torch.Tensor with shape [frames, height, width, channels=3]
                       dtype: float32 with values in range [0.0, 1.0]
                       Color format: RGB
        - fps: Frame rate extracted from the video file

    Raises:
        Exception: If no frames are found in the video

    Note:
        - Values are clamped to ensure valid range
    """
    with tempfile.NamedTemporaryFile(suffix=".mp4") as f:
        f.write(video_bytes)
        f.flush()
        cap = cv2.VideoCapture(f.name)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)
        cap.release()

    if len(frames) == 0:
        raise Exception("No frames found in video")

    video_tensor = (torch.from_numpy(np.stack(frames)).float() / 255.0).clamp(0.0, 1.0)
    return video_tensor, fps

def generate_edited_video_tensor(video: torch.Tensor, prompt: str, api_key: str, fps: float) -> Tuple[torch.Tensor, float]:
    """
    Generate an edited video using the Decart API.

    Args:
        video: Input video tensor with shape [frames, height, width, channels=3]
               Expected dtype: float32 with values in range [0.0, 1.0] or torch.uint8 with values in range [0, 255]
               Color format: RGB
        prompt: Text description of the desired video edits
        api_key: API key for the Decart service
        fps: Frame rate for video processing

    Returns:
        Tuple containing:
        - edited_video: torch.Tensor with shape [frames, height, width, channels=3]
                       dtype: float32 with values in range [0.0, 1.0]
                       Color format: RGB
        - output_fps: Frame rate of the generated video

    Raises:
        Exception: If the API call fails or output processing fails

    Note:
        This is a high-level function that handles tensor-to-bytes conversion,
        API communication, and bytes-to-tensor conversion automatically.
    """
    video_bytes = get_video_bytes_from_tensor(video, fps)
    output_video_bytes = generate_edited_video_bytes(video_bytes, prompt, api_key)
    try:
        return get_tensor_from_video_bytes(output_video_bytes)
    except Exception as e:
        raise Exception(f"Failed to get tensor from output video bytes: {e}")


def generate_edited_video_bytes(video_bytes: bytes, prompt: str, api_key: str) -> bytes:
    """
    Send video bytes to Decart API for editing and return the result.

    Args:
        video_bytes: MP4 video data as bytes
        prompt: Text description of desired video edits
        api_key: API key for authentication with Decart service

    Returns:
        bytes: Edited video as MP4 bytes

    Raises:
        Exception: If the API request fails (non-200 status code)

    Note:
        - Uses multipart form data with video file attachment
        - Requires valid API key for authentication
    """
    video_buffer = io.BytesIO(video_bytes)

    formData = {
        "prompt": prompt
    }

    files = {
        "data": ("video.mp4", video_buffer, "video/mp4")
    }

    response = requests.post(
        API_URL,
        headers={"X-API-KEY": api_key},
        data=formData,
        files=files
    )
    if response.status_code != 200:
        raise Exception(f"Failed to generate edited video: {response.status_code} {response.text}")

    return response.content

