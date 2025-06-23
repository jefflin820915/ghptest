"""This module provides functions for analyzing the color composition of an image."""
import numpy as np
from PIL import Image


def is_mostly_blue(image_path: str, threshold: float = 0.5) -> bool:
    """Determines whether the majority of the image is in the blue color range.

    Args:
        image_path (str): Path to the image file.
        threshold (float): The minimum ratio of blue pixels required to return
          True. Default is 0.5 (50%).

    Returns:
        bool: True if the proportion of blue pixels exceeds the threshold,
          otherwise False.
    """
    image = Image.open(image_path)
    pixels = np.array(image.resize((100, 100), Image.BICUBIC))
    # Only blue color, and blue color is more than 100, and red color is less
    # than 20, and green color is less than 20
    blue_pixels = np.logical_and(
        pixels[:, :, 2] > 100,
        np.logical_and(
            pixels[:, :, 2] > pixels[:, :, 0] + 20,
            pixels[:, :, 2] > pixels[:, :, 1] + 20
        )
    )
    blue_count = np.count_nonzero(blue_pixels)
    total_pixels = pixels.shape[0] * pixels.shape[1]

    return (blue_count / total_pixels) >= threshold
