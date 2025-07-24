"""
Text alignment functionality for matching source and target texts.
"""

import math
from typing import List, Tuple


class Aligner:
    """
    A class for aligning source and target texts using the Gale-Church algorithm.

    This class provides functionality to align segments of text between
    source and target languages, creating parallel corpora for translation
    and analysis purposes.
    """

    def __init__(self, language_pair: str = "en-es"):
        """
        Initialize the Aligner with language-specific parameters.

        Args:
            language_pair: Language pair code (e.g., "en-es", "en-fr", "en-de").
                          Defaults to "en-es" (English-Spanish).
        """
        # Language-specific parameters for the Gale-Church algorithm
        self.language_params = {
            "en-es": {
                "mean_ratio": 1.0,  # Mean length ratio (target/source)
                "variance": 0.3,  # Variance of the length ratio
                "gap_penalty": 3.0,  # Gap penalty (in standard deviations)
            },
            "en-fr": {
                "mean_ratio": 1.1,
                "variance": 0.35,
                "gap_penalty": 3.0,
            },
            "en-de": {
                "mean_ratio": 1.2,
                "variance": 0.4,
                "gap_penalty": 3.0,
            },
            "en-it": {
                "mean_ratio": 1.05,
                "variance": 0.32,
                "gap_penalty": 3.0,
            },
        }

        # Use default parameters if language pair not found
        self.params = self.language_params.get(
            language_pair, self.language_params["en-es"]
        )

        # Extract parameters for easier access
        self.mean_ratio = self.params["mean_ratio"]
        self.variance = self.params["variance"]
        self.gap_penalty = self.params["gap_penalty"]

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

                # 1-1 alignment
                if i > 0 and j > 0:
                    cost = self._alignment_cost(
                        source_lengths[i - 1], target_lengths[j - 1]
                    )
                    candidates.append((dp[i - 1][j - 1] + cost, (i - 1, j - 1, 1, 1)))

                # 1-0 alignment (source sentence with no target)
                if i > 0:
                    cost = self._gap_penalty_cost()
                    candidates.append((dp[i - 1][j] + cost, (i - 1, j, 1, 0)))

                # 0-1 alignment (target sentence with no source)
                if j > 0:
                    cost = self._gap_penalty_cost()
                    candidates.append((dp[i][j - 1] + cost, (i, j - 1, 0, 1)))

                # 2-1 alignment (two source sentences with one target)
                if i > 1 and j > 0:
                    src_len = source_lengths[i - 2] + source_lengths[i - 1]
                    cost = self._alignment_cost(src_len, target_lengths[j - 1])
                    candidates.append((dp[i - 2][j - 1] + cost, (i - 2, j - 1, 2, 1)))

                # 1-2 alignment (one source sentence with two target)
                if i > 0 and j > 1:
                    tgt_len = target_lengths[j - 2] + target_lengths[j - 1]
                    cost = self._alignment_cost(source_lengths[i - 1], tgt_len)
                    candidates.append((dp[i - 1][j - 2] + cost, (i - 1, j - 2, 1, 2)))

                # 2-2 alignment (two source sentences with two target)
                if i > 1 and j > 1:
                    src_len = source_lengths[i - 2] + source_lengths[i - 1]
                    tgt_len = target_lengths[j - 2] + target_lengths[j - 1]
                    cost = self._alignment_cost(src_len, tgt_len)
                    candidates.append((dp[i - 2][j - 2] + cost, (i - 2, j - 2, 2, 2)))

                # Choose best candidate
                if candidates:
                    best_cost, best_move = min(candidates, key=lambda x: x[0])
                    dp[i][j] = best_cost
                    backtrack[i][j] = best_move

        # Reconstruct alignment path
        return self._reconstruct_alignment(backtrack, m, n)

    def _alignment_cost(self, src_len: int, tgt_len: int) -> float:
        """
        Calculate alignment cost using statistically sound Gale-Church model.

        Args:
            src_len: Source sentence length.
            tgt_len: Target sentence length.

        Returns:
            Alignment cost (negative log probability).
        """
        if src_len == 0 and tgt_len == 0:
            return 0.0

        # Calculate the length ratio
        if src_len == 0:
            ratio = float("inf")
        elif tgt_len == 0:
            ratio = 0.0
        else:
            ratio = tgt_len / src_len

        # Calculate delta (number of standard deviations from mean)
        if ratio == 0.0 or ratio == float("inf"):
            delta = float("inf")
        else:
            delta = abs(ratio - self.mean_ratio) / self.variance

        # Convert delta to probability using normal distribution CDF
        # For large delta, use approximation to avoid numerical issues
        if delta > 10:
            # Very unlikely match
            probability = 1e-10
        else:
            # Use normal distribution CDF approximation
            probability = self._normal_cdf(delta)

        # Convert probability to cost (negative log probability)
        cost = -math.log(probability) if probability > 0 else 100.0

        return cost

    def _normal_cdf(self, delta: float) -> float:
        """
        Calculate the cumulative distribution function of the normal distribution.

        Args:
            delta: Number of standard deviations from mean.

        Returns:
            Probability of observing a deviation as large or larger than delta.
        """
        # Use approximation for normal CDF
        # This is the complementary error function approximation
        if delta < 0:
            return 1.0

        # For delta >= 0, P(X >= delta) = 1 - P(X < delta)
        # Using approximation: P(X < delta) ≈ 1 - 0.5 * erfc(delta/sqrt(2))
        # where erfc is the complementary error function

        # Simple approximation for erfc
        if delta > 8:
            return 1e-10  # Very small probability

        # Use polynomial approximation for erfc
        t = 1.0 / (1.0 + 0.5 * delta)
        erfc = (
            t
            * math.exp(-delta * delta / 2.0)
            * (1.0 - 0.5 * delta * delta * t * t * (1.0 - 0.5 * delta * delta * t * t))
        )

        return 0.5 * erfc

    def _gap_penalty_cost(self) -> float:
        """
        Calculate the cost for gap alignments (1-0 or 0-1).

        Returns:
            Gap penalty cost.
        """
        # Convert gap penalty (in standard deviations) to probability
        # A gap penalty of 3.0 means the cost is equivalent to a 3-sigma deviation
        probability = self._normal_cdf(self.gap_penalty)

        # Convert to cost
        return -math.log(probability) if probability > 0 else 100.0

    def _reconstruct_alignment(
        self, backtrack: List[List], m: int, n: int
    ) -> List[Tuple[int, int, int, int]]:
        """
        Reconstruct the alignment path from the backtracking table.

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

            # Add alignment segment
            alignment.append((prev_i, i, prev_j, j))

            # Move to previous position
            i, j = prev_i, prev_j

        # Reverse to get correct order
        alignment.reverse()
        return alignment
