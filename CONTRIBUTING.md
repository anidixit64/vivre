# Contributing to Vivre

Thank you for your interest in contributing to Vivre! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/vivre.git`
3. **Create** a feature branch: `git checkout -b feature/your-feature-name`
4. **Make** your changes
5. **Test** your changes: `pytest tests/`
6. **Commit** with a clear message: `git commit -m "feat: add new feature"`
7. **Push** to your fork: `git push origin feature/your-feature-name`
8. **Submit** a pull request

## 🛠️ Development Setup

### Prerequisites

- Python 3.11 or higher
- Git
- Poetry (recommended) or pip

### Local Development

```bash
# Clone the repository
git clone https://github.com/anidixit64/vivre.git
cd vivre

# Install dependencies
pip install -e .

# Install spaCy models
python -m spacy download en_core_web_sm
python -m spacy download es_core_news_sm
python -m spacy download fr_core_news_sm
python -m spacy download it_core_news_sm

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Docker Development

```bash
# Build the development image
docker build -t vivre .

# Run tests
docker run --rm vivre python -m pytest tests/ -v

# Interactive development shell
docker run --rm -it vivre /bin/bash
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src/vivre --cov-report=html

# Run specific test files
pytest tests/test_api.py

# Run tests in parallel
pytest tests/ -n auto
```

### Code Quality

```bash
# Run pre-commit hooks
pre-commit run --all-files

# Run linting
ruff check .

# Run formatting
ruff format .

# Run type checking
mypy src/ tests/
```

## 📝 Code Style

### Python Code

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and under 50 lines when possible
- Use meaningful variable and function names

### Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```bash
git commit -m "feat: add support for German language"
git commit -m "fix: resolve memory leak in parser"
git commit -m "docs: update installation instructions"
```

### Pull Request Guidelines

1. **Title**: Use conventional commit format
2. **Description**: Clearly describe the changes and motivation
3. **Tests**: Include tests for new functionality
4. **Documentation**: Update docs if needed
5. **Coverage**: Maintain >90% test coverage

## 🎯 Areas for Contribution

### High Priority

- **Language Support**: Add support for more languages
- **Performance**: Optimize parsing and alignment algorithms
- **Documentation**: Improve examples and tutorials
- **Testing**: Add more comprehensive test coverage

### Medium Priority

- **CLI Features**: Add more command-line options
- **Output Formats**: Support additional export formats
- **Error Handling**: Improve error messages and recovery
- **Logging**: Add structured logging throughout

### Low Priority

- **UI/UX**: Create a web interface
- **Integration**: Add support for other file formats
- **Analytics**: Add usage analytics and metrics

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment**: Python version, OS, dependencies
2. **Steps**: Clear steps to reproduce the issue
3. **Expected**: What you expected to happen
4. **Actual**: What actually happened
5. **Files**: Sample EPUB files if relevant (small ones please!)

## 💡 Feature Requests

When requesting features, please:

1. **Describe** the feature clearly
2. **Explain** why it's needed
3. **Provide** use cases or examples
4. **Consider** implementation complexity

## 🤝 Code Review Process

1. **Automated Checks**: All PRs must pass CI/CD checks
2. **Code Review**: At least one maintainer must approve
3. **Testing**: All new code must have tests
4. **Documentation**: New features must be documented

## 📚 Documentation

### Adding Documentation

- Update docstrings for new functions/classes
- Add examples to the tutorial
- Update README.md if needed
- Add type hints for better IDE support

### Building Docs

```bash
# Install docs dependencies
pip install -e ".[docs]"

# Build documentation
cd docs
make html

# View documentation
open _build/html/index.html
```

## 🏷️ Release Process

1. **Version Bump**: Update version in `pyproject.toml`
2. **Changelog**: Update CHANGELOG.md
3. **Tests**: Ensure all tests pass
4. **Documentation**: Update docs if needed
5. **Tag**: Create a git tag
6. **Publish**: Release to PyPI

## 📞 Getting Help

- **Issues**: Use GitHub Issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Email**: Contact the maintainer directly for sensitive issues

## 🙏 Acknowledgments

Thank you to all contributors who have helped make Vivre better! Your contributions are greatly appreciated.

---

**Note**: This is a living document. If you see something that could be improved, please submit a pull request!
