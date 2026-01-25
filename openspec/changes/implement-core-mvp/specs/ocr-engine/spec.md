## ADDED Requirements
### Requirement: Image Preprocessing Pipeline
The system SHALL preprocess input images to optimize OCR accuracy for book page photographs.

#### Scenario: Valid image preprocessing
- **WHEN** a valid image file path is provided to `preprocess_image(image_path: str)`
- **THEN** the system SHALL load the image using OpenCV
- **AND** apply shadow removal algorithms to handle lighting variations
- **AND** enhance contrast to improve text readability
- **AND** return a processed numpy array suitable for OCR input

#### Scenario: Invalid image path handling
- **WHEN** an invalid or non-existent file path is provided
- **THEN** the system SHALL raise a FileNotFoundError
- **AND** include a descriptive error message

### Requirement: Basic OCR Text Extraction
The system SHALL extract text from preprocessed images using PaddleOCR with English language support.

#### Scenario: Successful text extraction
- **WHEN** a preprocessed image array is provided to the OCR engine
- **THEN** the system SHALL initialize PaddleOCR with `lang='en'`
- **AND** process the image to detect and recognize text
- **AND** return the extracted text as a single concatenated string

#### Scenario: Empty or unreadable image
- **WHEN** an image contains no readable text
- **THEN** the system SHALL return an empty string
- **AND** not raise an exception

### Requirement: Core Module Structure
The system SHALL provide a foundational module structure following the project conventions.

#### Scenario: Module organization
- **WHEN** the core module is imported
- **THEN** the system SHALL expose the preprocessing function
- **AND** provide access to the OCR engine
- **AND** follow PEP 8 naming conventions
- **AND** include type hints for all function signatures
- **AND** provide Google-style docstrings for public functions