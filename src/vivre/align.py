"""
Text alignment functionality for matching source and target texts.
"""

import math
import re
from typing import List, Tuple


class Aligner:
    """
    A class for aligning source and target texts.

    This class provides functionality to align segments of text between
    source and target languages, creating parallel corpora for translation
    and analysis purposes.
    """

    def __init__(self):
        """Initialize the Aligner."""
        pass

    def align(self, source_text: str, target_text: str) -> List[Tuple[str, str]]:
        """
        Align source and target texts into parallel segments.

        Args:
            source_text: The source language text.
            target_text: The target language text.

        Returns:
            A list of tuples containing aligned (source_segment, target_segment) pairs.
        """
        # Handle empty or whitespace-only texts
        if not source_text or not source_text.strip():
            return []
        if not target_text or not target_text.strip():
            return []

        # For perfectly matched texts, split into sentences and align 1-1
        if source_text == target_text:
            return self._align_perfect_match(source_text)

        # Use Gale-Church algorithm for different texts
        return self._align_gale_church(source_text, target_text)

    def _align_perfect_match(self, text: str) -> List[Tuple[str, str]]:
        """
        Align perfectly matched text by splitting into sentences.

        Args:
            text: The text to split and align.

        Returns:
            List of (sentence, sentence) tuples for perfect alignment.
        """
        # Split text into sentences using regex
        # This handles various sentence endings: . ! ?
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())

        # Filter out empty sentences and create alignments
        alignments = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                alignments.append((sentence, sentence))

        return alignments

    def _align_gale_church(
        self, source_text: str, target_text: str
    ) -> List[Tuple[str, str]]:
        """
        Align texts using the Gale-Church algorithm.

        Args:
            source_text: The source language text.
            target_text: The target language text.

        Returns:
            List of aligned (source_segment, target_segment) tuples.
        """
        # Split texts into sentences
        source_sentences = self._split_into_sentences(source_text)
        target_sentences = self._split_into_sentences(target_text)

        if not source_sentences or not target_sentences:
            return []

        # Calculate sentence lengths (in characters)
        source_lengths = [len(s) for s in source_sentences]
        target_lengths = [len(s) for s in target_sentences]

        # Find optimal alignment using dynamic programming
        alignment = self._gale_church_dp(source_lengths, target_lengths)

        # Convert alignment indices to actual sentence pairs
        result = []
        for src_start, src_end, tgt_start, tgt_end in alignment:
            src_segment = " ".join(source_sentences[src_start:src_end])
            tgt_segment = " ".join(target_sentences[tgt_start:tgt_end])
            result.append((src_segment, tgt_segment))

        return result

    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.

        Args:
            text: The text to split.

        Returns:
            List of sentences.
        """
        # Split on sentence boundaries: . ! ? followed by whitespace
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())

        # Filter out empty sentences
        return [s.strip() for s in sentences if s.strip()]

    def _gale_church_dp(
        self, source_lengths: List[int], target_lengths: List[int]
    ) -> List[Tuple[int, int, int, int]]:
        """
        Dynamic programming implementation of Gale-Church algorithm.

        Args:
            source_lengths: List of source sentence lengths.
            target_lengths: List of target sentence lengths.

        Returns:
            List of (src_start, src_end, tgt_start, tgt_end) tuples.
        """
        m, n = len(source_lengths), len(target_lengths)

        # Initialize DP table
        # dp[i][j] = minimum cost to align source[0:i] with target[0:j]
        dp = [[float("inf")] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = 0

        # Backtracking table to reconstruct alignment
        backtrack: List[List] = [[None] * (n + 1) for _ in range(m + 1)]

        # Fill DP table
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0 and j == 0:
                    continue

                # Try different alignment types
                candidates = []

                # 1-1 alignment (preferred)
                if i > 0 and j > 0:
                    cost = self._alignment_cost(
                        source_lengths[i - 1], target_lengths[j - 1]
                    )
                    # Add bias towards 1-1 alignment
                    cost -= 2.0  # Prefer 1-1 alignments
                    candidates.append((dp[i - 1][j - 1] + cost, (i - 1, j - 1, 1, 1)))

                # 1-0 alignment (source sentence with no target)
                if i > 0:
                    cost = self._alignment_cost(source_lengths[i - 1], 0)
                    candidates.append((dp[i - 1][j] + cost, (i - 1, j, 1, 0)))

                # 0-1 alignment (target sentence with no source)
                if j > 0:
                    cost = self._alignment_cost(0, target_lengths[j - 1])
                    candidates.append((dp[i][j - 1] + cost, (i, j - 1, 0, 1)))

                # 2-1 alignment (two source sentences with one target)
                if i > 1 and j > 0:
                    src_len = source_lengths[i - 2] + source_lengths[i - 1]
                    cost = self._alignment_cost(src_len, target_lengths[j - 1])
                    # Add penalty for non-1-1 alignments
                    cost += 5.0
                    candidates.append((dp[i - 2][j - 1] + cost, (i - 2, j - 1, 2, 1)))

                # 1-2 alignment (one source sentence with two target)
                if i > 0 and j > 1:
                    tgt_len = target_lengths[j - 2] + target_lengths[j - 1]
                    cost = self._alignment_cost(source_lengths[i - 1], tgt_len)
                    # Add penalty for non-1-1 alignments
                    cost += 5.0
                    candidates.append((dp[i - 1][j - 2] + cost, (i - 1, j - 2, 1, 2)))

                # 2-2 alignment (two source sentences with two target)
                if i > 1 and j > 1:
                    src_len = source_lengths[i - 2] + source_lengths[i - 1]
                    tgt_len = target_lengths[j - 2] + target_lengths[j - 1]
                    cost = self._alignment_cost(src_len, tgt_len)
                    # Add penalty for non-1-1 alignments
                    cost += 5.0
                    candidates.append((dp[i - 2][j - 2] + cost, (i - 2, j - 2, 2, 2)))

                # Choose best candidate
                if candidates:
                    best_cost, best_move = min(candidates, key=lambda x: x[0])
                    dp[i][j] = best_cost
                    backtrack[i][j] = best_move

        # Reconstruct alignment
        return self._reconstruct_alignment(backtrack, m, n)

    def _alignment_cost(self, src_len: int, tgt_len: int) -> float:
        """
        Calculate alignment cost using Gale-Church statistical model.

        Args:
            src_len: Source sentence length.
            tgt_len: Target sentence length.

        Returns:
            Alignment cost.
        """
        if src_len == 0 and tgt_len == 0:
            return 0.0

        # Parameters for the statistical model
        # These can be tuned based on language pair
        c = 1.0  # Length ratio parameter
        p0 = 0.6  # Probability of 1-1 alignment (increased)
        p1 = 0.2  # Probability of 1-0 or 0-1 alignment (decreased)

        # Calculate length ratio
        if src_len == 0:
            ratio = float("inf")
        elif tgt_len == 0:
            ratio = 0.0
        else:
            ratio = tgt_len / src_len

        # Calculate log probability
        if ratio == 0.0 or ratio == float("inf"):
            log_prob = -100.0  # Very low probability
        else:
            # Normal distribution approximation with tighter variance
            log_prob = -0.5 * ((ratio - c) / 0.3) ** 2

        # Add alignment type penalty
        if src_len == 0 or tgt_len == 0:
            log_prob += math.log(p1)
        elif src_len > 0 and tgt_len > 0:
            log_prob += math.log(p0)

        # Add penalty for very large alignments to encourage sentence-level alignment
        if src_len > 50 or tgt_len > 50:
            log_prob -= 10.0  # Heavy penalty for large alignments

        return -log_prob  # Return negative log probability as cost

    def _reconstruct_alignment(
        self, backtrack: List[List], m: int, n: int
    ) -> List[Tuple[int, int, int, int]]:
        """
        Reconstruct alignment from backtracking table.

        Args:
            backtrack: Backtracking table.
            m: Number of source sentences.
            n: Number of target sentences.

        Returns:
            List of (src_start, src_end, tgt_start, tgt_end) tuples.
        """
        alignment = []
        i, j = m, n

        while i > 0 or j > 0:
            if backtrack[i][j] is None:
                break

            prev_i, prev_j, src_count, tgt_count = backtrack[i][j]

            # Add alignment
            alignment.append((prev_i, i, prev_j, j))

            # Move to previous position
            i, j = prev_i, prev_j

        # Reverse to get correct order
        return list(reversed(alignment))
