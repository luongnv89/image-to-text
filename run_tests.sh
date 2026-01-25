#!/bin/bash
# Test runner script for the OCR project

# Check for virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠ No virtual environment detected"
    echo "Consider using: python -m venv venv && source venv/bin/activate"
fi

# Run tests
echo "Running tests..."
python -m pytest tests/ -v --cov=src/image_to_text --cov-report=term-missing

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "✓ All tests passed!"
else
    echo "✗ Tests failed with exit code $exit_code"
fi

exit $exit_code
