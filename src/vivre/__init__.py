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

Example:
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
]
