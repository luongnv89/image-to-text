"""OCR engine wrapper for text extraction using PaddleOCR."""

import threading
from typing import Optional

import numpy as np
from paddleocr import PaddleOCR


class OCREngine:
    """
    Singleton OCR engine for extracting text from images using PaddleOCR.

    This class provides a thread-safe singleton wrapper around PaddleOCR with
    English language support, ONNX acceleration, and angle classification for
    reliable text extraction from preprocessed book page images.

    The model is loaded only once on first instantiation and reused for all
    subsequent calls, providing significant performance improvements.

    Attributes:
        ocr: PaddleOCR instance configured with English language support
             and ONNX acceleration.
        _instance: Class-level singleton instance.
        _lock: Thread lock for thread-safe initialization.
    """

    _instance: Optional["OCREngine"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls) -> "OCREngine":
        """
        Create or retrieve the singleton instance in a thread-safe manner.

        Returns:
            The singleton OCREngine instance.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize OCR engine with angle classification on first instantiation.

        Subsequent calls reuse the loaded model without re-initialization.
        Model loading happens only once, providing significant performance
        improvements for repeated use.

        Note: ONNX acceleration is automatically used by PaddleOCR when
        onnxruntime is installed. Angle classification is enabled to handle
        rotated and upside-down text.
        """
        if self._initialized:
            return

        # Initialize PaddleOCR with angle classification
        # ONNX acceleration is automatically enabled if onnxruntime is available
        self.ocr = PaddleOCR(
            use_angle_cls=True,   # Enable angle classification to handle rotated text
            lang="en"              # English language support
        )
        self._initialized = True

    def extract_text(self, image: np.ndarray) -> str:
        """
        Extract text from a preprocessed image array.

        Processes the image using PaddleOCR to detect and recognize text,
        then returns the extracted text as a single concatenated string.
        Empty images return an empty string.

        Args:
            image: Preprocessed image as a numpy array (height, width, 3).

        Returns:
            Extracted text as a single concatenated string. Returns an
            empty string if no readable text is found.

        Example:
            >>> engine = OCREngine()
            >>> text = engine.extract_text(preprocessed_image)
            >>> print(text)
            "The quick brown fox..."
        """
        # Run OCR on the image
        result = self.ocr.ocr(image, cls=True)

        # Handle empty result
        if not result or not result[0]:
            return ""

        # Extract text from all detected text boxes
        texts = []
        for line in result:
            for text_box in line:
                if text_box and len(text_box) >= 2:
                    # text_box format: [[points], [text, confidence]]
                    text = text_box[1][0]
                    texts.append(text)

        # Join all text with spaces
        extracted_text = " ".join(texts)
        return extracted_text.strip()
