.. vivre documentation master file, created by
   sphinx-quickstart on Tue Jul 29 17:37:18 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Vivre
================

Vivre is a powerful Python library for processing and analyzing EPUB files. It provides comprehensive tools for extracting, parsing, and manipulating EPUB content with a focus on text processing and analysis.

Key Features
------------

* **EPUB Processing**: Extract and parse EPUB files with ease
* **Text Analysis**: Advanced text processing and segmentation capabilities
* **Format Support**: Handle various EPUB formats and structures
* **CLI Interface**: Command-line tools for quick file operations
* **API Integration**: Clean Python API for programmatic access
* **Documentation**: Comprehensive documentation with examples

Installation
------------

Vivre can be installed using pip or by cloning the repository.

Using pip
~~~~~~~~~

.. code-block:: bash

   pip install vivre

From Source
~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/anidixit64/vivre.git
   cd vivre
   pip install -e .
   python -m spacy download en_core_web_sm
   python -m spacy download es_core_news_sm
   python -m spacy download fr_core_news_sm
   python -m spacy download it_core_news_sm

Quick Start
-----------

Basic usage example:

.. code-block:: python

   import vivre

   # Parse an EPUB file
   chapters = vivre.read("path/to/book.epub")
   print(f"Found {len(chapters)} chapters")

   # Align two books
   result = vivre.align("english.epub", "french.epub", "en-fr")
   print(result.to_json())

Command Line Usage
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Parse an EPUB file
   vivre parse book.epub --verbose

   # Align two books
   vivre align english.epub french.epub en-fr --format json

   # Get help
   vivre --help

Documentation
------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   tutorial
   api
   cli
   examples

Development
-----------

For development setup and contributing guidelines, see the project's `GitHub repository <https://github.com/anidixit64/vivre>`_.

Contributing
-----------

We welcome contributions to Vivre! Here's how you can help:

1. **Fork the repository** on GitHub
2. **Create a feature branch** for your changes
3. **Make your changes** following the coding standards
4. **Add tests** for any new functionality
5. **Ensure all tests pass** and coverage remains >90%
6. **Submit a pull request** with a clear description

Development Setup
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Clone and setup
   git clone https://github.com/anidixit64/vivre.git
   cd vivre
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

Running Tests
~~~~~~~~~~~~

.. code-block:: bash

   # Run all tests
   pytest tests/

   # Run with coverage
   pytest tests/ --cov=src/vivre --cov-report=html

   # Run specific test files
   pytest tests/test_api.py

Code Quality
~~~~~~~~~~~

The project uses pre-commit hooks for code quality:

.. code-block:: bash

   # Run hooks manually
   pre-commit run --all-files

License
-------

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
