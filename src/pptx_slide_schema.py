"""
PPTX slide schema standardization
Fixes Issue #5: Inconsistent slide boundaries and metadata
"""
import re
from typing import List, Dict, Optional
from xml.etree import ElementTree as ET
import logging

logger = logging.getLogger(__name__)


class PPTXSlideSchema:
    """
    Standardizes PPTX slide structure for machine readability.
    
    Addresses Issue #5:
    - Enforces deterministic schema: ## Slide N: <title>
    - Removes stray tokens (e.g., "# - Decision Question")
    - Consistent title/body segmentation
    - Optional section headers: ### Section: <name>
    - No ambiguous header patterns
    """
    
    def __init__(self):
        # PPT namespace for XML parsing
        self.namespaces = {
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
        }
        
        # Schema template
        self.slide_template = "## Slide {number}: {title}"
        self.section_template = "### Section: {name}"
    
    def extract_slide_title(self, slide_xml: str) -> Optional[str]:
        """
        Extract the title from a slide's XML.
        
        Looks for title placeholder shapes in PPTX structure.
        
        Args:
            slide_xml: Raw XML string from PPTX slide
        
        Returns:
            Slide title or None if not found
        """
        try:
            root = ET.fromstring(slide_xml)
        except ET.ParseError as e:
            logger.warning(f"Failed to parse slide XML: {e}")
            return None
        
        # Look for title shape (usually has type="title" or idx="0")
        for shape in root.findall('.//p:sp', self.namespaces):
            # Check if this is a title shape
            nvSpPr = shape.find('.//p:nvSpPr', self.namespaces)
            if nvSpPr is not None:
                ph = nvSpPr.find('.//p:ph', self.namespaces)
                if ph is not None:
                    ph_type = ph.get('type')
                    if ph_type in ['title', 'ctrTitle']:
                        # Extract text from this shape
                        text_parts = []
                        for t_elem in shape.findall('.//a:t', self.namespaces):
                            if t_elem.text:
                                text_parts.append(t_elem.text)
                        
                        if text_parts:
                            title = ' '.join(text_parts).strip()
                            return title
        
        # Fallback: first text element if no title shape found
        first_text = root.find('.//a:t', self.namespaces)
        if first_text is not None and first_text.text:
            return first_text.text.strip()
        
        return None
    
    def format_slide_header(self, slide_number: int, title: Optional[str] = None) -> str:
        """
        Format a standardized slide header.
        
        Args:
            slide_number: Slide number (1-indexed)
            title: Optional slide title
        
        Returns:
            Standardized Markdown header string
        """
        if title:
            # Clean title: remove stray markdown tokens
            title = self.clean_title(title)
            return self.slide_template.format(number=slide_number, title=title)
        else:
            return self.slide_template.format(number=slide_number, title="Untitled")
    
    def clean_title(self, title: str) -> str:
        """
        Remove markdown tokens and clean title text.
        
        Removes patterns like:
        - Leading/trailing whitespace
        - Markdown headers (#, ##, etc.)
        - Stray delimiters (# -, - # etc.)
        - Multiple spaces
        
        Args:
            title: Raw title text
        
        Returns:
            Cleaned title
        """
        if not title:
            return "Untitled"
        
        # Remove leading markdown headers
        title = re.sub(r'^#+\s*', '', title)
        
        # Remove stray delimiters (Issue #5 requirement)
        # Pattern: "# - Something" or "- # Something"
        title = re.sub(r'^[#\-\s]+', '', title)
        title = re.sub(r'[#\-\s]+$', '', title)
        
        # Remove multiple spaces
        title = re.sub(r'\s+', ' ', title)
        
        # Strip and ensure not empty
        title = title.strip()
        if not title:
            return "Untitled"
        
        return title
    
    def format_section_header(self, section_name: str) -> str:
        """
        Format a section header within a slide.
        
        Args:
            section_name: Name of the section
        
        Returns:
            Standardized section header
        """
        clean_name = self.clean_title(section_name)
        return self.section_template.format(name=clean_name)
    
    def standardize_slide_markdown(self, slide_number: int, raw_markdown: str, 
                                   slide_title: Optional[str] = None) -> str:
        """
        Standardize markdown for a single slide.
        
        Args:
            slide_number: Slide number
            raw_markdown: Existing markdown content
            slide_title: Optional explicit title
        
        Returns:
            Standardized markdown with proper schema
        """
        lines = raw_markdown.split('\n')
        result = []
        
        # Extract or determine title
        if not slide_title:
            # Try to find title in first few lines
            for line in lines[:5]:
                if line.strip() and not line.strip().startswith('-'):
                    # First non-empty, non-bullet line is likely the title
                    slide_title = line.strip()
                    break
        
        # Add standardized header
        header = self.format_slide_header(slide_number, slide_title)
        result.append(header)
        result.append('')  # Blank line after header
        
        # Process content
        skip_first_title = False
        if slide_title:
            # Skip the first occurrence of the title in content
            skip_first_title = True
        
        for line in lines:
            stripped = line.strip()
            
            # Skip the original title if we used it in header
            if skip_first_title and stripped == slide_title:
                skip_first_title = False
                continue
            
            # Skip old-style slide headers
            if re.match(r'^##\s+Slide\s+\d+', stripped):
                continue
            
            # Skip stray header tokens (Issue #5)
            if re.match(r'^#+\s*-\s*', stripped):
                # Convert to regular text
                cleaned = re.sub(r'^#+\s*-\s*', '', stripped)
                result.append(cleaned)
                continue
            
            # Keep other content
            result.append(line)
        
        return '\n'.join(result)
    
    def validate_slide_schema(self, markdown: str) -> Dict:
        """
        Validate that markdown follows the standard schema.
        
        Args:
            markdown: Markdown text to validate
        
        Returns:
            Dictionary with validation results:
            - valid: bool
            - issues: List of issues found
            - slide_count: Number of slides detected
        """
        lines = markdown.split('\n')
        issues = []
        slide_count = 0
        
        # Find all slide headers
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check for properly formatted slide headers
            if stripped.startswith('## Slide '):
                slide_count += 1
                
                # Validate format
                if not re.match(r'^## Slide \d+: ', stripped):
                    issues.append(f"Line {i}: Slide header missing colon and title")
            
            # Check for stray header tokens (should not exist)
            if re.match(r'^#+\s*-\s+', stripped):
                issues.append(f"Line {i}: Stray header token found: {stripped[:30]}...")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'slide_count': slide_count,
            'schema_compliant': len(issues) == 0 and slide_count > 0
        }
    
    def fix_legacy_format(self, markdown: str) -> str:
        """
        Fix legacy/inconsistent slide formatting.
        
        Converts various formats to standard schema:
        - "## Slide 1\nSome title" → "## Slide 1: Some title"
        - "# - Decision" → Removes stray tokens
        - "## Slide X - Title" → "## Slide X: Title"
        
        Args:
            markdown: Markdown with legacy formatting
        
        Returns:
            Markdown with standard schema
        """
        lines = markdown.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Case 1: Slide header without title, title on next line
            if re.match(r'^## Slide \d+\s*$', stripped):
                slide_num_match = re.search(r'Slide (\d+)', stripped)
                if slide_num_match:
                    slide_num = slide_num_match.group(1)
                    
                    # Look for title on next non-empty line
                    title = None
                    j = i + 1
                    while j < len(lines) and j < i + 5:
                        next_line = lines[j].strip()
                        if next_line and not next_line.startswith('#'):
                            title = self.clean_title(next_line)
                            break
                        j += 1
                    
                    # Create standard header
                    if title:
                        result.append(f"## Slide {slide_num}: {title}")
                        i = j + 1  # Skip past the title line
                    else:
                        result.append(f"## Slide {slide_num}: Untitled")
                        i += 1
                    continue
            
            # Case 2: Slide header with dash instead of colon
            if re.match(r'^## Slide \d+ -', stripped):
                fixed = re.sub(r'(## Slide \d+) -', r'\1:', stripped)
                result.append(fixed)
                i += 1
                continue
            
            # Case 3: Stray header tokens
            if re.match(r'^#+\s*-\s+', stripped):
                # Remove the token, keep the content
                cleaned = re.sub(r'^#+\s*-\s+', '', stripped)
                result.append(cleaned)
                i += 1
                continue
            
            # Default: keep line as-is
            result.append(line)
            i += 1
        
        return '\n'.join(result)


