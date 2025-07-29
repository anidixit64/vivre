API Reference
============

This page provides detailed documentation for all classes and functions in the Vivre library. The documentation is automatically generated from the source code docstrings.

Top-Level Functions
------------------

These are the main functions you'll use for most tasks.

.. autofunction:: vivre.read

.. autofunction:: vivre.align

.. autofunction:: vivre.quick_align

.. autofunction:: vivre.get_supported_languages

.. autofunction:: vivre.clear_pipeline_cache

Core Classes
-----------

The main classes that provide the core functionality.

AlignmentResult
~~~~~~~~~~~~~~

.. autoclass:: vivre.AlignmentResult
   :members:
   :undoc-members:
   :show-inheritance:

Chapters
~~~~~~~~

.. autoclass:: vivre.Chapters
   :members:
   :undoc-members:
   :show-inheritance:

VivreParser
~~~~~~~~~~

.. autoclass:: vivre.VivreParser
   :members:
   :undoc-members:
   :show-inheritance:

Segmenter
~~~~~~~~~

.. autoclass:: vivre.Segmenter
   :members:
   :undoc-members:
   :show-inheritance:

Aligner
~~~~~~~

.. autoclass:: vivre.Aligner
   :members:
   :undoc-members:
   :show-inheritance:

VivrePipeline
~~~~~~~~~~~~

.. autoclass:: vivre.VivrePipeline
   :members:
   :undoc-members:
   :show-inheritance:

Pipeline Functions
-----------------

.. autofunction:: vivre.create_pipeline

CLI Functions
------------

Command-line interface functions for processing EPUB files.

.. autofunction:: vivre.cli.align

.. autofunction:: vivre.cli.parse

.. autofunction:: vivre.cli.main

Internal Functions
-----------------

These functions are used internally but may be useful for advanced users.

.. autofunction:: vivre.api._create_aligned_corpus

.. autofunction:: vivre.api._format_as_text

.. autofunction:: vivre.api._format_as_csv

.. autofunction:: vivre.api._format_as_xml

.. autofunction:: vivre.api._parse_source_or_chapters

CLI Formatting Functions
~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: vivre.cli._format_alignments_as_text

.. autofunction:: vivre.cli._format_alignments_as_csv

.. autofunction:: vivre.cli._format_alignments_as_xml

.. autofunction:: vivre.cli._format_parse_as_text

.. autofunction:: vivre.cli._format_parse_as_csv

.. autofunction:: vivre.cli._format_parse_as_xml

Module Index
-----------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
