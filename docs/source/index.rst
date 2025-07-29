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

Vivre can be installed using Poetry, pip, or by cloning the repository.

Using Poetry (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   poetry add vivre

Using pip
~~~~~~~~~

.. code-block:: bash

   pip install vivre

From Source
~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/anidixit64/vivre.git
   cd vivre
   poetry install

Quick Start
-----------

Basic usage example:

.. code-block:: python

   from vivre import VivreProcessor

   # Process an EPUB file
   processor = VivreProcessor("path/to/book.epub")
   content = processor.extract_content()

   # Analyze the text
   segments = processor.segment_text(content)

Command Line Usage
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Process a single file
   vivre process book.epub

   # Process multiple files
   vivre process *.epub

   # Get help
   vivre --help

Documentation
------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

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
