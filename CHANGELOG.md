# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Docker support with comprehensive setup
- Professional documentation with badges
- Contributing guidelines and development setup
- Enhanced CLI examples and Python API documentation
- Support for 4 languages: English, Spanish, French, Italian

### Changed
- Improved installation instructions
- Updated Sphinx documentation to match current API
- Enhanced README with comprehensive examples

### Fixed
- Corrected license information (Apache 2.0)
- Updated language support documentation

## [0.1.0] - 2025-01-XX

### Added
- Initial release of Vivre
- EPUB parsing and text extraction
- Sentence segmentation using spaCy
- Text alignment using Gale-Church algorithm
- Command-line interface with parse and align commands
- Python API with top-level functions
- Support for multiple output formats (JSON, CSV, XML, text)
- Comprehensive test suite with >90% coverage
- Pre-commit hooks for code quality
- Sphinx documentation

### Features
- **EPUB Processing**: Robust parsing with content filtering
- **Text Segmentation**: Multi-language sentence segmentation
- **Text Alignment**: Statistical alignment of parallel texts
- **CLI Interface**: Clean command-line tools
- **Python API**: Easy-to-use library functions
- **Multiple Formats**: JSON, CSV, XML, text output
- **Language Support**: English, Spanish, French, Italian

---

## Version History

- **0.1.0**: Initial release with core functionality
- **Unreleased**: Docker support, documentation improvements, professional setup

## Contributing

To add entries to this changelog:

1. Add your changes under the `[Unreleased]` section
2. Use the appropriate category: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`
3. Write clear, concise descriptions
4. Reference issues and pull requests when applicable

## Release Process

1. Update version in `pyproject.toml`
2. Move `[Unreleased]` changes to new version section
3. Update release date
4. Create git tag
5. Publish to PyPI
