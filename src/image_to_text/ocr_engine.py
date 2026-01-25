"""OCR engine wrapper for text extraction using PaddleOCR."""

import numpy as np
from paddleocr import PaddleOCR


class OCREngine:
    """
    OCR engine for extracting text from images using PaddleOCR.

    This class provides a wrapper around PaddleOCR with English language
    support and text confidence filtering for reliable text extraction
    from preprocessed book page images.

    Attributes:
        ocr: PaddleOCR instance configured with English language support.
    """

    def __init__(self) -> None:
        """Initialize OCR engine with English language support."""
        self.ocr = PaddleOCR(use_angle_cls=True, lang="en")

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
