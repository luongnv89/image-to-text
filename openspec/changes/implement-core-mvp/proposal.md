# Change: Implement Core OCR MVP

## Why
Build the foundational OCR functionality to extract text from book page images using state-of-the-art libraries, establishing the core capability for the entire project.

## What Changes
- **NEW** Environment setup with performance-optimized dependencies (PaddleOCR, ONNX Runtime, OpenCV)
- **NEW** Image preprocessing pipeline for book page optimization (shadow removal, contrast enhancement)
- **NEW** Basic OCR engine wrapper using PaddleOCR with English language support
- **NEW** Text extraction and processing pipeline with confidence filtering

## Impact
- **Affected specs**: `specs/ocr-engine/spec.md` (new capability)
- **Project structure**: Creates the core module foundation
- **Dependencies**: Establishes the technology stack for the entire project
- **Performance**: Sets up the foundation for meeting <0.5s GPU / <2.0s CPU targets