"""
Text cleaning utilities for fixing PDF and PPTX extraction artifacts
"""
import re
from typing import Dict, Pattern, Optional
from pptx_text_fixer import PPTXTextFixer


class MarkdownCleaner:
    """
    Cleans common document extraction artifacts from markdown text.
    
    Handles:
    - PDF: Ligature splitting, hyphenation, medical terms, special characters
    - PPTX: Run-on words, contractions, word boundary issues
    - General: Spacing issues, sentence breaks
    """
    
    def __init__(self):
        # Common ligature patterns
        self.ligature_patterns = {
            r'\bArti\s*fi\s*cial\b': 'Artificial',
            r'\barti\s*fi\s*cial\b': 'artificial',
            r'\bde\s*fi\s*ned\b': 'defined',
            r'\bDe\s*fi\s*ned\b': 'Defined',
            r'\bspeci\s*fi\s*c\b': 'specific',
            r'\bSpeci\s*fi\s*c\b': 'Specific',
            r'\bef\s*fi\s*cient\b': 'efficient',
            r'\bEf\s*fi\s*cient\b': 'Efficient',
            r'\bsuf\s*fi\s*cient\b': 'sufficient',
            r'\bSuf\s*fi\s*cient\b': 'Sufficient',
            r'\bdi\s*ff\s*erent\b': 'different',
            r'\bDi\s*ff\s*erent\b': 'Different',
            r'\bof\s*fi\s*ce\b': 'office',
            r'\bOf\s*fi\s*ce\b': 'Office',
            r'\bcon\s*fi\s*rm\b': 'confirm',
            r'\bCon\s*fi\s*rm\b': 'Confirm',
            r'\bclassi\s*fi\s*cation\b': 'classification',
            r'\bClassi\s*fi\s*cation\b': 'Classification',
        }
        
        # Hyphenation artifacts (common in medical/scientific papers)
        self.hyphen_patterns = {
            r'non-\s+invasive': 'non-invasive',
            r'receiver-\s+operating': 'receiver-operating',
            r'cross-\s+sectional': 'cross-sectional',
            r'double-\s+blind': 'double-blind',
            r'multi-\s+center': 'multi-center',
            r'multi-\s+variate': 'multi-variate',
            r'long-\s+term': 'long-term',
            r'short-\s+term': 'short-term',
            r'high-\s+risk': 'high-risk',
            r'low-\s+risk': 'low-risk',
            r'well-\s+established': 'well-established',
            r'post-\s+operative': 'post-operative',
            r'pre-\s+operative': 'pre-operative',
        }
        
        # Medical/biomarker terms
        self.medical_patterns = {
            r'β-\s*blockers': 'β-blockers',
            r'NT-\s*proBNP': 'NT-proBNP',
            r'MR-\s*proADM': 'MR-proADM',
            r'C-\s*reactive': 'C-reactive',
            r'D-\s*dimer': 'D-dimer',
            r'HbA\s*1c': 'HbA1c',
            r'CD\s*4': 'CD4',
            r'CD\s*8': 'CD8',
            r'IL-\s*6': 'IL-6',
            r'TNF-\s*α': 'TNF-α',
            r'IFN-\s*γ': 'IFN-γ',
        }
        
        # Compile all patterns for efficiency
        self.all_patterns: Dict[Pattern, str] = {}
        for patterns_dict in [self.ligature_patterns, self.hyphen_patterns, self.medical_patterns]:
            for pattern, replacement in patterns_dict.items():
                compiled = re.compile(pattern, re.IGNORECASE if pattern[0] != '\\b' or pattern[2].islower() else 0)
                self.all_patterns[compiled] = replacement
        
        # PPTX text fixer
        self.pptx_fixer = PPTXTextFixer()
    
    def clean(self, text: str, source_format: Optional[str] = None) -> str:
        """
        Apply all cleaning rules to the text.
        
        Args:
            text: Raw markdown text from document extraction
            source_format: Optional hint about source ('pptx', 'pdf', etc.)
                          Enables format-specific cleaning
        
        Returns:
            Cleaned markdown text
        """
        if not text:
            return text
        
        cleaned = text
        
        # PPTX-specific fixes (applied first for PPTX sources)
        if source_format and source_format.lower() in ['pptx', 'ppt']:
            cleaned = self.pptx_fixer.fix_run_on_words(cleaned)
        
        # Apply pattern replacements (ligatures, hyphens, medical terms)
        for pattern, replacement in self.all_patterns.items():
            cleaned = pattern.sub(replacement, cleaned)
        
        # Fix spacing issues
        cleaned = self._fix_spacing(cleaned)
        
        # Fix special characters
        cleaned = self._fix_special_chars(cleaned)
        
        # Fix common sentence breaks
        cleaned = self._fix_sentence_breaks(cleaned)
        
        return cleaned
    
    def _fix_spacing(self, text: str) -> str:
        """Fix common spacing issues"""
        # Multiple spaces to single space (but preserve double spaces after periods)
        text = re.sub(r'(?<!\.)  +', ' ', text)
        
        # Remove spaces before punctuation
        text = re.sub(r'\s+([.,;:!?)])', r'\1', text)
        
        # Add space after punctuation if missing
        text = re.sub(r'([.,;:!?)])([A-Z])', r'\1 \2', text)
        
        # Fix multiple newlines (max 2)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove trailing whitespace from lines
        text = '\n'.join(line.rstrip() for line in text.split('\n'))
        
        return text
    
    def _fix_special_chars(self, text: str) -> str:
        """Ensure special characters are properly encoded"""
        replacements = {
            '±': '±',  # Plus-minus
            'μ': 'μ',  # Micro
            '≥': '≥',  # Greater than or equal
            '≤': '≤',  # Less than or equal
            '≠': '≠',  # Not equal
            '→': '→',  # Right arrow
            '←': '←',  # Left arrow
            '↑': '↑',  # Up arrow
            '↓': '↓',  # Down arrow
            '×': '×',  # Multiplication
            '÷': '÷',  # Division
            '°': '°',  # Degree
            'α': 'α',  # Alpha
            'β': 'β',  # Beta
            'γ': 'γ',  # Gamma
            'δ': 'δ',  # Delta
        }
        
        for original, replacement in replacements.items():
            text = text.replace(original, replacement)
        
        return text
    
    def _fix_sentence_breaks(self, text: str) -> str:
        """Fix broken sentences from PDF extraction"""
        # Fix sentences that are incorrectly broken across lines
        # Pattern: lowercase word at end of line followed by lowercase word at start of next line
        text = re.sub(r'([a-z,])\n([a-z])', r'\1 \2', text)
        
        return text
    
    def get_cleaning_report(self, original: str, cleaned: str, source_format: Optional[str] = None) -> dict:
        """
        Generate a report of cleaning operations performed.
        
        Args:
            original: Original text
            cleaned: Cleaned text
            source_format: Optional source format for format-specific stats
        
        Returns:
            Dictionary with statistics about cleaning operations
        """
        report = {
            'original_length': len(original),
            'cleaned_length': len(cleaned),
            'characters_changed': len(original) - len(cleaned),
            'encoding_fixes': self._count_pattern_matches(original, self.ligature_patterns),
            'hyphen_fixes': self._count_pattern_matches(original, self.hyphen_patterns),
            'medical_term_fixes': self._count_pattern_matches(original, self.medical_patterns),
        }
        
        # Add PPTX-specific statistics
        if source_format and source_format.lower() in ['pptx', 'ppt']:
            pptx_stats = self.pptx_fixer.get_repair_stats(original, cleaned)
            report.update({
                'pptx_token_delta': pptx_stats['token_delta'],
                'pptx_contraction_fixes': pptx_stats['contraction_fixes'],
                'pptx_run_on_fixes': pptx_stats['estimated_run_on_fixes']
            })
        
        return report
    
    def _count_pattern_matches(self, text: str, patterns: dict) -> int:
        """Count how many times patterns match in text"""
        count = 0
        for pattern in patterns.keys():
            count += len(re.findall(pattern, text, re.IGNORECASE))
        return count
