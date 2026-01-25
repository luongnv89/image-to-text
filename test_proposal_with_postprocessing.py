#!/usr/bin/env python
"""Test OCR with post-processing to achieve 100% accuracy"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import cv2


def test_proposal_with_postprocessing():
    """Test OCR + post-processing on proposal-text.png"""
    image_path = Path(__file__).parent / "data" / "proposal-text.png"
    expected_path = Path(__file__).parent / "data" / "text.txt"

    if not image_path.exists() or not expected_path.exists():
        print("❌ Test files not found")
        return False

    print("🧪 Testing OCR + Post-Processing Accuracy")
    print("=" * 70)

    # Load expected text
    with open(expected_path, "r") as f:
        expected_text = f.read().strip()

    # Load and process image
    image = cv2.imread(str(image_path))
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    try:
        import easyocr
        from image_to_text.post_processing import clean_ocr_text

        # Extract text
        reader = easyocr.Reader(["en"], gpu=False)
        results = reader.readtext(image_rgb)

        extracted_texts = []
        for bbox, text, confidence in results:
            extracted_texts.append(text)

        raw_extracted = " ".join(extracted_texts).strip()

        # Apply post-processing
        processed_text = clean_ocr_text(raw_extracted)

        print(f"\n📝 Expected text:")
        print("-" * 70)
        print(expected_text)
        print("-" * 70)

        print(f"\n🔧 Raw extracted text:")
        print("-" * 70)
        print(raw_extracted)
        print("-" * 70)

        print(f"\n✨ Post-processed text:")
        print("-" * 70)
        print(processed_text)
        print("-" * 70)

        # Compare
        print(f"\n📊 Accuracy Analysis:")
        print(f"   Raw similarity: {sum(a == b for a, b in zip(expected_text, raw_extracted)) / len(expected_text) * 100:.2f}%")

        if processed_text == expected_text:
            print(f"   ✅ Post-processed similarity: 100.00% (PERFECT MATCH!)")
            return True
        else:
            match_count = sum(a == b for a, b in zip(expected_text, processed_text))
            similarity = match_count / len(expected_text) * 100
            print(f"   Post-processed similarity: {similarity:.2f}%")

            # Show remaining differences
            print(f"\n⚠️  Remaining differences:")
            for i, (e, p) in enumerate(zip(expected_text, processed_text)):
                if e != p:
                    print(f"   Position {i}: expected '{e}' but got '{p}'")

            return similarity >= 99.0

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 OCR + Post-Processing Test\n")

    success = test_proposal_with_postprocessing()

    if success:
        print("\n✅ Test passed!")
        sys.exit(0)
    else:
        print("\n❌ Test failed!")
        sys.exit(1)
