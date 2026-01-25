# Project Context

## Purpose
High-performance OCR (Optical Character Recognition) module for extracting text from book page images. The project aims to create a reusable, optimized Python module that takes a local image path and returns extracted text with maximum performance using State-of-the-Art (SOTA) libraries.

## Tech Stack
- **Python 3.8+** - Primary programming language
- **PaddleOCR >= 2.7** - Main OCR engine with SOTA performance
- **PaddlePaddle** - Deep learning framework (CPU or GPU version)
- **ONNX Runtime** - Inference acceleration (onnxruntime or onnxruntime-gpu)
- **OpenCV (opencv-python-headless)** - Image preprocessing and manipulation
- **NumPy** - Array operations for image processing

## Project Conventions

### Code Style
- **PEP 8 compliant** Python code
- **Type hints** required for all function signatures
- **Docstrings** following Google style for all public functions
- **Snake_case** for variable and function names
- **PascalCase** for class names
- **UPPER_CASE** for constants

### Architecture Patterns
- **Singleton Pattern** for OCR engine to avoid model loading overhead
- **Factory Pattern** for creating OCR instances with different configurations
- **Utility Functions** for image preprocessing (separate concerns)
- **Error Handling** with custom exceptions for specific failure modes
- **Performance-First** design with lazy loading and caching

### Testing Strategy
- **Unit Tests** using pytest framework
- **Test Coverage** minimum 80% for core functionality
- **Performance Benchmarks** to verify optimization goals
- **Mock Testing** for external dependencies
- **Integration Tests** for end-to-end workflows

### Git Workflow
- **Feature Branches** for new development
- **Descriptive Commit Messages** following conventional commits
- **Pull Requests** required for code review
- **Semantic Versioning** for releases
- **No Direct Commits** to main branch

## Domain Context
This project specializes in OCR for book page images captured with mobile phones. Key domain considerations:
- **Shadow Removal** - Book pages often have lighting variations
- **Contrast Enhancement** - Improves text readability
- **Rotation Handling** - Automatic detection of rotated/upside-down images
- **Confidence Filtering** - Remove low-confidence OCR results (< 50%)
- **Performance Optimization** - Target < 0.5s per image (GPU) or < 2.0s (CPU)

## Important Constraints
- **Model Loading Time** - Must use singleton to avoid 1-2s penalty on each call
- **Memory Efficiency** - OCR model stays in memory after first load
- **Hardware Compatibility** - Support both CPU and GPU inference
- **Error Gracefulness** - Return empty string for unreadable images, don't crash
- **Production Ready** - Must handle concurrent usage safely

## External Dependencies
- **PaddleOCR Models** - Pre-trained OCR models downloaded on first use
- **ONNX Runtime** - For accelerated inference (requires proper provider configuration)
- **System Libraries** - OpenCV system dependencies for image processing
- **Hardware Acceleration** - CUDA support for GPU inference (optional)
