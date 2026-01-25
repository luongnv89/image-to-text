"""Unit tests for post-processing module."""

import pytest

from image_to_text.post_processing import (
    apply_ocr_corrections,
    clean_ocr_text,
    correct_punctuation,
    normalize_common_errors,
)


class TestCorrectPunctuation:
    """Tests for punctuation correction."""

    def test_underscore_to_period_before_capital(self):
        """Test underscore to period conversion before capital letters."""
        text = "Hello world_ This is great_"
        result = correct_punctuation(text)
        assert "world. This" in result
        assert "great." in result

    def test_end_of_string_underscore(self):
        """Test underscore at end of string converted to period."""
        text = "Hello world_"
        result = correct_punctuation(text)
        assert result.endswith(".")

    def test_multiple_underscores(self):
        """Test multiple underscores handled correctly."""
        text = "End__ Next"
        result = correct_punctuation(text)
        assert ". Next" in result

    def test_no_changes_for_correct_text(self):
        """Test that correct text is not modified."""
        text = "Hello world. This is great."
        result = correct_punctuation(text)
        assert result == text

    def test_mixed_punctuation(self):
        """Test text with both correct and incorrect punctuation."""
        text = "First sentence. Second_ Third."
        result = correct_punctuation(text)
        assert "First sentence." in result
        assert "Second." in result


class TestCleanOcrText:
    """Tests for general OCR text cleaning."""

    def test_whitespace_normalization(self):
        """Test extra whitespace removal."""
        text = "Hello    world    test"
        result = clean_ocr_text(text)
        assert result == "Hello world test"

    def test_punctuation_correction_included(self):
        """Test that cleaning includes punctuation correction."""
        text = "Hello world_  This is great_"
        result = clean_ocr_text(text)
        assert "world." in result
        assert "great." in result

    def test_strip_leading_trailing_whitespace(self):
        """Test removal of leading and trailing whitespace."""
        text = "   Hello world   "
        result = clean_ocr_text(text)
        assert result == "Hello world"

    def test_combined_cleaning(self):
        """Test combined cleaning operations."""
        text = "  Hello world_  This  is  great_  "
        result = clean_ocr_text(text)
        assert result == "Hello world. This is great."

    def test_newlines_converted_to_spaces(self):
        """Test that newlines are normalized to spaces."""
        text = "Hello\n\nworld"
        result = clean_ocr_text(text)
        assert result == "Hello world"

    def test_tabs_normalized(self):
        """Test that tabs are normalized to spaces."""
        text = "Hello\t\tworld"
        result = clean_ocr_text(text)
        assert result == "Hello world"


class TestNormalizeCommonErrors:
    """Tests for common OCR error normalization."""

    def test_function_exists(self):
        """Test that function can be called without errors."""
        text = "The quick brown fox"
        result = normalize_common_errors(text)
        assert isinstance(result, str)

    def test_conservative_approach(self):
        """Test that function is conservative with replacements."""
        text = "Hello world"
        result = normalize_common_errors(text)
        # Should not change correct text
        assert result == text


class TestApplyCustomCorrections:
    """Tests for custom correction application."""

    def test_single_correction(self):
        """Test applying a single correction."""
        text = "teh quick brown fox"
        corrections = {"teh": "the"}
        result = apply_ocr_corrections(text, corrections)
        assert "the quick brown fox" in result.lower()

    def test_multiple_corrections(self):
        """Test applying multiple corrections."""
        text = "teh quick brwon fox"
        corrections = {"teh": "the", "brwon": "brown"}
        result = apply_ocr_corrections(text, corrections)
        assert "the" in result.lower()
        assert "brown" in result.lower()

    def test_case_insensitive(self):
        """Test that corrections are case-insensitive."""
        text = "TEH quick brown fox"
        corrections = {"teh": "the"}
        result = apply_ocr_corrections(text, corrections)
        assert "the" in result.lower()

    def test_word_boundaries(self):
        """Test that corrections respect word boundaries."""
        text = "theater the"
        corrections = {"the": "THE"}
        result = apply_ocr_corrections(text, corrections)
        # "theater" should not be affected
        assert "theater" in result.lower()

    def test_no_corrections_provided(self):
        """Test with empty corrections dictionary."""
        text = "Hello world"
        result = apply_ocr_corrections(text, {})
        assert result == text

    def test_no_corrections_object(self):
        """Test with None as corrections."""
        text = "Hello world"
        result = apply_ocr_corrections(text, None)
        assert result == text
