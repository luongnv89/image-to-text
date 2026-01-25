"""Unit tests for OCR engine singleton pattern implementation."""

import threading
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_paddle_ocr():
    """Mock PaddleOCR to avoid initialization issues."""
    with patch('image_to_text.ocr_engine.PaddleOCR') as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock


def test_ocr_engine_is_singleton(mock_paddle_ocr):
    """Test that OCREngine follows the singleton pattern."""
    from image_to_text.ocr_engine import OCREngine

    engine1 = OCREngine()
    engine2 = OCREngine()

    assert engine1 is engine2, "OCREngine should return the same instance"


def test_singleton_model_loaded_once(mock_paddle_ocr):
    """Test that PaddleOCR is initialized only once."""
    from image_to_text.ocr_engine import OCREngine

    # Reset singleton for test
    OCREngine._instance = None
    OCREngine._initialized = False

    engine1 = OCREngine()
    engine2 = OCREngine()
    engine3 = OCREngine()

    # PaddleOCR should be called only once despite multiple instantiations
    assert mock_paddle_ocr.call_count == 1, \
        "PaddleOCR should be initialized only once"

    # All instances should share the same model
    assert engine1.ocr is engine2.ocr, \
        "All instances should share the same PaddleOCR model"
    assert engine2.ocr is engine3.ocr, \
        "All instances should share the same PaddleOCR model"


def test_singleton_thread_safe(mock_paddle_ocr):
    """Test that singleton initialization is thread-safe."""
    from image_to_text.ocr_engine import OCREngine

    # Reset singleton for test
    OCREngine._instance = None

    engines = []
    lock = threading.Lock()

    def create_engine():
        engine = OCREngine()
        with lock:
            engines.append(engine)

    # Create engines from multiple threads
    threads = [threading.Thread(target=create_engine) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # All engines should be the same instance
    first_engine = engines[0]
    for engine in engines[1:]:
        assert engine is first_engine, \
            "All engines created from different threads should be the same instance"

    # PaddleOCR should still be called only once
    assert mock_paddle_ocr.call_count == 1, \
        "PaddleOCR should be initialized only once even with multiple threads"


def test_singleton_configuration(mock_paddle_ocr):
    """Test that PaddleOCR is configured with correct parameters."""
    from image_to_text.ocr_engine import OCREngine

    # Reset singleton for test
    OCREngine._instance = None

    engine = OCREngine()

    # Verify PaddleOCR was called with correct parameters
    mock_paddle_ocr.assert_called_once()
    call_kwargs = mock_paddle_ocr.call_args[1]

    assert 'use_angle_cls' in call_kwargs, \
        "use_angle_cls should be configured"
    assert call_kwargs['use_angle_cls'] is True, \
        "use_angle_cls should be True"

    assert 'lang' in call_kwargs, \
        "lang should be configured"
    assert call_kwargs['lang'] == 'en', \
        "lang should be set to 'en'"


def test_singleton_reuse_avoids_reload(mock_paddle_ocr):
    """Test that reusing singleton avoids reloading the model."""
    from image_to_text.ocr_engine import OCREngine

    # Reset singleton for test
    OCREngine._instance = None

    # Create multiple instances
    for _ in range(5):
        engine = OCREngine()
        # Access the model to ensure it's used
        assert engine.ocr is not None

    # PaddleOCR should only be initialized once
    assert mock_paddle_ocr.call_count == 1, \
        "Model should be loaded only once even when accessing multiple times"
