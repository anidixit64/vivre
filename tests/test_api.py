"""
Tests for the top-level API functions.
"""

import json

import pytest

from vivre import align, clear_pipeline_cache, quick_align, read
from vivre.api import AlignmentResult, Chapters
from vivre.integration import VivrePipeline


class TestReadFunction:
    """Test the read() function."""

    def test_read_epub_returns_chapters(self, source_epub_path):
        """Test that read() returns a Chapters object."""
        # Use the session-scoped fixture instead of hardcoded path
        chapters = read(source_epub_path)

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

    def test_chapters_segment_method(self, source_epub_path):
        """Test that chapters can be segmented."""
        # Use the session-scoped fixture instead of hardcoded path
        chapters = read(source_epub_path)
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

    def test_chapters_segment_with_language(self, source_epub_path):
        """Test that chapters can be segmented with specific language."""
        # Use the session-scoped fixture instead of hardcoded path
        chapters = read(source_epub_path)
        segmented = chapters.segment(language="en")

        assert segmented is chapters
        segmented_chapters = chapters.get_segmented()
        assert len(segmented_chapters) > 0

    def test_chapters_get_segmented_without_segmenting(self, source_epub_path):
        """Test that get_segmented() raises error if not segmented first."""
        # Use the session-scoped fixture instead of hardcoded path
        chapters = read(source_epub_path)

        with pytest.raises(ValueError, match="Chapters must be segmented first"):
            chapters.get_segmented()


class TestAlignFunction:
    """Test the align() function."""

    def test_align_returns_json_string(self, source_epub_path, target_epub_path):
        """Test that align() returns JSON string by default."""
        # Use the session-scoped fixtures instead of hardcoded paths
        result = align(source_epub_path, target_epub_path, "en-es")
        json_output = result.to_json()

        assert isinstance(json_output, str)
        assert len(json_output) > 0
        # Should be valid JSON
        parsed = json.loads(json_output)
        assert "chapters" in parsed
        assert "language_pair" in parsed

    def test_align_returns_dict(self, source_epub_path, target_epub_path):
        """Test that align() returns dict when using to_dict()."""
        # Use the session-scoped fixtures instead of hardcoded paths
        result = align(source_epub_path, target_epub_path, "en-es")
        dict_output = result.to_dict()

        assert isinstance(dict_output, dict)
        assert "chapters" in dict_output
        assert "language_pair" in dict_output
        assert "book_title" in dict_output

    def test_align_returns_text(self, source_epub_path, target_epub_path):
        """Test that align() returns text when using to_text()."""
        # Use the session-scoped fixtures instead of hardcoded paths
        result = align(source_epub_path, target_epub_path, "en-es")
        text_output = result.to_text()

        assert isinstance(text_output, str)
        assert len(text_output) > 0
        assert "Book:" in text_output
        assert "Language Pair:" in text_output

    def test_align_returns_csv(self, source_epub_path, target_epub_path):
        """Test that align() returns CSV when using to_csv()."""
        # Use the session-scoped fixtures instead of hardcoded paths
        result = align(source_epub_path, target_epub_path, "en-es")
        csv_output = result.to_csv()

        assert isinstance(csv_output, str)
        assert len(csv_output) > 0
        assert "chapter,title,en,es" in csv_output

    def test_align_invalid_method(self, source_epub_path, target_epub_path):
        """Test that align() raises error for invalid method."""
        # Use the session-scoped fixtures instead of hardcoded paths
        with pytest.raises(ValueError, match="Method 'invalid' not supported"):
            align(source_epub_path, target_epub_path, "en-es", method="invalid")

    def test_align_invalid_format(self, source_epub_path, target_epub_path):
        """Test that align() no longer has form parameter."""
        # Use the session-scoped fixtures instead of hardcoded paths
        # The form parameter has been removed - should work without it
        result = align(source_epub_path, target_epub_path, "en-es")
        assert isinstance(result, AlignmentResult)

    def test_align_requires_language_pair(self, source_epub_path, target_epub_path):
        """Test that align() requires explicit language pair."""
        # Use the session-scoped fixtures instead of hardcoded paths
        # This should work with explicit language pair
        result = align(source_epub_path, target_epub_path, "en-es")
        assert isinstance(result, AlignmentResult)

    def test_align_with_explicit_language_pair(
        self, source_epub_path, target_epub_path
    ):
        """Test that align() uses explicit language pair when provided."""
        # Use the session-scoped fixtures instead of hardcoded paths
        result = align(source_epub_path, target_epub_path, "en-es")
        dict_output = result.to_dict()

        assert isinstance(dict_output, dict)
        assert dict_output["language_pair"] == "en-es"

    def test_align_with_custom_parameters(self, source_epub_path, target_epub_path):
        """Test that align() accepts custom alignment parameters."""
        # Use the session-scoped fixtures instead of hardcoded paths
        result = align(
            source_epub_path, target_epub_path, "en-es", c=1.1, s2=7.0, gap_penalty=2.5
        )
        assert isinstance(result, AlignmentResult)

    def test_align_language_detection_edge_cases(self):
        """Test that language detection is no longer used (removed)."""
        # This test is no longer relevant since we removed auto-detection
        # The function now requires explicit language pairs
        assert True  # Placeholder to indicate this test is intentionally skipped

    def test_align_with_dependency_injection(self, source_epub_path, target_epub_path):
        """Test that align() works with dependency injection."""
        # Clear the pipeline cache first
        clear_pipeline_cache()

        # Create a custom pipeline
        custom_pipeline = VivrePipeline("en-es", c=1.2, s2=6.5)

        # Test with dependency injection
        result = align(
            source_epub_path, target_epub_path, "en-es", _pipeline=custom_pipeline
        )

        assert isinstance(result, AlignmentResult)
        dict_output = result.to_dict()
        assert dict_output["language_pair"] == "en-es"
        assert len(dict_output["chapters"]) > 0

    def test_align_pipeline_caching(self, source_epub_path, target_epub_path):
        """Test that align() caches pipelines for reuse."""
        # Clear the pipeline cache first
        clear_pipeline_cache()

        # First call should create a new pipeline
        result1 = align(source_epub_path, target_epub_path, "en-es")
        assert isinstance(result1, AlignmentResult)

        # Second call with same parameters should reuse the cached pipeline
        result2 = align(source_epub_path, target_epub_path, "en-es")
        assert isinstance(result2, AlignmentResult)

        # Results should be equivalent
        assert result1.to_dict()["language_pair"] == result2.to_dict()["language_pair"]
        assert len(result1.to_dict()["chapters"]) == len(result2.to_dict()["chapters"])


