"""Image preprocessing utilities for OCR optimization."""

import os
from pathlib import Path

import cv2
import numpy as np


def preprocess_image(image_path: str) -> np.ndarray:
    """
    Preprocess an image for optimal OCR performance.

    Loads an image from the given path and applies preprocessing techniques
    including shadow removal and contrast enhancement to optimize text
    recognition accuracy for book page images.

    Args:
        image_path: Path to the image file to preprocess.

    Returns:
        Preprocessed image as a numpy array suitable for OCR input.

    Raises:
        FileNotFoundError: If the image file does not exist or cannot be read.

    Example:
        >>> preprocessed = preprocess_image("book_page.jpg")
        >>> print(preprocessed.shape)
        (height, width, 3)
    """
    # Validate file path
    if not isinstance(image_path, str):
        raise FileNotFoundError(f"Image path must be a string, got {type(image_path)}")

    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Load image
    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(f"Failed to read image file: {image_path}")

    # Convert to RGB for processing
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Apply shadow removal using morphological operations
    # Convert to grayscale for shadow analysis
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Create shadow mask using threshold
    _, shadow_mask = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Apply morphological closing to fill small holes
    kernel = cv2.getStructuringElement(cv2.MORPH_CLOSE, (5, 5))
    shadow_mask = cv2.morphologyEx(shadow_mask, cv2.MORPH_CLOSE, kernel)

    # Dilate shadow mask slightly to remove shadow boundaries
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    shadow_mask = cv2.dilate(shadow_mask, kernel, iterations=1)

    # Apply shadow removal using inpainting
    shadow_mask = cv2.cvtColor(shadow_mask, cv2.COLOR_GRAY2RGB)
    image = cv2.inpaint(image, cv2.cvtColor(shadow_mask, cv2.COLOR_RGB2GRAY), 3, cv2.INPAINT_TELEA)

    # Convert to LAB color space for better contrast enhancement
    lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)

    # Merge back to LAB
    lab = cv2.merge([l, a, b])

    # Convert back to RGB
    image = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

    # Normalize to 0-255 range
    image = np.clip(image, 0, 255).astype(np.uint8)

    return image
