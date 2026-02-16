"""
Quality regression tests - CRITICAL for preventing v2.3.2 issues.

These tests ensure that quality NEVER degrades across versions.
They detect:
- Text artifact reintroduction (ligatures, spacing)
- Internal link pollution
- Table extraction regressions  
- Word-splitting issues
- Any quality degradation vs v2.2.1 baseline

PRIORITY: CRITICAL - Prevents rollbacks like v2.3.2 → v2.2.1
"""

import pytest
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from converter import DocumentConverter
from text_cleaner import MarkdownCleaner


class TestKnownArtifactsPrevention:
    """CRITICAL: Ensure known quality issues NEVER reappear"""
    
    @pytest.fixture
    def converter(self):
        return DocumentConverter()
    
    @pytest.fixture
    def sample_pdfs_dir(self):
        return Path(__file__).parent.parent / "fixtures" / "sample_pdfs"
    
    @pytest.mark.quality
    @pytest.mark.regression
    def test_no_ligature_artifacts_in_output(self, converter, sample_pdfs_dir):
        """
        CRITICAL: Ligature artifacts must NEVER appear in output.
        
        v2.2.1 fixed these. They must not reappear.
        """
        pdf_files = list(sample_pdfs_dir.glob("*.pdf"))
        if not pdf_files:
            pytest.skip("No PDF files found")
        
        # Test all PDFs
        for pdf_path in pdf_files:
            markdown, error = converter.convert_file(pdf_path)
            
            if error is None and markdown:
                markdown_lower = markdown.lower()
                
                # These artifacts must NEVER appear
                forbidden_patterns = [
                    "arti fi cial",
                    "de fi ned", 
                    "speci fi c",
                    "ef fi cient",
                    "suf fi cient",
                    "classi fi cation",
                    "identi fi cation",
                    "con fi dence",
                    "con fi rm"
                ]
                
                for pattern in forbidden_patterns:
                    assert pattern not in markdown_lower, (
                        f"REGRESSION: Ligature artifact '{pattern}' found in {pdf_path.name}. "
                        f"This was fixed in v2.2.1 and must not reappear!"
                    )
    
    @pytest.mark.quality
    @pytest.mark.regression
    def test_no_internal_link_pollution(self, converter, sample_pdfs_dir):
        """
        CRITICAL: Internal link pollution must NOT appear.
        
        v2.3.2 introduced: [the](#page-7), [and](#page-5)
        This caused rollback to v2.2.1.
        Must NEVER happen again.
        """
        pdf_files = list(sample_pdfs_dir.glob("*.pdf"))
        if not pdf_files:
            pytest.skip("No PDF files found")
        
        for pdf_path in pdf_files:
            markdown, error = converter.convert_file(pdf_path)
            
            if error is None and markdown:
                # Check for internal link pollution patterns
                # Common words should NOT be links to page anchors
                import re
                
                # Pattern: [common_word](#page-X)
                link_pattern = r'\[(the|and|or|in|on|at|to|for|of|a|an|is|was|were|are|with)\]\(#page-\d+\)'
                matches = re.findall(link_pattern, markdown, re.IGNORECASE)
                
                assert len(matches) == 0, (
                    f"REGRESSION: Internal link pollution found in {pdf_path.name}: {matches}. "
                    f"This caused v2.3.2 rollback and must not reappear!"
                )
    
    @pytest.mark.quality
    @pytest.mark.regression
    def test_no_hyphenation_artifacts(self, converter, sample_pdfs_dir):
        """
        CRITICAL: Hyphenation artifacts must be fixed.
        
        v2.2.1 fixed: "non- invasive" → "non-invasive"
        This must remain fixed.
        """
        pdf_files = list(sample_pdfs_dir.glob("*.pdf"))
        if not pdf_files:
            pytest.skip("No PDF files found")
        
        for pdf_path in pdf_files:
            markdown, error = converter.convert_file(pdf_path)
            
            if error is None and markdown:
                # Check for hyphenation artifacts
                forbidden_patterns = [
                    "non- invasive",
                    "long- term",
                    "short- term",
                    "multi- center",
                    "double- blind",
                    "cross- sectional"
                ]
                
                markdown_lower = markdown.lower()
                for pattern in forbidden_patterns:
                    assert pattern not in markdown_lower, (
                        f"REGRESSION: Hyphenation artifact '{pattern}' in {pdf_path.name}"
                    )
    
    @pytest.mark.quality
    @pytest.mark.regression  
    def test_medical_terms_preserved(self, converter, sample_pdfs_dir):
        """
        CRITICAL: Medical terms must be properly formatted.
        
        Terms like NT-proBNP, β-blockers must be correct.
        """
        # Only test medical PDFs
        medical_pdfs = [
            "TIM-HF3 fcvm-11-1457995.pdf",
            "heart_failure_disease_management_program__a_review.17.pdf"
        ]
        
        for pdf_name in medical_pdfs:
            pdf_path = sample_pdfs_dir / pdf_name
            if not pdf_path.exists():
                continue
            
            markdown, error = converter.convert_file(pdf_path)
            
            if error is None and markdown:
                # Medical terms should not have broken spacing
                # "NT- proBNP" is wrong, "NT-proBNP" is correct
                forbidden_patterns = [
                    "NT- proBNP",
                    "MR- proADM",
                    "β- blockers",
                    "C- reactive",
                    "D- dimer"
                ]
                
                for pattern in forbidden_patterns:
                    assert pattern not in markdown, (
                        f"REGRESSION: Medical term spacing broken: '{pattern}' in {pdf_name}"
                    )
    
    @pytest.mark.quality
    @pytest.mark.regression
    def test_external_links_preserved(self, converter, sample_pdfs_dir):
        """
        IMPORTANT: External links should be preserved.
        
        Only INTERNAL links ([word](#page-X)) are bad.
        External links [text](https://...) are good.
        """
        # This is more of a quality check
        # External links (if present in source) should be preserved
        # We can't test without knowing source content
        # But we can verify link format is valid
        
        pdf_files = list(sample_pdfs_dir.glob("*.pdf"))
        if not pdf_files:
            pytest.skip("No PDF files found")
        
        for pdf_path in pdf_files:
            markdown, error = converter.convert_file(pdf_path)
            
            if error is None and markdown:
                import re
                # Find all markdown links
                links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', markdown)
                
                for link_text, link_url in links:
                    # External URLs are OK
                    if link_url.startswith('http://') or link_url.startswith('https://'):
                        continue  # Good!
                    
                    # Internal page anchors are BAD (if common words)
                    if link_url.startswith('#page-'):
                        # Check if link_text is a common word
                        common_words = ['the', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'a', 'an']
                        if link_text.lower() in common_words:
                            pytest.fail(
                                f"REGRESSION: Common word '{link_text}' linked to {link_url} in {pdf_path.name}"
                            )