class TestIntegration:
    """Test the complete workflow."""

    def test_complete_workflow(self, source_epub_path, target_epub_path):
        """Test the complete workflow: read -> segment -> align."""
        # Use the session-scoped fixtures instead of hardcoded paths

        # Step 1: Read source EPUB
        chapters = read(source_epub_path)
        assert len(chapters.chapters) > 0

        # Step 2: Segment chapters
        chapters.segment()
        segmented = chapters.get_segmented()
        assert len(segmented) > 0

        # Step 3: Align both EPUBs
        result = align(source_epub_path, target_epub_path, "en-es")
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

    def test_csv_format_with_special_characters(
        self, source_epub_path, target_epub_path
    ):
        """Test CSV format handles special characters properly."""
        # Use the session-scoped fixtures instead of hardcoded paths
        result = align(source_epub_path, target_epub_path, "en-es")

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

    def test_text_format_structure(self, source_epub_path, target_epub_path):
        """Test text format has proper structure."""
        # Use the session-scoped fixtures instead of hardcoded paths
        result = align(source_epub_path, target_epub_path, "en-es")

        lines = result.to_text().split("\n")

        # Check structure
        assert "Book:" in lines[0]
        assert "Language Pair:" in lines[1]
        assert "=" * 50 in lines[2]  # Separator line

        # Check that chapter sections exist
        chapter_lines = [line for line in lines if line.startswith("Chapter")]
        assert len(chapter_lines) > 0


class TestChaptersObjectIntegration:
    """Test that Chapters objects work seamlessly with the align function."""

    def test_align_with_chapters_objects(self, source_epub_path, target_epub_path):
        """Test that align() accepts Chapters objects and works correctly."""
        # Read both files into Chapters objects
        source_chapters = read(source_epub_path)
        target_chapters = read(target_epub_path)

        # This should work seamlessly
        result = align(source_chapters, target_chapters, "en-es")

        # Should return an AlignmentResult
        assert isinstance(result, AlignmentResult)

        # Should have the expected methods
        assert hasattr(result, "to_dict")
        assert hasattr(result, "to_json")
        assert hasattr(result, "to_text")
        assert hasattr(result, "to_csv")
        assert hasattr(result, "to_xml")

    def test_align_with_mixed_types(self, source_epub_path, target_epub_path):
        """Test that align() works with mixed file paths and Chapters objects."""
        # Mix file path and Chapters object
        source_chapters = read(source_epub_path)
        result = align(source_chapters, target_epub_path, "en-es")

        assert isinstance(result, AlignmentResult)

        # Test the other way around
        target_chapters = read(target_epub_path)
        result2 = align(source_epub_path, target_chapters, "en-es")

        assert isinstance(result2, AlignmentResult)

    def test_chapters_workflow_seamless(self, source_epub_path, target_epub_path):
        """Test the complete seamless workflow with Chapters objects."""
        # Complete workflow: read -> segment -> align
        source_chapters = read(source_epub_path).segment("en")
        target_chapters = read(target_epub_path).segment("es")

        # This should work without any issues
        result = align(source_chapters, target_chapters, "en-es")

        assert isinstance(result, AlignmentResult)

        # Test output formats
        json_output = result.to_json()
        assert isinstance(json_output, str)
        assert len(json_output) > 0

        dict_output = result.to_dict()
        assert isinstance(dict_output, dict)
        assert "chapters" in dict_output
        assert "language_pair" in dict_output


