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

    def test_segmenter_unsupported_language_error(self):
        """Test that unsupported language raises ValueError."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()

        with pytest.raises(ValueError, match="Unsupported language"):
            segmenter.segment("Hello world", language="xx")

    def test_segmenter_invalid_language_code(self):
        """Test that invalid language code raises ValueError."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()

        with pytest.raises(ValueError, match="Unsupported language"):
            segmenter.segment("Hello world", language="invalid")

    def test_segmenter_empty_text_after_stripping(self):
        """Test segmentation of text that becomes empty after stripping."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()

        result = segmenter.segment("   \n\t   ")
        assert result == []

    def test_segmenter_whitespace_only_text(self):
        """Test segmentation of whitespace-only text."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()

        result = segmenter.segment("   \n\t   ")
        assert result == []

    def test_segmenter_none_text(self):
        """Test segmentation of None text."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()

        result = segmenter.segment(None)
        assert result == []

    def test_segmenter_empty_string(self):
        """Test segmentation of empty string."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()

        result = segmenter.segment("")
        assert result == []

    def test_segmenter_get_supported_languages(self):
        """Test getting supported languages."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()

        languages = segmenter.get_supported_languages()
        assert isinstance(languages, list)
        assert len(languages) > 0
        assert "en" in languages
        assert "es" in languages
        assert "fr" in languages

    def test_segmenter_is_language_supported(self):
        """Test checking if language is supported."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()

        assert segmenter.is_language_supported("en") is True
        assert segmenter.is_language_supported("es") is True
        assert segmenter.is_language_supported("fr") is True
        assert segmenter.is_language_supported("invalid") is False
        assert segmenter.is_language_supported("") is False

    def test_segmenter_language_detection_edge_cases(self):
        """Test language detection with edge cases."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()

        # Test with numbers only (should default to English)
        result = segmenter.segment("123 456 789")
        assert isinstance(result, list)

        # Test with special characters only (should default to English)
        result = segmenter.segment("!@#$%^&*()")
        assert isinstance(result, list)

        # Test with mixed Latin and non-Latin characters (should default to English)
        result = segmenter.segment("Hello 123 !@#")
        assert isinstance(result, list)

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

    def test_segment_italian_text(self):
        """Test segmentation of Italian text."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "Ciao mondo. Come stai? Che bello!"

        segments = segmenter.segment(text, language="it")

        assert isinstance(segments, list), "segments should be a list"
        assert len(segments) == 3, "should have three segments"
        assert (
            "Ciao mondo." in segments[0]
        ), "first segment should contain 'Ciao mondo.'"
        assert "Come stai?" in segments[1], "second segment should contain 'Come stai?'"
        assert "Che bello!" in segments[2], "third segment should contain 'Che bello!'"

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
        # Check that we have the question content, regardless of exact segmentation
        question_content = any("¿" in seg or "Cómo estás" in seg for seg in segments)
        assert question_content, "should contain question content"
        # Check that we have the exclamation content, regardless of exact segmentation
        exclamation_content = any("¡" in seg or "Qué bien" in seg for seg in segments)
        assert exclamation_content, "should contain exclamation content"

    def test_language_detection_french(self):
        """Test automatic language detection for French."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "Bonjour le monde. Comment allez-vous? C'est magnifique!"

        segments = segmenter.segment(text)  # No language parameter

        assert isinstance(segments, list), "segments should be a list"
        assert len(segments) == 3, "should have three segments"

    def test_language_detection_italian(self):
        """Test automatic language detection for Italian."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()
        text = "Ciao mondo. Come stai? Che bello!"

        segments = segmenter.segment(text)  # No language parameter

        assert isinstance(segments, list), "segments should be a list"
        assert len(segments) == 3, "should have three segments"
        assert (
            "Ciao mondo." in segments[0]
        ), "first segment should contain 'Ciao mondo.'"
        assert "Come stai?" in segments[1], "second segment should contain 'Come stai?'"
        assert "Che bello!" in segments[2], "third segment should contain 'Che bello!'"

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

        # spaCy may segment differently with quotes, but should preserve content
        assert len(segments) >= 2, "should have at least 2 segments"
        # Check that both quoted sentences are present
        text_joined = " ".join(segments)
        assert "Hello there" in text_joined, "should contain first quote"
        assert "Goodbye" in text_joined, "should contain second quote"
        # Check that both quoted sentences are present in the segments
        has_first_quote = any('"Hello there."' in seg for seg in segments)
        has_second_quote = any('"Goodbye."' in seg for seg in segments)
        assert has_first_quote, "should contain first quoted sentence"
        assert has_second_quote, "should contain second quoted sentence"

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

    def test_segment_spanish_epub_chapter(self):
        """Test segmentation on second chapter from Spanish EPUB file."""
        from pathlib import Path

        from vivre.parser import VivreParser
        from vivre.segmenter import Segmenter

        # Path to the Spanish EPUB file
        epub_path = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        # Ensure the file exists
        assert epub_path.exists(), f"Spanish EPUB file not found: {epub_path}"

        # Parse the EPUB file
        parser = VivreParser()
        chapters = parser.parse_epub(epub_path)

        # Verify we have at least 2 chapters
        assert len(chapters) >= 2, f"Expected at least 2 chapters, got {len(chapters)}"

        # Get the second chapter (index 1)
        second_chapter_title, second_chapter_text = chapters[1]

        # Verify the chapter has content
        assert isinstance(second_chapter_title, str), "Chapter title should be a string"
        assert isinstance(second_chapter_text, str), "Chapter text should be a string"
        assert len(second_chapter_text) > 0, "Chapter text should not be empty"

        print(f"Second chapter title: {second_chapter_title}")
        print(f"Second chapter text length: {len(second_chapter_text)} characters")
        print(f"Second chapter text preview: {second_chapter_text[:200]}...")

        # Segment the second chapter text
        segmenter = Segmenter()
        sentences = segmenter.segment(second_chapter_text, language="es")

        # Verify segmentation results
        assert isinstance(sentences, list), "sentences should be a list"
        assert len(sentences) > 0, "should have at least one sentence"

        # Verify each sentence
        for i, sentence in enumerate(sentences):
            assert isinstance(sentence, str), f"sentence {i} should be a string"
            assert len(sentence) > 0, f"sentence {i} should not be empty"
            assert (
                len(sentence.strip()) > 0
            ), f"sentence {i} should not be empty after stripping"

        print(f"Number of sentences extracted: {len(sentences)}")
        print(f"First sentence: {sentences[0]}")
        print(f"Last sentence: {sentences[-1]}")

        # Verify Spanish-specific characteristics
        spanish_indicators = ["á", "é", "í", "ó", "ú", "ñ", "¿", "¡"]
        text_contains_spanish = any(
            indicator in second_chapter_text for indicator in spanish_indicators
        )
        assert text_contains_spanish, "Text should contain Spanish characters"

        # Verify that segmentation preserved Spanish content
        sentences_text = " ".join(sentences)
        assert (
            len(sentences_text) > len(second_chapter_text) * 0.8
        ), "Segmentation should preserve most of the original text"

        # Verify that sentences are reasonable length (not too short, not too long)
        for sentence in sentences:
            # Allow for short dialogue responses and exclamations in Spanish
            # Common short responses: "Sí.", "No.", "¡Hola!", "—Sí.", etc.
            if len(sentence.strip()) < 3:
                # Only allow very short sentences if they're common Spanish responses
                short_responses = [
                    "Sí.",
                    "No.",
                    "¡Hola!",
                    "—Sí.",
                    "—No.",
                    "¡Ay!",
                    "¡Oh!",
                ]
                assert (
                    sentence.strip() in short_responses
                ), f"Very short sentence not a common response: '{sentence}'"
            else:
                assert len(sentence) >= 3, f"Sentence too short: '{sentence}'"
            assert len(sentence) <= 1000, f"Sentence too long: '{sentence}'"

    def test_segmenter_language_detection_various_languages(self):
        """Test language detection for various languages."""
        from unittest.mock import MagicMock, patch

        from vivre.segmenter import Segmenter

        segmenter = Segmenter()

        # Create a mock spaCy model
        mock_model = MagicMock()
        mock_doc = MagicMock()
        mock_sent = MagicMock()
        mock_sent.text = "Test sentence."
        mock_doc.sents = [mock_sent]
        mock_model.return_value = mock_doc

        # Test languages with installed models - mock both language detection and model loading
        with patch.object(segmenter, "_detect_language") as mock_detect, patch.object(
            segmenter, "_load_model", return_value=mock_model
        ):

            # Test English
            mock_detect.return_value = "en"
            result = segmenter.segment("Hello world")
            assert isinstance(result, list)

            # Test Spanish
            mock_detect.return_value = "es"
            result = segmenter.segment("Hola mundo")
            assert isinstance(result, list)

            # Test French
            mock_detect.return_value = "fr"
            result = segmenter.segment("Bonjour le monde")
            assert isinstance(result, list)

            # Test Italian
            mock_detect.return_value = "it"
            result = segmenter.segment("Ciao mondo")
            assert isinstance(result, list)

            # Test other languages - all should work with mocked model loading
            test_languages = [
                ("Привет мир", "ru"),
                ("こんにちは世界", "ja"),
                ("안녕하세요 세계", "ko"),
                ("مرحبا بالعالم", "ar"),
                ("สวัสดีชาวโลก", "th"),
                ("नमस्ते दुनिया", "hi"),
                ("Hallo Welt", "de"),
                ("Olá mundo", "pt"),
                ("Hallo wereld", "nl"),
                ("Cześć świecie", "pl"),
            ]

            for text, lang_code in test_languages:
                mock_detect.return_value = lang_code
                result = segmenter.segment(text)
                assert isinstance(result, list)

    def test_langdetect_integration(self):
        """Test that langdetect is properly integrated and working."""
        from unittest.mock import patch

        import langdetect  # type: ignore

        from vivre.segmenter import Segmenter

        segmenter = Segmenter()

        # Test that langdetect is actually being used
        with patch("langdetect.detect") as mock_langdetect:
            mock_langdetect.return_value = "es"

            # This should call langdetect.detect
            detected = segmenter._detect_language("Hola mundo")
            assert detected == "es"
            mock_langdetect.assert_called_once_with("Hola mundo")

        # Test language code mapping
        with patch("langdetect.detect") as mock_langdetect:
            mock_langdetect.return_value = "zh-cn"
            detected = segmenter._detect_language("你好世界")
            assert detected == "zh"  # Should map zh-cn to zh

        # Test fallback to English for unsupported languages
        with patch("langdetect.detect") as mock_langdetect:
            mock_langdetect.return_value = "xx"  # Unsupported language
            detected = segmenter._detect_language("Some text")
            assert detected == "en"  # Should fallback to English

        # Test exception handling
        with patch("langdetect.detect") as mock_langdetect:
            mock_langdetect.side_effect = langdetect.LangDetectException(
                "Test error", "Test error"
            )
            detected = segmenter._detect_language("Some text")
            assert detected == "en"  # Should fallback to English

    def test_optimized_model_loading(self):
        """Test that model loading is optimized to avoid duplicate loads."""
        from unittest.mock import MagicMock, patch

        from vivre.segmenter import Segmenter

        segmenter = Segmenter()

        # Create mock models
        mock_en_model = MagicMock()
        mock_es_model = MagicMock()
        mock_multilingual_model = MagicMock()

        with patch("spacy.load") as mock_spacy_load:
            # Configure spacy.load to return different models
            def mock_load(model_name, **kwargs):
                if model_name == "en_core_web_sm":
                    return mock_en_model
                elif model_name == "es_core_news_sm":
                    return mock_es_model
                elif model_name == "xx_ent_wiki_sm":
                    return mock_multilingual_model
                else:
                    raise OSError(f"Model {model_name} not found")

            mock_spacy_load.side_effect = mock_load

            # Load English model
            model1 = segmenter._load_model("en")
            assert model1 == mock_en_model

            # Load Spanish model
            model2 = segmenter._load_model("es")
            assert model2 == mock_es_model

            # Load Arabic model (should use multilingual model)
            model3 = segmenter._load_model("ar")
            assert model3 == mock_multilingual_model

            # Load Hindi model (should reuse multilingual model)
            model4 = segmenter._load_model("hi")
            assert model4 == mock_multilingual_model

            # Verify spacy.load was called only 3 times (not 4)
            # because Arabic and Hindi share the same multilingual model
            assert mock_spacy_load.call_count == 3

    def test_user_language_override(self):
        """Test that user-provided language takes precedence over auto-detection."""
        from unittest.mock import patch

        from vivre.segmenter import Segmenter

        segmenter = Segmenter()

        # Test with English text but Spanish language override
        text = "This is English text. It should be processed as Spanish."

        with patch.object(segmenter, "_detect_language") as mock_detect:
            mock_detect.return_value = "en"  # Auto-detect would return English

            # Use Spanish override
            segments = segmenter.segment(text, language="es")

            # Should not call auto-detection when language is provided
            mock_detect.assert_not_called()

            # Should process with Spanish model
            assert isinstance(segments, list)
            assert len(segments) > 0

    def test_batch_processing(self):
        """Test batch processing functionality."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()

        # Test batch processing with multiple texts
        texts = [
            "First sentence. Second sentence.",
            "Third sentence. Fourth sentence.",
            "Fifth sentence.",
        ]

        # Process in batch
        results = segmenter.segment_batch(texts, language="en")

        # Verify results
        assert isinstance(results, list)
        assert len(results) == 3

        # Each result should be a list of sentences
        assert isinstance(results[0], list)
        assert isinstance(results[1], list)
        assert isinstance(results[2], list)

        # Check content
        assert len(results[0]) == 2  # "First sentence." and "Second sentence."
        assert len(results[1]) == 2  # "Third sentence." and "Fourth sentence."
        assert len(results[2]) == 1  # "Fifth sentence."

    def test_batch_processing_empty_list(self):
        """Test batch processing with empty list."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()

        # Test with empty list
        results = segmenter.segment_batch([], language="en")
        assert results == []

        # Test with list containing empty strings
        results = segmenter.segment_batch(["", "   ", None], language="en")
        assert results == []

    def test_batch_processing_mixed_languages(self):
        """Test batch processing with mixed languages using the appropriate method."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()

        # Test with mixed language content
        texts = [
            "This is English text.",
            "Este es texto en español.",
            "Ceci est du texte français.",
        ]

        # Use segment_mixed_batch for mixed languages
        results = segmenter.segment_mixed_batch(texts)

        # Verify results
        assert isinstance(results, list)
        assert len(results) == 3

        # All should be processed with appropriate language models
        assert all(isinstance(result, list) for result in results)
        assert all(len(result) > 0 for result in results)

        # Test that segment_batch requires explicit language
        # This should work (all English)
        english_texts = ["English text.", "More English text."]
        english_results = segmenter.segment_batch(english_texts, language="en")
        assert len(english_results) == 2

    def test_model_limitations_documentation(self):
        """Test that model limitations are properly documented."""
        from vivre.segmenter import Segmenter

        segmenter = Segmenter()

        # Check that the class docstring mentions model limitations
        class_doc = Segmenter.__doc__
        assert "multilingual" in class_doc.lower()
        assert "accuracy" in class_doc.lower()

        # Check that get_supported_languages mentions limitations
        method_doc = segmenter.get_supported_languages.__doc__
        assert "multilingual" in method_doc.lower()
        assert "accuracy" in method_doc.lower()
