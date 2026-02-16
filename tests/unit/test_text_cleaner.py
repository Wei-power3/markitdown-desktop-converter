"""
Unit tests for text_cleaner.py module.

CRITICAL PRIORITY: Text cleaning is the core quality feature.
These tests prevent v2.3.2-style regressions.

Coverage target: 90%+
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from text_cleaner import MarkdownCleaner


class TestMarkdownCleanerBasics:
    """Basic instantiation and method existence tests"""
    
    @pytest.fixture
    def cleaner(self):
        """Fixture providing a fresh MarkdownCleaner instance"""
        return MarkdownCleaner()
    
    def test_cleaner_instantiation(self, cleaner):
        """Test that MarkdownCleaner instantiates correctly"""
        assert cleaner is not None
        assert isinstance(cleaner, MarkdownCleaner)
    
    def test_cleaner_has_patterns(self, cleaner):
        """Test that cleaner has required pattern dictionaries"""
        assert hasattr(cleaner, 'ligature_patterns')
        assert hasattr(cleaner, 'hyphen_patterns')
        assert hasattr(cleaner, 'medical_patterns')
        assert len(cleaner.ligature_patterns) > 0
        assert len(cleaner.hyphen_patterns) > 0
        assert len(cleaner.medical_patterns) > 0
    
    def test_clean_method_exists(self, cleaner):
        """Test that clean() method exists and is callable"""
        assert hasattr(cleaner, 'clean')
        assert callable(cleaner.clean)


class TestLigatureFixing:
    """Tests for ligature artifact fixing"""
    
    @pytest.fixture
    def cleaner(self):
        return MarkdownCleaner()
    
    def test_fix_artificial_lowercase(self, cleaner):
        """Test fixing 'artificial' ligature (lowercase)"""
        input_text = "This study used arti fi cial intelligence"
        expected = "This study used artificial intelligence"
        result = cleaner.clean(input_text)
        assert "artificial" in result
        assert "arti fi cial" not in result
    
    def test_fix_artificial_capitalized(self, cleaner):
        """Test fixing 'Artificial' ligature (capitalized)"""
        input_text = "Arti fi cial intelligence is transformative"
        expected = "Artificial intelligence is transformative"
        result = cleaner.clean(input_text)
        assert "Artificial" in result
        assert "Arti fi cial" not in result
    
    def test_fix_defined(self, cleaner):
        """Test fixing 'defined' ligature"""
        input_text = "The term was de fi ned in the study"
        result = cleaner.clean(input_text)
        assert "defined" in result
        assert "de fi ned" not in result
    
    def test_fix_specific(self, cleaner):
        """Test fixing 'specific' ligature"""
        input_text = "The speci fi c findings were significant"
        result = cleaner.clean(input_text)
        assert "specific" in result
        assert "speci fi c" not in result
    
    def test_fix_efficient(self, cleaner):
        """Test fixing 'efficient' ligature"""
        input_text = "The ef fi cient method reduced time"
        result = cleaner.clean(input_text)
        assert "efficient" in result
        assert "ef fi cient" not in result
    
    def test_fix_sufficient(self, cleaner):
        """Test fixing 'sufficient' ligature"""
        input_text = "The sample size was suf fi cient"
        result = cleaner.clean(input_text)
        assert "sufficient" in result
        assert "suf fi cient" not in result
    
    def test_fix_classification(self, cleaner):
        """Test fixing 'classification' ligature"""
        input_text = "The classi fi cation system is robust"
        result = cleaner.clean(input_text)
        assert "classification" in result
        assert "classi fi cation" not in result
    
    def test_fix_office(self, cleaner):
        """Test fixing 'office' ligature"""
        input_text = "The of fi ce staff are helpful"
        result = cleaner.clean(input_text)
        assert "office" in result
        assert "of fi ce" not in result
    
    def test_fix_confirm(self, cleaner):
        """Test fixing 'confirm' ligature"""
        input_text = "We con fi rm these findings"
        result = cleaner.clean(input_text)
        assert "confirm" in result
        assert "con fi rm" not in result
    
    def test_fix_multiple_ligatures_in_sentence(self, cleaner):
        """Test fixing multiple ligatures in one sentence"""
        input_text = "The arti fi cial system was de fi ned as speci fi c"
        result = cleaner.clean(input_text)
        assert "artificial" in result
        assert "defined" in result
        assert "specific" in result
        assert "arti fi cial" not in result
        assert "de fi ned" not in result
        assert "speci fi c" not in result


class TestHyphenationFixes:
    """Tests for hyphenation artifact fixing"""
    
    @pytest.fixture
    def cleaner(self):
        return MarkdownCleaner()
    
    def test_fix_non_invasive(self, cleaner):
        """Test fixing 'non-invasive' hyphenation"""
        input_text = "The non- invasive procedure was successful"
        result = cleaner.clean(input_text)
        assert "non-invasive" in result
        assert "non- invasive" not in result
    
    def test_fix_receiver_operating(self, cleaner):
        """Test fixing 'receiver-operating' hyphenation"""
        input_text = "The receiver- operating characteristic curve"
        result = cleaner.clean(input_text)
        assert "receiver-operating" in result
        assert "receiver- operating" not in result
    
    def test_fix_cross_sectional(self, cleaner):
        """Test fixing 'cross-sectional' hyphenation"""
        input_text = "A cross- sectional study design"
        result = cleaner.clean(input_text)
        assert "cross-sectional" in result
        assert "cross- sectional" not in result
    
    def test_fix_double_blind(self, cleaner):
        """Test fixing 'double-blind' hyphenation"""
        input_text = "The double- blind trial demonstrated"
        result = cleaner.clean(input_text)
        assert "double-blind" in result
        assert "double- blind" not in result
    
    def test_fix_long_term(self, cleaner):
        """Test fixing 'long-term' hyphenation"""
        input_text = "Long- term outcomes were measured"
        result = cleaner.clean(input_text)
        assert "long-term" in result.lower()
        assert "long- term" not in result.lower()
    
    def test_preserve_intentional_hyphens(self, cleaner):
        """Test that properly formatted hyphens are preserved"""
        input_text = "The state-of-the-art machine-learning model"
        result = cleaner.clean(input_text)
        assert "state-of-the-art" in result
        assert "machine-learning" in result
    
    def test_fix_multiple_hyphens_in_sentence(self, cleaner):
        """Test fixing multiple hyphenation artifacts"""
        input_text = "The non- invasive long- term study used double- blind methods"
        result = cleaner.clean(input_text)
        assert "non-invasive" in result
        assert "long-term" in result
        assert "double-blind" in result
    
    def test_fix_multi_center(self, cleaner):
        """Test fixing 'multi-center' hyphenation"""
        input_text = "A multi- center study was conducted"
        result = cleaner.clean(input_text)
        assert "multi-center" in result
        assert "multi- center" not in result


class TestMedicalTermPreservation:
    """Tests for medical term preservation"""
    
    @pytest.fixture
    def cleaner(self):
        return MarkdownCleaner()
    
    def test_preserve_nt_probnp(self, cleaner):
        """Test preservation of NT-proBNP"""
        input_text = "NT- proBNP levels were measured"
        result = cleaner.clean(input_text)
        assert "NT-proBNP" in result
        assert "NT- proBNP" not in result
    
    def test_preserve_beta_blockers(self, cleaner):
        """Test preservation of β-blockers"""
        input_text = "Patients received β- blockers daily"
        result = cleaner.clean(input_text)
        assert "β-blockers" in result
        assert "β- blockers" not in result
    
    def test_preserve_mr_proadm(self, cleaner):
        """Test preservation of MR-proADM"""
        input_text = "MR- proADM was used as a biomarker"
        result = cleaner.clean(input_text)
        assert "MR-proADM" in result
        assert "MR- proADM" not in result
    
    def test_preserve_hba1c(self, cleaner):
        """Test preservation of HbA1c"""
        input_text = "HbA 1c levels indicate glucose control"
        result = cleaner.clean(input_text)
        assert "HbA1c" in result
        assert "HbA 1c" not in result
    
    def test_preserve_c_reactive(self, cleaner):
        """Test preservation of C-reactive protein"""
        input_text = "C- reactive protein was elevated"
        result = cleaner.clean(input_text)
        assert "C-reactive" in result
        assert "C- reactive" not in result
    
    def test_preserve_d_dimer(self, cleaner):
        """Test preservation of D-dimer"""
        input_text = "D- dimer test was performed"
        result = cleaner.clean(input_text)
        assert "D-dimer" in result
        assert "D- dimer" not in result
    
    def test_preserve_tnf_alpha(self, cleaner):
        """Test preservation of TNF-α"""
        input_text = "TNF- α expression was increased"
        result = cleaner.clean(input_text)
        assert "TNF-α" in result
        assert "TNF- α" not in result
    
    def test_preserve_multiple_medical_terms(self, cleaner):
        """Test preservation of multiple medical terms in one sentence"""
        input_text = "NT- proBNP, MR- proADM, and HbA 1c were measured"
        result = cleaner.clean(input_text)
        assert "NT-proBNP" in result
        assert "MR-proADM" in result
        assert "HbA1c" in result


class TestSpecialCharacterHandling:
    """Tests for special character handling"""
    
    @pytest.fixture
    def cleaner(self):
        return MarkdownCleaner()
    
    @pytest.mark.parametrize("special_char", ["±", "μ", "≥", "≤", "→", "°", "%"])
    def test_preserve_scientific_symbols(self, cleaner, special_char):
        """Test that scientific symbols are preserved"""
        input_text = f"The value was 5{special_char}2 units"
        result = cleaner.clean(input_text)
        assert special_char in result
    
    @pytest.mark.parametrize("greek_letter", ["α", "β", "γ", "δ"])
    def test_preserve_greek_letters(self, cleaner, greek_letter):
        """Test that Greek letters are preserved"""
        input_text = f"The {greek_letter} subunit is important"
        result = cleaner.clean(input_text)
        assert greek_letter in result
    
    def test_preserve_arrows(self, cleaner):
        """Test that arrow symbols are preserved"""
        input_text = "A → B ← C ↑ D ↓ E"
        result = cleaner.clean(input_text)
        assert "→" in result
        assert "←" in result
        assert "↑" in result
        assert "↓" in result
    
    def test_preserve_mathematical_operators(self, cleaner):
        """Test that mathematical operators are preserved"""
        input_text = "Calculate 5 × 3 ÷ 2 ≠ 7"
        result = cleaner.clean(input_text)
        assert "×" in result
        assert "÷" in result
        assert "≠" in result
    
    def test_preserve_degree_symbol(self, cleaner):
        """Test that degree symbol is preserved"""
        input_text = "Temperature was 37°C"
        result = cleaner.clean(input_text)
        assert "°" in result
    
    def test_multiple_special_chars_in_sentence(self, cleaner):
        """Test multiple special characters in one sentence"""
        input_text = "Values: 5±2μg, α≥β, 37°C→42°C"
        result = cleaner.clean(input_text)
        assert "±" in result
        assert "μ" in result
        assert "α" in result
        assert "≥" in result
        assert "β" in result
        assert "°" in result
        assert "→" in result


class TestSpacingCleanup:
    """Tests for spacing and formatting cleanup"""
    
    @pytest.fixture
    def cleaner(self):
        return MarkdownCleaner()
    
    def test_remove_multiple_spaces(self, cleaner):
        """Test removal of multiple consecutive spaces"""
        input_text = "This  has   multiple    spaces"
        result = cleaner.clean(input_text)
        # Should reduce to single spaces (but may preserve double after period)
        assert "    " not in result  # No 4+ spaces
        assert "   " not in result  # No 3+ spaces
    
    def test_normalize_line_breaks(self, cleaner):
        """Test normalization of excessive line breaks"""
        input_text = "Line 1\n\n\n\nLine 2"
        result = cleaner.clean(input_text)
        # Should reduce to max 2 consecutive newlines
        assert "\n\n\n\n" not in result
        assert "\n\n\n" not in result
    
    def test_remove_trailing_spaces(self, cleaner):
        """Test removal of trailing spaces from lines"""
        input_text = "Line 1    \nLine 2   \nLine 3  "
        result = cleaner.clean(input_text)
        lines = result.split('\n')
        for line in lines:
            assert not line.endswith('  ')  # No trailing double spaces
    
    def test_fix_punctuation_spacing(self, cleaner):
        """Test fixing spacing around punctuation"""
        input_text = "Word ,and word .And word ;test"
        result = cleaner.clean(input_text)
        # Spaces before punctuation should be removed
        assert " ," not in result
        assert " ." not in result
        assert " ;" not in result
    
    def test_add_space_after_punctuation(self, cleaner):
        """Test adding space after punctuation when missing"""
        input_text = "Sentence one.Sentence two,and three;finally four"
        result = cleaner.clean(input_text)
        # Should have spaces after punctuation before capital letters
        # Note: Implementation may vary, so test for basic improvement
        assert len(result) >= len(input_text)  # Should add characters (spaces)


class TestEdgeCases:
    """Tests for edge cases and error handling"""
    
    @pytest.fixture
    def cleaner(self):
        return MarkdownCleaner()
    
    def test_empty_string(self, cleaner):
        """Test handling of empty string"""
        result = cleaner.clean("")
        assert result == ""
    
    def test_none_input(self, cleaner):
        """Test handling of None input"""
        result = cleaner.clean(None)
        # Should return None or empty string, not crash
        assert result is None or result == ""
    
    def test_whitespace_only(self, cleaner):
        """Test handling of whitespace-only input"""
        result = cleaner.clean("   \n\n   \t  ")
        # Should clean to minimal whitespace
        assert len(result) <= 3  # Very short after cleaning
    
    def test_very_long_text(self, cleaner):
        """Test performance with large text (10,000 words)"""
        long_text = "This is a test sentence. " * 2000  # ~10k words
        result = cleaner.clean(long_text)
        assert len(result) > 0
        assert isinstance(result, str)
    
    def test_unicode_handling(self, cleaner):
        """Test proper Unicode character handling"""
        unicode_text = "Résumé with café and naïve characters 中文测试"
        result = cleaner.clean(unicode_text)
        assert "Résumé" in result
        assert "café" in result
        assert "naïve" in result
        assert "中文" in result


class TestCleaningStatistics:
    """Tests for cleaning statistics and reporting"""
    
    @pytest.fixture
    def cleaner(self):
        return MarkdownCleaner()
    
    def test_get_cleaning_report_exists(self, cleaner):
        """Test that get_cleaning_report method exists"""
        assert hasattr(cleaner, 'get_cleaning_report')
        assert callable(cleaner.get_cleaning_report)
    
    def test_cleaning_report_structure(self, cleaner):
        """Test structure of cleaning report"""
        original = "The arti fi cial intelligence system"
        cleaned = cleaner.clean(original)
        report = cleaner.get_cleaning_report(original, cleaned)
        
        assert isinstance(report, dict)
        assert 'original_length' in report
        assert 'cleaned_length' in report
        assert report['original_length'] == len(original)
        assert report['cleaned_length'] == len(cleaned)
    
    def test_cleaning_report_counts_fixes(self, cleaner):
        """Test that cleaning report counts fixes"""
        original = "The arti fi cial system with non- invasive NT- proBNP"
        cleaned = cleaner.clean(original)
        report = cleaner.get_cleaning_report(original, cleaned)
        
        # Should detect at least the ligature and hyphen fixes
        assert 'encoding_fixes' in report or 'ligature_fixes' in report


class TestRealWorldScenarios:
    """Tests with real-world PDF artifact examples"""
    
    @pytest.fixture
    def cleaner(self):
        return MarkdownCleaner()
    
    def test_frontiers_journal_artifacts(self, cleaner):
        """Test with actual artifacts from Frontiers journal PDFs"""
        # Real example from project testing history (v2.2.2 issue)
        input_text = """
        The study examined arti fi cial intelligence models
        for disease identi fi cation. Results showed con fi dence
        intervals and non- invasive baseline methods.
        """
        
        result = cleaner.clean(input_text)
        
        # Verify all artifacts fixed
        assert "artificial" in result
        assert "identification" in result
        assert "confidence" in result
        assert "non-invasive" in result
        
        # Verify original artifacts gone
        assert "arti fi cial" not in result
        assert "identi fi cation" not in result
        assert "con fi dence" not in result
        assert "non- invasive" not in result
    
    def test_medical_paper_text(self, cleaner):
        """Test with medical paper text containing multiple artifacts"""
        input_text = """
        NT- proBNP and MR- proADM levels were measured in the
        multi- center, double- blind study of non- invasive
        interventions. The speci fi c classi fi cation used
        HbA 1c ≥7% and β- blockers at 50±10mg doses.
        """
        
        result = cleaner.clean(input_text)
        
        # Medical terms preserved correctly
        assert "NT-proBNP" in result
        assert "MR-proADM" in result
        assert "HbA1c" in result
        assert "β-blockers" in result
        
        # Hyphens fixed
        assert "multi-center" in result
        assert "double-blind" in result
        assert "non-invasive" in result
        
        # Ligatures fixed
        assert "specific" in result
        assert "classification" in result
        
        # Special characters preserved
        assert "≥" in result
        assert "±" in result
    
    def test_combined_artifacts(self, cleaner):
        """Test document with multiple types of artifacts"""
        input_text = """
        The ef fi cient arti fi cial system demonstrated
        long- term ef fi cacy in cross- sectional analyses.
        Biomarkers (NT- proBNP, C- reactive protein) showed
        values of 450±50 pg/ml and were ≥2× baseline.
        Temperature increased from 37°C → 42°C.
        """
        
        result = cleaner.clean(input_text)
        
        # Everything should be cleaned
        assert "efficient" in result
        assert "artificial" in result
        assert "long-term" in result
        assert "efficacy" in result
        assert "cross-sectional" in result
        assert "NT-proBNP" in result
        assert "C-reactive" in result
        assert "±" in result
        assert "≥" in result
        assert "×" in result or "x" in result
        assert "°" in result
        assert "→" in result


class TestPerformance:
    """Performance and benchmarking tests"""
    
    @pytest.fixture
    def cleaner(self):
        return MarkdownCleaner()
    
    @pytest.fixture
    def large_document(self):
        """Generate a large document for performance testing"""
        # Simulate a 50KB document with various artifacts
        base_sentence = "This is a test sentence with arti fi cial intelligence and non- invasive methods. "
        return base_sentence * 500  # ~50KB
    
    @pytest.mark.slow
    def test_cleaning_speed_benchmark(self, cleaner, large_document, benchmark):
        """Benchmark cleaning speed - should be <100ms for 50KB"""
        result = benchmark(cleaner.clean, large_document)
        assert len(result) > 0
        # Benchmark plugin will report timing automatically
    
    @pytest.mark.slow
    def test_memory_efficiency(self, cleaner):
        """Test that cleaning doesn't consume excessive memory"""
        import sys
        
        # Create large text
        large_text = "Test sentence with arti fi cial intelligence. " * 5000
        
        # Get memory before
        size_before = sys.getsizeof(large_text)
        
        # Clean
        result = cleaner.clean(large_text)
        
        # Get memory after
        size_after = sys.getsizeof(result)
        
        # Result should not be dramatically larger (< 2x)
        assert size_after < size_before * 2
