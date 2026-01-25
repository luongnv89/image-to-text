# Image-to-Text OCR MVP Implementation

## Overview

This is the core MVP implementation of the image-to-text OCR system. It provides foundational OCR functionality to extract text from book page images using state-of-the-art libraries.

## Project Structure

```
image-to-text/
├── src/
│   └── image_to_text/
│       ├── __init__.py           # Module initialization and exports
│       ├── preprocessing.py       # Image preprocessing pipeline
│       └── ocr_engine.py         # OCR engine wrapper using PaddleOCR
├── tests/
│   ├── __init__.py
│   ├── test_preprocessing.py     # Tests for image preprocessing
│   └── test_ocr_engine.py        # Tests for OCR engine
├── requirements.txt              # Python dependencies
├── setup.py                      # Project setup with GPU detection
├── pytest.ini                    # Pytest configuration
├── conftest.py                   # Pytest path configuration
└── run_tests.sh                  # Test runner script
```

## Features

### 1. Image Preprocessing (`preprocessing.py`)

The `preprocess_image()` function optimizes images for OCR accuracy:

- **File Validation**: Validates image file existence and readability
- **Shadow Removal**: Uses morphological operations and inpainting to remove lighting variations common in book page photographs
- **Contrast Enhancement**: Applies CLAHE (Contrast Limited Adaptive Histogram Equalization) in LAB color space for improved text readability
- **Color Space Optimization**: Works in LAB color space for perceptually-informed enhancement

**Usage:**
```python
from image_to_text import preprocess_image

preprocessed = preprocess_image("book_page.jpg")
```

### 2. OCR Engine (`ocr_engine.py`)

The `OCREngine` class provides text extraction using PaddleOCR:

- **English Language Support**: Configured for English text recognition
- **Angle Detection**: Includes `use_angle_cls=True` for rotated text handling
- **Text Confidence Filtering**: Processes confidence scores from PaddleOCR
- **Robust Handling**: Returns empty string for images with no readable text instead of raising exceptions

**Usage:**
```python
from image_to_text import OCREngine, preprocess_image

engine = OCREngine()
preprocessed = preprocess_image("book_page.jpg")
text = engine.extract_text(preprocessed)
print(text)
```

## Installation

### Prerequisites
- Python 3.8+
- Virtual environment recommended

### Setup Steps

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   python setup.py
   ```

   Or manually with pip:
   ```bash
   pip install -r requirements.txt
   ```

### GPU Support

The `setup.py` script automatically detects GPU availability and installs:
- `paddlepaddle-gpu` and `onnxruntime-gpu` if CUDA is detected
- `paddlepaddle` and `onnxruntime` for CPU-only systems

## Running Tests

Execute the test suite:

```bash
./run_tests.sh
```

Or directly with pytest:

```bash
pytest tests/ -v
```

With coverage reporting:

```bash
pytest tests/ -v --cov=src/image_to_text --cov-report=term-missing
```

## Dependencies

### Core Dependencies
- **paddlepaddle** (>=2.5.0): PaddlePaddle deep learning framework
- **paddleocr** (>=2.7.0): PaddleOCR engine for text recognition
- **onnxruntime** (>=1.15.0): ONNX Runtime for inference acceleration
- **opencv-python-headless** (>=4.8.0): Computer vision library for image processing
- **numpy** (>=1.24.0): Numerical computing library

### Optional Dependencies
- **Pillow** (>=9.5.0): Additional image format support

### Development Dependencies
- **pytest** (>=7.4.0): Testing framework
- **pytest-cov** (>=4.1.0): Code coverage plugin

## Performance Targets

The implementation is designed to meet the following performance targets:
- **GPU**: <0.5 seconds per image
- **CPU**: <2.0 seconds per image

## API Reference

### `preprocess_image(image_path: str) -> np.ndarray`

Preprocess an image for optimal OCR performance.

**Parameters:**
- `image_path` (str): Path to the image file to preprocess

**Returns:**
- `np.ndarray`: Preprocessed image as a numpy array (RGB format)

**Raises:**
- `FileNotFoundError`: If the image file does not exist or cannot be read

### `OCREngine`

OCR engine wrapper for text extraction using PaddleOCR.

#### `__init__()`
Initialize OCR engine with English language support and angle detection.

#### `extract_text(image: np.ndarray) -> str`

Extract text from a preprocessed image array.

**Parameters:**
- `image` (np.ndarray): Preprocessed image as numpy array (height, width, 3)

**Returns:**
- `str`: Extracted text as a concatenated string. Empty string if no readable text is found.

## Code Quality

The implementation follows:
- **PEP 8** naming conventions
- **Type hints** for all function signatures
- **Google-style docstrings** for public functions and classes
- **Comprehensive unit tests** for all major components

## Testing Coverage

The test suite includes:

### Preprocessing Tests
- Valid image preprocessing
- File path validation and error handling
- Output format and range validation
- Shadow removal verification
- Contrast enhancement verification
- Image dimension preservation

### OCR Engine Tests
- Engine initialization
- Text extraction from various image types
- Handling of blank images
- Text extraction from preprocessed images
- Output type validation
- Various image sizes
- Robust error handling

## Future Enhancements

Potential improvements for future iterations:
- Multi-language support
- Confidence score reporting
- Batch image processing
- Performance optimization with model quantization
- Support for handwritten text
- Document layout analysis
