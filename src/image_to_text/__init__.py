"""Core image-to-text OCR module."""

from .ocr_engine import OCREngine
from .preprocessing import preprocess_image

__all__ = ["OCREngine", "preprocess_image"]
__version__ = "0.1.0"
