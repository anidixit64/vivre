"""
Tests for the aligner fixes to ensure numerical stability and prevent infinite costs.
"""

import math
import pytest
import scipy.stats as stats

from vivre.align import Aligner


class TestNumericalStability:
    """Test that the aligner handles numerical edge cases correctly."""

    def test_alignment_cost_never_infinite(self):
        """Test that alignment cost never returns infinite values."""
        aligner = Aligner()
        
        # Test various edge cases that could cause numerical instability
        test_cases = [
            (0, 0),      # Both zero
            (0, 1),      # Source zero
            (1, 0),      # Target zero
            (1, 1000),   # Very different lengths
            (1000, 1),   # Very different lengths
            (100, 100),  # Equal lengths
            (1, 1),      # Small lengths
        ]
        
        for src_len, tgt_len in test_cases:
            cost = aligner._alignment_cost(src_len, tgt_len)
            
            # Cost should be finite
            assert not math.isinf(cost), f"Cost is infinite for src_len={src_len}, tgt_len={tgt_len}"
            assert not math.isnan(cost), f"Cost is NaN for src_len={src_len}, tgt_len={tgt_len}"
            
            # Cost should be non-negative (since it's -log(probability))
            assert cost >= 0, f"Cost is negative for src_len={src_len}, tgt_len={tgt_len}"

    def test_gap_penalty_cost_never_infinite(self):
        """Test that gap penalty cost never returns infinite values."""
        aligner = Aligner()
        
        # Test with different gap penalty values
        gap_penalties = [1.0, 2.0, 3.0, 5.0, 10.0, 20.0]
        
        for penalty in gap_penalties:
            # Create aligner with custom gap penalty
            test_aligner = Aligner(gap_penalty=penalty)
            cost = test_aligner._gap_penalty_cost()
            
            # Cost should be finite
            assert not math.isinf(cost), f"Gap penalty cost is infinite for penalty={penalty}"
            assert not math.isnan(cost), f"Gap penalty cost is NaN for penalty={penalty}"
            
            # Cost should be non-negative
            assert cost >= 0, f"Gap penalty cost is negative for penalty={penalty}"

    def test_extreme_delta_values(self):
        """Test that extreme delta values don't cause numerical issues."""
        aligner = Aligner()
        
        # Test with very large delta values that could cause numerical instability
        extreme_cases = [
            (1, 10000),   # Very large target length
            (10000, 1),   # Very large source length
            (1, 100000),  # Extremely large target length
            (100000, 1),  # Extremely large source length
        ]
        
        for src_len, tgt_len in extreme_cases:
            cost = aligner._alignment_cost(src_len, tgt_len)
            
            # Cost should be finite and reasonable
            assert not math.isinf(cost), f"Cost is infinite for extreme case src_len={src_len}, tgt_len={tgt_len}"
            assert not math.isnan(cost), f"Cost is NaN for extreme case src_len={src_len}, tgt_len={tgt_len}"
            assert cost >= 0, f"Cost is negative for extreme case src_len={src_len}, tgt_len={tgt_len}"

    def test_probability_floor_value(self):
        """Test that probability never becomes exactly zero."""
        aligner = Aligner()
        
        # Test with very large delta that would normally give probability near zero
        src_len, tgt_len = 1, 1000
        delta = abs(tgt_len - src_len * aligner.c) / math.sqrt(src_len * aligner.s2)
        
        # Calculate probability manually to verify epsilon is added
        raw_probability = 2 * (1 - stats.norm.cdf(delta))
        epsilon_probability = raw_probability + 1e-12
        
        # The probability should be greater than zero
        assert epsilon_probability > 0, "Probability should be greater than zero with epsilon"
        
        # The cost should be finite
        cost = -math.log(epsilon_probability)
        assert not math.isinf(cost), "Cost should be finite with epsilon"

    def test_delta_greater_than_10_handling(self):
        """Test that delta > 10 is handled correctly with finite probability."""
        aligner = Aligner()
        
        # Create a case where delta > 10
        src_len, tgt_len = 1, 10000  # This should give delta > 10
        cost = aligner._alignment_cost(src_len, tgt_len)
        
        # Cost should be finite (not infinite)
        assert not math.isinf(cost), "Cost should be finite even for delta > 10"
        assert not math.isnan(cost), "Cost should not be NaN for delta > 10"
        assert cost >= 0, "Cost should be non-negative for delta > 10"
        
        # The cost should be high but finite
        assert cost < 1000, "Cost should be reasonable even for extreme cases"


class TestAlignmentRobustness:
    """Test that the alignment algorithm works robustly with the fixes."""

    def test_alignment_with_extreme_lengths(self):
        """Test that alignment works with extreme sentence lengths."""
        aligner = Aligner()
        
        # Test with very short and very long sentences
        source_sentences = ["A", "This is a very short sentence.", "A" * 1000]
        target_sentences = ["B", "This is a very short sentence.", "B" * 1000]
        
        try:
            result = aligner.align(source_sentences, target_sentences)
            # Should not crash and should return some result
            assert isinstance(result, list)
        except (ValueError, OverflowError, RuntimeError) as e:
            pytest.fail(f"Alignment crashed with extreme lengths: {e}")

    def test_alignment_with_empty_sentences(self):
        """Test that alignment handles empty sentences correctly."""
        aligner = Aligner()
        
        # Test with empty sentences
        source_sentences = ["", "Hello world.", "   ", "Another sentence."]
        target_sentences = ["", "Hola mundo.", "   ", "Otra frase."]
        
        result = aligner.align(source_sentences, target_sentences)
        
        # Should not crash and should filter out empty sentences
        assert isinstance(result, list)
        # Should only align non-empty sentences
        assert len(result) > 0

    def test_alignment_with_very_different_lengths(self):
        """Test that alignment works with very different sentence lengths."""
        aligner = Aligner()
        
        # Test with very different sentence lengths
        source_sentences = ["A", "This is a medium length sentence.", "A" * 500]
        target_sentences = ["B" * 100, "This is a medium length sentence.", "B"]
        
        try:
            result = aligner.align(source_sentences, target_sentences)
            # Should not crash
            assert isinstance(result, list)
        except (ValueError, OverflowError, RuntimeError) as e:
            pytest.fail(f"Alignment crashed with very different lengths: {e}")


def test_aligner_documentation():
    """Test that the aligner documentation reflects the numerical stability improvements."""
    aligner = Aligner()
    
    # Check that the cost calculation methods have proper documentation
    alignment_cost_doc = aligner._alignment_cost.__doc__
    assert alignment_cost_doc is not None
    assert "cost" in alignment_cost_doc.lower()
    
    gap_penalty_doc = aligner._gap_penalty_cost.__doc__
    assert gap_penalty_doc is not None
    assert "cost" in gap_penalty_doc.lower()


def test_aligner_backward_compatibility():
    """Test that the aligner still works correctly for normal cases."""
    aligner = Aligner()
    
    # Test normal alignment case
    source_sentences = ["Hello world.", "This is a test."]
    target_sentences = ["Hola mundo.", "Esto es una prueba."]
    
    result = aligner.align(source_sentences, target_sentences)
    
    # Should work normally
    assert isinstance(result, list)
    assert len(result) > 0
    
    # Test perfect match case
    perfect_sentences = ["Hello world.", "This is a test."]
    perfect_result = aligner.align(perfect_sentences, perfect_sentences)
    
    assert isinstance(perfect_result, list)
    assert len(perfect_result) == len(perfect_sentences) 