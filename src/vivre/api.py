"""
Top-level API functions for the vivre library.

This module provides simple, user-friendly functions for common tasks:
- read(): Parse EPUB files and extract chapters
- align(): Align parallel texts and output in various formats
- quick_align(): Simple one-liner for basic alignment
- get_supported_languages(): Get list of supported languages
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from .integration import VivrePipeline
from .parser import VivreParser
from .segmenter import Segmenter


class Chapters:
    """
    A container for parsed chapters with segmentation capabilities.

    This class holds the parsed chapters and provides methods to segment
    the text into sentences.
    """

    def __init__(self, chapters: List[Tuple[str, str]], book_title: str = ""):
        """
        Initialize with parsed chapters.

        Args:
            chapters: List of (title, content) tuples
            book_title: Title of the book
        """
        self.chapters = chapters
        self.book_title = book_title
        self._segmented_chapters: Optional[List[Tuple[str, List[str]]]] = None
        self._segmenter = Segmenter()

    def segment(self, language: Optional[str] = None) -> "Chapters":
        """
        Segment all chapters into sentences.

        Args:
            language: Language code for segmentation (auto-detected if None)

        Returns:
            Self with segmented chapters
        """
        segmented = []
        for title, content in self.chapters:
            sentences = self._segmenter.segment(content, language)
            segmented.append((title, sentences))

        self._segmented_chapters = segmented
        return self

    def get_segmented(self) -> List[Tuple[str, List[str]]]:
        """Get the segmented chapters."""
        if self._segmented_chapters is None:
            raise ValueError(
                "Chapters must be segmented first. Call .segment() method."
            )
        return self._segmented_chapters

    def __len__(self) -> int:
        """Return the number of chapters."""
        return len(self.chapters)

    def __getitem__(self, index: int) -> Tuple[str, str]:
        """Get a chapter by index."""
        return self.chapters[index]

    def __iter__(self):
        """Iterate over chapters."""
        return iter(self.chapters)

    def __repr__(self) -> str:
        """String representation."""
        return f"Chapters(book_title='{self.book_title}', chapters={len(self.chapters)})"


def read(epub_path: Union[str, Path]) -> Chapters:
    """
    Parse an EPUB file and extract chapters.

    Args:
        epub_path: Path to the EPUB file

    Returns:
        Chapters object containing parsed chapters

    Raises:
        FileNotFoundError: If the EPUB file doesn't exist
        ValueError: If the file is not a valid EPUB

    Example:
        >>> chapters = vivre.read('path/to/epub')
        >>> print(f"Found {len(chapters)} chapters")
        >>> for title, content in chapters:
        ...     print(f"Chapter: {title}")
    """
    epub_path = Path(epub_path)
    if not epub_path.exists():
        raise FileNotFoundError(f"EPUB file not found: {epub_path}")
    
    parser = VivreParser()
    try:
        chapters = parser.parse_epub(epub_path)
        book_title = getattr(parser, "_book_title", "")
        return Chapters(chapters, book_title)
    except Exception as e:
        raise ValueError(f"Failed to parse EPUB file {epub_path}: {e}")


def align(
    source_epub: Union[str, Path],
    target_epub: Union[str, Path],
    method: str = "gale-church",
    form: str = "json",
    language_pair: Optional[str] = None,
    **kwargs: Any,
) -> Union[str, Dict[str, Any]]:
    """
    Align parallel EPUB files and output in the specified format.

    Args:
        source_epub: Path to source language EPUB
        target_epub: Path to target language EPUB
        method: Alignment method (currently only "gale-church" supported)
        form: Output format ("json", "text", "csv", "xml", "dict")
        language_pair: Language pair code (e.g., "en-fr", auto-detected if None)
        **kwargs: Additional arguments passed to the pipeline

    Returns:
        Aligned corpus in the specified format

    Raises:
        FileNotFoundError: If either EPUB file doesn't exist
        ValueError: If method or format is not supported

    Example:
        >>> corpus = vivre.align('english.epub', 'french.epub', form='json')
        >>> print(corpus)
        
        >>> # Get as dictionary for programmatic access
        >>> data = vivre.align('english.epub', 'french.epub', form='dict')
        >>> print(f"Found {data['total_alignments']} alignments")
    """
    source_epub = Path(source_epub)
    target_epub = Path(target_epub)
    
    if not source_epub.exists():
        raise FileNotFoundError(f"Source EPUB file not found: {source_epub}")
    if not target_epub.exists():
        raise FileNotFoundError(f"Target EPUB file not found: {target_epub}")
    
    if method != "gale-church":
        raise ValueError(f"Method '{method}' not supported. Only 'gale-church' is available.")
    
    if form.lower() not in ["json", "dict", "text", "csv", "xml"]:
        raise ValueError(f"Format '{form}' not supported. Use 'json', 'dict', 'text', 'csv', or 'xml'.")
    
    # Auto-detect language pair from filenames if not provided
    if language_pair is None:
        source_lang = _detect_language_from_filename(source_epub)
        target_lang = _detect_language_from_filename(target_epub)
        language_pair = f"{source_lang}-{target_lang}"
    
    # Create pipeline and process
    try:
        pipeline = VivrePipeline(language_pair, **kwargs)
        
        # Parse both EPUBs
        source_chapters = pipeline.parser.parse_epub(source_epub)
        target_chapters = pipeline.parser.parse_epub(target_epub)
        
        # Get book titles
        source_title = getattr(pipeline.parser, '_book_title', '')
        target_title = getattr(pipeline.parser, '_book_title', '')
        book_title = source_title or target_title
        
        # Process chapters and create aligned corpus
        aligned_corpus = _create_aligned_corpus(
            source_chapters, target_chapters, pipeline, book_title, language_pair
        )
        
        # Format output
        if form.lower() == "json":
            return json.dumps(aligned_corpus, indent=2, ensure_ascii=False)
        elif form.lower() == "dict":
            return aligned_corpus
        elif form.lower() == "text":
            return _format_as_text(aligned_corpus)
        elif form.lower() == "csv":
            return _format_as_csv(aligned_corpus)
        elif form.lower() == "xml":
            return _format_as_xml(aligned_corpus)
        else:
            return json.dumps(aligned_corpus, indent=2, ensure_ascii=False)
    except Exception as e:
        raise ValueError(f"Failed to align EPUB files: {e}")


def quick_align(
    source_epub: Union[str, Path],
    target_epub: Union[str, Path],
    language_pair: Optional[str] = None,
) -> List[Tuple[str, str]]:
    """
    Quick alignment function that returns simple sentence pairs.
    
    This is a convenience function for when you just need the aligned sentences
    without the full metadata and formatting options.

    Args:
        source_epub: Path to source language EPUB
        target_epub: Path to target language EPUB
        language_pair: Language pair code (auto-detected if None)

    Returns:
        List of (source_sentence, target_sentence) tuples

    Example:
        >>> pairs = vivre.quick_align('english.epub', 'french.epub')
        >>> for source, target in pairs[:5]:  # Show first 5 pairs
        ...     print(f"EN: {source}")
        ...     print(f"FR: {target}")
        ...     print()
    """
    result = align(source_epub, target_epub, form="dict", language_pair=language_pair)
    
    # Extract sentence pairs from the result
    pairs = []
    for chapter_data in result["chapters"].values():
        for alignment in chapter_data["alignments"]:
            source_lang, target_lang = result["language_pair"].split("-")
            pairs.append((alignment[source_lang], alignment[target_lang]))
    
    return pairs


def get_supported_languages() -> List[str]:
    """
    Get a list of supported languages for segmentation.
    
    Returns:
        List of supported language codes
        
    Example:
        >>> langs = vivre.get_supported_languages()
        >>> print(f"Supported languages: {', '.join(langs)}")
    """
    segmenter = Segmenter()
    return list(segmenter._supported_languages.keys())


def _detect_language_from_filename(filepath: Union[str, Path]) -> str:
    """Detect language from filename patterns."""
    filename = str(filepath).lower()

    # Common language patterns in filenames
    lang_patterns = {
        "en": ["english", "en_", "_en", ".en", "vacation under the volcano"],
        "fr": ["french", "fr_", "_fr", ".fr"],
        "es": ["spanish", "es_", "_es", ".es", "vacaciones al pie de un volcán"],
        "de": ["german", "de_", "_de", ".de"],
        "it": ["italian", "it_", "_it", ".it"],
        "pt": ["portuguese", "pt_", "_pt", ".pt"],
    }

    for lang, patterns in lang_patterns.items():
        if any(pattern in filename for pattern in patterns):
            return lang

    # Default to English if no pattern matches
    return "en"


def _create_aligned_corpus(
    source_chapters: List[Tuple[str, str]],
    target_chapters: List[Tuple[str, str]],
    pipeline: VivrePipeline,
    book_title: str,
    language_pair: str,
) -> Dict[str, Any]:
    """Create the aligned corpus structure."""
    source_lang, target_lang = language_pair.split("-")

    corpus: Dict[str, Any] = {
        "book_title": book_title,
        "language_pair": language_pair,
        "chapters": {},
    }

    # Process each chapter pair
    for i, (
        (source_title, source_content),
        (target_title, target_content),
    ) in enumerate(zip(source_chapters, target_chapters), 1):
        # Segment both chapters
        source_sentences = pipeline.segmenter.segment(source_content)
        target_sentences = pipeline.segmenter.segment(target_content)

        # Align sentences
        alignments = pipeline.aligner.align(source_sentences, target_sentences)

        # Format alignments
        chapter_alignments = []
        for source_sent, target_sent in alignments:
            chapter_alignments.append(
                {source_lang: source_sent, target_lang: target_sent}
            )

        # Add chapter to corpus
        corpus["chapters"][str(i)] = {
            "title": source_title,  # Use source title as primary
            "alignments": chapter_alignments,
        }

    return corpus


def _format_as_text(corpus: Dict[str, Any]) -> str:
    """Format corpus as plain text."""
    lines = []
    lines.append(f"Book: {corpus['book_title']}")
    lines.append(f"Language Pair: {corpus['language_pair']}")
    lines.append("=" * 50)

    for chapter_num, chapter_data in corpus["chapters"].items():
        lines.append(f"\nChapter {chapter_num}: {chapter_data['title']}")
        lines.append("-" * 30)

        for i, alignment in enumerate(chapter_data["alignments"], 1):
            source_lang, target_lang = corpus["language_pair"].split("-")
            lines.append(f"{i}. {source_lang.upper()}: {alignment[source_lang]}")
            lines.append(f"   {target_lang.upper()}: {alignment[target_lang]}")
            lines.append("")

    return "\n".join(lines)


def _format_as_csv(corpus: Dict[str, Any]) -> str:
    """Format corpus as CSV."""
    source_lang, target_lang = corpus["language_pair"].split("-")

    lines = [f"chapter,title,{source_lang},{target_lang}"]

    for chapter_num, chapter_data in corpus["chapters"].items():
        title = chapter_data["title"].replace('"', '""')  # Escape quotes

        for alignment in chapter_data["alignments"]:
            source_text = alignment[source_lang].replace('"', '""')
            target_text = alignment[target_lang].replace('"', '""')
            lines.append(f'"{chapter_num}","{title}","{source_text}","{target_text}"')

    return "\n".join(lines)


def _format_as_xml(corpus: Dict[str, Any]) -> str:
    """Format corpus as XML."""
    source_lang, target_lang = corpus['language_pair'].split('-')
    
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<alignments>',
        f'  <book_title>{corpus["book_title"]}</book_title>',
        f'  <language_pair>{corpus["language_pair"]}</language_pair>',
        f'  <total_alignments>{len(corpus["chapters"])}</total_alignments>',
    ]
    
    for chapter_num, chapter_data in corpus['chapters'].items():
        xml_lines.extend([
            f'  <chapter number="{chapter_num}">',
            f'    <title>{chapter_data["title"]}</title>',
            '    <alignments>',
        ])
        
        for alignment in chapter_data['alignments']:
            xml_lines.extend([
                '      <alignment>',
                f'        <{source_lang}>{alignment[source_lang]}</{source_lang}>',
                f'        <{target_lang}>{alignment[target_lang]}</{target_lang}>',
                '      </alignment>',
            ])
        
        xml_lines.extend(['    </alignments>', '  </chapter>'])
    
    xml_lines.append('</alignments>')
    return '\n'.join(xml_lines)
