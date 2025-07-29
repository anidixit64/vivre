"""
Tests for the integration module.
"""

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

    def test_pipeline_initialization_custom_parameters(self):
        """Test pipeline initialization with custom alignment parameters."""
        pipeline = VivrePipeline("en-es", c=1.1, s2=7.0, gap_penalty=2.5)

        assert pipeline.language_pair == "en-es"
        assert pipeline.aligner.c == 1.1
        assert pipeline.aligner.s2 == 7.0
        assert pipeline.aligner.gap_penalty == 2.5

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
