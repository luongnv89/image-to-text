## Project: High-Performance OCR Module
**Context:** A reusable, optimized Python module that takes a local image path and returns extracted text.
**Core Requirement:** Maximum performance using State-of-the-Art (SOTA) libraries.

---

## Phase 1: Core Implementation (MVP)
**Goal:** Build the functional logic to convert an image file to text using the optimal stack.

### Task 1.1: Environment & Dependency Definition
*   **Description:** specific versions of libraries to ensure compatibility and performance.
*   **Acceptance Criteria:**
    *   `requirements.txt` created containing:
        *   `paddlepaddle` (or `paddlepaddle-gpu` if hardware supports it)
        *   `paddleocr>=2.7`
        *   `onnxruntime-gpu` (for production speed) or `onnxruntime`
        *   `opencv-python-headless`
    *   Virtual environment setup and installation successful.

### Task 1.2: Image Pre-processing Utility
*   **Description:** Implement a helper function to prepare the image for the OCR engine. Since inputs are phone photos, we must handle noise and shadows to ensure accuracy.
*   **Acceptance Criteria:**
    *   Function `preprocess_image(image_path: str) -> np.array` created.
    *   Validates the file path exists.
    *   Loads image using OpenCV (`cv2.imread`).
    *   Applies basic shadow removal/contrast enhancement (crucial for book pages).

### Task 1.3: OCR Engine Integration (PaddleOCR)
*   **Description:** Implement the basic wrapper around the PaddleOCR library.
*   **Acceptance Criteria:**
    *   Module initializes `PaddleOCR` with `lang='en'`.
    *   Function extracts text from the pre-processed image array.
    *   Returns a simple string (joined text).

---

## Phase 2: Performance Optimization & Reliability
**Goal:** Refactor the MVP into a production-ready class that meets the "maximum performance" requirement.

### Task 2.1: Implement Singleton Pattern
*   **Description:** The OCR model takes 1-2 seconds to load. You cannot afford this penalty on every function call. Wrap the engine in a Singleton class.
*   **Acceptance Criteria:**
    *   Class `BookOCR` created.
    *   Model loading happens only on the first instantiation.
    *   Subsequent calls reuse the loaded model from memory.

### Task 2.2: Enable ONNX & Acceleration
*   **Description:** Switch the inference backend from standard PyTorch to ONNX Runtime for significant speed gains.
*   **Acceptance Criteria:**
    *   PaddleOCR instantiation updated with `use_onnx=True`.
    *   `use_angle_cls=True` enabled (to handle rotated/upside-down book photos automatically).
    *   CPU/GPU providers configured correctly in ONNX settings.

### Task 2.3: The Interface Wrapper
*   **Description:** Create the final, simple entry point function requested.
*   **Acceptance Criteria:**
    *   Function signature: `def convert_book_to_text(image_path: str) -> str`.
    *   Internal logic:
        1.  Get `BookOCR` instance.
        2.  Pre-process image at `image_path`.
        3.  Run inference.
        4.  Filter low-confidence garbage (< 50%).
        5.  Join and return clean string.
    *   Error handling: Returns empty string or raises specific custom Exception if image is unreadable.

---

## Phase 3: Validation
**Goal:** Verify the module works as a "black box" input/output system.

### Task 3.1: Unit Testing
*   **Description:** create a test suite to verify functionality.
*   **Acceptance Criteria:**
    *   Test case: Valid image path -> Returns correct text.
    *   Test case: Invalid path -> Raises `FileNotFoundError`.
    *   Test case: Non-text image -> Returns empty string (graceful failure).

### Task 3.2: Performance Benchmark
*   **Description:** Verify the optimization works.
*   **Acceptance Criteria:**
    *   Script created to process 10 images in a loop.
    *   Average processing time per image (after initial load) is < 0.5s (GPU) or < 2.0s (CPU).

---

## Final Output Structure
When completed, the usage in your main application will look exactly like this:

```python
from my_ocr_module import convert_book_to_text

# The first call takes ~1.5s (loads model)
text1 = convert_book_to_text("/path/to/page1.jpg")

# All subsequent calls take ~0.2s (fast)
text2 = convert_book_to_text("/path/to/page2.jpg")
```