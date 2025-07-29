# Vivre

[![codecov](https://codecov.io/github/anidixit64/vivre/graph/badge.svg?token=JJLN3K87G4)](https://codecov.io/github/anidixit64/vivre)

A Python library for parsing EPUB files and aligning parallel texts.

## Description

Vivre provides tools for processing parallel texts through a complete pipeline: parsing EPUB files, segmenting text into sentences, and aligning sentences between languages using the Gale-Church algorithm. The library offers both a simple API for programmatic use and a powerful command-line interface.

## Features

- **EPUB Parsing**: Robust parsing with content filtering and chapter extraction
- **Sentence Segmentation**: Multi-language sentence segmentation using spaCy
- **Text Alignment**: Statistical text alignment using the Gale-Church algorithm
- **Multiple Output Formats**: JSON, CSV, XML, text, and dictionary formats
- **Language Support**: English, Spanish, French, German, Italian, Portuguese, and more
- **Simple API**: Easy-to-use top-level functions for common tasks
- **Command Line Interface**: Clean CLI with two powerful commands
- **Error Handling**: Comprehensive error handling with helpful messages
- **Type Safety**: Full type hints and validation

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd vivre
```

2. Install the package:
```bash
pip install -e .
```

3. Install required spaCy models:
```bash
python -m spacy download en_core_web_sm
python -m spacy download es_core_news_sm
python -m spacy download fr_core_news_sm
# Add other language models as needed
```

## Usage

### Command Line Interface

Vivre provides a clean CLI with two powerful commands:

```bash
# Parse and analyze an EPUB file
vivre parse book.epub --verbose

# Parse with content display and segmentation
vivre parse book.epub --show-content --segment --language en

# Parse with custom output format
vivre parse book.epub --format csv --output analysis.csv

# Align two EPUB files (language pair is required)
vivre align english.epub french.epub en-fr

# Align with different output formats
vivre align english.epub french.epub en-fr --format json
vivre align english.epub french.epub en-fr --format csv --output alignments.csv
vivre align english.epub french.epub en-fr --format xml --output alignments.xml

# Align with custom parameters
vivre align english.epub french.epub en-fr --c 1.1 --s2 7.0 --gap-penalty 2.5

# Get help
vivre --help
vivre align --help
vivre parse --help
```

### Simple API

Vivre provides easy-to-use top-level functions for common tasks:

```python
import vivre

# Parse EPUB and extract chapters
chapters = vivre.read('path/to/epub')
print(f"Found {len(chapters)} chapters")

# Segment chapters into sentences
segmented = chapters.segment('en')  # Specify language for better accuracy
sentences = segmented.get_segmented()

# Quick alignment - returns simple sentence pairs
pairs = vivre.quick_align('english.epub', 'french.epub', 'en-fr')
for source, target in pairs[:5]:
    print(f"EN: {source}")
    print(f"FR: {target}")

# Full alignment with rich output
result = vivre.align('english.epub', 'french.epub', 'en-fr')
print(result.to_json())      # JSON output
print(result.to_csv())       # CSV output
print(result.to_text())      # Formatted text
print(result.to_xml())       # XML output
print(result.to_dict())      # Python dictionary

# Work with Chapters objects seamlessly
source_chapters = vivre.read('english.epub')
target_chapters = vivre.read('french.epub')
result = vivre.align(source_chapters, target_chapters, 'en-fr')  # Works with objects too!

# Get supported languages
languages = vivre.get_supported_languages()
print(f"Supported languages: {languages}")
```

### Advanced Usage

For more control, you can use the individual components:

```python
from vivre import VivreParser, Segmenter, Aligner

# Parse EPUB
parser = VivreParser()
chapters = parser.parse_epub('book.epub')

# Segment text
segmenter = Segmenter()
sentences = segmenter.segment('Hello world!', 'en')

# Align texts
aligner = Aligner()
alignments = aligner.align(['Hello'], ['Bonjour'])

# Pipeline for complex workflows
from vivre import VivrePipeline
pipeline = VivrePipeline('en-fr')
result = pipeline.process_parallel_epubs('english.epub', 'french.epub')
```

## API Reference

### Top-level Functions

- `read(epub_path)` - Parse EPUB and return Chapters object
- `align(source, target, language_pair)` - Align parallel texts, returns AlignmentResult
- `quick_align(source_epub, target_epub, language_pair)` - Simple alignment, returns sentence pairs
- `get_supported_languages()` - Get list of supported language codes

### Classes

- `Chapters` - Container for parsed EPUB chapters with segmentation support
- `AlignmentResult` - Container for alignment results with multiple output formats
- `VivreParser` - Low-level EPUB parser
- `Segmenter` - Sentence segmentation using spaCy
- `Aligner` - Text alignment using Gale-Church algorithm
- `VivrePipeline` - High-level pipeline for complete workflows

## Output Formats

The library supports multiple output formats:

- **JSON**: Structured data for programmatic use
- **CSV**: Tabular data for spreadsheet applications
- **XML**: Hierarchical data for document processing
- **Text**: Human-readable formatted output
- **Dict**: Python dictionary for direct manipulation

## Language Support

Vivre supports multiple languages through spaCy models:

- English (`en_core_web_sm`)
- Spanish (`es_core_news_sm`)
- French (`fr_core_news_sm`)
- German (`de_core_news_sm`)
- Italian (`it_core_news_sm`)
- Portuguese (`pt_core_news_sm`)
- And more...

## Development

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=vivre --cov-report=html

# Run specific test files
pytest tests/test_api.py
pytest tests/test_parser.py
```

### Code Quality

The project uses pre-commit hooks for code quality:

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass and coverage remains >90%
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
