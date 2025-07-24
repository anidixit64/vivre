"""
Text segmentation module for the vivre library.

This module provides functionality to segment text into sentences or other units.
"""

import re
from typing import List, Optional

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
        Detect the language of the given text.

        Args:
            text: The text to detect language for.

        Returns:
            Language code (e.g., 'en', 'es', 'fr').
        """
        # Simple language detection based on character sets and common patterns
        # This is a basic implementation - in production, you might want to use
        # a more sophisticated language detection library like langdetect

        # Check for specific language indicators
        if re.search(r"[а-яё]", text, re.IGNORECASE):
            return "ru"
        elif re.search(r"[一-龯]", text):
            return "zh"
        elif re.search(r"[あ-んア-ン]", text):
            return "ja"
        elif re.search(r"[가-힣]", text):
            return "ko"
        elif re.search(r"[ا-ي]", text):
            return "ar"
        elif re.search(r"[ก-๙]", text):
            return "th"
        elif re.search(r"[àâäéèêëïîôöùûüÿç]", text, re.IGNORECASE):
            return "fr"
        elif re.search(r"[ñáéíóúü¿¡]", text, re.IGNORECASE):
            return "es"
        elif re.search(r"[äöüß]", text, re.IGNORECASE):
            return "de"
        elif re.search(r"[àèéìíîòóù]", text, re.IGNORECASE):
            return "it"
        elif re.search(r"[ãâáàçéêíóôõú]", text, re.IGNORECASE):
            return "pt"
        elif re.search(r"[àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]", text, re.IGNORECASE):
            return "nl"
        elif re.search(r"[ąćęłńóśźż]", text, re.IGNORECASE):
            return "pl"
        elif re.search(r"[क-ह]", text):
            return "hi"
        else:
            # Default to English for Latin script
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

        if lang_code not in self._models:
            model_name = self._supported_languages[lang_code]
            try:
                self._models[lang_code] = spacy.load(model_name)
            except OSError:
                raise OSError(
                    f"spaCy model '{model_name}' not found. "
                    f"Install it with: python -m spacy download {model_name}"
                )

        return self._models[lang_code]

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
