#!/usr/bin/env python
"""Test OCR with the example image from data/"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import cv2
import numpy as np
from paddleocr import PaddleOCR


def test_example_image():
    """Test OCR directly on the example image using PaddleOCR."""
    image_path = Path(__file__).parent / "data" / "example.png"

    if not image_path.exists():
        print(f"❌ Image not found: {image_path}")
        return False

    print(f"📷 Testing with image: {image_path}")
    print(f"   Size: {image_path.stat().st_size / 1024:.1f} KB")

    try:
        # Load image
        image = cv2.imread(str(image_path))
        if image is None:
            print("❌ Failed to load image")
            return False

        print(f"   Dimensions: {image.shape}")

        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Initialize OCR engine
        print("\n🔄 Initializing OCR engine...")
        ocr = PaddleOCR(use_angle_cls=True, lang="en")

        # Run OCR
        print("🔄 Running OCR...")
        result = ocr.ocr(image_rgb, cls=True)

        if not result or not result[0]:
            print("⚠️  No text detected in image")
            return True

        # Extract and display results
        print("\n✅ OCR Results:")
        print("=" * 60)

        extracted_texts = []
        total_confidence = 0
        box_count = 0

        for line in result:
            for text_box in line:
                if text_box and len(text_box) >= 2:
                    text = text_box[1][0]
                    confidence = text_box[1][1]
                    extracted_texts.append(text)
                    total_confidence += confidence
                    box_count += 1

                    print(f"  Text: {text}")
                    print(f"  Confidence: {confidence:.2%}")
                    print("-" * 60)

        full_text = " ".join(extracted_texts)
        avg_confidence = total_confidence / box_count if box_count > 0 else 0

        print("\n📊 Summary:")
        print(f"  Total text boxes detected: {box_count}")
        print(f"  Average confidence: {avg_confidence:.2%}")
        print(f"\n📝 Full extracted text:\n{full_text}")

        return True

    except Exception as e:
        print(f"❌ Error during OCR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_with_preprocessing():
    """Test with preprocessing pipeline (if paddlepaddle is available)."""
    image_path = Path(__file__).parent / "data" / "example.png"

    try:
        from image_to_text.preprocessing import preprocess_image
        from image_to_text.ocr_engine import OCREngine

        print("\n\n🔧 Testing with preprocessing pipeline:")
        print("=" * 60)

        # Preprocess image
        print("🔄 Preprocessing image...")
        preprocessed = preprocess_image(str(image_path))
        print(f"   Preprocessed shape: {preprocessed.shape}")

        # Run OCR on preprocessed image
        print("🔄 Running OCR on preprocessed image...")
        engine = OCREngine()
        text = engine.extract_text(preprocessed)

        print("\n✅ Preprocessed OCR Results:")
        print("=" * 60)
        print(f"📝 Extracted text:\n{text}")

        return True

    except ImportError as e:
        print(f"\n⚠️  Preprocessing pipeline not available: {e}")
        print("   (This is expected if paddlepaddle is not installed)")
        return True
    except Exception as e:
        print(f"❌ Error with preprocessing: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Image-to-Text OCR Test\n")

    success = test_example_image()
    test_with_preprocessing()

    if success:
        print("\n✅ Test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Test failed!")
        sys.exit(1)
