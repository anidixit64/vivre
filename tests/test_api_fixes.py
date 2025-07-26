"""
Tests for the API fixes to ensure proper integration and user-friendly design.
"""

from pathlib import Path

import pytest

from vivre.api import AlignmentResult, Chapters, align, quick_align, read


class TestChaptersObjectIntegration:
    """Test that Chapters objects work seamlessly with the align function."""

    def test_align_with_chapters_objects(self):
        """Test that align() accepts Chapters objects and works correctly."""
        # Find test files
        test_files = list(Path("tests/data").glob("*.epub"))
        if len(test_files) < 2:
            pytest.skip("Need at least 2 test EPUB files")

        file1, file2 = test_files[0], test_files[1]

        # Read both files into Chapters objects
        source_chapters = read(file1)
        target_chapters = read(file2)

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

    def test_align_with_mixed_types(self):
        """Test that align() works with mixed file paths and Chapters objects."""
        test_files = list(Path("tests/data").glob("*.epub"))
        if len(test_files) < 2:
            pytest.skip("Need at least 2 test EPUB files")

        file1, file2 = test_files[0], test_files[1]

        # Mix file path and Chapters object
        source_chapters = read(file1)
        result = align(source_chapters, file2, "en-es")

        assert isinstance(result, AlignmentResult)

        # Test the other way around
        target_chapters = read(file2)
        result2 = align(file1, target_chapters, "en-es")

        assert isinstance(result2, AlignmentResult)

    def test_chapters_workflow_seamless(self):
        """Test the complete seamless workflow with Chapters objects."""
        test_files = list(Path("tests/data").glob("*.epub"))
        if len(test_files) < 2:
            pytest.skip("Need at least 2 test EPUB files")

        file1, file2 = test_files[0], test_files[1]

        # Complete workflow: read -> segment -> align
        source_chapters = read(file1).segment("en")
        target_chapters = read(file2).segment("es")

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

    def test_align_requires_language_pair(self):
        """Test that align() requires explicit language_pair parameter."""
        test_files = list(Path("tests/data").glob("*.epub"))
        if len(test_files) < 2:
            pytest.skip("Need at least 2 test EPUB files")

        file1, file2 = test_files[0], test_files[1]

        # This should fail - missing language_pair
        with pytest.raises(TypeError):
            align(file1, file2)

        # This should work
        result = align(file1, file2, "en-es")
        assert isinstance(result, AlignmentResult)

    def test_quick_align_requires_language_pair(self):
        """Test that quick_align() requires explicit language_pair parameter."""
        test_files = list(Path("tests/data").glob("*.epub"))
        if len(test_files) < 2:
            pytest.skip("Need at least 2 test EPUB files")

        file1, file2 = test_files[0], test_files[1]

        # This should fail - missing language_pair
        with pytest.raises(TypeError):
            quick_align(file1, file2)

        # This should work
        pairs = quick_align(file1, file2, "en-es")
        assert isinstance(pairs, list)

    def test_invalid_language_pair_format(self):
        """Test that invalid language_pair formats are rejected."""
        test_files = list(Path("tests/data").glob("*.epub"))
        if len(test_files) < 2:
            pytest.skip("Need at least 2 test EPUB files")

        file1, file2 = test_files[0], test_files[1]

        # Invalid formats
        invalid_formats = ["en", "english", "en_fr", "en/fr", ""]

        for invalid_format in invalid_formats:
            with pytest.raises(ValueError, match="Invalid language_pair"):
                align(file1, file2, invalid_format)

    def test_valid_language_pair_formats(self):
        """Test that valid language_pair formats are accepted."""
        test_files = list(Path("tests/data").glob("*.epub"))
        if len(test_files) < 2:
            pytest.skip("Need at least 2 test EPUB files")

        file1, file2 = test_files[0], test_files[1]

        # Valid formats
        valid_formats = ["en-es", "es-en", "en-fr", "fr-en", "de-en"]

        for valid_format in valid_formats:
            try:
                result = align(file1, file2, valid_format)
                assert isinstance(result, AlignmentResult)
            except Exception as e:
                # It's okay if it fails for unsupported language pairs
                # as long as it doesn't fail due to format validation
                assert "language_pair" not in str(e)


class TestAlignmentResultClass:
    """Test the new AlignmentResult class functionality."""

    def test_alignment_result_methods(self):
        """Test that AlignmentResult has all expected methods."""
        test_files = list(Path("tests/data").glob("*.epub"))
        if len(test_files) < 2:
            pytest.skip("Need at least 2 test EPUB files")

        file1, file2 = test_files[0], test_files[1]

        result = align(file1, file2, "en-es")

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

    def test_alignment_result_repr(self):
        """Test that AlignmentResult has a proper string representation."""
        test_files = list(Path("tests/data").glob("*.epub"))
        if len(test_files) < 2:
            pytest.skip("Need at least 2 test EPUB files")

        file1, file2 = test_files[0], test_files[1]

        result = align(file1, file2, "en-es")

        repr_str = repr(result)
        assert isinstance(repr_str, str)
        assert "AlignmentResult" in repr_str
        assert "language_pair" in repr_str

    def test_alignment_result_json_indent(self):
        """Test that to_json() accepts indent parameter."""
        test_files = list(Path("tests/data").glob("*.epub"))
        if len(test_files) < 2:
            pytest.skip("Need at least 2 test EPUB files")

        file1, file2 = test_files[0], test_files[1]

        result = align(file1, file2, "en-es")

        # Test with different indent values
        json_compact = result.to_json(indent=None)
        json_indented = result.to_json(indent=4)

        assert isinstance(json_compact, str)
        assert isinstance(json_indented, str)
        assert len(json_indented) > len(json_compact)  # Indented should be longer


class TestBackwardCompatibility:
    """Test that the API changes don't break existing functionality."""

    def test_read_function_unchanged(self):
        """Test that read() function still works as before."""
        test_files = list(Path("tests/data").glob("*.epub"))
        if not test_files:
            pytest.skip("Need at least 1 test EPUB file")

        file1 = test_files[0]

        chapters = read(file1)
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
