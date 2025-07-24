"""
Tests for segmenter functionality.
"""


class TestSegmenter:
    """Test cases for segmenter functionality."""

    def test_segmenter_initialization(self):
        """Test that Segmenter can be initialized."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        assert segmenter is not None

    def test_segment_text_basic(self):
        """Test basic text segmentation."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "This is a sentence. This is another sentence. And a third one."

        segments = segmenter.segment(text)

        # Should return a list of strings
        assert isinstance(segments, list), "segments should be a list"
        assert len(segments) > 0, "should have at least one segment"

        for segment in segments:
            assert isinstance(segment, str), "each segment should be a string"
            assert len(segment) > 0, "each segment should not be empty"

    def test_segment_empty_text(self):
        """Test segmentation of empty text."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = ""

        segments = segmenter.segment(text)

        assert isinstance(segments, list), "segments should be a list"
        assert len(segments) == 0, "empty text should return empty list"

    def test_segment_single_sentence(self):
        """Test segmentation of a single sentence."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "This is a single sentence."

        segments = segmenter.segment(text)

        assert isinstance(segments, list), "segments should be a list"
        assert len(segments) == 1, "single sentence should return one segment"
        assert segments[0] == text, "segment should match input text"

    def test_segment_multiple_sentences(self):
        """Test segmentation of multiple sentences."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "First sentence. Second sentence. Third sentence."

        segments = segmenter.segment(text)

        assert isinstance(segments, list), "segments should be a list"
        assert len(segments) == 3, "should have three segments"

        expected_segments = ["First sentence.", "Second sentence.", "Third sentence."]

        for i, segment in enumerate(segments):
            assert (
                segment.strip() == expected_segments[i]
            ), f"segment {i} should match expected"

    def test_segment_with_whitespace(self):
        """Test segmentation with extra whitespace."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "  First sentence.  Second sentence.  Third sentence.  "

        segments = segmenter.segment(text)

        assert isinstance(segments, list), "segments should be a list"
        assert len(segments) == 3, "should have three segments"

        for segment in segments:
            assert isinstance(segment, str), "each segment should be a string"
            assert (
                len(segment.strip()) > 0
            ), "each segment should not be empty after stripping"
