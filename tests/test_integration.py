"""
Integration tests for the full vivre pipeline.

This module contains tests that verify the complete workflow from EPUB parsing
through sentence segmentation to text alignment, ensuring all components work
together correctly.
"""

from pathlib import Path

import pytest

from vivre.align import Aligner
from vivre.parser import VivreParser
from vivre.segmenter import Segmenter


class TestFullPipeline:
    """Test the complete vivre pipeline from parsing to alignment."""

    def test_english_spanish_pipeline_integration(
        self, english_epub_path: str, spanish_epub_path: str
    ) -> None:
        """
        Test complete pipeline: parse EPUBs -> segment chapters -> align sentences.

        This test verifies that the full workflow works correctly:
        1. Parse English and Spanish EPUB files
        2. Extract first chapters from both
        3. Segment chapters into sentences
        4. Align sentences between languages

        Args:
            english_epub_path: Path to English EPUB test file
            spanish_epub_path: Path to Spanish EPUB test file

        Raises:
            AssertionError: If any step in the pipeline fails
        """
        # Initialize components
        parser = VivreParser()
        segmenter = Segmenter()
        aligner = Aligner(language_pair="en-es")

        # Step 1: Parse both EPUB files
        english_chapters = parser.parse_epub(english_epub_path)
        spanish_chapters = parser.parse_epub(spanish_epub_path)

        # Verify we got chapters from both files
        assert len(english_chapters) > 0, "Should extract chapters from English EPUB"
        assert len(spanish_chapters) > 0, "Should extract chapters from Spanish EPUB"

        # Step 2: Get first chapters and segment into sentences
        english_title, english_content = english_chapters[0]
        spanish_title, spanish_content = spanish_chapters[0]

        english_sentences = segmenter.segment(english_content, language="en")
        spanish_sentences = segmenter.segment(spanish_content, language="es")

        # Verify segmentation worked
        assert len(english_sentences) > 0, "Should segment English content"
        assert len(spanish_sentences) > 0, "Should segment Spanish content"

        # Step 3: Align sentences
        alignment = aligner.align(english_sentences, spanish_sentences)

        # Verify alignment produced results
        assert len(alignment) > 0, "Should produce alignments"

        # Verify alignment structure
        for source_seg, target_seg in alignment:
            assert isinstance(source_seg, str), "Source segment should be string"
            assert isinstance(target_seg, str), "Target segment should be string"
            assert (
                len(source_seg) > 0 or len(target_seg) > 0
            ), "Segments should not be empty"

    def test_pipeline_with_language_detection(
        self, english_epub_path: str, spanish_epub_path: str
    ) -> None:
        """
        Test pipeline with automatic language detection.

        This test verifies that the pipeline works when language detection
        is left to the segmenter rather than being explicitly specified.

        Args:
            english_epub_path: Path to English EPUB test file
            spanish_epub_path: Path to Spanish EPUB test file
        """
        parser = VivreParser()
        segmenter = Segmenter()
        aligner = Aligner(language_pair="en-es")

        # Parse and get first chapters
        english_chapters = parser.parse_epub(english_epub_path)
        spanish_chapters = parser.parse_epub(spanish_epub_path)

        english_title, english_content = english_chapters[0]
        spanish_title, spanish_content = spanish_chapters[0]

        # Segment with automatic language detection
        english_sentences = segmenter.segment(english_content)  # No language specified
        spanish_sentences = segmenter.segment(spanish_content)  # No language specified

        # Verify segmentation worked
        assert (
            len(english_sentences) > 0
        ), "Should segment English content with auto-detection"
        assert (
            len(spanish_sentences) > 0
        ), "Should segment Spanish content with auto-detection"

        # Align sentences
        alignment = aligner.align(english_sentences, spanish_sentences)
        assert (
            len(alignment) > 0
        ), "Should produce alignments with auto-detected languages"

    def test_pipeline_with_batch_processing(
        self, english_epub_path: str, spanish_epub_path: str
    ) -> None:
        """
        Test pipeline using batch processing for efficiency.

        This test verifies that the pipeline works correctly when using
        batch processing methods for better performance.

        Args:
            english_epub_path: Path to English EPUB test file
            spanish_epub_path: Path to Spanish EPUB test file
        """
        parser = VivreParser()
        segmenter = Segmenter()
        aligner = Aligner(language_pair="en-es")

        # Parse and get first few chapters
        english_chapters = parser.parse_epub(english_epub_path)
        spanish_chapters = parser.parse_epub(spanish_epub_path)

        # Take first 3 chapters from each
        english_contents = [content for _, content in english_chapters[:3]]
        spanish_contents = [content for _, content in spanish_chapters[:3]]

        # Batch segment all chapters
        english_sentence_lists = segmenter.segment_batch(
            english_contents, language="en"
        )
        spanish_sentence_lists = segmenter.segment_batch(
            spanish_contents, language="es"
        )

        # Verify batch processing worked
        assert len(english_sentence_lists) == len(
            english_contents
        ), "Should process all English chapters"
        assert len(spanish_sentence_lists) == len(
            spanish_contents
        ), "Should process all Spanish chapters"

        # Align each chapter pair
        for i, (eng_sentences, esp_sentences) in enumerate(
            zip(english_sentence_lists, spanish_sentence_lists)
        ):
            if eng_sentences and esp_sentences:  # Only align if both have content
                alignment = aligner.align(eng_sentences, esp_sentences)
                assert len(alignment) > 0, f"Should align chapter {i}"

    def test_pipeline_error_handling(self) -> None:
        """
        Test pipeline error handling with invalid inputs.

        This test verifies that the pipeline handles errors gracefully
        when given invalid or missing data.
        """
        segmenter = Segmenter()
        aligner = Aligner(language_pair="en-es")

        # Test with empty content
        empty_sentences = segmenter.segment("")
        assert empty_sentences == [], "Should handle empty content"

        # Test with None content
        none_sentences = segmenter.segment(None)  # type: ignore
        assert none_sentences == [], "Should handle None content"

        # Test alignment with empty lists
        empty_alignment = aligner.align([], [])
        assert empty_alignment == [], "Should handle empty sentence lists"

    def test_pipeline_with_custom_aligner_parameters(
        self, english_epub_path: str, spanish_epub_path: str
    ) -> None:
        """
        Test pipeline with custom aligner parameters.

        This test verifies that the pipeline works correctly when using
        custom alignment parameters for different language pairs.

        Args:
            english_epub_path: Path to English EPUB test file
            spanish_epub_path: Path to Spanish EPUB test file
        """
        parser = VivreParser()
        segmenter = Segmenter()

        # Test with custom aligner parameters
        custom_aligner = Aligner(
            language_pair="en-es",
            c=1.1,  # Custom mean ratio
            s2=7.0,  # Custom variance
            gap_penalty=4.0,  # Custom gap penalty
        )

        # Parse and segment
        english_chapters = parser.parse_epub(english_epub_path)
        spanish_chapters = parser.parse_epub(spanish_epub_path)

        english_title, english_content = english_chapters[0]
        spanish_title, spanish_content = spanish_chapters[0]

        english_sentences = segmenter.segment(english_content, language="en")
        spanish_sentences = segmenter.segment(spanish_content, language="es")

        # Align with custom parameters
        alignment = custom_aligner.align(english_sentences, spanish_sentences)
        assert len(alignment) > 0, "Should align with custom parameters"


@pytest.fixture
def english_epub_path() -> str:
    """
    Provide path to English EPUB test file.

    Returns:
        Path to English EPUB test file for integration tests.
    """
    # Use the existing Percy Jackson English EPUB if available
    test_data_dir = Path(__file__).parent / "data"
    english_epub = test_data_dir / "percy_jackson_english.epub"

    if not english_epub.exists():
        pytest.skip("English EPUB test file not found")

    return str(english_epub)


@pytest.fixture
def spanish_epub_path() -> str:
    """
    Provide path to Spanish EPUB test file.

    Returns:
        Path to Spanish EPUB test file for integration tests.
    """
    # Use the existing Percy Jackson Spanish EPUB if available
    test_data_dir = Path(__file__).parent / "data"
    spanish_epub = test_data_dir / "percy_jackson_spanish.epub"

    if not spanish_epub.exists():
        pytest.skip("Spanish EPUB test file not found")

    return str(spanish_epub)