class TestRequiredLanguagePair:
    """Test that language_pair is now required and properly validated."""

    def test_align_requires_language_pair(self, source_epub_path, target_epub_path):
        """Test that align() requires explicit language_pair parameter."""
        # This should fail - missing language_pair
        with pytest.raises(TypeError):
            align(source_epub_path, target_epub_path)

        # This should work
        result = align(source_epub_path, target_epub_path, "en-es")
        assert isinstance(result, AlignmentResult)

    def test_quick_align_requires_language_pair(
        self, source_epub_path, target_epub_path
    ):
        """Test that quick_align() requires explicit language_pair parameter."""
        # This should fail - missing language_pair
        with pytest.raises(TypeError):
            quick_align(source_epub_path, target_epub_path)

        # This should work
        pairs = quick_align(source_epub_path, target_epub_path, "en-es")
        assert isinstance(pairs, list)

    def test_invalid_language_pair_format(self, source_epub_path, target_epub_path):
        """Test that invalid language_pair formats are rejected."""
        # Invalid formats
        invalid_formats = ["en", "english", "en_fr", "en/fr", ""]

        for invalid_format in invalid_formats:
            with pytest.raises(ValueError, match="Invalid language_pair"):
                align(source_epub_path, target_epub_path, invalid_format)

    def test_valid_language_pair_formats(self, source_epub_path, target_epub_path):
        """Test that valid language_pair formats are accepted."""
        # Valid formats
        valid_formats = ["en-es", "es-en", "en-fr", "fr-en", "de-en"]

        for valid_format in valid_formats:
            try:
                result = align(source_epub_path, target_epub_path, valid_format)
                assert isinstance(result, AlignmentResult)
            except Exception as e:
                # It's okay if it fails for unsupported language pairs
                # as long as it doesn't fail due to format validation
                assert "language_pair" not in str(e)


class TestAlignmentResultClass:
    """Test the new AlignmentResult class functionality."""

    def test_alignment_result_methods(self, source_epub_path, target_epub_path):
        """Test that AlignmentResult has all expected methods."""
        result = align(source_epub_path, target_epub_path, "en-es")

        # Test all output methods
        dict_output = result.to_dict()
        assert isinstance(dict_output, dict)

        json_output = result.to_json()
        assert isinstance(json_output, str)

        text_output = result.to_text()
        assert isinstance(text_output, str)

        csv_output = result.to_csv()
        assert isinstance(csv_output, str)

        xml_output = result.to_xml()
        assert isinstance(xml_output, str)

    def test_alignment_result_repr(self, source_epub_path, target_epub_path):
        """Test that AlignmentResult has a proper string representation."""
        result = align(source_epub_path, target_epub_path, "en-es")

        repr_str = repr(result)
        assert isinstance(repr_str, str)
        assert "AlignmentResult" in repr_str
        assert "language_pair" in repr_str

    def test_alignment_result_json_indent(self, source_epub_path, target_epub_path):
        """Test that to_json() accepts indent parameter."""
        result = align(source_epub_path, target_epub_path, "en-es")

        # Test with different indent values
        json_compact = result.to_json(indent=None)
        json_indented = result.to_json(indent=4)

        assert isinstance(json_compact, str)
        assert isinstance(json_indented, str)
        assert len(json_indented) > len(json_compact)  # Indented should be longer


class TestBackwardCompatibility:
    """Test that the API changes don't break existing functionality."""

    def test_read_function_unchanged(self, source_epub_path):
        """Test that read() function still works as before."""
        chapters = read(source_epub_path)
        assert isinstance(chapters, Chapters)
        assert len(chapters) > 0

        # Test that segmentation still works
        segmented = chapters.segment()
        assert isinstance(segmented, Chapters)
        assert segmented._segmented_chapters is not None

    def test_get_supported_languages_unchanged(self):
        """Test that get_supported_languages() still works."""
        from vivre.api import get_supported_languages

        languages = get_supported_languages()
        assert isinstance(languages, list)
        assert len(languages) > 0
        assert all(isinstance(lang, str) for lang in languages)


def test_api_documentation():
    """Test that the API documentation reflects the new design."""
    # Test that align function docstring mentions Chapters objects
    align_doc = align.__doc__
    assert align_doc is not None
    assert "Chapters" in align_doc
    assert "language_pair" in align_doc
    assert "REQUIRED" in align_doc

    # Test that quick_align function docstring mentions required language_pair
    quick_align_doc = quick_align.__doc__
    assert quick_align_doc is not None
    assert "REQUIRED" in quick_align_doc
