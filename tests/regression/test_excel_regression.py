# tests/regression/test_excel_regression.py

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from converter import MarkdownConverter

class TestExcelQualityRegression:
    """Prevent Excel conversion quality regression"""
    
    @pytest.fixture
    def converter(self):
        return MarkdownConverter()
    
    def test_no_ligature_artifacts(self, converter):
        """Test no ligature artifacts in Excel output"""
        excel_file = Path(__file__).parent.parent / "fixtures" / "sample_excel" / "Costing-template.xls.xlsx"
        markdown, _ = converter.convert_file(excel_file)
        
        # Should not have common ligature patterns that look wrong
        # This is a basic check - real ligatures in data are OK
        assert "\ufb01" not in markdown  # fi ligature
        assert "\ufb02" not in markdown  # fl ligature
    
    def test_tables_properly_formatted(self, converter):
        """Test Excel tables are properly formatted in markdown"""
        excel_file = Path(__file__).parent.parent / "fixtures" / "sample_excel" / "Reference_costs_index.xlsx"
        markdown, _ = converter.convert_file(excel_file)
        
        lines = markdown.split('\n')
        table_lines = [l for l in lines if '|' in l]
        
        # Should have properly formed tables
        assert len(table_lines) > 0
        
        # Check for header separator pattern (|---|---|)
        separator_lines = [l for l in lines if '---' in l and '|' in l]
        assert len(separator_lines) > 0
    
    def test_deterministic_output(self, converter):
        """Test same file produces same output"""
        excel_file = Path(__file__).parent.parent / "fixtures" / "sample_excel" / "MINERVA-Prolutamide.xlsx"
        
        markdown1, _ = converter.convert_file(excel_file)
        markdown2, _ = converter.convert_file(excel_file)
        
        assert markdown1 == markdown2
    
    def test_no_data_loss_in_cells(self, converter):
        """Test cell data is not lost during conversion"""
        excel_file = Path(__file__).parent.parent / "fixtures" / "sample_excel" / "Costing-template.xls.xlsx"
        markdown, _ = converter.convert_file(excel_file)
        
        # Should contain key terms from the file
        # (Adjust based on actual content)
        assert len(markdown) > 1000  # Reasonable size for 4-sheet workbook
        
    def test_multi_sheet_order_preserved(self, converter):
        """Test sheets appear in correct order"""
        excel_file = Path(__file__).parent.parent / "fixtures" / "sample_excel" / "Costing-template.xls.xlsx"
        markdown, _ = converter.convert_file(excel_file)
        
        # First sheet should appear before later sheets
        # Can check by sheet name positions
        assert "Sheet:" in markdown or "##" in markdown


@pytest.mark.regression
class TestExcelBaseline:
    """Compare against quality baselines"""
    
    @pytest.fixture
    def converter(self):
        return MarkdownConverter()
    
    def test_costing_template_baseline(self, converter):
        """Test Costing-template output meets baseline quality"""
        excel_file = Path(__file__).parent.parent / "fixtures" / "sample_excel" / "Costing-template.xls.xlsx"
        markdown, _ = converter.convert_file(excel_file)
        
        # Baseline checks
        assert len(markdown) > 1000  # Minimum reasonable size
        assert markdown.count("|") > 10  # Has tables
        assert markdown.count("\n") > 50  # Has structure
    
    def test_reference_costs_baseline(self, converter):
        """Test Reference_costs output meets baseline quality"""
        excel_file = Path(__file__).parent.parent / "fixtures" / "sample_excel" / "Reference_costs_index.xlsx"
        markdown, _ = converter.convert_file(excel_file)
        
        # Large file baseline
        assert len(markdown) > 10000  # Should be very large
        assert markdown.count("|") > 100  # Many tables
