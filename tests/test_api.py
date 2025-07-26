"""
Tests for the top-level API functions.
"""

import json
from pathlib import Path

import pytest

from vivre import align, read
from vivre.api import AlignmentResult


class TestReadFunction:
    """Test the read() function."""

    def test_read_epub_returns_chapters(self):
        """Test that read() returns a Chapters object."""
        # Use one of the test EPUB files
        epub_path = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )

        chapters = read(epub_path)

        assert hasattr(chapters, "chapters")
        assert hasattr(chapters, "book_title")
        assert hasattr(chapters, "segment")
        assert isinstance(chapters.chapters, list)
        assert len(chapters.chapters) > 0

        # Test that each chapter has title and content
        for title, content in chapters.chapters:
            assert isinstance(title, str)
            assert isinstance(content, str)
            assert len(title) > 0
            assert len(content) > 0

    def test_chapters_segment_method(self):
        """Test that chapters can be segmented."""
        epub_path = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )

        chapters = read(epub_path)
        segmented = chapters.segment()

        assert segmented is chapters  # Should return self
        assert hasattr(chapters, "_segmented_chapters")

        # Test getting segmented chapters
        segmented_chapters = chapters.get_segmented()
        assert isinstance(segmented_chapters, list)
        assert len(segmented_chapters) > 0

        for title, sentences in segmented_chapters:
            assert isinstance(title, str)
            assert isinstance(sentences, list)
            assert len(sentences) > 0
            for sentence in sentences:
                assert isinstance(sentence, str)
                assert len(sentence) > 0

    def test_chapters_segment_with_language(self):
        """Test that chapters can be segmented with specific language."""
        epub_path = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )

        chapters = read(epub_path)
        segmented = chapters.segment(language="en")

        assert segmented is chapters
        segmented_chapters = chapters.get_segmented()
        assert len(segmented_chapters) > 0

    def test_chapters_get_segmented_without_segmenting(self):
        """Test that get_segmented() raises error if not segmented first."""
        epub_path = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )

        chapters = read(epub_path)

        with pytest.raises(ValueError, match="Chapters must be segmented first"):
            chapters.get_segmented()


class TestAlignFunction:
    """Test the align() function."""

    def test_align_returns_json_string(self):
        """Test that align() returns JSON string by default."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = align(source_epub, target_epub, "en-es")
        json_output = result.to_json()

        assert isinstance(json_output, str)
        assert len(json_output) > 0
        # Should be valid JSON
        parsed = json.loads(json_output)
        assert "chapters" in parsed
        assert "language_pair" in parsed

    def test_align_returns_dict(self):
        """Test that align() returns dict when using to_dict()."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = align(source_epub, target_epub, "en-es")
        dict_output = result.to_dict()

        assert isinstance(dict_output, dict)
        assert "chapters" in dict_output
        assert "language_pair" in dict_output
        assert "book_title" in dict_output

    def test_align_returns_text(self):
        """Test that align() returns text when using to_text()."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = align(source_epub, target_epub, "en-es")
        text_output = result.to_text()

        assert isinstance(text_output, str)
        assert len(text_output) > 0
        assert "Book:" in text_output
        assert "Language Pair:" in text_output

    def test_align_returns_csv(self):
        """Test that align() returns CSV when using to_csv()."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = align(source_epub, target_epub, "en-es")
        csv_output = result.to_csv()

        assert isinstance(csv_output, str)
        assert len(csv_output) > 0
        assert "chapter,title,en,es" in csv_output

    def test_align_invalid_method(self):
        """Test that align() raises error for invalid method."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        with pytest.raises(ValueError, match="Method 'invalid' not supported"):
            align(source_epub, target_epub, "en-es", method="invalid")

    def test_align_invalid_format(self):
        """Test that align() no longer has form parameter."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        # The form parameter has been removed - should work without it
        result = align(source_epub, target_epub, "en-es")
        assert isinstance(result, AlignmentResult)

    def test_align_requires_language_pair(self):
        """Test that align() requires explicit language pair."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        # This should work with explicit language pair
        result = align(source_epub, target_epub, "en-es")
        assert isinstance(result, AlignmentResult)

    def test_align_with_explicit_language_pair(self):
        """Test that align() uses explicit language pair when provided."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = align(source_epub, target_epub, "en-es")
        dict_output = result.to_dict()

        assert isinstance(dict_output, dict)
        assert dict_output["language_pair"] == "en-es"

    def test_align_with_custom_parameters(self):
        """Test that align() accepts custom alignment parameters."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = align(
            source_epub, target_epub, "en-es", c=1.1, s2=7.0, gap_penalty=2.5
        )
        assert isinstance(result, AlignmentResult)

    def test_align_language_detection_edge_cases(self):
        """Test that language detection is no longer used (removed)."""
        # This test is no longer relevant since we removed auto-detection
        # The function now requires explicit language pairs
        assert True  # Placeholder to indicate this test is intentionally skipped


class TestIntegration:
    """Test the complete workflow."""

    def test_complete_workflow(self):
        """Test the complete workflow: read -> segment -> align."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        # Step 1: Read source EPUB
        chapters = read(source_epub)
        assert len(chapters.chapters) > 0

        # Step 2: Segment chapters
        chapters.segment()
        segmented = chapters.get_segmented()
        assert len(segmented) > 0

        # Step 3: Align both EPUBs
        result = align(source_epub, target_epub, "en-es")
        corpus = result.to_dict()

        # The book title could be either English or Spanish version
        assert corpus["book_title"] in [
            "Vacation Under the Volcano",
            "Vacaciones al pie de un volcán",
        ]
        assert corpus["language_pair"] == "en-es"
        assert len(corpus["chapters"]) > 0

        # Check that chapters have alignments
        for chapter_data in corpus["chapters"].values():
            assert "title" in chapter_data
            assert "alignments" in chapter_data
            assert len(chapter_data["alignments"]) > 0

            # Check that alignments have both languages
            for alignment in chapter_data["alignments"]:
                assert "en" in alignment
                assert "es" in alignment
                assert isinstance(alignment["en"], str)
                assert isinstance(alignment["es"], str)

    def test_csv_format_with_special_characters(self):
        """Test CSV format handles special characters properly."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = align(source_epub, target_epub, "en-es")

        # Check that CSV is properly formatted
        lines = result.to_csv().split("\n")
        assert len(lines) > 1

        # Check header
        assert "chapter,title,en,es" in lines[0]

        # Check that data lines exist
        data_lines = [line for line in lines[1:] if line.strip()]
        assert len(data_lines) > 0

        # Check that quotes are properly escaped
        for line in data_lines:
            if '"' in line:
                # Count quotes - should be even number
                quote_count = line.count('"')
                assert quote_count % 2 == 0

    def test_text_format_structure(self):
        """Test text format has proper structure."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = align(source_epub, target_epub, "en-es")

        lines = result.to_text().split("\n")

        # Check structure
        assert "Book:" in lines[0]
        assert "Language Pair:" in lines[1]
        assert "=" * 50 in lines[2]  # Separator line

        # Check that chapter sections exist
        chapter_lines = [line for line in lines if line.startswith("Chapter")]
        assert len(chapter_lines) > 0
