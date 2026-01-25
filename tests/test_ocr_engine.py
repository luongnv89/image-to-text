"""Unit tests for OCR engine module."""

import tempfile
from pathlib import Path

import cv2
import numpy as np
import pytest

from image_to_text.ocr_engine import OCREngine
from image_to_text.preprocessing import preprocess_image


@pytest.fixture
def ocr_engine():
    """Create an OCR engine instance."""
    return OCREngine()


@pytest.fixture
def simple_text_image():
    """Create a simple image with readable text."""
    img = np.ones((200, 400, 3), dtype=np.uint8) * 255
    # Add text to the image
    cv2.putText(img, "Hello World", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
    return img


@pytest.fixture
def blank_image():
    """Create a blank image with no text."""
    return np.ones((200, 400, 3), dtype=np.uint8) * 255


def test_ocr_engine_initialization(ocr_engine):
    """Test OCR engine initialization."""
    assert ocr_engine is not None
    assert ocr_engine.ocr is not None


def test_extract_text_from_simple_image(ocr_engine, simple_text_image):
    """Test text extraction from a simple image."""
    text = ocr_engine.extract_text(simple_text_image)
    assert isinstance(text, str)
    # The extracted text should contain some content
    assert len(text) > 0


def test_extract_text_from_blank_image(ocr_engine, blank_image):
    """Test that blank image returns empty string."""
    text = ocr_engine.extract_text(blank_image)
    assert isinstance(text, str)
    assert text == ""


def test_extract_text_with_preprocessed_image(ocr_engine, simple_text_image):
    """Test text extraction from preprocessed image."""
    # Create a temporary image file
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp_path = tmp.name
        img_bgr = cv2.cvtColor(simple_text_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(tmp_path, img_bgr)

    # Preprocess and extract
    preprocessed = preprocess_image(tmp_path)
    text = ocr_engine.extract_text(preprocessed)

    Path(tmp_path).unlink()

    assert isinstance(text, str)


def test_extract_text_returns_string(ocr_engine, simple_text_image):
    """Test that extract_text returns a string type."""
    result = ocr_engine.extract_text(simple_text_image)
    assert isinstance(result, str)


def test_extract_text_with_different_image_sizes(ocr_engine):
    """Test OCR engine with various image sizes."""
    sizes = [(100, 200), (300, 300), (500, 1000)]
    for height, width in sizes:
        img = np.ones((height, width, 3), dtype=np.uint8) * 255
        cv2.putText(img, "Test", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1)
        text = ocr_engine.extract_text(img)
        assert isinstance(text, str)


def test_extract_text_handles_no_text_boxes(ocr_engine):
    """Test handling of images with no detectable text."""
    # Create a gradient image (no clear text)
    gradient = np.zeros((200, 200, 3), dtype=np.uint8)
    for i in range(200):
        gradient[i, :] = int(255 * i / 200)
    text = ocr_engine.extract_text(gradient)
    assert isinstance(text, str)
