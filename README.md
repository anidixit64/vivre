# Vivre

A Python library for machine learning and corpus linguistics.

## Description

Vivre provides tools for processing parallel texts through a complete pipeline: parsing EPUB files, segmenting text into sentences, and aligning sentences between languages using the Gale-Church algorithm.

## Features

- **EPUB Parsing**: Robust parsing with content filtering and chapter extraction
- **Sentence Segmentation**: Multi-language sentence segmentation using spaCy
- **Text Alignment**: Statistical text alignment using the Gale-Church algorithm
- **Multiple Output Formats**: JSON, CSV, XML, text, and dictionary formats
- **Language Support**: English, Spanish, French, German, Italian, Portuguese, and more
- **Simple API**: Easy-to-use top-level functions for common tasks
- **Command Line Interface**: Full CLI with rich output and progress indicators
- **Error Handling**: Comprehensive error handling with helpful messages

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

Vivre provides a comprehensive CLI for easy command-line usage:

```bash
# Parse an EPUB file
vivre parse book.epub

# Parse with content display
vivre parse book.epub --show-content

# Align two EPUB files
vivre align english.epub french.epub

# Align with different output formats
vivre align english.epub french.epub --format json
vivre align english.epub french.epub --format csv --output alignments.csv
vivre align english.epub french.epub --format xml --output alignments.xml

# Align with custom parameters
vivre align english.epub french.epub --c 1.1 --s2 7.0 --gap-penalty 2.5

# Get help
vivre --help
vivre align --help
```

### Simple API

Vivre provides easy-to-use top-level functions for common tasks:

```python
import vivre

# Parse EPUB and extract chapters
chapters = vivre.read('path/to/epub')
print(f"Found {len(chapters)} chapters")

# Segment chapters into sentences
segmented = chapters.segment()
sentences = segmented.get_segmented()

# Quick alignment - returns simple sentence pairs
pairs = vivre.quick_align('english.epub', 'french.epub')
for source, target in pairs[:5]:
    print(f"EN: {source}")
    print(f"FR: {target}")

# Full alignment with different outputs
corpus = vivre.align('english.epub', 'french.epub', form='json')
corpus_dict = vivre.align('english.epub', 'french.epub', form='dict')
corpus_text = vivre.align('english.epub', 'french.epub', form='text')
corpus_csv = vivre.align('english.epub', 'french.epub', form='csv')
corpus_xml = vivre.align('english.epub', 'french.epub', form='xml')

# Check supported languages
languages = vivre.get_supported_languages()
print(f"Supported: {', '.join(languages)}")
```

### Advanced Usage

For more control, use the individual components:

```python
from vivre import VivrePipeline

# Create pipeline with custom parameters
pipeline = VivrePipeline("en-es", c=1.1, s2=7.0, gap_penalty=2.5)

# Process parallel EPUBs
alignments = pipeline.process_parallel_epubs(
    "english_book.epub", "spanish_book.epub"
)

# Process text directly
alignments = pipeline.process_parallel_texts(
    "Hello world.", "Hola mundo."
)

# Get pipeline information
info = pipeline.get_pipeline_info()
print(f"Pipeline info: {info}")
```

### Error Handling

Vivre provides comprehensive error handling:

```python
import vivre

try:
    # This will raise FileNotFoundError if the file doesn't exist
    chapters = vivre.read('nonexistent.epub')
except FileNotFoundError as e:
    print(f"File not found: {e}")

try:
    # This will raise ValueError for unsupported formats
    result = vivre.align('book1.epub', 'book2.epub', form='unsupported')
except ValueError as e:
    print(f"Invalid format: {e}")
```

### Output Format

The JSON output format includes:

```json
{
  "book_title": "Book Title",
  "language_pair": "en-fr",
  "chapters": {
    "1": {
      "title": "Chapter 1 Title",
      "alignments": [
        {
          "en": "First sentence in English",
          "fr": "Première phrase en français"
        },
        {
          "en": "Second sentence in English",
          "fr": "Deuxième phrase en français"
        }
      ]
    }
  }
}
```

## Examples

Run the included examples:

```bash
# Run basic usage examples
python examples/basic_usage.py

# Or use the package directly
python -m vivre parse tests/data/your_book.epub
python -m vivre align tests/data/book1.epub tests/data/book2.epub
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=vivre

# Run specific test file
pytest tests/test_api.py
```

### Code Quality

```bash
# Run pre-commit hooks
pre-commit run --all-files

# Format code
black src/
isort src/

# Type checking
mypy src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- spaCy for sentence segmentation
- Gale-Church algorithm for text alignment
- ebooklib for EPUB parsing
