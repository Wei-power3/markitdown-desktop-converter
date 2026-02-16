# tests/integration/test_excel_workflow.py

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from converter import MarkdownConverter

class TestExcelEndToEnd:
    """End-to-end Excel conversion tests"""
    
    @pytest.fixture
    def converter(self):
        return MarkdownConverter()
    
    @pytest.fixture
    def excel_files(self):
        fixtures_dir = Path(__file__).parent.parent / "fixtures" / "sample_excel"
        return list(fixtures_dir.glob("*.xls*"))
    
    def test_all_fixtures_convert_successfully(self, converter, excel_files):
        """Test all 4 fixtures convert without errors"""
        results = []
        
        for excel_file in excel_files:
            try:
                markdown, _ = converter.convert_file(excel_file)
                results.append({
                    "file": excel_file.name,
                    "success": True,
                    "length": len(markdown)
                })
            except Exception as e:
                results.append({
                    "file": excel_file.name,
                    "success": False,
                    "error": str(e)
                })
        
        # All should succeed
        assert all(r["success"] for r in results), f"Some files failed: {results}"
        
        # All should have content
        assert all(r["length"] > 100 for r in results)
    
    def test_output_files_created(self, converter, excel_files, tmp_path):
        """Test markdown files are created with proper names"""
        for excel_file in excel_files:
            markdown, _ = converter.convert_file(excel_file)
            
            # Write output
            output_file = tmp_path / f"{excel_file.stem}.md"
            output_file.write_text(markdown)
            
            assert output_file.exists()
            assert output_file.stat().st_size > 100


class TestExcelBatchProcessing:
    """Test batch processing of multiple Excel files"""
    
    @pytest.fixture
    def converter(self):
        return MarkdownConverter()
    
    def test_mixed_xlsx_and_xls(self, converter, tmp_path):
        """Test batch processing of .xlsx and .xls together"""
        fixtures_dir = Path(__file__).parent.parent / "fixtures" / "sample_excel"
        files = [
            fixtures_dir / "Costing-template.xls.xlsx",
            fixtures_dir / "Introduction-to-Evidence-Synthesis-Solutions.xls",
            fixtures_dir / "MINERVA-Prolutamide.xlsx"
        ]
        
        results = []
        for f in files:
            if f.exists():
                markdown, _ = converter.convert_file(f)
                results.append(len(markdown))
        
        assert len(results) > 0
        assert all(length > 100 for length in results)


class TestExcelQuality:
    """Test quality of Excel output"""
    
    @pytest.fixture
    def converter(self):
        return MarkdownConverter()
    
    def test_large_file_quality(self, converter):
        """Test Reference_costs_index (large file) quality"""
        excel_file = Path(__file__).parent.parent / "fixtures" / "sample_excel" / "Reference_costs_index.xlsx"
        
        markdown, _ = converter.convert_file(excel_file)
        
        # Should be large output
        assert len(markdown) > 5000
        
        # Should have multiple tables
        assert markdown.count("|") > 100
        
    def test_complex_financial_model_quality(self, converter):
        """Test MINERVA (complex formulas) quality"""
        excel_file = Path(__file__).parent.parent / "fixtures" / "sample_excel" / "MINERVA-Prolutamide.xlsx"
        
        markdown, _ = converter.convert_file(excel_file)
        
        # Should preserve structure
        assert "Sheet:" in markdown or "##" in markdown
        
        # Should have tables
        assert "|" in markdown
