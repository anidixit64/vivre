"""
Text segmentation module for the vivre library.

This module provides functionality to segment text into sentences or other units.
"""

import re
from typing import List


class Segmenter:
    """
    A text segmenter that splits text into sentences or other units.

    This class provides methods to segment text into meaningful units
    such as sentences, paragraphs, or other text segments.
    """

    def __init__(self) -> None:
        """Initialize the Segmenter instance."""
        pass

    def segment(self, text: str) -> List[str]:
        """
        Segment text into sentences or other units.

        Args:
            text: The text to segment.

        Returns:
            List of text segments.
        """
        if not text or not text.strip():
            return []

        # Basic sentence segmentation using regex
        # Split on sentence endings (.!?) followed by whitespace or end of string
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())

        # Filter out empty sentences and clean up
        segments = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                segments.append(sentence)

        return segments
