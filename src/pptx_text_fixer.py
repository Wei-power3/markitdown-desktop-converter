"""
PPTX-specific text repair utilities
Fixes run-on words, hard breaks, and structure issues
"""
import re
from typing import List, Tuple, Dict


class PPTXTextFixer:
    """
    Repairs PPTX extraction artifacts that break tokenization.
    
    Focuses on fixing:
    - Run-on words (e.g., "withabusiness" → "with a business")
    - Contractions without spaces (e.g., "what'saworthy" → "what's a worthy")
    - Word boundary issues from adjacent text boxes
    """
    
    def __init__(self):
        # Known contraction patterns that need space insertion
        self.contraction_patterns = {
            r"what'sa\b": "what's a",
            r"it'sa\b": "it's a",
            r"that'sa\b": "that's a",
            r"here'sa\b": "here's a",
            r"there'sa\b": "there's a",
            r"who'sa\b": "who's a",
            r"where'sa\b": "where's a",
        }
        
        # Common articles and short prepositions
        self.short_words = ['a', 'an', 'the', 'in', 'on', 'at', 'to', 'of', 'as', 'is', 'or', 'and']
        
        # Common words that often get concatenated
        self.common_joins = {
            'with': ['a', 'the', 'an', 'business', 'good', 'some', 'any'],
            'about': ['a', 'the', 'an'],
            'from': ['a', 'the', 'an'],
            'into': ['a', 'the', 'an'],
            'onto': ['a', 'the', 'an'],
        }
    
    def fix_run_on_words(self, text: str) -> str:
        """
        Detect and repair run-on words using multiple heuristics.
        
        Strategy:
        1. Fix known contractions (what'saworthy → what's a worthy)
        2. Fix common word joins (withabusiness → with a business)
        3. Fix article/preposition patterns (wordasomething → word a something)
        4. Apply conservative spacing rules
        
        Args:
            text: Text with potential run-on words
            
        Returns:
            Text with run-on words repaired
        """
        if not text:
            return text
        
        fixed = text
        
        # Step 1: Fix contractions
        for pattern, replacement in self.contraction_patterns.items():
            fixed = re.sub(pattern, replacement, fixed, flags=re.IGNORECASE)
        
        # Step 2: Fix common word joins (withabusiness, aboutaproject, etc.)
        fixed = self._fix_common_word_joins(fixed)
        
        # Step 3: Fix article/preposition joins (wordasomething → word a something)
        fixed = self._fix_article_joins(fixed)
        
        # Step 4: Fix general apostrophe contractions (It'sastrategic → It's a strategic)
        fixed = self._fix_contractions(fixed)
        
        return fixed
    
    def _fix_common_word_joins(self, text: str) -> str:
        """
        Fix patterns like "withabusiness" → "with a business"
        Uses known common word combinations.
        """
        for word, targets in self.common_joins.items():
            for target in targets:
                # Pattern: word + target without space
                # Case-insensitive for the word, preserve case
                pattern = rf'\b({word})({target})\b'
                
                def replacer(match):
                    w = match.group(1)
                    t = match.group(2)
                    # Only replace if target looks like it should be separate word
                    if t in ['a', 'an', 'the'] or len(t) >= 4:
                        return f"{w} {t}"
                    return match.group(0)
                
                text = re.sub(pattern, replacer, text, flags=re.IGNORECASE)
        
        return text
    
    def _fix_article_joins(self, text: str) -> str:
        """
        Fix patterns like "wordasomething" → "word a something"
        Only apply when high confidence (article followed by valid word).
        """
        for article in ['a', 'an', 'the', 'as', 'is', 'in', 'on', 'at', 'to']:
            # Pattern: lowercase letter + article + lowercase word (2+ chars)
            pattern = rf'([a-z])({article})([a-z]{{2,}})'
            
            def replacer(match):
                before = match.group(1)
                art = match.group(2)
                after = match.group(3)
                
                # Heuristic: Check if 'after' looks like a word start
                # Common starting patterns in English
                common_starts = [
                    'go', 'wo', 'se', 'bu', 'st', 'mo', 'po', 'pr', 'gr',
                    'good', 'work', 'some', 'business', 'strategic', 'model',
                    'portfolio', 'segment', 'extension', 'question'
                ]
                
                # If starts with common pattern, or is a longer word (likely real)
                if after[:2] in common_starts or len(after) >= 6:
                    return f"{before} {art} {after}"
                
                # Keep original if uncertain
                return match.group(0)
            
            text = re.sub(pattern, replacer, text)
        
        return text
    
    def _fix_contractions(self, text: str) -> str:
        """
        Fix missing spaces around contractions.
        Example: "It'sastrategic" → "It's a strategic"
        """
        # Pattern: word + 's + lowercase letter (should be: word's + space + word)
        pattern = r"(\w+)'s([a-z])"
        text = re.sub(pattern, r"\1's \2", text)
        
        return text
    
    def get_repair_stats(self, original: str, repaired: str) -> Dict[str, int]:
        """
        Generate statistics about repairs performed.
        
        Args:
            original: Original text before repair
            repaired: Text after repair
            
        Returns:
            Dictionary with repair statistics
        """
        original_tokens = original.split()
        repaired_tokens = repaired.split()
        
        # Count contraction fixes
        contraction_fixes = 0
        for pattern in self.contraction_patterns.keys():
            contraction_fixes += len(re.findall(pattern, original, re.IGNORECASE))
        
        return {
            'original_tokens': len(original_tokens),
            'repaired_tokens': len(repaired_tokens),
            'token_delta': len(repaired_tokens) - len(original_tokens),
            'contraction_fixes': contraction_fixes,
            'estimated_run_on_fixes': max(0, len(repaired_tokens) - len(original_tokens) - contraction_fixes)
        }


# Example usage and testing
if __name__ == "__main__":
    fixer = PPTXTextFixer()
    
    # Test cases from user requirements
    test_cases = [
        "what'saworthy portfolio",
        "withabusiness segment model",
        "Could it work withabusiness segment model?",
        "asagood extension",
        "It'sastrategic extension",
        "It's the most straightforward one but with less strategic-fit."
    ]
    
    print("=== PPTX Text Fixer Test ===\n")
    for test in test_cases:
        fixed = fixer.fix_run_on_words(test)
        if test != fixed:
            print(f"Original: {test}")
            print(f"Fixed:    {fixed}")
            print()
        else:
            print(f"No change: {test}\n")
    
    # Statistics example
    sample_text = "what'saworthy portfolio withabusiness model asagood fit"
    fixed_text = fixer.fix_run_on_words(sample_text)
    stats = fixer.get_repair_stats(sample_text, fixed_text)
    print(f"=== Statistics ===")
    print(f"Original tokens: {stats['original_tokens']}")
    print(f"Repaired tokens: {stats['repaired_tokens']}")
    print(f"Token increase: +{stats['token_delta']}")
    print(f"Contraction fixes: {stats['contraction_fixes']}")
    print(f"Run-on fixes: {stats['estimated_run_on_fixes']}")
