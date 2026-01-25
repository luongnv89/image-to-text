# OCR MVP Testing Guide

## Quick Start

### Run Tests on Example Image

```bash
# Activate virtual environment
source venv/bin/activate

# Test with preprocessing pipeline
python test_example_simple.py

# Or test with direct OCR
python test_example.py
```

### Run Unit Tests

```bash
source venv/bin/activate
pytest tests/ -v --cov=src/image_to_text
```

## Test Files

| File | Purpose | Status |
|------|---------|--------|
| `test_example_simple.py` | Real-world OCR on book page | ✅ 31+ regions detected |
| `test_example.py` | Direct PaddleOCR test | ⚠️ Requires paddlepaddle |
| `tests/test_preprocessing.py` | Unit tests for preprocessing | ✅ 7/7 passing |
| `tests/test_ocr_engine.py` | Unit tests for OCR engine | ✅ 7/7 passing |

## Expected Results

### Test Image: `data/example.png`

**Content**: Book page (Jayneen Sanders - "Would You Like to Play?")
**Size**: 773×1000 pixels, 83.5 KB
**Format**: PNG (JPEG data)

### Direct OCR Output

```
Text Regions Detected: 32
Average Confidence: 75.07%

Sample Extract:
"Meet Sam;, Rishi, Audrey; Ty and Zaral Six wonderful kids who are just
like kids everywhere: They love playing games, books making stuff and being
silly..."

High Confidence Detections (>90%):
- "and" (99.98%)
- "they" (99.98%)
- "000" (99.99%)
- "'My hope is that all kids be that child that says," (93.74%)
```

### Preprocessed OCR Output

```
Text Regions Detected: 31
Processing: Bilateral Filter → CLAHE Enhancement

Sample Extract:
"Meet Sam, Rishi, Audrey; Ty and Zaral Six wonderful kids who are just like
kids everywhere They love playing games_ books making stuff and being silly..."
```

## Performance Metrics

### CPU-Based Processing (macOS ARM64)

| Stage | Duration |
|-------|----------|
| Model Initialization | 15-20 seconds |
| Image Preprocessing | <1 second |
| OCR Processing | 20-30 seconds |
| **First Run Total** | 40-50 seconds |
| **Subsequent Runs** | 20-30 seconds |

### GPU Expected (with CUDA/Metal)

| Stage | Duration |
|-------|----------|
| Model Initialization | 5-10 seconds |
| Image Preprocessing | <1 second |
| OCR Processing | 0.5 seconds |
| **First Run Total** | 5-15 seconds |
| **Subsequent Runs** | <0.5 seconds |

## Troubleshooting

### Issue: ModuleNotFoundError: paddle

**Cause**: PaddleOCR requires PaddlePaddle, which has limited platform support

**Solution**: Use `test_example_simple.py` which uses EasyOCR instead

```bash
python test_example_simple.py
```

### Issue: No text detected in preprocessed image

**Possible Causes**:
1. Preprocessing parameters too aggressive
2. Image quality too low
3. OCR model not suitable for image type

**Solution**: Adjust CLAHE parameters in `src/image_to_text/preprocessing.py`:

```python
clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(12, 12))
# Try different values:
# clipLimit: 1.5-3.0 (higher = more contrast)
# tileGridSize: (8,8) to (16,16) (larger = broader enhancement)
```

### Issue: Low confidence scores

**Typical Range**: 50-95% for book pages
**Average Expected**: 70-80%

**If Below 50%**:
- Image quality may be poor
- Font size too small
- Heavy shadows or reflections
- Try preprocessing with different parameters

## Integration Examples

### Basic Usage

```python
from image_to_text import preprocess_image, OCREngine

# Initialize engine
engine = OCREngine()

# Preprocess and extract text
preprocessed = preprocess_image("book_page.png")
text = engine.extract_text(preprocessed)

print(text)
```

### Batch Processing

```python
from pathlib import Path
from image_to_text import preprocess_image, OCREngine

engine = OCREngine()
image_dir = Path("books/pages")

for image_path in image_dir.glob("*.png"):
    try:
        preprocessed = preprocess_image(str(image_path))
        text = engine.extract_text(preprocessed)
        print(f"{image_path.name}: {text[:100]}...")
    except FileNotFoundError as e:
        print(f"Error processing {image_path}: {e}")
```

### With Confidence Filtering

```python
from image_to_text import OCREngine
import easyocr

# For more detailed results with confidence scores
engine = OCREngine()
preprocessed = preprocess_image("book_page.png")

# Use easyocr directly for confidence values
reader = easyocr.Reader(['en'], gpu=False)
results = reader.readtext(preprocessed)

# Filter by confidence threshold
high_confidence = [
    (text, conf) for bbox, text, conf in results if conf > 0.80
]

for text, conf in high_confidence:
    print(f"{text}: {conf:.2%}")
```

## Validation Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Example image exists (`data/example.png`)
- [ ] Test script runs without errors
- [ ] Text regions detected (>20)
- [ ] Confidence scores in range (>50%)
- [ ] No unexpected exceptions raised

## Advanced Testing

### Performance Profiling

```bash
pip install py-spy
py-spy record -o profile.svg -- python test_example_simple.py
```

### Memory Usage

```bash
pip install memory-profiler
python -m memory_profiler test_example_simple.py
```

### Debugging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from image_to_text import preprocess_image

# Will show detailed processing steps
preprocessed = preprocess_image("book_page.png")
```

## Reporting Issues

When reporting test failures:

1. **Include environment info**:
   ```bash
   python --version
   pip list | grep -E "opencv|numpy|easyocr|paddleocr"
   ```

2. **Provide test output**:
   ```bash
   python test_example_simple.py > test_output.log 2>&1
   ```

3. **Include image info**:
   ```bash
   file data/example.png
   identify data/example.png  # if ImageMagick installed
   ```

## Reference

- **Implementation**: `src/image_to_text/`
- **Tests**: `tests/`
- **Results**: `TEST_RESULTS.md`
- **Guide**: `README_IMPLEMENTATION.md`
- **Spec**: `openspec/changes/implement-core-mvp/`
