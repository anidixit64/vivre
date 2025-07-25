"""
Tests for the top-level API functions.
"""

import json
from pathlib import Path

import pytest

from vivre import align, read


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

        result = align(source_epub, target_epub, form="json")

        assert isinstance(result, str)

        # Should be valid JSON
        parsed = json.loads(result)
        assert "book_title" in parsed
        assert "language_pair" in parsed
        assert "chapters" in parsed
        assert isinstance(parsed["chapters"], dict)

    def test_align_returns_dict(self):
        """Test that align() returns dict when form='dict'."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = align(source_epub, target_epub, form="dict")

        assert isinstance(result, dict)
        assert "book_title" in result
        assert "language_pair" in result
        assert "chapters" in result

    def test_align_returns_text(self):
        """Test that align() returns text when form='text'."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = align(source_epub, target_epub, form="text")

        assert isinstance(result, str)
        assert "Book:" in result
        assert "Language Pair:" in result
        assert "Chapter" in result

    def test_align_returns_csv(self):
        """Test that align() returns CSV when form='csv'."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = align(source_epub, target_epub, form="csv")

        assert isinstance(result, str)
        lines = result.split("\n")
        assert len(lines) > 1
        assert "chapter,title," in lines[0]

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
            align(source_epub, target_epub, method="invalid")

    def test_align_invalid_format(self):
        """Test that align() raises error for invalid format."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        with pytest.raises(ValueError, match="Format 'invalid' not supported"):
            align(source_epub, target_epub, form="invalid")

    def test_align_auto_detect_language_pair(self):
        """Test that align() auto-detects language pair from filenames."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = align(source_epub, target_epub, form="dict")

        # Should auto-detect en-es from filenames
        assert result["language_pair"] == "en-es"

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

        result = align(source_epub, target_epub, language_pair="en-fr", form="dict")

        assert result["language_pair"] == "en-fr"

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
            source_epub, target_epub, c=1.1, s2=7.0, gap_penalty=2.5, form="dict"
        )

        assert isinstance(result, dict)
        assert "book_title" in result
        assert "language_pair" in result

    def test_align_language_detection_edge_cases(self):
        """Test language detection with various filename patterns."""
        from vivre.api import _detect_language_from_filename

        # Test English patterns
        assert _detect_language_from_filename("english_book.epub") == "en"
        assert _detect_language_from_filename("book_en.epub") == "en"
        assert _detect_language_from_filename("book.en.epub") == "en"
        assert _detect_language_from_filename("vacation under the volcano.epub") == "en"

        # Test Spanish patterns
        assert _detect_language_from_filename("spanish_book.epub") == "es"
        assert _detect_language_from_filename("book_es.epub") == "es"
        assert _detect_language_from_filename("book.es.epub") == "es"
        assert (
            _detect_language_from_filename("vacaciones al pie de un volcán.epub")
            == "es"
        )

        # Test French patterns
        assert _detect_language_from_filename("french_book.epub") == "fr"
        assert _detect_language_from_filename("book_fr.epub") == "fr"
        assert _detect_language_from_filename("book.fr.epub") == "fr"

        # Test unknown pattern (should default to English)
        assert _detect_language_from_filename("unknown_book.epub") == "en"


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
        corpus = align(source_epub, target_epub, form="dict")

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

            # Check alignment structure
            for alignment in chapter_data["alignments"]:
                assert "en" in alignment
                assert "es" in alignment
                # Allow empty strings as they might occur in alignment
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

        result = align(source_epub, target_epub, form="csv")

        # Check that CSV is properly formatted
        lines = result.split("\n")
        assert len(lines) > 1

        # Check header
        assert "chapter,title,en,es" in lines[0]

        # Check that quotes are properly escaped in CSV
        for line in lines[1:]:
            if line.strip():  # Skip empty lines
                # Should have proper CSV structure
                assert line.count('"') % 2 == 0  # Even number of quotes

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

        result = align(source_epub, target_epub, form="text")

        lines = result.split("\n")

        # Check structure
        assert any("Book:" in line for line in lines)
        assert any("Language Pair:" in line for line in lines)
        assert any("Chapter" in line for line in lines)
        assert any("EN:" in line for line in lines)
        assert any("ES:" in line for line in lines)
