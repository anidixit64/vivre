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

Example:
    >>> import vivre

    # Simple usage with top-level functions
    >>> chapters = vivre.read('path/to/epub')
    >>> sentences = chapters.segment()
    >>> corpus = vivre.align('english.epub', 'french.epub', form='json')

    # Advanced usage with classes
    >>> from vivre import VivrePipeline
    >>> pipeline = VivrePipeline("en-es")
    >>> alignments = pipeline.process_parallel_epubs(
    ...     "english_book.epub", "spanish_book.epub"
    ... )
    >>> for source, target in alignments:
    ...     print(f"EN: {source}")
    ...     print(f"ES: {target}")
"""

from .align import Aligner
from .api import Chapters, align, read
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
    "Chapters",
]
