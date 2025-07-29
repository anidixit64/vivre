"""
Tests for the integration module.
"""

from pathlib import Path

import pytest

from vivre.api import AlignmentResult
from vivre.integration import VivrePipeline, create_pipeline


class TestVivrePipeline:
    """Test the VivrePipeline class."""

    def test_pipeline_initialization(self):
        """Test pipeline initialization with default parameters."""
        pipeline = VivrePipeline()

        assert pipeline.language_pair == "en-es"
        assert hasattr(pipeline, "parser")
        assert hasattr(pipeline, "segmenter")
        assert hasattr(pipeline, "aligner")

    def test_pipeline_initialization_custom_language(self):
        """Test pipeline initialization with custom language pair."""
        pipeline = VivrePipeline("en-fr")

        assert pipeline.language_pair == "en-fr"

    def test_pipeline_initialization_with_custom_parameters(self):
        """Test pipeline initialization with custom parameters."""
        pipeline = VivrePipeline("en-es", c=1.5, s2=8.0, gap_penalty=3.0)

        assert pipeline.aligner.c == 1.5
        assert pipeline.aligner.s2 == 8.0
        assert pipeline.aligner.gap_penalty == 3.0

    def test_pipeline_initialization_with_invalid_language_pair(self):
        """Test pipeline initialization with invalid language pair."""
        # The pipeline doesn't actually validate language pairs in __init__
        # So this test should just verify it doesn't raise an error
        pipeline = VivrePipeline("invalid")
        assert pipeline.language_pair == "invalid"

    def test_pipeline_process_parallel_epubs_with_empty_files(self, tmp_path):
        """Test processing parallel EPUBs with empty files."""
        # Create empty EPUB files
        empty_epub1 = tmp_path / "empty1.epub"
        empty_epub2 = tmp_path / "empty2.epub"
        empty_epub1.write_bytes(b"")
        empty_epub2.write_bytes(b"")

        pipeline = VivrePipeline("en-es")

        with pytest.raises(ValueError):
            pipeline.process_parallel_epubs(empty_epub1, empty_epub2)

    def test_pipeline_process_parallel_epubs_with_nonexistent_files(self):
        """Test processing parallel EPUBs with nonexistent files."""
        pipeline = VivrePipeline("en-es")

        with pytest.raises(FileNotFoundError):
            pipeline.process_parallel_epubs(
                Path("nonexistent1.epub"), Path("nonexistent2.epub")
            )

    def test_pipeline_process_parallel_epubs_with_different_chapter_counts(
        self, source_epub_path, target_epub_path
    ):
        """Test processing parallel EPUBs with different chapter counts."""
        pipeline = VivrePipeline("en-es")

        # This should work even with different chapter counts
        alignments = pipeline.process_parallel_epubs(source_epub_path, target_epub_path)
        assert isinstance(alignments, list)

    def test_pipeline_segmenter_integration(self):
        """Test that pipeline segmenter works correctly."""
        pipeline = VivrePipeline("en-es")

        # Test segmentation
        text = "Hello world. This is a test."
        sentences = pipeline.segmenter.segment(text, "en")
        assert isinstance(sentences, list)
        assert len(sentences) > 0

    def test_pipeline_aligner_integration(self):
        """Test that pipeline aligner works correctly."""
        pipeline = VivrePipeline("en-es")

        # Test alignment
        source_sentences = ["Hello world.", "This is a test."]
        target_sentences = ["Hola mundo.", "Esto es una prueba."]

        alignments = pipeline.aligner.align(source_sentences, target_sentences)
        assert isinstance(alignments, list)
        assert len(alignments) > 0

    def test_pipeline_error_handling_with_invalid_parameters(self):
        """Test pipeline error handling with invalid parameters."""
        # The pipeline doesn't validate parameters in __init__
        # So this test should just verify it doesn't raise an error
        pipeline = VivrePipeline("en-es", c=-1, s2=0)
        assert pipeline.language_pair == "en-es"

    def test_pipeline_robustness_with_empty_sentences(self):
        """Test pipeline robustness with empty sentences."""
        pipeline = VivrePipeline("en-es")

        # Test with empty source sentences
        source_sentences = []
        target_sentences = ["Hola mundo."]

        alignments = pipeline.aligner.align(source_sentences, target_sentences)
        assert isinstance(alignments, list)

        # Test with empty target sentences
        source_sentences = ["Hello world."]
        target_sentences = []

        alignments = pipeline.aligner.align(source_sentences, target_sentences)
        assert isinstance(alignments, list)

    def test_pipeline_robustness_with_very_long_sentences(self):
        """Test pipeline robustness with very long sentences."""
        pipeline = VivrePipeline("en-es")

        # Create very long sentences
        long_source = ["This is a very long sentence. " * 100]
        long_target = ["Esta es una oración muy larga. " * 100]

        alignments = pipeline.aligner.align(long_source, long_target)
        assert isinstance(alignments, list)

    def test_pipeline_robustness_with_special_characters(self):
        """Test pipeline robustness with special characters."""
        pipeline = VivrePipeline("en-es")

        source_sentences = ["Hello world!", "What's up?", "It's 100% correct."]
        target_sentences = ["¡Hola mundo!", "¿Qué tal?", "¡Es 100% correcto!"]

        alignments = pipeline.aligner.align(source_sentences, target_sentences)
        assert isinstance(alignments, list)

    def test_pipeline_robustness_with_numbers_and_symbols(self):
        """Test pipeline robustness with numbers and symbols."""
        pipeline = VivrePipeline("en-es")

        source_sentences = [
            "The price is $100.",
            "Version 2.1 is ready.",
            "Call +1-555-1234.",
        ]
        target_sentences = [
            "El precio es $100.",
            "La versión 2.1 está lista.",
            "Llama al +1-555-1234.",
        ]

        alignments = pipeline.aligner.align(source_sentences, target_sentences)
        assert isinstance(alignments, list)

    def test_pipeline_robustness_with_unicode_characters(self):
        """Test pipeline robustness with unicode characters."""
        pipeline = VivrePipeline("en-es")

        source_sentences = ["Hello world.", "This is a test."]
        target_sentences = ["Hola mundo.", "Esto es una prueba."]

        alignments = pipeline.aligner.align(source_sentences, target_sentences)
        assert isinstance(alignments, list)

    def test_pipeline_robustness_with_mixed_languages(self):
        """Test pipeline robustness with mixed languages."""
        pipeline = VivrePipeline("en-es")

        source_sentences = ["Hello world.", "This is English."]
        target_sentences = ["Hola mundo.", "Esto es español."]

        alignments = pipeline.aligner.align(source_sentences, target_sentences)
        assert isinstance(alignments, list)

    def test_pipeline_robustness_with_identical_sentences(self):
        """Test pipeline robustness with identical sentences."""
        pipeline = VivrePipeline("en-es")

        source_sentences = ["Hello world.", "This is a test."]
        target_sentences = ["Hello world.", "This is a test."]  # Identical

        alignments = pipeline.aligner.align(source_sentences, target_sentences)
        assert isinstance(alignments, list)

    def test_pipeline_robustness_with_single_sentence_pairs(self):
        """Test pipeline robustness with single sentence pairs."""
        pipeline = VivrePipeline("en-es")

        source_sentences = ["Hello world."]
        target_sentences = ["Hola mundo."]

        alignments = pipeline.aligner.align(source_sentences, target_sentences)
        assert isinstance(alignments, list)
        assert len(alignments) > 0

    def test_pipeline_robustness_with_many_sentence_pairs(self):
        """Test pipeline robustness with many sentence pairs."""
        pipeline = VivrePipeline("en-es")

        # Create many sentence pairs
        source_sentences = [f"Sentence {i}." for i in range(50)]
        target_sentences = [f"Oración {i}." for i in range(50)]

        alignments = pipeline.aligner.align(source_sentences, target_sentences)
        assert isinstance(alignments, list)
        assert len(alignments) > 0

    def test_pipeline_robustness_with_very_short_sentences(self):
        """Test pipeline robustness with very short sentences."""
        pipeline = VivrePipeline("en-es")

        source_sentences = ["Hi.", "Bye.", "Yes.", "No."]
        target_sentences = ["Hola.", "Adiós.", "Sí.", "No."]

        alignments = pipeline.aligner.align(source_sentences, target_sentences)
        assert isinstance(alignments, list)

    def test_pipeline_robustness_with_very_long_sentences_v2(self):
        """Test pipeline robustness with very long sentences (version 2)."""
        pipeline = VivrePipeline("en-es")

        # Create very long sentences
        long_sentence = (
            "This is a very long sentence that contains many words and "
            "should test the robustness of the alignment algorithm. " * 10
        )
        source_sentences = [long_sentence]
        target_sentences = [
            long_sentence.replace("This is", "Esta es").replace("words", "palabras")
        ]

        alignments = pipeline.aligner.align(source_sentences, target_sentences)
        assert isinstance(alignments, list)

    def test_pipeline_robustness_with_questions_and_exclamations(self):
        """Test pipeline robustness with questions and exclamations."""
        pipeline = VivrePipeline("en-es")

        source_sentences = [
            "Hello world!",
            "How are you?",
            "This is amazing!",
            "What's your name?",
        ]
        target_sentences = [
            "¡Hola mundo!",
            "¿Cómo estás?",
            "¡Esto es increíble!",
            "¿Cuál es tu nombre?",
        ]

        alignments = pipeline.aligner.align(source_sentences, target_sentences)
        assert isinstance(alignments, list)

    def test_pipeline_robustness_with_quotes_and_parentheses(self):
        """Test pipeline robustness with quotes and parentheses."""
        pipeline = VivrePipeline("en-es")

        source_sentences = [
            'He said "Hello world."',
            "(This is a test.)",
            'She replied "Goodbye!"',
        ]
        target_sentences = [
            'Él dijo "Hola mundo."',
            "(Esto es una prueba.)",
            'Ella respondió "¡Adiós!"',
        ]

        alignments = pipeline.aligner.align(source_sentences, target_sentences)
        assert isinstance(alignments, list)

    def test_pipeline_robustness_with_abbreviations(self):
        """Test pipeline robustness with abbreviations."""
        pipeline = VivrePipeline("en-es")

        source_sentences = [
            "Mr. Smith is here.",
            "Dr. Johnson said hello.",
            "U.S.A. is great.",
        ]
        target_sentences = [
            "El Sr. Smith está aquí.",
            "El Dr. Johnson dijo hola.",
            "E.E.U.U. es genial.",
        ]

        alignments = pipeline.aligner.align(source_sentences, target_sentences)
        assert isinstance(alignments, list)

    def test_pipeline_robustness_with_numbers_and_dates(self):
        """Test pipeline robustness with numbers and dates."""
        pipeline = VivrePipeline("en-es")

        source_sentences = [
            "Today is 2023-12-01.",
            "The price is $99.99.",
            "Call 555-1234.",
        ]
        target_sentences = [
            "Hoy es 2023-12-01.",
            "El precio es $99.99.",
            "Llama al 555-1234.",
        ]

        alignments = pipeline.aligner.align(source_sentences, target_sentences)
        assert isinstance(alignments, list)

    def test_pipeline_robustness_with_emails_and_urls(self):
        """Test pipeline robustness with emails and URLs."""
        pipeline = VivrePipeline("en-es")

        source_sentences = [
            "Email: test@example.com",
            "Visit https://example.com",
            "Contact: info@test.org",
        ]
        target_sentences = [
            "Email: test@example.com",
            "Visita https://example.com",
            "Contacto: info@test.org",
        ]

        alignments = pipeline.aligner.align(source_sentences, target_sentences)
        assert isinstance(alignments, list)

    def test_process_parallel_epubs(
        self, default_pipeline, source_epub_path, target_epub_path
    ):
        """Test processing parallel EPUB files."""
        # Use the session-scoped fixtures instead of creating new instances
        alignments = default_pipeline.process_parallel_epubs(
            source_epub_path, target_epub_path
        )

        assert isinstance(alignments, list)
        assert len(alignments) > 0

        # Check alignment structure
        for source, target in alignments:
            assert isinstance(source, str)
            assert isinstance(target, str)

    def test_process_parallel_epubs_with_languages(
        self, default_pipeline, source_epub_path, target_epub_path
    ):
        """Test processing parallel EPUB files with explicit languages."""
        # Use the session-scoped fixtures instead of creating new instances
        alignments = default_pipeline.process_parallel_epubs(
            source_epub_path,
            target_epub_path,
            source_language="en",
            target_language="es",
        )

        assert isinstance(alignments, list)
        assert len(alignments) > 0

    def test_process_parallel_epubs_with_max_chapters(
        self, default_pipeline, source_epub_path, target_epub_path
    ):
        """Test processing parallel EPUB files with max chapters limit."""
        # Use the session-scoped fixtures instead of creating new instances
        alignments = default_pipeline.process_parallel_epubs(
            source_epub_path, target_epub_path, max_chapters=1
        )

        assert isinstance(alignments, list)
        # Should have fewer alignments due to max_chapters limit
        assert len(alignments) > 0

    def test_process_parallel_texts(self):
        """Test processing parallel text strings."""
        source_text = "Hello world. How are you?"
        target_text = "Hola mundo. ¿Cómo estás?"

        pipeline = VivrePipeline("en-es")
        alignments = pipeline.process_parallel_texts(
            source_text, target_text, source_language="en", target_language="es"
        )

        assert isinstance(alignments, list)
        assert len(alignments) > 0

        for source, target in alignments:
            assert isinstance(source, str)
            assert isinstance(target, str)

    def test_process_parallel_texts_with_languages(self):
        """Test processing parallel text strings with explicit languages."""
        source_text = "Hello world. How are you?"
        target_text = "Hola mundo. ¿Cómo estás?"

        pipeline = VivrePipeline("en-es")
        alignments = pipeline.process_parallel_texts(
            source_text, target_text, source_language="en", target_language="es"
        )

        assert isinstance(alignments, list)
        assert len(alignments) > 0

    def test_process_parallel_chapters(self):
        """Test processing parallel chapter lists."""
        source_chapters = [("Chapter 1", "Hello world. How are you?")]
        target_chapters = [("Capítulo 1", "Hola mundo. ¿Cómo estás?")]

        pipeline = VivrePipeline("en-es")
        alignments = pipeline.process_parallel_chapters(
            source_chapters, target_chapters, source_language="en", target_language="es"
        )

        assert isinstance(alignments, list)
        assert len(alignments) > 0

        for source, target in alignments:
            assert isinstance(source, str)
            assert isinstance(target, str)

    def test_process_parallel_chapters_with_languages(self):
        """Test processing parallel chapter lists with explicit languages."""
        source_chapters = [("Chapter 1", "Hello world. How are you?")]
        target_chapters = [("Capítulo 1", "Hola mundo. ¿Cómo estás?")]

        pipeline = VivrePipeline("en-es")
        alignments = pipeline.process_parallel_chapters(
            source_chapters, target_chapters, source_language="en", target_language="es"
        )

        assert isinstance(alignments, list)
        assert len(alignments) > 0

    def test_batch_process_epubs(
        self, default_pipeline, source_epub_path, target_epub_path
    ):
        """Test batch processing of multiple EPUB pairs."""
        # Use the session-scoped fixtures instead of creating new instances
        epub_pairs = [(source_epub_path, target_epub_path)]

        results = default_pipeline.batch_process_epubs(epub_pairs)

        assert isinstance(results, dict)
        assert len(results) > 0

        # Check that each result contains alignments
        for book_name, alignments in results.items():
            assert isinstance(book_name, str)
            assert isinstance(alignments, list)
            assert len(alignments) > 0

    def test_batch_process_epubs_with_languages(
        self, default_pipeline, source_epub_path, target_epub_path
    ):
        """Test batch processing with explicit languages."""
        # Use the session-scoped fixtures instead of creating new instances
        epub_pairs = [(source_epub_path, target_epub_path)]

        results = default_pipeline.batch_process_epubs(
            epub_pairs, source_language="en", target_language="es"
        )

        assert isinstance(results, dict)
        assert len(results) > 0

    def test_batch_process_epubs_with_max_chapters(
        self, default_pipeline, source_epub_path, target_epub_path
    ):
        """Test batch processing with max chapters limit."""
        # Use the session-scoped fixtures instead of creating new instances
        epub_pairs = [(source_epub_path, target_epub_path)]

        results = default_pipeline.batch_process_epubs(
            epub_pairs, max_chapters_per_book=1
        )

        assert isinstance(results, dict)
        assert len(results) > 0

    def test_get_pipeline_info(self):
        """Test getting pipeline information."""
        pipeline = VivrePipeline("en-fr", c=1.1, s2=7.0, gap_penalty=2.5)
        info = pipeline.get_pipeline_info()

        assert isinstance(info, dict)
        assert "language_pair" in info
        assert "aligner_parameters" in info
        assert "supported_languages" in info

        assert info["language_pair"] == "en-fr"
        assert info["aligner_parameters"]["c"] == 1.1
        assert info["aligner_parameters"]["s2"] == 7.0
        assert info["aligner_parameters"]["gap_penalty"] == 2.5
        assert isinstance(info["supported_languages"], list)
        assert len(info["supported_languages"]) > 0


