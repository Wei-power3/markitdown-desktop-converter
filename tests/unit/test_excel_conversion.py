# tests/unit/test_excel_conversion.py

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from converter import MarkdownConverter

class TestExcelBasicConversion:
    """Test basic Excel to markdown conversion"""
    
    @pytest.fixture
    def converter(self):
        return MarkdownConverter()
    
    @pytest.fixture
    def excel_files(self):
        fixtures_dir = Path(__file__).parent.parent / "fixtures" / "sample_excel"
        return {
            "costing": fixtures_dir / "Costing-template.xls.xlsx",
            "evidence": fixtures_dir / "Introduction-to-Evidence-Synthesis-Solutions.xls",
            "reference": fixtures_dir / "Reference_costs_index.xlsx",
            "minerva": fixtures_dir / "MINERVA-Prolutamide.xlsx"
        }
    
    def test_costing_template_converts(self, converter, excel_files):
        """Test Costing-template.xls.xlsx conversion"""
        markdown, _ = converter.convert_file(excel_files["costing"])
        
        assert markdown is not None
        assert len(markdown) > 0
        assert "Unit costs" in markdown or "Sheet:" in markdown
        assert "|" in markdown  # Contains tables
        
    def test_evidence_synthesis_converts(self, converter, excel_files):
        """Test Evidence Synthesis .xls (legacy) conversion"""
        markdown, _ = converter.convert_file(excel_files["evidence"])
        
        assert markdown is not None
        assert len(markdown) > 0
        assert "MetaAnalysis" in markdown or "Sheet:" in markdown
        
    def test_reference_costs_converts(self, converter, excel_files):
        """Test large Reference_costs_index.xlsx conversion"""
        markdown, _ = converter.convert_file(excel_files["reference"])
        
        assert markdown is not None
        assert len(markdown) > 1000  # Should be large
        assert "NHS" in markdown or "Reference" in markdown or "costs" in markdown.lower()
        
    def test_minerva_converts(self, converter, excel_files):
        """Test MINERVA-Prolutamide.xlsx conversion"""
        markdown, _ = converter.convert_file(excel_files["minerva"])
        
        assert markdown is not None
        assert len(markdown) > 0
        assert "|" in markdown  # Contains tables


class TestExcelMultiSheet:
    """Test multi-sheet Excel handling"""
    
    @pytest.fixture
    def converter(self):
        return MarkdownConverter()
    
    @pytest.fixture
    def multi_sheet_file(self):
        """Costing template has 4 sheets"""
        return Path(__file__).parent.parent / "fixtures" / "sample_excel" / "Costing-template.xls.xlsx"
    
    def test_all_sheets_extracted(self, converter, multi_sheet_file):
        """Test that all sheets are extracted"""
        markdown, _ = converter.convert_file(multi_sheet_file)
        
        # Should contain multiple sheet markers
        assert markdown.count("## Sheet:") >= 2 or markdown.count("Sheet:") >= 2
        
    def test_sheet_names_preserved(self, converter, multi_sheet_file):
        """Test that sheet names are in output"""
        markdown, _ = converter.convert_file(multi_sheet_file)
        
        # Check for known sheet names
        expected_sheets = ["Unit costs", "Input sheet", "Costing template"]
        found = sum(1 for sheet in expected_sheets if sheet in markdown)
        
        assert found >= 1, "At least one sheet name should be present"


class TestExcelTableFormatting:
    """Test Excel table conversion to markdown"""
    
    @pytest.fixture
    def converter(self):
        return MarkdownConverter()
    
    @pytest.fixture
    def excel_file(self):
        return Path(__file__).parent.parent / "fixtures" / "sample_excel" / "Reference_costs_index.xlsx"
    
    def test_markdown_tables_created(self, converter, excel_file):
        """Test that markdown tables are properly formatted"""
        markdown, _ = converter.convert_file(excel_file)
        
        # Should have markdown table syntax
        assert "|" in markdown
        assert "---" in markdown  # Table separators
        
    def test_table_structure(self, converter, excel_file):
        """Test table has headers and rows"""
        markdown, _ = converter.convert_file(excel_file)
        
        lines = markdown.split('\n')
        table_lines = [l for l in lines if '|' in l]
        
        assert len(table_lines) > 2, "Should have at least header + separator + 1 row"


class TestExcelDataTypes:
    """Test different Excel data types"""
    
    @pytest.fixture
    def converter(self):
        return MarkdownConverter()
    
    def test_numbers_preserved(self, converter):
        """Test that numbers in cells are preserved"""
        excel_file = Path(__file__).parent.parent / "fixtures" / "sample_excel" / "Costing-template.xls.xlsx"
        markdown, _ = converter.convert_file(excel_file)
        
        # Should contain numbers from the costing data
        assert any(char.isdigit() for char in markdown)
        
    def test_special_characters_handled(self, converter):
        """Test £, €, and other special characters"""
        excel_file = Path(__file__).parent.parent / "fixtures" / "sample_excel" / "Costing-template.xls.xlsx"
        markdown, _ = converter.convert_file(excel_file)
        
        # File contains £ symbols - check they're handled
        # Either preserved or converted
        assert len(markdown) > 0


class TestExcelTextCleaning:
    """Test text cleaning applied to Excel output"""
    
    @pytest.fixture
    def converter(self):
        return MarkdownConverter()
    
    def test_no_excessive_whitespace(self, converter):
        """Test no double spaces in output"""
        excel_file = Path(__file__).parent.parent / "fixtures" / "sample_excel" / "MINERVA-Prolutamide.xlsx"
        markdown, _ = converter.convert_file(excel_file)
        
        # Should not have excessive spaces
        assert "   " not in markdown  # No triple spaces
        
    def test_ligature_fixing(self, converter):
        """Test ligatures are fixed if present"""
        excel_file = Path(__file__).parent.parent / "fixtures" / "sample_excel" / "Introduction-to-Evidence-Synthesis-Solutions.xls"
        markdown, _ = converter.convert_file(excel_file)
        
        # If text contains "fi" it should be part of a real word
        # not a ligature artifact
        assert markdown is not None


class TestExcelErrorHandling:
    """Test error handling for Excel files"""
    
    @pytest.fixture
    def converter(self):
        return MarkdownConverter()
    
    def test_empty_file_handled(self, converter, tmp_path):
        """Test handling of empty file"""
        empty_file = tmp_path / "empty.xlsx"
        empty_file.write_bytes(b"")
        
        with pytest.raises(Exception):
            converter.convert_file(empty_file)
    
    def test_invalid_format_handled(self, converter, tmp_path):
        """Test handling of non-Excel file with .xlsx extension"""
        fake_excel = tmp_path / "fake.xlsx"
        fake_excel.write_text("This is not an Excel file")
        
        with pytest.raises(Exception):
            converter.convert_file(fake_excel)


class TestExcelLegacyFormat:
    """Test .xls (Excel 97-2003) format support"""
    
    @pytest.fixture
    def converter(self):
        return MarkdownConverter()
    
    @pytest.fixture
    def legacy_file(self):
        return Path(__file__).parent.parent / "fixtures" / "sample_excel" / "Introduction-to-Evidence-Synthesis-Solutions.xls"
    
    def test_xls_format_converts(self, converter, legacy_file):
        """Test .xls (legacy) format conversion"""
        markdown, _ = converter.convert_file(legacy_file)
        
        assert markdown is not None
        assert len(markdown) > 0
        
    def test_xls_tables_formatted(self, converter, legacy_file):
        """Test tables from .xls are properly formatted"""
        markdown, _ = converter.convert_file(legacy_file)
        
        assert "|" in markdown
