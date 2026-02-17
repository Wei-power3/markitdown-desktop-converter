"""
PPTX text quality fixes: run-on words, line breaks, and Unicode normalization
"""
import re
import logging
from typing import Dict

# Setup logging
logger = logging.getLogger(__name__)


class PPTXTextFixer:
    """
    Fixes PPTX-specific text quality issues:
    1. Run-on words (withabusiness → with a business)
    2. Broken contractions (what'sa → what's a)
    3. Hard line breaks within sentences (Issue #3)
    4. Split words across lines (o \n perational → operational)
    5. Non-standard Unicode glyphs (Issue #4:  → →)
    
    Critical for machine readability and RAG/semantic search.
    """
    
    def __init__(self):
        # Known contraction patterns
        self.contraction_patterns = {
            r"what'sa\b": "what's a",
            r"it'sa\b": "it's a",
            r"that'sa\b": "that's a",
            r"here'sa\b": "here's a",
            r"there'sa\b": "there's a",
            r"who'sa\b": "who's a",
            r"where'sa\b": "where's a",
        }
        
        # Common words that often get concatenated
        self.common_joins = {
            'with': ['a', 'the', 'an', 'business', 'good', 'some', 'any'],
            'about': ['a', 'the', 'an'],
            'from': ['a', 'the', 'an'],
            'into': ['a', 'the', 'an'],
            'onto': ['a', 'the', 'an'],
        }
        
        # Unicode normalization map (Issue #4)
        self.unicode_map = {
            # Arrows
            '\ue000': '→',  # Private use area arrow
            '\uf0e0': '→',  # Another common PUA arrow
            '\u2192': '→',  # Right arrow (normalize to consistent)
            '\u279c': '→',  # Heavy round-tipped rightwards arrow
            '\u279e': '→',  # Heavy triangle-headed rightwards arrow
            '\u27a1': '→',  # Black rightwards arrow
            '\u2794': '→',  # Heavy wide-headed rightwards arrow
            '\u21d2': '⇒',  # Rightwards double arrow (keep distinct)
            '\u21e8': '⇨',  # Rightwards white arrow (keep distinct)
            
            # Bullets and markers
            '\uf0b7': '•',  # PUA bullet
            '\uf0a7': '◦',  # PUA hollow bullet
            '\uf0fc': '▪',  # PUA square bullet
            
            # Quotes
            '\u201c': '"',  # Left double quote
            '\u201d': '"',  # Right double quote
            '\u2018': "'",  # Left single quote
            '\u2019': "'",  # Right single quote
            
            # Dashes
            '\u2013': '–',  # En dash (keep)
            '\u2014': '—',  # Em dash (keep)
            '\u2212': '-',  # Minus sign → hyphen
            
            # Other common artifacts
            '\ufeff': '',   # Zero-width no-break space
            '\u200b': '',   # Zero-width space
            '\xa0': ' ',    # Non-breaking space → normal space
        }
    
    def fix_run_on_words(self, text: str) -> str:
        """
        Legacy method - maintained for backward compatibility.
        Calls fix_text() internally.
        """
        result = self.fix_text(text)
        return result['text']
    
    def fix_text(self, text: str) -> Dict:
        """
        Apply all PPTX text fixes.
        
        Args:
            text: Input text (potentially with PPTX artifacts)
        
        Returns:
            Dictionary with:
            - 'text': Fixed text
            - 'stats': Statistics about fixes applied
        """
        if not text:
            return {'text': '', 'stats': self._empty_stats()}
        
        stats = {
            'contraction_fixes': 0,
            'run_on_fixes': 0,
            'line_break_fixes': 0,
            'split_word_fixes': 0,
            'unicode_fixes': 0,
            'total_fixes': 0
        }
        
        original_text = text
        
        # Step 1: Fix contractions (what'sa → what's a)
        text, contraction_fixes = self._fix_contractions(text)
        stats['contraction_fixes'] = contraction_fixes
        
        # Step 2: Fix run-on words (withabusiness → with a business)
        text, run_on_fixes = self._fix_run_on_words(text)
        stats['run_on_fixes'] = run_on_fixes
        
        # Step 3: NEW - Remove hard line breaks (Issue #3)
        text, line_break_fixes = self._fix_hard_line_breaks(text)
        stats['line_break_fixes'] = line_break_fixes
        
        # Step 4: NEW - Rejoin split words (Issue #3)
        text, split_word_fixes = self._fix_split_words(text)
        stats['split_word_fixes'] = split_word_fixes
        
        # Step 5: NEW - Normalize Unicode (Issue #4)
        text, unicode_fixes = self._normalize_unicode(text)
        stats['unicode_fixes'] = unicode_fixes
        
        # Calculate totals
        stats['total_fixes'] = sum([
            stats['contraction_fixes'],
            stats['run_on_fixes'],
            stats['line_break_fixes'],
            stats['split_word_fixes'],
            stats['unicode_fixes']
        ])
        
        # Log if significant changes
        if stats['total_fixes'] > 0:
            logger.info(
                f"PPTX fixes applied: {stats['contraction_fixes']} contractions, "
                f"{stats['run_on_fixes']} run-ons, {stats['line_break_fixes']} line breaks, "
                f"{stats['split_word_fixes']} split words, {stats['unicode_fixes']} Unicode"
            )
        
        return {'text': text, 'stats': stats}
    
    def _fix_contractions(self, text: str) -> tuple:
        """
        Fix broken contractions: what'sa → what's a
        
        Returns:
            (fixed_text, fix_count)
        """
        fix_count = 0
        
        # Known contraction patterns
        for pattern, replacement in self.contraction_patterns.items():
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            if matches > 0:
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
                fix_count += matches
        
        # General apostrophe contractions (It'sastrategic → It's a strategic)
        pattern = r"(\w+)'s([a-z])"
        matches = len(re.findall(pattern, text))
        if matches > 0:
            text = re.sub(pattern, r"\1's \2", text)
            fix_count += matches
        
        return text, fix_count
    
    def _fix_run_on_words(self, text: str) -> tuple:
        """
        Fix run-on words: withabusiness → with a business
        
        Returns:
            (fixed_text, fix_count)
        """
        fix_count = 0
        
        # Fix common word joins
        for word, targets in self.common_joins.items():
            for target in targets:
                pattern = rf'\b({word})({target})\b'
                
                def replacer(match):
                    w = match.group(1)
                    t = match.group(2)
                    if t in ['a', 'an', 'the'] or len(t) >= 4:
                        return f"{w} {t}"
                    return match.group(0)
                
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                if matches > 0:
                    text = re.sub(pattern, replacer, text, flags=re.IGNORECASE)
                    fix_count += matches
        
        # Fix article/preposition joins (wordasomething → word a something)
        for article in ['a', 'an', 'the', 'as', 'is', 'in', 'on', 'at', 'to']:
            pattern = rf'([a-z])({article})([a-z]{{2,}})'
            
            def replacer(match):
                before = match.group(1)
                art = match.group(2)
                after = match.group(3)
                
                common_starts = [
                    'go', 'wo', 'se', 'bu', 'st', 'mo', 'po', 'pr', 'gr',
                    'good', 'work', 'some', 'business', 'strategic', 'model',
                    'portfolio', 'segment', 'extension', 'question'
                ]
                
                if after[:2] in common_starts or len(after) >= 6:
                    return f"{before} {art} {after}"
                
                return match.group(0)
            
            matches = len(re.findall(pattern, text))
            if matches > 0:
                text = re.sub(pattern, replacer, text)
                fix_count += matches
        
        return text, fix_count
    
    def _fix_hard_line_breaks(self, text: str) -> tuple:
        """
        Remove hard line breaks within sentences (Issue #3).
        
        Strategy:
        - Keep line breaks that are paragraph boundaries (double newline)
        - Keep line breaks before markdown elements (##, -, *, |, etc.)
        - Remove line breaks within sentences
        
        Returns:
            (fixed_text, fix_count)
        """
        fix_count = 0
        lines = text.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            current = lines[i].strip()
            
            # Empty line - keep as paragraph boundary
            if not current:
                result.append('')
                i += 1
                continue
            
            # Markdown element - keep break before it
            if self._is_markdown_element(current):
                result.append(current)
                i += 1
                continue
            
            # Look ahead: should we merge with next line?
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                
                # Don't merge if next is empty or markdown element
                if not next_line or self._is_markdown_element(next_line):
                    result.append(current)
                    i += 1
                    continue
                
                # Check if current line ends mid-sentence
                if self._ends_mid_sentence(current):
                    # Merge: add space between lines
                    result.append(current + ' ' + next_line)
                    fix_count += 1
                    i += 2  # Skip next line (already merged)
                    continue
            
            # Default: keep line as-is
            result.append(current)
            i += 1
        
        return '\n'.join(result), fix_count
    
    def _is_markdown_element(self, line: str) -> bool:
        """
        Check if line starts with markdown syntax.
        """
        if not line:
            return False
        
        # Headers
        if line.startswith('#'):
            return True
        
        # Lists
        if re.match(r'^[-*+]\s', line):
            return True
        
        # Numbered lists
        if re.match(r'^\d+\.\s', line):
            return True
        
        # Tables
        if line.startswith('|'):
            return True
        
        # Code blocks
        if line.startswith('```'):
            return True
        
        # Blockquotes
        if line.startswith('>'):
            return True
        
        return False
    
    def _ends_mid_sentence(self, line: str) -> bool:
        """
        Check if line ends mid-sentence (should be merged with next).
        
        Returns True if line does NOT end with:
        - Period, exclamation, question mark
        - Colon (section header)
        - Closing quote + punctuation
        """
        if not line:
            return False
        
        # Ends with sentence terminator
        if re.search(r'[.!?:]\s*$', line):
            return False
        
        # Ends with closing quote + punctuation
        if re.search(r'[.!?]["\')]\s*$', line):
            return False
        
        # Ends with closing parenthesis + punctuation
        if re.search(r'[.!?]\)\s*$', line):
            return False
        
        # Otherwise, likely mid-sentence
        return True
    
    def _fix_split_words(self, text: str) -> tuple:
        """
        Rejoin split words across lines (Issue #3).
        
        Pattern: "o \n perational" → "operational"
        
        Returns:
            (fixed_text, fix_count)
        """
        # Match: lowercase letter(s) + optional spaces + newline + spaces + lowercase letter(s)
        pattern = r'([a-z]{1,3})\s*\n\s*([a-z]{2,})'
        
        def replace_split(match):
            part1 = match.group(1)
            part2 = match.group(2)
            
            # Simple heuristic: if combined length is reasonable and looks like a word
            combined = part1 + part2
            if 3 <= len(combined) <= 20:
                return combined
            else:
                # Keep original if doesn't look like a word
                return match.group(0)
        
        original = text
        text = re.sub(pattern, replace_split, text)
        
        # Count fixes (approximate)
        fix_count = len(re.findall(pattern, original))
        
        return text, fix_count
    
    def _normalize_unicode(self, text: str) -> tuple:
        """
        Normalize non-standard Unicode glyphs (Issue #4).
        
        Returns:
            (fixed_text, fix_count)
        """
        fix_count = 0
        
        for old_char, new_char in self.unicode_map.items():
            count = text.count(old_char)
            if count > 0:
                text = text.replace(old_char, new_char)
                fix_count += count
        
        return text, fix_count
    
    def get_repair_stats(self, original: str, repaired: str) -> Dict[str, int]:
        """
        LEGACY METHOD - maintained for backward compatibility.
        Generate statistics about repairs performed.
        """
        original_tokens = original.split()
        repaired_tokens = repaired.split()
        
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
    
    def _empty_stats(self) -> Dict:
        """Return empty statistics dictionary."""
        return {
            'contraction_fixes': 0,
            'run_on_fixes': 0,
            'line_break_fixes': 0,
            'split_word_fixes': 0,
            'unicode_fixes': 0,
            'total_fixes': 0
        }


# Convenience function for direct use
def fix_pptx_text(text: str) -> Dict:
    """
    Convenience function to fix PPTX text issues.
    
    Args:
        text: Input text from PPTX conversion
    
    Returns:
        Dictionary with 'text' and 'stats' keys
    """
    fixer = PPTXTextFixer()
    return fixer.fix_text(text)


# Example usage
if __name__ == "__main__":
    # Test cases
    test_cases = [
        "what'saworthy portfolio withabusiness model",
        "This is o\nperational efficiency",
        "Decision → next steps",
        "We need\nto improve\nour process.",
    ]
    
    fixer = PPTXTextFixer()
    
    print("=== PPTX Text Fixer Examples ===")
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print(f"  Before: {repr(test)}")
        result = fixer.fix_text(test)
        print(f"  After:  {repr(result['text'])}")
        print(f"  Stats:  {result['stats']}")
