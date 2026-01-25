"""Unit tests for image preprocessing module."""

import tempfile
from pathlib import Path

import cv2
import numpy as np
import pytest

from image_to_text.preprocessing import preprocess_image


@pytest.fixture
def sample_image():
    """Create a sample test image."""
    # Create a simple test image with text-like patterns
    img = np.ones((200, 400, 3), dtype=np.uint8) * 255
    # Add some text-like patterns
    cv2.rectangle(img, (50, 50), (350, 150), (0, 0, 0), 2)
    cv2.putText(img, "Test Image", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    return img


@pytest.fixture
def temp_image_path(sample_image):
    """Create a temporary image file."""
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp_path = tmp.name
        # Convert RGB to BGR for OpenCV
        img_bgr = cv2.cvtColor(sample_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(tmp_path, img_bgr)
    yield tmp_path
    # Cleanup
    Path(tmp_path).unlink()


def test_preprocess_image_valid_input(temp_image_path):
    """Test preprocessing with a valid image file."""
    result = preprocess_image(temp_image_path)
    assert isinstance(result, np.ndarray)
    assert result.dtype == np.uint8
    assert result.shape[2] == 3  # RGB image
    assert result.shape[0] > 0 and result.shape[1] > 0


def test_preprocess_image_output_range(temp_image_path):
    """Test that preprocessed image values are in valid range."""
    result = preprocess_image(temp_image_path)
    assert result.min() >= 0
    assert result.max() <= 255


def test_preprocess_image_nonexistent_file():
    """Test preprocessing with a non-existent file path."""
    with pytest.raises(FileNotFoundError):
        preprocess_image("/nonexistent/path/to/image.jpg")


def test_preprocess_image_invalid_path_type():
    """Test preprocessing with invalid path type."""
    with pytest.raises(FileNotFoundError):
        preprocess_image(12345)


def test_preprocess_image_preserves_dimensions(temp_image_path, sample_image):
    """Test that preprocessing preserves original image dimensions."""
    result = preprocess_image(temp_image_path)
    assert result.shape[0] == sample_image.shape[0]
    assert result.shape[1] == sample_image.shape[1]
    assert result.shape[2] == 3


def test_preprocess_image_shadow_removal(temp_image_path):
    """Test that shadow removal is applied."""
    original = cv2.imread(temp_image_path)
    original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    result = preprocess_image(temp_image_path)
    # Result should be different from original due to preprocessing
    assert not np.array_equal(original, result)


def test_preprocess_image_contrast_enhancement(temp_image_path):
    """Test that contrast enhancement is applied."""
    # Create a low-contrast image
    low_contrast = np.ones((100, 100, 3), dtype=np.uint8) * 150
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp_path = tmp.name
        img_bgr = cv2.cvtColor(low_contrast, cv2.COLOR_RGB2BGR)
        cv2.imwrite(tmp_path, img_bgr)

    result = preprocess_image(tmp_path)
    Path(tmp_path).unlink()
    # Result should have better contrast (higher variance)
    assert result.std() > low_contrast.std()