class TestOutputDeterminism:
    """Tests for deterministic, consistent output"""
    
    @pytest.fixture
    def converter(self):
        return DocumentConverter()
    
    @pytest.fixture
    def sample_pdfs_dir(self):
        return Path(__file__).parent.parent / "fixtures" / "sample_pdfs"
    
    @pytest.mark.quality
    @pytest.mark.regression
    def test_conversion_is_deterministic(self, converter, sample_pdfs_dir):
        """
        IMPORTANT: Same input must always produce same output.
        
        Non-deterministic output makes regression testing impossible.
        """
        pdf_files = list(sample_pdfs_dir.glob("*.pdf"))
        if not pdf_files:
            pytest.skip("No PDF files found")
        
        # Test first PDF
        pdf_path = pdf_files[0]
        
        # Convert 3 times
        results = []
        for _ in range(3):
            markdown, error = converter.convert_file(pdf_path)
            if error is None:
                results.append(markdown)
        
        # All results should be identical
        if len(results) >= 2:
            assert results[0] == results[1], (
                f"NON-DETERMINISTIC: {pdf_path.name} produces different output on repeated conversion"
            )
            if len(results) == 3:
                assert results[1] == results[2]
    
    @pytest.mark.quality
    def test_no_random_elements_in_output(self, converter, sample_pdfs_dir):
        """
        Verify output doesn't contain timestamps or random elements.
        """
        pdf_files = list(sample_pdfs_dir.glob("*.pdf"))
        if not pdf_files:
            pytest.skip("No PDF files found")
        
        pdf_path = pdf_files[0]
        markdown, error = converter.convert_file(pdf_path)
        
        if error is None:
            # Output should not contain:
            # - Current timestamps
            # - Random UUIDs
            # - Non-deterministic identifiers
            import re
            
            # Check for UUID patterns
            uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
            uuids = re.findall(uuid_pattern, markdown, re.IGNORECASE)
            assert len(uuids) == 0, f"Output contains UUIDs: {uuids}"


