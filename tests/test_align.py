"""
Tests for the text alignment functionality.
"""

from vivre.align import Aligner


class TestAligner:
    """Test cases for the Aligner class."""

    def test_align_perfect_match_english(self):
        """Test alignment of perfectly matched English texts."""
        aligner = Aligner()

        source_text = "Hello world. This is a test. How are you today?"
        target_text = "Hello world. This is a test. How are you today?"

        alignment = aligner.align(source_text, target_text)

        # Should have perfect 1-1 alignment
        assert len(alignment) == 3, "Should have 3 aligned segments"

        # Each segment should be perfectly matched
        for source_seg, target_seg in alignment:
            assert (
                source_seg == target_seg
            ), f"Segments should match: '{source_seg}' != '{target_seg}'"
            assert len(source_seg) > 0, "Source segment should not be empty"
            assert len(target_seg) > 0, "Target segment should not be empty"

    def test_align_perfect_match_spanish(self):
        """Test alignment of perfectly matched Spanish texts."""
        aligner = Aligner()

        source_text = "Hola mundo. Esto es una prueba. ¿Cómo estás hoy?"
        target_text = "Hola mundo. Esto es una prueba. ¿Cómo estás hoy?"

        alignment = aligner.align(source_text, target_text)

        # Should have perfect 1-1 alignment
        assert len(alignment) == 3, "Should have 3 aligned segments"

        # Each segment should be perfectly matched
        for source_seg, target_seg in alignment:
            assert (
                source_seg == target_seg
            ), f"Segments should match: '{source_seg}' != '{target_seg}'"
            assert len(source_seg) > 0, "Source segment should not be empty"
            assert len(target_seg) > 0, "Target segment should not be empty"

    def test_align_perfect_match_french(self):
        """Test alignment of perfectly matched French texts."""
        aligner = Aligner()

        source_text = (
            "Bonjour le monde. Ceci est un test. Comment allez-vous aujourd'hui?"
        )
        target_text = (
            "Bonjour le monde. Ceci est un test. Comment allez-vous aujourd'hui?"
        )

        alignment = aligner.align(source_text, target_text)

        # Should have perfect 1-1 alignment
        assert len(alignment) == 3, "Should have 3 aligned segments"

        # Each segment should be perfectly matched
        for source_seg, target_seg in alignment:
            assert (
                source_seg == target_seg
            ), f"Segments should match: '{source_seg}' != '{target_seg}'"
            assert len(source_seg) > 0, "Source segment should not be empty"
            assert len(target_seg) > 0, "Target segment should not be empty"

    def test_align_single_sentence(self):
        """Test alignment of single sentences."""
        aligner = Aligner()

        source_text = "This is a simple sentence."
        target_text = "This is a simple sentence."

        alignment = aligner.align(source_text, target_text)

        # Should have exactly one aligned segment
        assert len(alignment) == 1, "Should have 1 aligned segment"

        source_seg, target_seg = alignment[0]
        assert source_seg == target_seg, "Single segments should match"
        assert source_seg == source_text, "Source segment should match input"

    def test_align_empty_texts(self):
        """Test alignment of empty texts."""
        aligner = Aligner()

        alignment = aligner.align("", "")

        # Should return empty alignment
        assert len(alignment) == 0, "Empty texts should result in empty alignment"

    def test_align_whitespace_only(self):
        """Test alignment of whitespace-only texts."""
        aligner = Aligner()

        alignment = aligner.align("   ", "   ")

        # Should return empty alignment
        assert (
            len(alignment) == 0
        ), "Whitespace-only texts should result in empty alignment"

    def test_align_with_punctuation(self):
        """Test alignment with various punctuation marks."""
        aligner = Aligner()

        source_text = "Hello! How are you? I'm fine, thank you."
        target_text = "Hello! How are you? I'm fine, thank you."

        alignment = aligner.align(source_text, target_text)

        # Should have 3 aligned segments (split by punctuation)
        assert len(alignment) == 3, "Should have 3 aligned segments"

        # Each segment should be perfectly matched
        for source_seg, target_seg in alignment:
            assert (
                source_seg == target_seg
            ), f"Segments should match: '{source_seg}' != '{target_seg}'"

    def test_align_with_numbers(self):
        """Test alignment with numbers and special characters."""
        aligner = Aligner()

        source_text = "Chapter 1: Introduction. Page 42. Version 2.0."
        target_text = "Chapter 1: Introduction. Page 42. Version 2.0."

        alignment = aligner.align(source_text, target_text)

        # Should have 3 aligned segments
        assert len(alignment) == 3, "Should have 3 aligned segments"

        # Each segment should be perfectly matched
        for source_seg, target_seg in alignment:
            assert (
                source_seg == target_seg
            ), f"Segments should match: '{source_seg}' != '{target_seg}'"

    def test_align_multilingual_mix(self):
        """Test alignment with multilingual content."""
        aligner = Aligner()

        source_text = "Hello world. ¡Hola mundo! Bonjour le monde."
        target_text = "Hello world. ¡Hola mundo! Bonjour le monde."

        alignment = aligner.align(source_text, target_text)

        # Should have 3 aligned segments
        assert len(alignment) == 3, "Should have 3 aligned segments"

        # Each segment should be perfectly matched
        for source_seg, target_seg in alignment:
            assert (
                source_seg == target_seg
            ), f"Segments should match: '{source_seg}' != '{target_seg}'"

    def test_align_long_text(self):
        """Test alignment of longer texts."""
        aligner = Aligner()

        source_text = "This is the first paragraph. It contains multiple sentences. Each sentence should be aligned properly. The alignment should work for longer texts as well."
        target_text = "This is the first paragraph. It contains multiple sentences. Each sentence should be aligned properly. The alignment should work for longer texts as well."

        alignment = aligner.align(source_text, target_text)

        # Should have 4 aligned segments
        assert len(alignment) == 4, "Should have 4 aligned segments"

        # Each segment should be perfectly matched
        for source_seg, target_seg in alignment:
            assert (
                source_seg == target_seg
            ), f"Segments should match: '{source_seg}' != '{target_seg}'"
            assert len(source_seg) > 0, "Source segment should not be empty"
            assert len(target_seg) > 0, "Target segment should not be empty"