def standardize_pptx_slides(markdown: str) -> Tuple[str, Dict]:
    """
    Convenience function to standardize PPTX slide formatting.
    
    Args:
        markdown: Raw markdown from PPTX conversion
    
    Returns:
        Tuple of (standardized_markdown, validation_results)
    """
    schema = PPTXSlideSchema()
    
    # Fix legacy format
    fixed = schema.fix_legacy_format(markdown)
    
    # Validate
    validation = schema.validate_slide_schema(fixed)
    
    return fixed, validation


# Type hint import
from typing import Tuple


# Example usage
if __name__ == "__main__":
    schema = PPTXSlideSchema()
    
    # Test legacy format fixing
    legacy_md = """## Slide 1
Decision Question

# - Important point
- Some content

## Slide 2 - Another Title
More content"""
    
    print("=== Legacy Format Fix ===")
    print("Before:")
    print(legacy_md)
    print("\nAfter:")
    fixed = schema.fix_legacy_format(legacy_md)
    print(fixed)
    
    # Validate
    print("\n=== Validation ===")
    validation = schema.validate_slide_schema(fixed)
    print(f"Valid: {validation['valid']}")
    print(f"Slides found: {validation['slide_count']}")
    if validation['issues']:
        print(f"Issues: {validation['issues']}")
