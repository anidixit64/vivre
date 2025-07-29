Tutorial: Aligning Two Books
============================

This tutorial will guide you through the process of aligning two books using Vivre. We'll cover both the Python library approach and the command-line interface.

Prerequisites
------------

Before starting, make sure you have:

* Vivre installed (see :doc:`index` for installation instructions)
* Two EPUB files to align (e.g., original and translated versions)
* Basic familiarity with Python

Getting Started
--------------

For this tutorial, we'll use two sample books:
* ``original_book.epub`` - The source book
* ``translated_book.epub`` - The target book to align

Using the Python Library
-----------------------

Step 1: Import and Initialize
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from vivre import VivreProcessor, BookAligner

   # Initialize processors for both books
   original_processor = VivreProcessor("original_book.epub")
   translated_processor = VivreProcessor("translated_book.epub")

Step 2: Extract Content
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Extract content from both books
   original_content = original_processor.extract_content()
   translated_content = translated_processor.extract_content()

   print(f"Original book has {len(original_content)} chapters")
   print(f"Translated book has {len(translated_content)} chapters")

Step 3: Create Alignment
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Initialize the aligner
   aligner = BookAligner()

   # Align the books
   alignment_result = aligner.align_books(
       original_content,
       translated_content,
       method="semantic"  # or "structural"
   )

   print(f"Alignment completed with {len(alignment_result)} matched pairs")

Step 4: Analyze Results
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get alignment statistics
   stats = alignment_result.get_statistics()
   print(f"Confidence score: {stats.confidence:.2f}")
   print(f"Coverage: {stats.coverage:.2%}")

   # Access specific alignments
   for i, (orig_chapter, trans_chapter) in enumerate(alignment_result.pairs):
       print(f"Chapter {i+1}: {orig_chapter.title} ↔ {trans_chapter.title}")

Step 5: Export Results
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Export to various formats
   alignment_result.export_to_json("alignment_result.json")
   alignment_result.export_to_csv("alignment_result.csv")

   # Generate a detailed report
   alignment_result.generate_report("alignment_report.html")

Complete Example
~~~~~~~~~~~~~~~

Here's a complete script that demonstrates the full workflow:

.. code-block:: python

   from vivre import VivreProcessor, BookAligner
   import logging

   # Set up logging
   logging.basicConfig(level=logging.INFO)

   def align_books(original_path, translated_path, output_dir="."):
       """Align two books and save results."""

       # Initialize processors
       original_processor = VivreProcessor(original_path)
       translated_processor = VivreProcessor(translated_path)

       # Extract content
       print("Extracting content...")
       original_content = original_processor.extract_content()
       translated_content = translated_processor.extract_content()

       # Create aligner and align
       print("Aligning books...")
       aligner = BookAligner()
       result = aligner.align_books(original_content, translated_content)

       # Save results
       print("Saving results...")
       result.export_to_json(f"{output_dir}/alignment.json")
       result.generate_report(f"{output_dir}/report.html")

       return result

   # Usage
   if __name__ == "__main__":
       result = align_books("original_book.epub", "translated_book.epub")
       print(f"Alignment complete! Found {len(result.pairs)} chapter pairs.")

Using the Command Line Interface
------------------------------

The CLI provides a simpler way to align books without writing Python code.

Basic Alignment
~~~~~~~~~~~~~~~

.. code-block:: bash

   # Simple alignment of two books
   vivre align original_book.epub translated_book.epub

   # Specify output directory
   vivre align original_book.epub translated_book.epub --output-dir results/

   # Use different alignment method
   vivre align original_book.epub translated_book.epub --method structural

Advanced CLI Options
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Verbose output with progress
   vivre align original_book.epub translated_book.epub --verbose

   # Set confidence threshold
   vivre align original_book.epub translated_book.epub --confidence 0.8

   # Export to specific formats
   vivre align original_book.epub translated_book.epub \
       --output-format json,csv,html

   # Process multiple book pairs
   vivre align-batch pairs.txt --output-dir batch_results/

Batch Processing
~~~~~~~~~~~~~~~

Create a file ``pairs.txt`` with book pairs:

.. code-block:: text

   original_book1.epub,translated_book1.epub
   original_book2.epub,translated_book2.epub
   original_book3.epub,translated_book3.epub

Then run:

.. code-block:: bash

   vivre align-batch pairs.txt --output-dir batch_results/

Understanding the Output
-----------------------

Alignment Results
~~~~~~~~~~~~~~~~

The alignment process produces several output files:

* ``alignment.json`` - Raw alignment data
* ``alignment.csv`` - Tabular format for analysis
* ``report.html`` - Detailed HTML report
* ``statistics.txt`` - Summary statistics

Key Metrics
~~~~~~~~~~~

* **Confidence Score**: How reliable the alignment is (0-1)
* **Coverage**: Percentage of chapters successfully aligned
* **Precision**: Accuracy of the alignments
* **Recall**: Completeness of the alignments

Troubleshooting
--------------

Common Issues
~~~~~~~~~~~~

**Low confidence scores:**
* Check if the books have similar structure
* Try different alignment methods
* Verify the books are actually related

**Missing alignments:**
* Ensure both books have similar chapter structures
* Check for encoding issues in the EPUB files
* Try preprocessing the content

**Performance issues:**
* Use smaller books for testing
* Enable parallel processing with ``--parallel``
* Check available memory

Getting Help
~~~~~~~~~~~

.. code-block:: bash

   # Get help for alignment command
   vivre align --help

   # Get help for all commands
   vivre --help

Next Steps
----------

* Explore the :doc:`api` for advanced usage
* Check out :doc:`examples` for more complex scenarios
* Learn about :doc:`cli` for additional command-line options
