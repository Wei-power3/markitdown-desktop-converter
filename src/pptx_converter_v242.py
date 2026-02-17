"""
Integrated PPTX Converter v2.4.2
Combines all 5 machine-readability fixes into a single pipeline
"""
import zipfile
import logging
from typing import Dict, List, Optional
from xml.etree import ElementTree as ET
from pathlib import Path

# Import all v2.4.2 modules
from pptx_table_extractor import PPTXTableExtractor
from pptx_list_hierarchy import PPTXListHierarchy
from pptx_text_fixer import PPTXTextFixer
from pptx_slide_schema import PPTXSlideSchema

logger = logging.getLogger(__name__)


class PPTXConverterV242:
    """
    Complete PPTX to Markdown converter with all v2.4.2 fixes.
    
    Integrates:
    - Issue #1: Table preservation (pptx_table_extractor)
    - Issue #2: List hierarchy (pptx_list_hierarchy)
    - Issue #3: Line breaks & split words (pptx_text_fixer)
    - Issue #4: Unicode normalization (pptx_text_fixer)
    - Issue #5: Slide schema (pptx_slide_schema)
    """
    
    def __init__(self):
        self.table_extractor = PPTXTableExtractor()
        self.list_processor = PPTXListHierarchy()
        self.text_fixer = PPTXTextFixer()
        self.slide_schema = PPTXSlideSchema()
        
        # Cumulative statistics
        self.stats = {
            'total_slides': 0,
            'tables_fixed': 0,
            'max_hierarchy_level': 0,
            'line_breaks_fixed': 0,
            'split_words_fixed': 0,
            'unicode_fixes': 0,
            'contraction_fixes': 0,
            'run_on_fixes': 0,
            'schema_compliant': True,
            'total_fixes': 0
        }
    
    def convert_file(self, pptx_path: str) -> Dict:
        """
        Convert PPTX file to machine-readable Markdown.
        
        Args:
            pptx_path: Path to PPTX file
        
        Returns:
            Dictionary with:
            - 'markdown': Complete Markdown output
            - 'stats': Detailed statistics about fixes applied
            - 'success': Boolean indicating success
            - 'error': Error message if failed
        """
        try:
            # Reset stats
            self.stats = {
                'total_slides': 0,
                'tables_fixed': 0,
                'max_hierarchy_level': 0,
                'line_breaks_fixed': 0,
                'split_words_fixed': 0,
                'unicode_fixes': 0,
                'contraction_fixes': 0,
                'run_on_fixes': 0,
                'schema_compliant': True,
                'total_fixes': 0
            }
            
            # Open PPTX file
            with zipfile.ZipFile(pptx_path, 'r') as pptx:
                markdown = self._process_pptx(pptx, Path(pptx_path).name)
            
            # Calculate total fixes
            self.stats['total_fixes'] = (
                self.stats['tables_fixed'] +
                self.stats['line_breaks_fixed'] +
                self.stats['split_words_fixed'] +
                self.stats['unicode_fixes'] +
                self.stats['contraction_fixes'] +
                self.stats['run_on_fixes']
            )
            
            # Final validation
            validation = self.slide_schema.validate_slide_schema(markdown)
            self.stats['schema_compliant'] = validation['valid']
            
            return {
                'success': True,
                'markdown': markdown,
                'stats': self.stats,
                'validation': validation
            }
            
        except Exception as e:
            logger.error(f"Conversion failed: {e}", exc_info=True)
            return {
                'success': False,
                'markdown': '',
                'stats': self.stats,
                'error': str(e)
            }
    
    def _process_pptx(self, pptx: zipfile.ZipFile, filename: str) -> str:
        """
        Process PPTX zip file and extract all content.
        
        Args:
            pptx: Opened ZipFile object
            filename: Original filename
        
        Returns:
            Complete Markdown string
        """
        # Header
        markdown_parts = [
            f"# {filename}",
            "",
            "**Converted with v2.4.2** • Machine-readable output with all 5 fixes",
            "",
            "---",
            ""
        ]
        
        # Get slide files
        slide_files = sorted(
            [f for f in pptx.namelist() 
             if f.startswith('ppt/slides/slide') and f.endswith('.xml')],
            key=lambda x: int(x.split('slide')[1].split('.')[0])
        )
        
        self.stats['total_slides'] = len(slide_files)
        
        # Process each slide
        for i, slide_file in enumerate(slide_files, start=1):
            slide_xml = pptx.read(slide_file).decode('utf-8')
            slide_md = self._process_slide(slide_xml, i)
            markdown_parts.append(slide_md)
            markdown_parts.append("")  # Blank line between slides
        
        return "\n".join(markdown_parts)
    
    def _process_slide(self, slide_xml: str, slide_number: int) -> str:
        """
        Process a single slide with all v2.4.2 fixes.
        
        Args:
            slide_xml: Raw XML content of slide
            slide_number: Slide number (1-indexed)
        
        Returns:
            Markdown for this slide
        """
        # Step 1: Extract title (Issue #5)
        title = self.slide_schema.extract_slide_title(slide_xml)
        if not title:
            title = f"Slide {slide_number}"
        
        # Step 2: Extract tables (Issue #1)
        tables = self.table_extractor.extract_tables_from_slide(slide_xml)
        table_md = self.table_extractor.convert_tables_to_markdown(tables)
        if tables:
            self.stats['tables_fixed'] += len(tables)
        
        # Step 3: Extract hierarchical lists (Issue #2)
        list_items = self.list_processor.extract_hierarchical_text(slide_xml)
        list_md = self.list_processor.format_as_markdown(list_items)
        
        # Track max hierarchy level
        if list_items:
            max_level = max(item['level'] for item in list_items)
            self.stats['max_hierarchy_level'] = max(
                self.stats['max_hierarchy_level'], 
                max_level
            )
        
        # Step 4: Combine content
        content_parts = []
        if table_md.strip():
            content_parts.append(table_md)
        if list_md.strip():
            content_parts.append(list_md)
        
        content = "\n\n".join(content_parts)
        
        # Step 5: Fix text issues (Issues #3 & #4)
        if content.strip():
            fix_result = self.text_fixer.fix_text(content)
            fixed_content = fix_result['text']
            
            # Accumulate statistics
            stats = fix_result['stats']
            self.stats['line_breaks_fixed'] += stats.get('line_break_fixes', 0)
            self.stats['split_words_fixed'] += stats.get('split_word_fixes', 0)
            self.stats['unicode_fixes'] += stats.get('unicode_fixes', 0)
            self.stats['contraction_fixes'] += stats.get('contraction_fixes', 0)
            self.stats['run_on_fixes'] += stats.get('run_on_fixes', 0)
        else:
            fixed_content = "*[No content on this slide]*"
        
        # Step 6: Apply standard schema (Issue #5)
        slide_header = self.slide_schema.format_slide_header(slide_number, title)
        
        # Combine header and content
        slide_md = f"{slide_header}\n\n{fixed_content}"
        
        return slide_md
    
    def get_statistics(self) -> Dict:
        """
        Get detailed statistics about the conversion.
        
        Returns:
            Dictionary with all statistics
        """
        return self.stats.copy()
    
    def get_quality_score(self) -> float:
        """
        Calculate overall quality score (0-100).
        
        Based on:
        - Tables preserved
        - Hierarchy maintained
        - Text quality fixes
        - Schema compliance
        
        Returns:
            Quality score from 0-100
        """
        score = 0.0
        
        # Base score for schema compliance
        if self.stats['schema_compliant']:
            score += 20
        
        # Points for tables fixed (up to 20 points)
        if self.stats['tables_fixed'] > 0:
            score += min(20, self.stats['tables_fixed'] * 10)
        
        # Points for hierarchy preservation (up to 20 points)
        if self.stats['max_hierarchy_level'] > 0:
            score += min(20, self.stats['max_hierarchy_level'] * 10)
        
        # Points for text quality fixes (up to 40 points)
        total_text_fixes = (
            self.stats['line_breaks_fixed'] +
            self.stats['split_words_fixed'] +
            self.stats['unicode_fixes'] +
            self.stats['contraction_fixes'] +
            self.stats['run_on_fixes']
        )
        if total_text_fixes > 0:
            score += min(40, total_text_fixes * 2)
        
        return min(100.0, score)


