# Vivre

A Python library for machine learning and corpus linguistics.

## Description

Vivre provides tools for processing parallel texts through a complete pipeline: parsing EPUB files, segmenting text into sentences, and aligning sentences between languages using the Gale-Church algorithm.

## Features

- **EPUB Parsing**: Robust parsing with content filtering and chapter extraction
- **Sentence Segmentation**: Multi-language sentence segmentation using spaCy
- **Text Alignment**: Statistical text alignment using the Gale-Church algorithm
- **Multiple Output Formats**: JSON, CSV, text, and dictionary formats
- **Language Support**: English, Spanish, French, German, Italian, Portuguese, and more
- **Simple API**: Easy-to-use top-level functions for common tasks

## Getting Started

### Prerequisites

- Python 3.8 or higher
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

### Simple API

Vivre provides easy-to-use top-level functions for common tasks:

```python
import vivre

# Parse EPUB and extract chapters
chapters = vivre.read('path/to/epub')
sentences = chapters.segment()

# Align parallel texts with different outputs
corpus = vivre.align('english.epub', 'french.epub', form='json')
corpus_dict = vivre.align('english.epub', 'french.epub', form='dict')
corpus_text = vivre.align('english.epub', 'french.epub', form='text')
corpus_csv = vivre.align('english.epub', 'french.epub', form='csv')
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
        }
      ]
    }
  }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src/vivre --cov-report=html
```

### Code Quality

The project uses pre-commit hooks for code quality:

```bash
# Install pre-commit hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- spaCy for natural language processing capabilities
- The Gale-Church algorithm for text alignment
- BeautifulSoup for HTML parsing
