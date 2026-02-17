"""
Unit tests for PPTX table extractor
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

try:
    from pptx_table_extractor import PPTXTableExtractor
    PPTX_AVAILABLE = True
except ImportError:
    PPTX_AVAILABLE = False


@pytest.mark.skipif(not PPTX_AVAILABLE, reason="python-pptx not available")
class TestPPTXTableExtractor:
    """Test suite for PPTX table extraction functionality"""
    
    @pytest.fixture
    def extractor(self):
        """Create a PPTXTableExtractor instance for testing"""
        return PPTXTableExtractor()
    
    def test_markdown_format_basic(self, extractor):
        """Test: Basic markdown table formatting"""
        test_data = [
            ["Header1", "Header2", "Header3"],
            ["Row1Col1", "Row1Col2", "Row1Col3"],
            ["Row2Col1", "Row2Col2", "Row2Col3"]
        ]
        
        markdown = extractor._format_as_markdown(test_data)
        
        # Check structure
        assert markdown.startswith("| Header1")
        assert "|------" in markdown or "|---" in markdown
        assert "| Row1Col1" in markdown
        
        # Check line count (header + separator + 2 data rows)
        lines = markdown.split('\n')
        assert len(lines) == 4, f"Expected 4 lines, got {len(lines)}"
    
    def test_markdown_format_with_empty_cells(self, extractor):
        """Test: Handles empty cells correctly"""
        test_data = [
            ["Header1", "Header2", "Header3"],
            ["Value1", "", "Value3"],
            ["", "Value2", ""]
        ]
        
        markdown = extractor._format_as_markdown(test_data)
        
        # Empty cells should be preserved with spacing
        lines = markdown.split('\n')
        assert len(lines) == 4
        
        # Check that pipes are balanced
        for line in lines:
            pipe_count = line.count('|')
            assert pipe_count == 4, f"Expected 4 pipes per line, got {pipe_count} in '{line}'"
    
    def test_markdown_format_single_row(self, extractor):
        """Test: Single row (header only) table"""
        test_data = [
            ["Header1", "Header2"]
        ]
        
        markdown = extractor._format_as_markdown(test_data)
        
        lines = markdown.split('\n')
        # Should have header + separator (no data rows)
        assert len(lines) == 2
        assert "Header1" in lines[0]
        assert "---" in lines[1]
    
    def test_markdown_format_wide_table(self, extractor):
        """Test: Table with many columns"""
        test_data = [
            ["C1", "C2", "C3", "C4", "C5", "C6"],
            ["A", "B", "C", "D", "E", "F"]
        ]
        
        markdown = extractor._format_as_markdown(test_data)
        
        # Check that all columns are present
        lines = markdown.split('\n')
        assert len(lines) == 3  # header + separator + 1 data row
        
        # Each line should have 7 pipes (6 columns + edges)
        for line in lines:
            assert line.count('|') == 7
    
    def test_markdown_format_alignment(self, extractor):
        """Test: Columns are properly aligned"""
        test_data = [
            ["Short", "Medium Length", "VeryLongHeaderName"],
            ["A", "B", "C"]
        ]
        
        markdown = extractor._format_as_markdown(test_data)
        lines = markdown.split('\n')
        
        # All lines should have similar lengths (within reason)
        lengths = [len(line) for line in lines]
        max_length = max(lengths)
        min_length = min(lengths)
        
        # Length difference should be small (just accounting for cell content)
        assert max_length - min_length < 30, "Lines should be relatively aligned"
    
    def test_format_tables_for_injection(self, extractor):
        """Test: Format tables for injection into markdown"""
        tables = [
            {
                'slide_number': 3,
                'slide_title': 'Test Slide',
                'rows': [["H1", "H2"], ["V1", "V2"]],
                'row_count': 2,
                'col_count': 2,
                'markdown': "| H1 | H2 |\n|---|---|\n| V1 | V2 |"
            },
            {
                'slide_number': 6,
                'slide_title': 'Another Slide',
                'rows': [["A", "B"], ["C", "D"]],
                'row_count': 2,
                'col_count': 2,
                'markdown': "| A | B |\n|---|---|\n| C | D |"
            }
        ]
        
        slide_tables = extractor.format_tables_for_injection(tables)
        
        # Should have entries for slide 3 and 6
        assert 3 in slide_tables
        assert 6 in slide_tables
        
        # Each entry should contain the markdown table
        assert "H1" in slide_tables[3]
        assert "A" in slide_tables[6]
        
        # Should include table size info
        assert "2×2" in slide_tables[3]
    
    def test_extraction_report_empty(self, extractor):
        """Test: Report for empty table list"""
        report = extractor.get_extraction_report([])
        
        assert report['total_tables'] == 0
        assert report['slides_with_tables'] == 0
        assert report['total_rows'] == 0
        assert report['total_cells'] == 0
    
    def test_extraction_report_with_tables(self, extractor):
        """Test: Report with multiple tables"""
        tables = [
            {
                'slide_number': 3,
                'row_count': 5,
                'col_count': 3
            },
            {
                'slide_number': 3,  # Same slide
                'row_count': 3,
                'col_count': 2
            },
            {
                'slide_number': 6,
                'row_count': 4,
                'col_count': 4
            }
        ]
        
        report = extractor.get_extraction_report(tables)
        
        assert report['total_tables'] == 3
        assert report['slides_with_tables'] == 2  # Slides 3 and 6
        assert report['total_rows'] == 12  # 5 + 3 + 4
        assert report['total_cells'] == 37  # (5*3) + (3*2) + (4*4)
        assert 3 in report['slide_numbers']
        assert 6 in report['slide_numbers']
    
    def test_empty_string_input(self, extractor):
        """Test: Handles empty table data"""
        result = extractor._format_as_markdown([])
        assert result == "", "Empty data should return empty string"
    
    def test_cell_cleaning(self, extractor):
        """Test: Cell content is cleaned (newlines removed)"""
        # Simulate a table with newlines in cells
        test_data = [
            ["Header"],
            ["Line1\nLine2\nLine3"]
        ]
        
        markdown = extractor._format_as_markdown(test_data)
        
        # Newlines should be replaced with spaces
        assert "\nLine" not in markdown
        assert "Line1" in markdown
    
    def test_special_characters_in_cells(self, extractor):
        """Test: Special characters are preserved"""
        test_data = [
            ["Header"],
            ["Value with | pipe"],  # Pipe character
            ["Value with * asterisk"],
            ["Value with # hash"]
        ]
        
        markdown = extractor._format_as_markdown(test_data)
        
        # Special characters should be in output
        # (though pipes might cause issues - this tests current behavior)
        assert "asterisk" in markdown
        assert "hash" in markdown


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
