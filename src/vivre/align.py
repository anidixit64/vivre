"""
Text alignment functionality for matching source and target texts.
"""

import math
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

    def align(
        self, source_sentences: List[str], target_sentences: List[str]
    ) -> List[Tuple[str, str]]:
        """
        Align source and target sentences into parallel segments.

        Args:
            source_sentences: List of source language sentences (pre-tokenized).
            target_sentences: List of target language sentences (pre-tokenized).

        Returns:
            A list of tuples containing aligned (source_segment, target_segment) pairs.
        """
        # Handle empty sentence lists
        if not source_sentences or not target_sentences:
            return []

        # Filter out empty sentences
        source_sentences = [s.strip() for s in source_sentences if s.strip()]
        target_sentences = [s.strip() for s in target_sentences if s.strip()]

        if not source_sentences or not target_sentences:
            return []

        # For perfectly matched sentences, align 1-1
        if source_sentences == target_sentences:
            return self._align_perfect_match(source_sentences)

        # Use Gale-Church algorithm for different sentences
        return self._align_gale_church(source_sentences, target_sentences)

    def _align_perfect_match(self, sentences: List[str]) -> List[Tuple[str, str]]:
        """
        Align perfectly matched sentences 1-1.

        Args:
            sentences: List of sentences to align.

        Returns:
            List of (sentence, sentence) tuples for perfect alignment.
        """
        # Create 1-1 alignments for each sentence
        alignments = []
        for sentence in sentences:
            if sentence.strip():
                alignments.append((sentence, sentence))

        return alignments

    def _align_gale_church(
        self, source_sentences: List[str], target_sentences: List[str]
    ) -> List[Tuple[str, str]]:
        """
        Align sentences using the Gale-Church algorithm.

        Args:
            source_sentences: List of source language sentences.
            target_sentences: List of target language sentences.

        Returns:
            List of aligned (source_segment, target_segment) tuples.
        """
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
