"""
Unit tests for PPTX text fixer
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from pptx_text_fixer import PPTXTextFixer


class TestPPTXTextFixer:
    """Test suite for PPTX text repair functionality"""
    
    @pytest.fixture
    def fixer(self):
        """Create a PPTXTextFixer instance for testing"""
        return PPTXTextFixer()
    
    def test_contraction_what_s_a(self, fixer):
        """Test: what'saworthy → what's a worthy"""
        input_text = "what'saworthy portfolio"
        expected = "what's a worthy portfolio"
        result = fixer.fix_run_on_words(input_text)
        assert result == expected, f"Expected '{expected}', got '{result}'"
    
    def test_contraction_it_s_a(self, fixer):
        """Test: It'sastrategic → It's a strategic"""
        input_text = "It'sastrategic extension"
        expected = "It's a strategic extension"
        result = fixer.fix_run_on_words(input_text)
        assert "It's a" in result, f"Expected 'It's a' in result, got '{result}'"
    
    def test_with_a_business(self, fixer):
        """Test: withabusiness → with a business"""
        input_text = "Could it work withabusiness segment model?"
        expected = "Could it work with a business segment model?"
        result = fixer.fix_run_on_words(input_text)
        assert "with a business" in result, f"Expected 'with a business', got '{result}'"
    
    def test_as_a_good(self, fixer):
        """Test: asagood → as a good"""
        input_text = "It's asagood extension"
        expected = "It's as a good extension"
        result = fixer.fix_run_on_words(input_text)
        assert "as a good" in result or "as a" in result, f"Expected 'as a', got '{result}'"
    
    def test_combined_issues(self, fixer):
        """Test: Multiple issues in one sentence"""
        input_text = "what'saworthy portfolio withabusiness segment model"
        result = fixer.fix_run_on_words(input_text)
        
        # Should fix both issues
        assert "what's a" in result.lower(), "Should fix contraction"
        assert "with a business" in result.lower(), "Should fix word join"
    
    def test_no_false_positives_normal_text(self, fixer):
        """Test: Don't break correctly spaced text"""
        input_text = "This is a normal sentence with proper spacing."
        result = fixer.fix_run_on_words(input_text)
        assert result == input_text, "Should not modify correct text"
    
    def test_no_false_positives_common_words(self, fixer):
        """Test: Don't break words like 'withdraw', 'together'"""
        test_cases = [
            "Please withdraw the funds.",
            "Let's work together on this.",
            "The athlete won the race.",
        ]
        
        for text in test_cases:
            result = fixer.fix_run_on_words(text)
            assert result == text, f"Should not modify: '{text}', got '{result}'"
    
    def test_preserves_punctuation(self, fixer):
        """Test: Punctuation is preserved"""
        input_text = "Could it work withabusiness? It'sastrategic!"
        result = fixer.fix_run_on_words(input_text)
        
        assert '?' in result, "Should preserve question mark"
        assert '!' in result, "Should preserve exclamation"
    
    def test_case_sensitivity(self, fixer):
        """Test: Handles various cases correctly"""
        test_cases = [
            ("What'saworthy idea", "what's a"),
            ("WHAT'SAWORTHY IDEA", "WHAT'S A"),
            ("It'sastrategic move", "It's a"),
        ]
        
        for input_text, expected_fragment in test_cases:
            result = fixer.fix_run_on_words(input_text)
            assert expected_fragment.lower() in result.lower(), \
                f"Expected '{expected_fragment}' in '{result}'"
    
    def test_statistics_generation(self, fixer):
        """Test: Statistics are correctly generated"""
        original = "what'saworthy portfolio withabusiness model"
        repaired = fixer.fix_run_on_words(original)
        stats = fixer.get_repair_stats(original, repaired)
        
        assert 'original_tokens' in stats
        assert 'repaired_tokens' in stats
        assert 'token_delta' in stats
        assert 'contraction_fixes' in stats
        
        # Should have more tokens after repair
        assert stats['repaired_tokens'] > stats['original_tokens'], \
            "Repaired text should have more tokens"
        
        # Should detect at least one contraction fix
        assert stats['contraction_fixes'] > 0, \
            "Should detect contraction fixes"
    
    def test_empty_string(self, fixer):
        """Test: Handles empty string gracefully"""
        result = fixer.fix_run_on_words("")
        assert result == "", "Should return empty string"
    
    def test_none_input(self, fixer):
        """Test: Handles None input gracefully"""
        result = fixer.fix_run_on_words(None)
        assert result is None, "Should return None for None input"
    
    def test_real_world_sentence(self, fixer):
        """Test: Real example from user requirements"""
        input_text = "It's the most straightforward one but with less strategic-fit."
        result = fixer.fix_run_on_words(input_text)
        
        # This sentence is already correct, should not change much
        # But should preserve hyphens and structure
        assert "strategic-fit" in result or "strategic fit" in result
        assert "It's" in result
    
    def test_multiple_articles_in_row(self, fixer):
        """Test: Handles multiple article joins"""
        input_text = "wordasomething intoanother fromaplace"
        result = fixer.fix_run_on_words(input_text)
        
        # Should increase word count significantly
        original_words = len(input_text.split())
        result_words = len(result.split())
        assert result_words > original_words, \
            f"Expected more words, got {result_words} vs {original_words}"
    
    def test_token_delta_calculation(self, fixer):
        """Test: Token delta is correctly calculated"""
        # Text with 2 known fixes
        original = "what'saworthy withabusiness"
        repaired = fixer.fix_run_on_words(original)
        stats = fixer.get_repair_stats(original, repaired)
        
        # Original: 2 tokens, Should become: 6 tokens (what's a worthy with a business)
        assert stats['token_delta'] >= 3, \
            f"Expected significant token increase, got {stats['token_delta']}"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
