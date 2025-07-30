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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
