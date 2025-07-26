"""
Tests for the segmenter fixes to ensure proper batch processing and model loading.
"""

import pytest

from vivre.segmenter import Segmenter


class TestSegmenterBatchProcessing:
    """Test that batch processing works correctly with the fixes."""

    def test_segment_batch_requires_language(self):
        """Test that segment_batch now requires explicit language specification."""
        segmenter = Segmenter()

        texts = ["Hello world.", "This is a test."]

        # This should work
        result = segmenter.segment_batch(texts, "en")
        assert len(result) == 2
        assert all(isinstance(sentences, list) for sentences in result)

        # This should fail (no language specified)
        with pytest.raises(TypeError):
            segmenter.segment_batch(texts)  # Missing language parameter

    def test_segment_batch_single_language(self):
        """Test that segment_batch works correctly for single-language batches."""
        segmenter = Segmenter()

        english_texts = [
            "Hello world. This is a test.",
            "Another sentence. And another one.",
            "Final sentence.",
        ]

        result = segmenter.segment_batch(english_texts, "en")

        assert len(result) == 3
        assert len(result[0]) == 2  # "Hello world." and "This is a test."
        assert len(result[1]) == 2  # "Another sentence." and "And another one."
        assert len(result[2]) == 1  # "Final sentence."

    def test_segment_mixed_batch_handles_different_languages(self):
        """Test that segment_mixed_batch correctly handles different languages."""
        segmenter = Segmenter()

        mixed_texts = [
            "Hello world. This is English.",
            "Hola mundo. Esto es español.",
            "Bonjour le monde. Ceci est français.",
            "Hello again. More English text.",
        ]

        result = segmenter.segment_mixed_batch(mixed_texts)

        assert len(result) == 4
        # All texts should be segmented (even if some languages might not be supported)
        assert all(isinstance(sentences, list) for sentences in result)

    def test_segment_mixed_batch_preserves_order(self):
        """Test that segment_mixed_batch preserves the original order of texts."""
        segmenter = Segmenter()

        texts = [
            "First text in English.",
            "Second text in English.",
            "Third text in English.",
        ]

        result = segmenter.segment_mixed_batch(texts)

        # Should preserve order
        assert len(result) == 3
        assert result[0] == segmenter.segment(texts[0], "en")
        assert result[1] == segmenter.segment(texts[1], "en")
        assert result[2] == segmenter.segment(texts[2], "en")

    def test_segment_batch_unsupported_language(self):
        """Test that segment_batch raises error for unsupported languages."""
        segmenter = Segmenter()

        texts = ["Some text."]

        with pytest.raises(ValueError, match="Unsupported language"):
            segmenter.segment_batch(texts, "xx")  # Unsupported language code

    def test_segment_batch_empty_list(self):
        """Test that segment_batch handles empty lists correctly."""
        segmenter = Segmenter()

        result = segmenter.segment_batch([], "en")
        assert result == []


class TestSegmenterModelLoading:
    """Test that model loading is simplified and works correctly."""

    def test_model_caching_by_model_name(self):
        """Test that models are cached by model name, not language code."""
        segmenter = Segmenter()

        # Load English model
        model1 = segmenter._load_model("en")
        assert "en_core_web_sm" in segmenter._models

        # Load Spanish model
        model2 = segmenter._load_model("es")
        assert "es_core_news_sm" in segmenter._models

        # Verify both models are cached
        assert len(segmenter._models) == 2
        assert "en_core_web_sm" in segmenter._models
        assert "es_core_news_sm" in segmenter._models

        # Verify models are different
        assert model1 != model2

    def test_model_reuse_from_cache(self):
        """Test that models are properly reused from cache."""
        segmenter = Segmenter()

        # Load model first time
        model1 = segmenter._load_model("en")

        # Load same model second time
        model2 = segmenter._load_model("en")

        # Should be the same object (from cache)
        assert model1 is model2

        # Cache should still have only one entry
        assert len(segmenter._models) == 1
        assert "en_core_web_sm" in segmenter._models


class TestSegmenterDocumentation:
    """Test that the segmenter documentation reflects the new behavior."""

    def test_segment_batch_docstring_warns_about_language(self):
        """Test that segment_batch docstring warns about language requirement."""
        segmenter = Segmenter()

        doc = segmenter.segment_batch.__doc__
        assert doc is not None
        assert "IMPORTANT" in doc
        assert "same language" in doc
        assert "Mixed-language batches are not supported" in doc

    def test_segment_mixed_batch_docstring_explains_usage(self):
        """Test that segment_mixed_batch docstring explains its purpose."""
        segmenter = Segmenter()

        doc = segmenter.segment_mixed_batch.__doc__
        assert doc is not None
        assert "different languages" in doc
        assert "automatically detects" in doc
        assert "recommended" in doc

    def test_class_docstring_mentions_batch_methods(self):
        """Test that class docstring mentions both batch methods."""
        doc = Segmenter.__doc__
        assert doc is not None
        assert "segment_batch" in doc
        assert "segment_mixed_batch" in doc
        assert "Batch Processing" in doc


def test_segmenter_backward_compatibility():
    """Test that individual text segmentation still works as before."""
    segmenter = Segmenter()

    # Test single text segmentation (should still work)
    text = "Hello world. This is a test."
    result = segmenter.segment(text)

    assert isinstance(result, list)
    assert len(result) == 2
    assert "Hello world." in result[0]
    assert "This is a test." in result[1]

    # Test with explicit language
    result2 = segmenter.segment(text, "en")
    assert result == result2
