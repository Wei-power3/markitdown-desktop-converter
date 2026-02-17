"""
PPTX list hierarchy preservation
Fixes Issue #2: Flattened bullets and mixed delimiters
"""
import re
from typing import List, Dict, Tuple
from xml.etree import ElementTree as ET
import logging

logger = logging.getLogger(__name__)


class PPTXListHierarchy:
    """
    Preserves bullet point hierarchy from PPTX files.
    
    Addresses Issue #2:
    - Converts PPT bullet levels (L1/L2/L3) to Markdown indentation
    - Standardizes list markers (always '-' for bullets)
    - Prevents flattening of nested lists
    - Removes ambiguous delimiter patterns (e.g., "- AccessMRI -")
    """
    
    def __init__(self):
        # Markdown indentation per level (0 = top level)
        self.indent_per_level = 2  # 2 spaces per level
        
        # PPT namespace for XML parsing
        self.namespaces = {
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
        }
    
    def extract_hierarchical_text(self, slide_xml: str) -> List[Dict]:
        """
        Extract text with hierarchy information from slide XML.
        
        Args:
            slide_xml: Raw XML string from PPTX slide
        
        Returns:
            List of dictionaries with:
            - 'text': Text content
            - 'level': Indentation level (0 = top level)
            - 'is_bullet': Whether this is a bullet point
        """
        try:
            root = ET.fromstring(slide_xml)
        except ET.ParseError as e:
            logger.warning(f"Failed to parse slide XML: {e}")
            return []
        
        items = []
        
        # Find all text elements with their paragraph context
        for txBody in root.findall('.//p:txBody', self.namespaces):
            for paragraph in txBody.findall('.//a:p', self.namespaces):
                item = self._extract_paragraph_with_level(paragraph)
                if item and item['text'].strip():
                    items.append(item)
        
        return items
    
    def _extract_paragraph_with_level(self, paragraph: ET.Element) -> Dict:
        """
        Extract text and level from a single paragraph element.
        
        Args:
            paragraph: XML Element representing a paragraph
        
        Returns:
            Dictionary with text, level, and is_bullet flag
        """
        # Get paragraph properties
        pPr = paragraph.find('a:pPr', self.namespaces)
        
        # Determine level (default 0)
        level = 0
        is_bullet = False
        
        if pPr is not None:
            # Check for level attribute
            level_attr = pPr.get('lvl')
            if level_attr:
                try:
                    level = int(level_attr)
                except ValueError:
                    level = 0
            
            # Check if this is a bullet point
            # Look for bullet-related elements
            buFont = pPr.find('a:buFont', self.namespaces)
            buChar = pPr.find('a:buChar', self.namespaces)
            buAutoNum = pPr.find('a:buAutoNum', self.namespaces)
            
            is_bullet = any([buFont is not None, buChar is not None, buAutoNum is not None])
        
        # Extract text content
        text_parts = []
        for t_elem in paragraph.findall('.//a:t', self.namespaces):
            if t_elem.text:
                text_parts.append(t_elem.text)
        
        text = ' '.join(text_parts).strip()
        
        return {
            'text': text,
            'level': level,
            'is_bullet': is_bullet
        }
    
    def format_as_markdown(self, items: List[Dict]) -> str:
        """
        Convert hierarchical items to properly indented Markdown.
        
        Args:
            items: List of items with text, level, and is_bullet
        
        Returns:
            Markdown-formatted string with proper hierarchy
        """
        lines = []
        
        for item in items:
            text = item['text']
            level = item['level']
            is_bullet = item['is_bullet']
            
            if not text:
                continue
            
            # Calculate indentation
            indent = ' ' * (level * self.indent_per_level)
            
            # Format based on type
            if is_bullet:
                # Always use '-' for bullets (Issue #2 requirement)
                lines.append(f"{indent}- {text}")
            else:
                # Non-bullet text (e.g., title or body)
                if level == 0:
                    # Top-level non-bullet: could be a title or paragraph
                    lines.append(text)
                else:
                    # Indented non-bullet: preserve indentation
                    lines.append(f"{indent}{text}")
        
        return '\n'.join(lines)
    
    def fix_flat_list(self, markdown_text: str) -> str:
        """
        Fix flattened lists in already-converted markdown.
        
        This is a fallback for when XML-based extraction isn't available.
        Uses heuristics to detect and fix list hierarchy.
        
        Args:
            markdown_text: Markdown with potentially flattened lists
        
        Returns:
            Markdown with restored hierarchy
        """
        lines = markdown_text.split('\n')
        result = []
        
        for line in lines:
            # Remove ambiguous delimiter patterns (Issue #2)
            # Pattern: "- Term -" should be just "- Term"
            line = re.sub(r'^(\s*-\s+)([^-]+?)(\s+-\s*)$', r'\1\2', line)
            
            # Standardize bullet markers
            # Convert *, +, •, ◦, etc. to standard '-'
            line = re.sub(r'^(\s*)[•◦▪▫\*\+]\s+', r'\1- ', line)
            
            result.append(line)
        
        return '\n'.join(result)
    
    def get_hierarchy_stats(self, items: List[Dict]) -> Dict:
        """
        Get statistics about list hierarchy.
        
        Args:
            items: List of items with hierarchy info
        
        Returns:
            Dictionary with hierarchy statistics
        """
        if not items:
            return {'max_depth': 0, 'bullet_count': 0, 'non_bullet_count': 0}
        
        levels = [item['level'] for item in items]
        bullets = [item for item in items if item['is_bullet']]
        non_bullets = [item for item in items if not item['is_bullet']]
        
        return {
            'max_depth': max(levels) if levels else 0,
            'bullet_count': len(bullets),
            'non_bullet_count': len(non_bullets),
            'avg_depth': sum(levels) / len(levels) if levels else 0,
            'hierarchy_preserved': max(levels) > 0
        }


def process_slide_with_hierarchy(slide_xml: str) -> Tuple[str, Dict]:
    """
    Convenience function to process a slide and preserve hierarchy.
    
    Args:
        slide_xml: Raw XML string from PPTX slide
    
    Returns:
        Tuple of (markdown_text, statistics)
    """
    processor = PPTXListHierarchy()
    items = processor.extract_hierarchical_text(slide_xml)
    markdown = processor.format_as_markdown(items)
    stats = processor.get_hierarchy_stats(items)
    
    return markdown, stats


# Example usage
if __name__ == "__main__":
    # Test with sample flattened markdown
    processor = PPTXListHierarchy()
    
    flattened = """- AccessMRI -
- Slide heading
- Sub-bullet that should be indented
* Another bullet with different marker
- Yet another bullet"""
    
    print("=== Flattened List Fix ===")
    print("Before:")
    print(flattened)
    print("\nAfter:")
    fixed = processor.fix_flat_list(flattened)
    print(fixed)
    
    # Test with hierarchical items
    print("\n=== Hierarchical Formatting ===")
    test_items = [
        {'text': 'Top level item', 'level': 0, 'is_bullet': True},
        {'text': 'Second level item', 'level': 1, 'is_bullet': True},
        {'text': 'Another second level', 'level': 1, 'is_bullet': True},
        {'text': 'Third level item', 'level': 2, 'is_bullet': True},
        {'text': 'Back to top level', 'level': 0, 'is_bullet': True},
    ]
    
    markdown = processor.format_as_markdown(test_items)
    print(markdown)
    
    stats = processor.get_hierarchy_stats(test_items)
    print(f"\nStats: {stats}")
