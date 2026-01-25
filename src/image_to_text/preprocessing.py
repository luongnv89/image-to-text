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

    # Apply light denoising while preserving text edges
    image = cv2.bilateralFilter(image, 9, 75, 75)

    # Convert to LAB color space for better contrast enhancement
    lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)

    # Apply moderate CLAHE to enhance text contrast
    # Tuned for book pages: higher clip limit for more enhancement
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(12, 12))
    l = clahe.apply(l)

    # Merge back to LAB
    lab = cv2.merge([l, a, b])

    # Convert back to RGB
    image = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

    # Normalize to 0-255 range
    image = np.clip(image, 0, 255).astype(np.uint8)

    return image
