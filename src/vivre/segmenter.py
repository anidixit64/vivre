"""
Text segmentation module for the vivre library.

This module provides functionality to segment text into sentences or other units.
"""

from typing import List, Optional

import langdetect
import spacy
from spacy.language import Language


class Segmenter:
    """
    A text segmenter that splits text into sentences using spaCy models.

    This class provides methods to segment text into meaningful units
    using language detection and spaCy's sentence tokenization.
    """

    def __init__(self) -> None:
        """Initialize the Segmenter instance."""
        self._models: dict[str, Language] = {}
        self._model_names: dict[str, str] = (
            {}
        )  # Track which model is loaded for each language
        self._supported_languages = {
            "en": "en_core_web_sm",
            "es": "es_core_news_sm",
            "fr": "fr_core_news_sm",
            "de": "de_core_news_sm",
            "it": "it_core_news_sm",
            "pt": "pt_core_news_sm",
            "nl": "nl_core_news_sm",
            "pl": "pl_core_news_sm",
            "ru": "ru_core_news_sm",
            "ja": "ja_core_news_sm",
            "zh": "zh_core_web_sm",
            "ko": "ko_core_news_sm",
            "ar": "xx_ent_wiki_sm",  # Arabic uses multilingual model
            "hi": "xx_ent_wiki_sm",  # Hindi uses multilingual model
            "th": "xx_ent_wiki_sm",  # Thai uses multilingual model
        }

    def _detect_language(self, text: str) -> str:
        """
        Detect the language of the given text using langdetect.

        Args:
            text: The text to detect language for.

        Returns:
            Language code (e.g., 'en', 'es', 'fr').
        """
        try:
            # Use langdetect for robust language detection
            detected_lang = langdetect.detect(text)

            # Validate that the detected language is supported
            if detected_lang in self._supported_languages:
                return detected_lang

            # If detected language is not supported, try to map to supported language
            # Handle common language code variations
            lang_mapping = {
                "zh-cn": "zh",  # Chinese (Simplified)
                "zh-tw": "zh",  # Chinese (Traditional)
                "zh-hans": "zh",  # Chinese (Simplified)
                "zh-hant": "zh",  # Chinese (Traditional)
                "ja-jp": "ja",  # Japanese
                "ko-kr": "ko",  # Korean
                "ar-sa": "ar",  # Arabic (Saudi Arabia)
                "hi-in": "hi",  # Hindi (India)
                "th-th": "th",  # Thai (Thailand)
            }

            if detected_lang in lang_mapping:
                return lang_mapping[detected_lang]

            # Default to English for unsupported languages
            return "en"

        except (langdetect.LangDetectException, Exception):
            # Fallback to English if language detection fails
            return "en"

    def _load_model(self, lang_code: str) -> Language:
        """
        Load or get cached spaCy model for the given language.

        Args:
            lang_code: Language code (e.g., 'en', 'es', 'fr').

        Returns:
            Loaded spaCy language model.

        Raises:
            OSError: If the model is not installed.
        """
        if lang_code not in self._supported_languages:
            raise ValueError(f"Unsupported language: {lang_code}")

        model_name = self._supported_languages[lang_code]

        # Check if this specific model is already loaded
        if model_name in self._models:
            # Model is already loaded, just update the mapping
            self._model_names[lang_code] = model_name
            return self._models[model_name]

        # Check if we already have a model loaded for this language
        if lang_code in self._models:
            return self._models[lang_code]

        # Load the model
        try:
            model = spacy.load(model_name)
            self._models[model_name] = model
            self._model_names[lang_code] = model_name
            return model
        except OSError:
            raise OSError(
                f"spaCy model '{model_name}' not found. "
                f"Install it with: python -m spacy download {model_name}"
            )

    def segment(self, text: str, language: Optional[str] = None) -> List[str]:
        """
        Segment text into sentences using spaCy models.

        Args:
            text: The text to segment.
            language: Optional language code (e.g., 'en', 'es', 'fr').
                     If not provided, language will be auto-detected.

        Returns:
            List of sentence segments.

        Raises:
            OSError: If the required spaCy model is not installed.
            ValueError: If the language is not supported.
        """
        if text is None or not text or not text.strip():
            return []

        # Detect language if not provided
        if language is None:
            language = self._detect_language(text)

        # Load the appropriate spaCy model
        nlp = self._load_model(language)

        # Process the text with spaCy
        doc = nlp(text.strip())

        # Extract sentences
        sentences = []
        for sent in doc.sents:
            sentence_text = sent.text.strip()
            if sentence_text:
                sentences.append(sentence_text)

        return sentences

    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported language codes.

        Returns:
            List of supported language codes.
        """
        return list(self._supported_languages.keys())

    def is_language_supported(self, language: str) -> bool:
        """
        Check if a language is supported.

        Args:
            language: Language code to check.

        Returns:
            True if language is supported, False otherwise.
        """
        return language in self._supported_languages
