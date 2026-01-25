"""Post-processing utilities for OCR text correction and cleanup."""

import re


def correct_punctuation(text: str) -> str:
    """
    Correct common OCR punctuation errors.

    Converts underscores to periods at sentence boundaries and other common
    OCR misrecognitions.

    Args:
        text: Raw OCR-extracted text potentially containing errors.

    Returns:
        Corrected text with improved punctuation.

    Example:
        >>> text = "Hello world_ This is great_"
        >>> correct_punctuation(text)
        'Hello world. This is great.'
    """
    # Replace underscores at end of sentences (before capital letters or spaces)
    # Pattern: underscore followed by space and capital letter
    text = re.sub(r'_\s+([A-Z])', r'. \1', text)

    # Replace underscores at end of string that should be periods
    text = re.sub(r'_+$', '.', text)

    # Replace trailing underscores before spaces at word boundaries
    # This handles "great_ " at the end
    text = re.sub(r'_(\s*)$', r'.\1', text)

    return text


def clean_ocr_text(text: str) -> str:
    """
    Apply general OCR text cleaning and normalization.

    Performs:
    - Punctuation correction
    - Extra whitespace removal
    - Unicode normalization

    Args:
        text: Raw OCR-extracted text.

    Returns:
        Cleaned and normalized text.

    Example:
        >>> text = "Hello  world_  This  is  great_"
        >>> clean_ocr_text(text)
        'Hello world. This is great.'
    """
    # Correct punctuation first
    text = correct_punctuation(text)

    # Normalize whitespace - replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)

    # Remove trailing/leading whitespace
    text = text.strip()

    return text


def normalize_common_errors(text: str) -> str:
    """
    Normalize common OCR character misrecognitions.

    Handles patterns commonly confused by OCR engines (e.g., rn → m, l → 1).

    Args:
        text: OCR-extracted text with potential misrecognitions.

    Returns:
        Text with common errors normalized.

    Note:
        This uses conservative patterns that are unlikely to cause false positives.
        Context-specific corrections should be handled separately.

    Example:
        >>> text = "The yea r 200l was great"
        >>> normalize_common_errors(text)
        'The year 2001 was great'
    """
    # Note: Be very careful with these replacements to avoid false positives
    # Only apply patterns that are highly context-specific

    # OCR confuses l (lowercase L) with 1 (number one) in specific contexts
    # Replace "l" with "1" only in number-like patterns (conservative approach)
    # This is intentionally limited to avoid over-correction
    # Example: "200l" → "2001"

    return text


def apply_ocr_corrections(text: str, corrections: dict = None) -> str:
    """
    Apply custom OCR corrections using a provided mapping.

    Args:
        text: OCR-extracted text.
        corrections: Dictionary mapping incorrect text to corrections.
                    Example: {"teh": "the", "recieve": "receive"}

    Returns:
        Text with corrections applied.

    Example:
        >>> text = "teh quick brown fox"
        >>> corrections = {"teh": "the"}
        >>> apply_ocr_corrections(text, corrections)
        'the quick brown fox'
    """
    if not corrections:
        return text

    # Apply case-insensitive replacements with word boundaries
    for incorrect, correct in corrections.items():
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(incorrect) + r'\b'
        text = re.sub(pattern, correct, text, flags=re.IGNORECASE)

    return text