def convert_pptx_v242(pptx_path: str) -> Dict:
    """
    Convenience function to convert PPTX with v2.4.2 fixes.
    
    Args:
        pptx_path: Path to PPTX file
    
    Returns:
        Dictionary with markdown, stats, and success status
    """
    converter = PPTXConverterV242()
    return converter.convert_file(pptx_path)


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pptx_converter_v242.py <pptx_file>")
        sys.exit(1)
    
    pptx_file = sys.argv[1]
    
    print(f"Converting {pptx_file} with v2.4.2...")
    result = convert_pptx_v242(pptx_file)
    
    if result['success']:
        print("\n" + "="*60)
        print("CONVERSION SUCCESSFUL")
        print("="*60)
        
        stats = result['stats']
        print(f"\nStatistics:")
        print(f"  Total Slides: {stats['total_slides']}")
        print(f"  Tables Fixed: {stats['tables_fixed']}")
        print(f"  Max Hierarchy: L{stats['max_hierarchy_level']}")
        print(f"  Line Breaks Fixed: {stats['line_breaks_fixed']}")
        print(f"  Split Words Fixed: {stats['split_words_fixed']}")
        print(f"  Unicode Fixes: {stats['unicode_fixes']}")
        print(f"  Contraction Fixes: {stats['contraction_fixes']}")
        print(f"  Run-on Fixes: {stats['run_on_fixes']}")
        print(f"  Total Fixes: {stats['total_fixes']}")
        print(f"  Schema Compliant: {stats['schema_compliant']}")
        
        converter = PPTXConverterV242()
        converter.stats = stats
        quality = converter.get_quality_score()
        print(f"  Quality Score: {quality:.1f}/100")
        
        # Save markdown
        output_file = pptx_file.replace('.pptx', '_v2.4.2_machine-readable.md')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result['markdown'])
        
        print(f"\nOutput saved to: {output_file}")
        
    else:
        print(f"\nERROR: {result['error']}")
        sys.exit(1)
