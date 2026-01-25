#!/usr/bin/env python3
"""
Setup script for OCR project dependencies.
Automatically detects GPU availability and installs appropriate packages.
"""

import subprocess
import sys
import os


def check_gpu_available():
    """Check if CUDA GPU is available for PaddlePaddle."""
    try:
        # Try to import paddle and check CUDA availability
        import paddle  # type: ignore

        return (
            paddle.device.is_compiled_with_cuda()
            and paddle.device.cuda.device_count() > 0
        )
    except ImportError:
        # If paddle not installed, check if CUDA toolkit is available
        try:
            result = subprocess.run(
                ["nvidia-smi"], capture_output=True, text=True, timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False


def install_requirements():
    """Install requirements with GPU-aware package selection."""
    gpu_available = check_gpu_available()

    print(f"GPU detected: {gpu_available}")

    # Base requirements
    base_packages = [
        "paddleocr>=2.7.0",
        "opencv-python-headless>=4.8.0",
        "numpy>=1.24.0",
        "Pillow>=9.5.0",
    ]

    # Framework and runtime packages based on GPU availability
    if gpu_available:
        framework_packages = ["paddlepaddle-gpu>=2.5.0", "onnxruntime-gpu>=1.15.0"]
        print("Installing GPU-optimized packages...")
    else:
        framework_packages = ["paddlepaddle>=2.5.0", "onnxruntime>=1.15.0"]
        print("Installing CPU-optimized packages...")

    # Install all packages
    all_packages = base_packages + framework_packages

    for package in all_packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}: {e}")
            return False

    print("\n✓ All dependencies installed successfully!")
    return True


if __name__ == "__main__":
    # Check if virtual environment is active
    if hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        print("✓ Virtual environment detected")
    else:
        print(
            "⚠ Warning: No virtual environment detected. It's recommended to use a virtual environment."
        )

    # Install dependencies
    success = install_requirements()

    if success:
        print("\n🎉 Setup complete! You can now use the OCR module.")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)
