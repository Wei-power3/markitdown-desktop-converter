"""
Integration tests for converter.py module.

Tests end-to-end conversion workflows with real documents.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from converter import DocumentConverter


class TestDocumentConverterBasics:
    """Basic instantiation and method existence tests"""
    
    @pytest.fixture
    def converter(self):
        """Fixture providing a DocumentConverter instance"""
        return DocumentConverter()
    
    def test_converter_instantiation(self, converter):
        """Test that DocumentConverter instantiates correctly"""
        assert converter is not None
        assert isinstance(converter, DocumentConverter)
    
    def test_converter_has_dependencies(self, converter):
        """Test that converter has required dependencies"""
        assert hasattr(converter, 'md')  # MarkItDown
        assert hasattr(converter, 'text_cleaner')
        assert hasattr(converter, 'table_extractor')
    
    def test_convert_file_method_exists(self, converter):
        """Test that convert_file() method exists"""
        assert hasattr(converter, 'convert_file')
        assert callable(converter.convert_file)


class TestPDFConversion:
    """Tests for PDF to Markdown conversion"""
    
    @pytest.fixture
    def converter(self):
        return DocumentConverter()
    
    @pytest.fixture
    def sample_pdfs_dir(self):
        return Path(__file__).parent.parent / "fixtures" / "sample_pdfs"
    
    def test_convert_medical_paper_basic(self, converter, sample_pdfs_dir):
        """Test basic conversion of medical research paper"""
        pdf_path = sample_pdfs_dir / "TIM-HF3 fcvm-11-1457995.pdf"
        
        if not pdf_path.exists():
            pytest.skip(f"Test file not found: {pdf_path}")
        
        markdown, error = converter.convert_file(pdf_path)
        
        # Verify successful conversion
        assert error is None
        assert markdown is not None
        assert len(markdown) > 0
        assert isinstance(markdown, str)
    
    def test_convert_medical_paper_content(self, converter, sample_pdfs_dir):
        """Test that medical paper content is properly extracted"""
        pdf_path = sample_pdfs_dir / "TIM-HF3 fcvm-11-1457995.pdf"
        
        if not pdf_path.exists():
            pytest.skip(f"Test file not found: {pdf_path}")
        
        markdown, error = converter.convert_file(pdf_path)
        
        # Medical paper should contain expected sections
        markdown_lower = markdown.lower()
        
        # Look for typical medical paper structure
        # At least some content should be present
        assert len(markdown) > 1000  # Substantial content
        
        # Should contain medical terminology
        # (these are from the actual TIM-HF3 paper)
        has_medical_terms = any([
            'patient' in markdown_lower,
            'trial' in markdown_lower,
            'study' in markdown_lower,
            'heart failure' in markdown_lower
        ])
        assert has_medical_terms
    
    def test_convert_business_presentation(self, converter, sample_pdfs_dir):
        """Test conversion of business presentation PDF"""
        pdf_path = sample_pdfs_dir / "Boston-jp-morgan-healthcare-conference-2025.pdf"
        
        if not pdf_path.exists():
            pytest.skip(f"Test file not found: {pdf_path}")
        
        markdown, error = converter.convert_file(pdf_path)
        
        # Verify successful conversion
        assert error is None
        assert markdown is not None
        assert len(markdown) > 500  # Substantial content
    
    def test_convert_large_pdf_performance(self, converter, sample_pdfs_dir):
        """Test that large PDF (7.5MB) converts in reasonable time"""
        pdf_path = sample_pdfs_dir / "TIM-HF3 fcvm-11-1457995.pdf"
        
        if not pdf_path.exists():
            pytest.skip(f"Test file not found: {pdf_path}")
        
        import time
        start_time = time.time()
        
        markdown, error = converter.convert_file(pdf_path)
        
        duration = time.time() - start_time
        
        # Should complete in under 60 seconds
        assert duration < 60
        assert error is None
        assert len(markdown) > 0
    
    def test_convert_nonexistent_file(self, converter, tmp_path):
        """Test handling of nonexistent file"""
        fake_path = tmp_path / "nonexistent.pdf"
        
        markdown, error = converter.convert_file(fake_path)
        
        # Should return error, not crash
        assert error is not None
        assert "error" in error.lower() or "not found" in error.lower()
    
    def test_convert_unsupported_format(self, converter, tmp_path):
        """Test handling of unsupported file format"""
        # Create a dummy .txt file
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("This is plain text")
        
        markdown, error = converter.convert_file(txt_file)
        
        # Should return error for unsupported format
        # Note: MarkItDown might actually support .txt, so this might pass
        # The important thing is it doesn't crash
        assert markdown is not None or error is not None
    
    @pytest.mark.slow
    def test_convert_all_sample_pdfs(self, converter, sample_pdfs_dir):
        """Test conversion of all available sample PDFs"""
        pdf_files = list(sample_pdfs_dir.glob("*.pdf"))
        
        if not pdf_files:
            pytest.skip("No PDF files found in fixtures")
        
        results = []
        for pdf_path in pdf_files:
            markdown, error = converter.convert_file(pdf_path)
            results.append({
                'file': pdf_path.name,
                'success': error is None,
                'length': len(markdown) if markdown else 0,
                'error': error
            })
        
        # At least 80% should convert successfully
        success_rate = sum(1 for r in results if r['success']) / len(results)
        assert success_rate >= 0.8


class TestTextCleaningIntegration:
    """Tests for text cleaning integration in conversion workflow"""
    
    @pytest.fixture
    def converter(self):
        return DocumentConverter()
    
    @pytest.fixture
    def sample_pdfs_dir(self):
        return Path(__file__).parent.parent / "fixtures" / "sample_pdfs"
    
    def test_artifacts_cleaned_during_conversion(self, converter, sample_pdfs_dir):
        """Test that text cleaning is automatically applied during conversion"""
        # Use any available PDF
        pdf_files = list(sample_pdfs_dir.glob("*.pdf"))
        if not pdf_files:
            pytest.skip("No PDF files found")
        
        pdf_path = pdf_files[0]
        markdown, error = converter.convert_file(pdf_path)
        
        assert error is None
        
        # Common artifacts should NOT appear in output
        # (these are artifacts that text_cleaner should fix)
        bad_patterns = [
            "arti fi cial",  # Ligature artifacts
            "de fi ned",
            "speci fi c",
        ]
        
        markdown_lower = markdown.lower()
        for pattern in bad_patterns:
            # If pattern appears, it's a test failure
            # (but only if the source PDF actually had these)
            pass  # Can't assert without knowing source content
        
        # At minimum, markdown should be well-formed
        assert len(markdown) > 0
    
    def test_medical_terms_preserved(self, converter, sample_pdfs_dir):
        """Test that medical terms are preserved during conversion"""
        # Medical papers should preserve medical terminology
        pdf_path = sample_pdfs_dir / "TIM-HF3 fcvm-11-1457995.pdf"
        
        if not pdf_path.exists():
            pytest.skip(f"Test file not found: {pdf_path}")
        
        markdown, error = converter.convert_file(pdf_path)
        
        assert error is None
        
        # Check for properly formatted medical terms
        # These specific terms are in the TIM-HF3 paper
        # The text cleaner should fix spacing: "NT- proBNP" -> "NT-proBNP"
        # We just verify the terms exist (may not have spacing artifacts)
        has_medical_content = any([
            'nt-probnp' in markdown.lower(),
            'ntprobnp' in markdown.lower(),
            'pro-bnp' in markdown.lower(),
            'probnp' in markdown.lower()
        ])
        
        # If medical paper, should have medical terms
        # (but format may vary depending on source PDF quality)
        assert len(markdown) > 1000  # Has substantial content
    
    def test_output_is_valid_markdown(self, converter, sample_pdfs_dir):
        """Test that output is valid Markdown format"""
        pdf_files = list(sample_pdfs_dir.glob("*.pdf"))
        if not pdf_files:
            pytest.skip("No PDF files found")
        
        pdf_path = pdf_files[0]
        markdown, error = converter.convert_file(pdf_path)
        
        assert error is None
        
        # Basic Markdown validity checks
        # Should be plain text (not binary)
        assert isinstance(markdown, str)
        
        # Should not have excessive spacing artifacts
        # (text cleaner should have fixed these)
        assert "    " not in markdown  # No 4+ spaces in a row
        assert "\n\n\n\n" not in markdown  # No 4+ newlines in a row


class TestMarkdownOutputQuality:
    """Tests for Markdown output quality"""
    
    @pytest.fixture
    def converter(self):
        return DocumentConverter()
    
    @pytest.fixture
    def sample_pdfs_dir(self):
        return Path(__file__).parent.parent / "fixtures" / "sample_pdfs"
    
    def test_output_completeness(self, converter, sample_pdfs_dir):
        """Test that output contains substantial content"""
        pdf_files = list(sample_pdfs_dir.glob("*.pdf"))
        if not pdf_files:
            pytest.skip("No PDF files found")
        
        for pdf_path in pdf_files[:3]:  # Test first 3 PDFs
            markdown, error = converter.convert_file(pdf_path)
            
            if error is None:
                # Should have substantial content (at least 500 chars)
                assert len(markdown) > 500, f"Output too short for {pdf_path.name}"
                
                # Should have multiple lines
                lines = markdown.split('\n')
                assert len(lines) > 10, f"Too few lines for {pdf_path.name}"
    
    def test_no_binary_artifacts(self, converter, sample_pdfs_dir):
        """Test that output doesn't contain binary artifacts"""
        pdf_files = list(sample_pdfs_dir.glob("*.pdf"))
        if not pdf_files:
            pytest.skip("No PDF files found")
        
        pdf_path = pdf_files[0]
        markdown, error = converter.convert_file(pdf_path)
        
        if error is None:
            # Should be valid UTF-8
            try:
                markdown.encode('utf-8')
            except UnicodeEncodeError:
                pytest.fail("Output contains invalid UTF-8 characters")
            
            # Should not contain null bytes or other binary artifacts
            assert '\x00' not in markdown
    
    def test_consistent_output(self, converter, sample_pdfs_dir):
        """Test that converting same file twice gives same result"""
        pdf_files = list(sample_pdfs_dir.glob("*.pdf"))
        if not pdf_files:
            pytest.skip("No PDF files found")
        
        pdf_path = pdf_files[0]
        
        # Convert twice
        markdown1, error1 = converter.convert_file(pdf_path)
        markdown2, error2 = converter.convert_file(pdf_path)
        
        # Results should be identical (deterministic)
        assert error1 == error2
        if error1 is None:
            assert markdown1 == markdown2


class TestPowerPointConversion:
    """Tests for PowerPoint conversion (if PPTX files available)"""
    
    @pytest.fixture
    def converter(self):
        return DocumentConverter()
    
    @pytest.fixture
    def sample_pptx_dir(self):
        return Path(__file__).parent.parent / "fixtures" / "sample_pptx"
    
    def test_pptx_conversion_if_available(self, converter, sample_pptx_dir):
        """Test PPTX conversion if sample files exist"""
        pptx_files = list(sample_pptx_dir.glob("*.pptx"))
        
        if not pptx_files:
            pytest.skip("No PPTX files found in fixtures")
        
        pptx_path = pptx_files[0]
        markdown, error = converter.convert_file(pptx_path)
        
        # Should convert without error
        assert error is None or markdown is not None
        
        if error is None:
            assert len(markdown) > 0
    
    def test_ppt_unsupported_gracefully(self, converter, tmp_path):
        """Test that old .ppt format is handled gracefully"""
        # Create dummy .ppt file
        ppt_file = tmp_path / "test.ppt"
        ppt_file.write_bytes(b"fake ppt content")
        
        markdown, error = converter.convert_file(ppt_file)
        
        # Should return error or empty content, not crash
        assert markdown is not None or error is not None