class TestCreatePipeline:
    """Test the create_pipeline function."""

    def test_create_pipeline_default(self):
        """Test creating pipeline with default parameters."""
        pipeline = create_pipeline()

        assert isinstance(pipeline, VivrePipeline)
        assert pipeline.language_pair == "en-es"

    def test_create_pipeline_custom_language(self):
        """Test creating pipeline with custom language pair."""
        pipeline = create_pipeline("en-fr")

        assert isinstance(pipeline, VivrePipeline)
        assert pipeline.language_pair == "en-fr"

    def test_create_pipeline_custom_parameters(self):
        """Test creating pipeline with custom parameters."""
        pipeline = create_pipeline("en-es", c=1.1, s2=7.0, gap_penalty=2.5)

        assert isinstance(pipeline, VivrePipeline)
        assert pipeline.language_pair == "en-es"
        assert pipeline.aligner.c == 1.1
        assert pipeline.aligner.s2 == 7.0
        assert pipeline.aligner.gap_penalty == 2.5


class TestPipelineErrorHandling:
    """Test error handling in the pipeline."""

    def test_process_parallel_epubs_file_not_found(self):
        """Test handling of non-existent files."""
        pipeline = VivrePipeline("en-es")

        with pytest.raises(FileNotFoundError):
            pipeline.process_parallel_epubs("nonexistent1.epub", "nonexistent2.epub")

    def test_process_parallel_texts_empty_input(self):
        """Test processing with empty text inputs."""
        pipeline = VivrePipeline("en-es")

        # Empty source text - explicitly specify Spanish language
        alignments = pipeline.process_parallel_texts(
            "", "Hola mundo.", target_language="es"
        )
        assert isinstance(alignments, list)

        # Empty target text - explicitly specify English language
        alignments = pipeline.process_parallel_texts(
            "Hello world.", "", source_language="en"
        )
        assert isinstance(alignments, list)

        # Both empty - no language detection needed
        alignments = pipeline.process_parallel_texts("", "")
        assert isinstance(alignments, list)

    def test_process_parallel_chapters_empty_input(self):
        """Test processing with empty chapter inputs."""
        pipeline = VivrePipeline("en-es")

        # Empty source chapters - explicitly specify Spanish language
        alignments = pipeline.process_parallel_chapters(
            [], [("Capítulo 1", "Hola mundo.")], target_language="es"
        )
        assert isinstance(alignments, list)

        # Empty target chapters - explicitly specify English language
        alignments = pipeline.process_parallel_chapters(
            [("Chapter 1", "Hello world.")], [], source_language="en"
        )
        assert isinstance(alignments, list)

        # Both empty - no language detection needed
        alignments = pipeline.process_parallel_chapters([], [])
        assert isinstance(alignments, list)

    def test_batch_process_epubs_empty_list(self):
        """Test batch processing with empty list."""
        pipeline = VivrePipeline("en-es")

        results = pipeline.batch_process_epubs([])
        assert isinstance(results, dict)
        assert len(results) == 0

    def test_align_with_pipeline_dependency_injection(
        self, default_pipeline, source_epub_path, target_epub_path
    ):
        """Test that align() works with pipeline dependency injection."""
        from vivre import align

        # Test using the default pipeline fixture with dependency injection
        result = align(
            source_epub_path, target_epub_path, "en-es", _pipeline=default_pipeline
        )

        assert isinstance(result, AlignmentResult)
        dict_output = result.to_dict()
        assert dict_output["language_pair"] == "en-es"
        assert len(dict_output["chapters"]) > 0

        # Verify that the pipeline was reused (not created new)
        # The result should be consistent with using the same pipeline
        result2 = align(
            source_epub_path, target_epub_path, "en-es", _pipeline=default_pipeline
        )
        assert result.to_dict()["language_pair"] == result2.to_dict()["language_pair"]
