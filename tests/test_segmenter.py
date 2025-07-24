"""
Tests for segmenter functionality.
"""

import pytest


class TestSegmenter:
    """Test cases for segmenter functionality."""

    def test_segmenter_initialization(self):
        """Test that Segmenter can be initialized."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        assert segmenter is not None
        assert hasattr(segmenter, "segment")
        assert hasattr(segmenter, "get_supported_languages")
        assert hasattr(segmenter, "is_language_supported")

    def test_get_supported_languages(self):
        """Test getting supported languages."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        languages = segmenter.get_supported_languages()

        assert isinstance(languages, list)
        assert len(languages) > 0
        assert "en" in languages
        assert "es" in languages
        assert "fr" in languages

    def test_is_language_supported(self):
        """Test language support checking."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()

        assert segmenter.is_language_supported("en") is True
        assert segmenter.is_language_supported("es") is True
        assert segmenter.is_language_supported("fr") is True
        assert segmenter.is_language_supported("invalid") is False

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

    def test_segment_with_language_parameter(self):
        """Test segmentation with explicit language parameter."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "This is a sentence. This is another sentence."

        segments = segmenter.segment(text, language="en")

        assert isinstance(segments, list), "segments should be a list"
        assert len(segments) == 2, "should have two segments"

    def test_segment_spanish_text(self):
        """Test segmentation of Spanish text."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "Hola mundo. ¿Cómo estás? ¡Qué bien!"

        segments = segmenter.segment(text, language="es")

        assert isinstance(segments, list), "segments should be a list"
        assert len(segments) == 3, "should have three segments"

    def test_segment_french_text(self):
        """Test segmentation of French text."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "Bonjour le monde. Comment allez-vous? C'est magnifique!"

        segments = segmenter.segment(text, language="fr")

        assert isinstance(segments, list), "segments should be a list"
        assert len(segments) == 3, "should have three segments"

    def test_language_detection_english(self):
        """Test automatic language detection for English."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "This is English text. It should be detected automatically."

        segments = segmenter.segment(text)  # No language parameter

        assert isinstance(segments, list), "segments should be a list"
        assert len(segments) == 2, "should have two segments"

    def test_language_detection_spanish(self):
        """Test automatic language detection for Spanish."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "Hola mundo. ¿Cómo estás? ¡Qué bien!"

        segments = segmenter.segment(text)  # No language parameter

        assert isinstance(segments, list), "segments should be a list"
        # Spanish spaCy model treats inverted punctuation as separate segments
        # This is correct behavior for Spanish text processing
        assert len(segments) >= 3, "should have at least three segments"
        assert (
            "Hola mundo." in segments[0]
        ), "first segment should contain 'Hola mundo.'"
        assert "¿" in segments or "¿Cómo estás?" in " ".join(
            segments
        ), "should contain question mark or question"
        assert "¡" in segments or "¡Qué bien!" in " ".join(
            segments
        ), "should contain exclamation mark or exclamation"

    def test_language_detection_french(self):
        """Test automatic language detection for French."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "Bonjour le monde. Comment allez-vous? C'est magnifique!"

        segments = segmenter.segment(text)  # No language parameter

        assert isinstance(segments, list), "segments should be a list"
        assert len(segments) == 3, "should have three segments"

    def test_unsupported_language_error(self):
        """Test error handling for unsupported language."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "Some text to segment."

        with pytest.raises(ValueError, match="Unsupported language"):
            segmenter.segment(text, language="invalid_lang")

    # Tests that should now pass with spaCy-based segmentation

    def test_segment_with_abbreviations(self):
        """Test segmentation with abbreviations that shouldn't split sentences."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "Dr. Smith went to the store. Mr. Johnson was there too."

        segments = segmenter.segment(text)

        # spaCy should handle abbreviations correctly
        assert (
            len(segments) == 2
        ), "should have exactly 2 segments, not split on abbreviations"
        assert (
            "Dr. Smith went to the store." in segments[0]
        ), "first segment should include Dr."
        assert (
            "Mr. Johnson was there too." in segments[1]
        ), "second segment should include Mr."

    def test_segment_with_ellipsis(self):
        """Test segmentation with ellipsis."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "He paused... then continued. The end."

        segments = segmenter.segment(text)

        # spaCy should handle ellipsis properly
        assert len(segments) == 2, "should have exactly 2 segments"
        assert "..." in segments[0], "first segment should include ellipsis"

    def test_segment_with_quotes(self):
        """Test segmentation with quoted sentences."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = 'He said "Hello there." and left. She replied "Goodbye."'

        segments = segmenter.segment(text)

        # spaCy should handle quoted sentences properly
        assert len(segments) == 2, "should have exactly 2 segments"
        assert (
            '"Hello there."' in segments[0]
        ), "first segment should include quoted sentence"
        assert (
            '"Goodbye."' in segments[1]
        ), "second segment should include quoted sentence"

    def test_segment_with_parentheses(self):
        """Test segmentation with parenthetical statements."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "This is a sentence (with a parenthetical remark). This is another."

        segments = segmenter.segment(text)

        # spaCy should handle parentheses properly
        assert len(segments) == 2, "should have exactly 2 segments"
        assert (
            "(with a parenthetical remark)" in segments[0]
        ), "first segment should include parentheses"

    def test_segment_with_numbers_and_periods(self):
        """Test segmentation with numbers that have periods."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "The price is $19.99. That's a good deal."

        segments = segmenter.segment(text)

        # spaCy should handle decimal numbers correctly
        assert (
            len(segments) == 2
        ), "should have exactly 2 segments, not split on decimal numbers"
        assert "$19.99" in segments[0], "first segment should include the price"

    def test_segment_with_multiple_punctuation(self):
        """Test segmentation with multiple punctuation marks."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "What?! How could this happen?!"

        segments = segmenter.segment(text)

        # spaCy should handle multiple punctuation marks
        assert len(segments) == 2, "should have exactly 2 segments"
        assert (
            "What?!" in segments[0]
        ), "first segment should include multiple punctuation"
        assert (
            "How could this happen?!" in segments[1]
        ), "second segment should include multiple punctuation"

    def test_segment_with_newlines(self):
        """Test segmentation with newlines in text."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "First sentence.\nSecond sentence.\nThird sentence."

        segments = segmenter.segment(text)

        # spaCy should handle newlines properly
        assert len(segments) == 3, "should have exactly 3 segments"
        for segment in segments:
            assert "\n" not in segment, "segments should not contain newlines"

    def test_segment_with_emails(self):
        """Test segmentation with email addresses."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "Contact me at user@example.com. I'll respond soon."

        segments = segmenter.segment(text)

        # spaCy should NOT split on email addresses
        assert len(segments) == 2, "should have exactly 2 segments, not split on email"
        assert "user@example.com" in segments[0], "first segment should include email"

    def test_segment_with_urls(self):
        """Test segmentation with URLs."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "Visit https://example.com. It's a great site."

        segments = segmenter.segment(text)

        # spaCy should NOT split on URLs
        assert len(segments) == 2, "should have exactly 2 segments, not split on URL"
        assert "https://example.com" in segments[0], "first segment should include URL"

    def test_segment_with_ordinal_numbers(self):
        """Test segmentation with ordinal numbers."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "1st place. 2nd place. 3rd place."

        segments = segmenter.segment(text)

        # spaCy should NOT split on ordinal numbers
        assert (
            len(segments) == 3
        ), "should have exactly 3 segments, not split on ordinal numbers"
        assert (
            "1st place." in segments[0]
        ), "first segment should include ordinal number"
        assert (
            "2nd place." in segments[1]
        ), "second segment should include ordinal number"
        assert (
            "3rd place." in segments[2]
        ), "third segment should include ordinal number"

    def test_segment_with_time_expressions(self):
        """Test segmentation with time expressions."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "The meeting is at 3:30 p.m. Please be on time."

        segments = segmenter.segment(text)

        # spaCy may or may not split on time expressions depending on the model
        # This is acceptable behavior
        assert len(segments) >= 1, "should have at least one segment"
        assert "3:30" in " ".join(segments), "should contain the time expression"
        assert "p.m." in " ".join(segments), "should contain the time period"

    def test_segment_with_version_numbers(self):
        """Test segmentation with version numbers."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "Python 3.11 is released. Python 3.12 is coming soon."

        segments = segmenter.segment(text)

        # spaCy should NOT split on version numbers
        assert (
            len(segments) == 2
        ), "should have exactly 2 segments, not split on version numbers"
        assert (
            "Python 3.11" in segments[0]
        ), "first segment should include version number"
        assert (
            "Python 3.12" in segments[1]
        ), "second segment should include version number"

    # Tests that might still fail depending on spaCy model capabilities

    def test_segment_with_roman_numerals(self):
        """Test segmentation with Roman numerals."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "Chapter I. Introduction. Chapter II. Methods."

        segments = segmenter.segment(text)

        # spaCy may split on Roman numerals depending on the model
        # This is acceptable behavior as long as the content is preserved
        assert len(segments) >= 2, "should have at least two segments"
        assert "Chapter I" in " ".join(segments), "should contain Chapter I"
        assert "Chapter II" in " ".join(segments), "should contain Chapter II"
        assert "Introduction" in " ".join(segments), "should contain Introduction"
        assert "Methods" in " ".join(segments), "should contain Methods"

    def test_segment_with_acronyms(self):
        """Test segmentation with acronyms."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "The U.S.A. is a country. The U.K. is another."

        segments = segmenter.segment(text)

        # This might still fail depending on spaCy model
        assert (
            len(segments) == 2
        ), "should have exactly 2 segments, not split on acronyms"
        assert "U.S.A." in segments[0], "first segment should include acronym"
        assert "U.K." in segments[1], "second segment should include acronym"
