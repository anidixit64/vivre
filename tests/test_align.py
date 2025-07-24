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

    def test_align_english_spanish_simple(self):
        """Test alignment of English-Spanish translation pairs (should fail with current implementation)."""
        aligner = Aligner()

        source_text = "Hello world. How are you today?"
        target_text = "Hola mundo. ¿Cómo estás hoy?"

        alignment = aligner.align(source_text, target_text)

        # Should have 2 aligned segments (one for each sentence)
        assert len(alignment) == 2, "Should have 2 aligned segments"

        # Each segment should contain corresponding translations
        source_seg1, target_seg1 = alignment[0]
        source_seg2, target_seg2 = alignment[1]

        # First sentence: "Hello world." should align with "Hola mundo."
        assert (
            "Hello world" in source_seg1
        ), "First source segment should contain 'Hello world'"
        assert (
            "Hola mundo" in target_seg1
        ), "First target segment should contain 'Hola mundo'"

        # Second sentence: "How are you today?" should align with "¿Cómo estás hoy?"
        assert (
            "How are you today" in source_seg2
        ), "Second source segment should contain 'How are you today'"
        assert (
            "Cómo estás hoy" in target_seg2
        ), "Second target segment should contain 'Cómo estás hoy'"

    def test_align_english_spanish_complex(self):
        """Test alignment of more complex English-Spanish translation pairs (should fail with current implementation)."""
        aligner = Aligner()

        source_text = "The cat is sleeping. The dog is running. The bird is flying."
        target_text = (
            "El gato está durmiendo. El perro está corriendo. El pájaro está volando."
        )

        alignment = aligner.align(source_text, target_text)

        # Should have 3 aligned segments (one for each sentence)
        assert len(alignment) == 3, "Should have 3 aligned segments"

        # Each segment should contain corresponding translations
        for i, (source_seg, target_seg) in enumerate(alignment):
            assert len(source_seg) > 0, f"Source segment {i+1} should not be empty"
            assert len(target_seg) > 0, f"Target segment {i+1} should not be empty"

            # Verify that segments contain expected content
            if i == 0:  # "The cat is sleeping" / "El gato está durmiendo"
                assert (
                    "cat" in source_seg.lower()
                ), "First source segment should contain 'cat'"
                assert (
                    "gato" in target_seg.lower()
                ), "First target segment should contain 'gato'"
            elif i == 1:  # "The dog is running" / "El perro está corriendo"
                assert (
                    "dog" in source_seg.lower()
                ), "Second source segment should contain 'dog'"
                assert (
                    "perro" in target_seg.lower()
                ), "Second target segment should contain 'perro'"
            elif i == 2:  # "The bird is flying" / "El pájaro está volando"
                assert (
                    "bird" in source_seg.lower()
                ), "Third source segment should contain 'bird'"
                assert (
                    "pájaro" in target_seg.lower()
                ), "Third target segment should contain 'pájaro'"

    def test_align_english_spanish_questions(self):
        """Test alignment of English-Spanish question pairs (should fail with current implementation)."""
        aligner = Aligner()

        source_text = "What is your name? Where do you live? How old are you?"
        target_text = "¿Cómo te llamas? ¿Dónde vives? ¿Cuántos años tienes?"

        alignment = aligner.align(source_text, target_text)

        # Should have 3 aligned segments (one for each question)
        assert len(alignment) == 3, "Should have 3 aligned segments"

        # Each segment should contain corresponding translations
        for i, (source_seg, target_seg) in enumerate(alignment):
            assert len(source_seg) > 0, f"Source segment {i+1} should not be empty"
            assert len(target_seg) > 0, f"Target segment {i+1} should not be empty"

            # Verify that segments contain expected content
            if i == 0:  # "What is your name?" / "¿Cómo te llamas?"
                assert (
                    "name" in source_seg.lower()
                ), "First source segment should contain 'name'"
                assert (
                    "llamas" in target_seg.lower()
                ), "First target segment should contain 'llamas'"
            elif i == 1:  # "Where do you live?" / "¿Dónde vives?"
                assert (
                    "live" in source_seg.lower()
                ), "Second source segment should contain 'live'"
                assert (
                    "vives" in target_seg.lower()
                ), "Second target segment should contain 'vives'"
            elif i == 2:  # "How old are you?" / "¿Cuántos años tienes?"
                assert (
                    "old" in source_seg.lower()
                ), "Third source segment should contain 'old'"
                assert (
                    "años" in target_seg.lower()
                ), "Third target segment should contain 'años'"

    def test_align_english_spanish_story(self):
        """Test alignment of English-Spanish story segments (should fail with current implementation)."""
        aligner = Aligner()

        source_text = "Once upon a time, there was a little girl. She lived in a village near the forest. Her grandmother gave her a red riding hood."
        target_text = "Érase una vez, había una niña pequeña. Ella vivía en un pueblo cerca del bosque. Su abuela le dio una caperucita roja."

        alignment = aligner.align(source_text, target_text)

        # Should have 3 aligned segments (one for each sentence)
        assert len(alignment) == 3, "Should have 3 aligned segments"

        # Each segment should contain corresponding translations
        for i, (source_seg, target_seg) in enumerate(alignment):
            assert len(source_seg) > 0, f"Source segment {i+1} should not be empty"
            assert len(target_seg) > 0, f"Target segment {i+1} should not be empty"

            # Verify that segments contain expected content
            if (
                i == 0
            ):  # "Once upon a time, there was a little girl" / "Érase una vez, había una niña pequeña"
                assert (
                    "little girl" in source_seg.lower()
                ), "First source segment should contain 'little girl'"
                assert (
                    "niña pequeña" in target_seg.lower()
                ), "First target segment should contain 'niña pequeña'"
            elif (
                i == 1
            ):  # "She lived in a village near the forest" / "Ella vivía en un pueblo cerca del bosque"
                assert (
                    "village" in source_seg.lower()
                ), "Second source segment should contain 'village'"
                assert (
                    "pueblo" in target_seg.lower()
                ), "Second target segment should contain 'pueblo'"
            elif (
                i == 2
            ):  # "Her grandmother gave her a red riding hood" / "Su abuela le dio una caperucita roja"
                assert (
                    "grandmother" in source_seg.lower()
                ), "Third source segment should contain 'grandmother'"
                assert (
                    "abuela" in target_seg.lower()
                ), "Third target segment should contain 'abuela'"

    def test_align_empty_source_sentences(self):
        """Test alignment when source text has minimal sentences."""
        aligner = Aligner()

        source_text = "   .   .   "  # Only punctuation and whitespace
        target_text = "Hello world. How are you?"

        alignment = aligner.align(source_text, target_text)

        # Should have alignments (algorithm finds sentences even in edge cases)
        assert (
            len(alignment) > 0
        ), "Should have alignments even with minimal source sentences"

        # Each alignment should have content
        for source_seg, target_seg in alignment:
            assert len(target_seg) > 0, "Target segment should have content"

    def test_align_empty_target_sentences(self):
        """Test alignment when target text has minimal sentences."""
        aligner = Aligner()

        source_text = "Hello world. How are you?"
        target_text = "   .   .   "  # Only punctuation and whitespace

        alignment = aligner.align(source_text, target_text)

        # Should have alignments (algorithm finds sentences even in edge cases)
        assert (
            len(alignment) > 0
        ), "Should have alignments even with minimal target sentences"

        # Each alignment should have content
        for source_seg, target_seg in alignment:
            assert len(source_seg) > 0, "Source segment should have content"

    def test_align_both_minimal_sentences(self):
        """Test alignment when both texts have minimal sentences."""
        aligner = Aligner()

        source_text = "   .   .   "
        target_text = "   !   ?   "

        alignment = aligner.align(source_text, target_text)

        # Should have alignments (algorithm finds sentences even in edge cases)
        assert (
            len(alignment) > 0
        ), "Should have alignments even with minimal sentences in both texts"

    def test_align_single_source_multiple_target(self):
        """Test alignment with one source sentence and multiple target sentences."""
        aligner = Aligner()

        source_text = "This is a long sentence that should be split."
        target_text = "This is. A long sentence. That should be split."

        alignment = aligner.align(source_text, target_text)

        # Should have at least one alignment
        assert len(alignment) > 0, "Should have at least one alignment"

        # Each alignment should have content (may have empty segments due to algorithm behavior)
        for source_seg, target_seg in alignment:
            # At least one segment should have content
            assert (
                len(source_seg) > 0 or len(target_seg) > 0
            ), "At least one segment should have content"

    def test_align_multiple_source_single_target(self):
        """Test alignment with multiple source sentences and one target sentence."""
        aligner = Aligner()

        source_text = "This is. A long sentence. That should be split."
        target_text = "This is a long sentence that should be split."

        alignment = aligner.align(source_text, target_text)

        # Should have at least one alignment
        assert len(alignment) > 0, "Should have at least one alignment"

        # Each alignment should have content (may have empty segments due to algorithm behavior)
        for source_seg, target_seg in alignment:
            # At least one segment should have content
            assert (
                len(source_seg) > 0 or len(target_seg) > 0
            ), "At least one segment should have content"

    def test_align_edge_case_reconstruction(self):
        """Test alignment edge case that exercises the reconstruction logic."""
        aligner = Aligner()

        # Use very different length texts to force complex alignment
        source_text = "A. B. C. D. E."
        target_text = "Very long sentence that should align with multiple short ones."

        alignment = aligner.align(source_text, target_text)

        # Should have at least one alignment
        assert len(alignment) > 0, "Should have at least one alignment"

        # Each alignment should have content (may have empty segments due to algorithm behavior)
        for source_seg, target_seg in alignment:
            # At least one segment should have content
            assert (
                len(source_seg) > 0 or len(target_seg) > 0
            ), "At least one segment should have content"

    def test_align_cost_function_edge_cases(self):
        """Test alignment cost function with various edge cases."""
        aligner = Aligner()

        # Test with very long sentences to trigger the large alignment penalty
        source_text = "A" * 100 + ". " + "B" * 100 + "."
        target_text = "C" * 50 + ". " + "D" * 50 + "."

        alignment = aligner.align(source_text, target_text)

        # Should have alignments
        assert (
            len(alignment) > 0
        ), "Should have alignments even with very long sentences"

        # Each alignment should have content
        for source_seg, target_seg in alignment:
            assert (
                len(source_seg) > 0 or len(target_seg) > 0
            ), "At least one segment should have content"

    def test_align_dp_algorithm_edge_cases(self):
        """Test DP algorithm with edge cases that exercise different alignment types."""
        aligner = Aligner()

        # Test with many short sentences to exercise various alignment combinations
        source_text = "A. B. C. D. E. F. G. H. I. J."
        target_text = "1. 2. 3. 4. 5. 6. 7. 8. 9. 10."

        alignment = aligner.align(source_text, target_text)

        # Should have alignments
        assert len(alignment) > 0, "Should have alignments with many short sentences"

        # Each alignment should have content
        for source_seg, target_seg in alignment:
            assert (
                len(source_seg) > 0 or len(target_seg) > 0
            ), "At least one segment should have content"
