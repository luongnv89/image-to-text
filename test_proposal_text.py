#!/usr/bin/env python
"""Test OCR accuracy with proposal-text.png against expected text.txt"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import cv2
from difflib import SequenceMatcher


def test_proposal_text_ocr():
    """Test OCR on proposal-text.png and compare with text.txt"""
    image_path = Path(__file__).parent / "data" / "proposal-text.png"
    expected_path = Path(__file__).parent / "data" / "text.txt"

    if not image_path.exists():
        print(f"❌ Image not found: {image_path}")
        return False

    if not expected_path.exists():
        print(f"❌ Expected text file not found: {expected_path}")
        return False

    print("🧪 Testing OCR Accuracy on Proposal Text")
    print("=" * 70)
    print(f"📷 Image: {image_path.name}")
    print(f"📄 Expected: {expected_path.name}")

    try:
        # Load expected text
        with open(expected_path, "r") as f:
            expected_text = f.read().strip()

        print(f"\n📝 Expected text:")
        print("-" * 70)
        print(expected_text)
        print("-" * 70)

        # Load image
        image = cv2.imread(str(image_path))
        if image is None:
            print("❌ Failed to load image")
            return False

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        print(f"\n📊 Image info:")
        print(f"   Dimensions: {image_rgb.shape}")
        print(f"   Size: {image_path.stat().st_size / 1024:.1f} KB")

        # Try with easyocr
        try:
            import easyocr

            print("\n🔄 Extracting text with EasyOCR...")
            reader = easyocr.Reader(["en"], gpu=False)
            results = reader.readtext(image_rgb)

            if not results:
                print("⚠️  No text detected")
                return False

            # Extract text
            extracted_texts = []
            confidences = []

            for bbox, text, confidence in results:
                extracted_texts.append(text)
                confidences.append(confidence)

            extracted_text = " ".join(extracted_texts).strip()
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0

            print(f"\n✅ Extracted text ({len(results)} regions):")
            print("-" * 70)
            print(extracted_text)
            print("-" * 70)

            # Calculate similarity
            similarity = SequenceMatcher(None, expected_text, extracted_text).ratio()

            print(f"\n📊 Analysis:")
            print(f"   Expected length: {len(expected_text)} chars")
            print(f"   Extracted length: {len(extracted_text)} chars")
            print(f"   Text regions: {len(results)}")
            print(f"   Average confidence: {avg_confidence:.2%}")
            print(f"   Similarity score: {similarity:.2%}")

            # Check character-by-character differences
            if similarity < 0.95:
                print(f"\n⚠️  Differences detected:")
                print("-" * 70)

                # Find differences
                import difflib

                diff = difflib.unified_diff(
                    expected_text.splitlines(keepends=True),
                    extracted_text.splitlines(keepends=True),
                    fromfile="expected",
                    tofile="extracted",
                    lineterm="",
                )
                print("".join(diff))
            else:
                print("\n✅ Text matches expected output!")

            return True

        except ImportError:
            print("⚠️  EasyOCR not available, trying with preprocessing pipeline...")

            # Test with preprocessing
            from image_to_text.preprocessing import preprocess_image

            preprocessed = preprocess_image(str(image_path))
            print(f"   Preprocessed shape: {preprocessed.shape}")

            try:
                import easyocr

                reader = easyocr.Reader(["en"], gpu=False)
                results = reader.readtext(preprocessed)

                if results:
                    extracted_texts = []
                    for bbox, text, confidence in results:
                        extracted_texts.append(text)

                    extracted_text = " ".join(extracted_texts).strip()
                    print(f"\n✅ Extracted text (preprocessed):")
                    print("-" * 70)
                    print(extracted_text)
                    print("-" * 70)

                    similarity = SequenceMatcher(None, expected_text, extracted_text).ratio()
                    print(f"\n   Similarity: {similarity:.2%}")
                    return True
            except ImportError:
                pass

            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Proposal Text OCR Test\n")

    success = test_proposal_text_ocr()

    if success:
        print("\n✅ Test completed!")
        sys.exit(0)
    else:
        print("\n❌ Test failed!")
        sys.exit(1)
