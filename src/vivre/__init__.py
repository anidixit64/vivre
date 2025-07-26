"""
Vivre - A Python library for machine learning and corpus linguistics.

This library provides tools for processing parallel texts through a complete
pipeline: parsing EPUB files, segmenting text into sentences, and aligning
sentences between languages.

Main Components:
    - VivreParser: Robust EPUB parsing with content filtering
    - Segmenter: Multi-language sentence segmentation using spaCy
    - Aligner: Statistical text alignment using the Gale-Church algorithm
    - VivrePipeline: High-level interface for the complete pipeline

Top-level Functions:
    - read(): Parse EPUB files and extract chapters
    - align(): Align parallel texts and output in various formats
    - quick_align(): Simple one-liner for basic alignment
    - get_supported_languages(): Get list of supported languages

Example:
    >>> import vivre

    # Simple usage with top-level functions
    >>> chapters = vivre.read('path/to/epub')
    >>> print(f"Found {len(chapters)} chapters")
    >>> sentences = chapters.segment()
    >>> corpus = vivre.align('english.epub', 'french.epub', form='json')

    # Quick alignment for simple use cases
    >>> pairs = vivre.quick_align('english.epub', 'french.epub')
    >>> for source, target in pairs[:3]:
    ...     print(f"EN: {source}")
    ...     print(f"FR: {target}")

    # Advanced usage with classes
    >>> from vivre import VivrePipeline
    >>> pipeline = VivrePipeline("en-es")
    >>> alignments = pipeline.process_parallel_epubs(
    ...     "english_book.epub", "spanish_book.epub"
    ... )
    >>> for source, target in alignments:
    ...     print(f"EN: {source}")
    ...     print(f"ES: {target}")

Command Line Usage:
    # Parse an EPUB file
    $ vivre parse book.epub

    # Align two EPUB files
    $ vivre align english.epub french.epub --format json

    # Get help
    $ vivre --help
"""

from .align import Aligner
from .api import Chapters, align, get_supported_languages, quick_align, read
from .integration import VivrePipeline, create_pipeline
from .parser import VivreParser
from .segmenter import Segmenter

__version__ = "0.1.0"
__author__ = "Aniket Dixit"
__email__ = "aniketdixit00.ani@gmail.com"

__all__ = [
    "Aligner",
    "VivreParser",
    "Segmenter",
    "VivrePipeline",
    "create_pipeline",
    "read",
    "align",
    "quick_align",
    "get_supported_languages",
    "Chapters",
]