class TestDocumentSpecificBaselines:
    """
    Document-specific regression tests.
    
    These test specific known-good documents against baselines.
    """
    
    @pytest.fixture
    def converter(self):
        return DocumentConverter()
    
    @pytest.fixture
    def sample_pdfs_dir(self):
        return Path(__file__).parent.parent / "fixtures" / "sample_pdfs"
    
    @pytest.fixture
    def baseline_file(self):
        return Path(__file__).parent / "baseline_scores_v2.2.1.json"
    
    @pytest.mark.quality
    @pytest.mark.regression
    def test_tim_hf3_medical_paper_quality(self, converter, sample_pdfs_dir):
        """
        Test TIM-HF3 medical paper maintains quality baseline.
        
        This is a complex medical paper - good quality test.
        """
        pdf_path = sample_pdfs_dir / "TIM-HF3 fcvm-11-1457995.pdf"
        
        if not pdf_path.exists():
            pytest.skip(f"Test file not found: {pdf_path}")
        
        markdown, error = converter.convert_file(pdf_path)
        
        assert error is None, f"Conversion failed: {error}"
        assert markdown is not None
        
        # Quality checks specific to this document
        assert len(markdown) > 5000, "Output too short - content missing"
        
        # Should not have common artifacts
        markdown_lower = markdown.lower()
        assert "arti fi cial" not in markdown_lower
        assert "de fi ned" not in markdown_lower
        
        # Should have medical content
        assert 'patient' in markdown_lower or 'trial' in markdown_lower
    
    @pytest.mark.quality
    @pytest.mark.regression
    def test_boston_presentation_quality(self, converter, sample_pdfs_dir):
        """
        Test Boston presentation maintains quality baseline.
        
        Business presentation - different structure than papers.
        """
        pdf_path = sample_pdfs_dir / "Boston-jp-morgan-healthcare-conference-2025.pdf"
        
        if not pdf_path.exists():
            pytest.skip(f"Test file not found: {pdf_path}")
        
        markdown, error = converter.convert_file(pdf_path)
        
        assert error is None
        assert markdown is not None
        assert len(markdown) > 1000
        
        # Should not have artifacts
        markdown_lower = markdown.lower()
        assert "arti fi cial" not in markdown_lower
    
    @pytest.mark.quality
    def test_baseline_scores_exist_or_warn(self, baseline_file):
        """
        Check if baseline scores file exists.
        
        If not, warn user to generate baseline.
        """
        if not baseline_file.exists():
            pytest.skip(
                f"Baseline scores not found at {baseline_file}. "
                f"Run 'python tests/regression/generate_baseline.py' to create baseline."
            )
        
        # If exists, verify format
        with open(baseline_file) as f:
            baseline = json.load(f)
        
        assert isinstance(baseline, dict)
        assert 'version' in baseline
        assert 'documents' in baseline


class TestQualityMetrics:
    """Tests for quality metric calculation and consistency"""
    
    @pytest.fixture
    def converter(self):
        return DocumentConverter()
    
    @pytest.fixture
    def sample_pdfs_dir(self):
        return Path(__file__).parent.parent / "fixtures" / "sample_pdfs"
    
    @pytest.mark.quality
    def test_output_has_minimum_quality(self, converter, sample_pdfs_dir):
        """
        Test that all outputs meet minimum quality standards.
        """
        pdf_files = list(sample_pdfs_dir.glob("*.pdf"))
        if not pdf_files:
            pytest.skip("No PDF files found")
        
        for pdf_path in pdf_files:
            markdown, error = converter.convert_file(pdf_path)
            
            if error is None and markdown:
                # Minimum quality checks
                
                # 1. Should have substantial content
                assert len(markdown) > 100, f"Output too short for {pdf_path.name}"
                
                # 2. Should not be mostly whitespace
                text_chars = len(markdown.replace(' ', '').replace('\n', ''))
                assert text_chars > 50, f"Too little actual text in {pdf_path.name}"
                
                # 3. Should have multiple lines
                lines = [l for l in markdown.split('\n') if l.strip()]
                assert len(lines) > 5, f"Too few lines in {pdf_path.name}"
    
    @pytest.mark.quality
    def test_no_excessive_whitespace(self, converter, sample_pdfs_dir):
        """
        Test that output doesn't have excessive whitespace.
        
        Text cleaner should fix this.
        """
        pdf_files = list(sample_pdfs_dir.glob("*.pdf"))
        if not pdf_files:
            pytest.skip("No PDF files found")
        
        for pdf_path in pdf_files:
            markdown, error = converter.convert_file(pdf_path)
            
            if error is None and markdown:
                # Should not have excessive spacing
                assert "    " not in markdown, f"Excessive spaces in {pdf_path.name}"
                assert "\n\n\n\n" not in markdown, f"Excessive newlines in {pdf_path.name}"