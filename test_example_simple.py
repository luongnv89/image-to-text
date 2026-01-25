#!/usr/bin/env python
"""Test OCR with the example image from data/ using easyocr"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import cv2


def test_example_with_easyocr():
    """Test OCR on the example image using EasyOCR."""
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

        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        print(f"   Dimensions: {image_rgb.shape}")

        # Initialize OCR engine using easyocr
        print("\n🔄 Initializing OCR engine (EasyOCR)...")
        try:
            import easyocr
            reader = easyocr.Reader(["en"], gpu=False)
        except ImportError:
            print("❌ EasyOCR not available")
            return False

        # Run OCR
        print("🔄 Running OCR on image...")
        results = reader.readtext(image_rgb)

        if not results:
            print("⚠️  No text detected in image")
            return True

        # Extract and display results
        print("\n✅ OCR Results:")
        print("=" * 60)

        extracted_texts = []
        total_confidence = 0

        for (bbox, text, confidence) in results:
            extracted_texts.append(text)
            total_confidence += confidence

            print(f"  Text: {text}")
            print(f"  Confidence: {confidence:.2%}")
            print("-" * 60)

        full_text = " ".join(extracted_texts)
        avg_confidence = total_confidence / len(results) if results else 0

        print("\n📊 Summary:")
        print(f"  Total text regions detected: {len(results)}")
        print(f"  Average confidence: {avg_confidence:.2%}")
        print(f"\n📝 Full extracted text:\n{full_text}")

        return True

    except Exception as e:
        print(f"❌ Error during OCR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_with_preprocessing():
    """Test with preprocessing pipeline."""
    image_path = Path(__file__).parent / "data" / "example.png"

    try:
        from image_to_text.preprocessing import preprocess_image
        import easyocr

        print("\n\n🔧 Testing with preprocessing pipeline:")
        print("=" * 60)

        # Preprocess image
        print("🔄 Preprocessing image...")
        preprocessed = preprocess_image(str(image_path))
        print(f"   Preprocessed shape: {preprocessed.shape}")
        print(f"   Value range: [{preprocessed.min()}, {preprocessed.max()}]")

        # Run OCR on preprocessed image
        print("🔄 Running OCR on preprocessed image...")
        reader = easyocr.Reader(["en"], gpu=False)
        results = reader.readtext(preprocessed)

        if not results:
            print("⚠️  No text detected in preprocessed image")
            return True

        extracted_texts = []
        for (bbox, text, confidence) in results:
            extracted_texts.append(text)

        full_text = " ".join(extracted_texts)

        print("\n✅ Preprocessed OCR Results:")
        print("=" * 60)
        print(f"  Text regions detected: {len(results)}")
        print(f"📝 Extracted text:\n{full_text}")

        return True

    except ImportError as e:
        print(f"\n⚠️  Could not test preprocessing: {e}")
        return True
    except Exception as e:
        print(f"❌ Error with preprocessing: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Image-to-Text OCR Test\n")

    success = test_example_with_easyocr()
    test_with_preprocessing()

    if success:
        print("\n✅ Test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Test failed!")
        sys.exit(1)
