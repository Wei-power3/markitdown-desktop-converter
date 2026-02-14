"""
Document conversion logic using MarkItDown
"""
from pathlib import Path
from typing import Tuple, Optional
from markitdown import MarkItDown
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from pptx import Presentation
import io
from config import CONVERT_PPTX_TO_PDF, CONVERT_PPTX_DIRECT


class DocumentConverter:
    """Handles document conversion operations"""
    
    def __init__(self):
        self.md = MarkItDown()
    
    def convert_file(self, file_path: Path) -> Tuple[str, Optional[str]]:
        """
        Convert file to Markdown
        
        Args:
            file_path: Path to file to convert
        
        Returns:
            Tuple of (markdown_content, error_message)
            error_message is None if successful
        """
        try:
            extension = file_path.suffix.lower()
            
            if extension == '.pdf':
                return self._convert_pdf(file_path)
            elif extension in ['.pptx', '.ppt']:
                return self._convert_powerpoint(file_path)
            else:
                return "", f"Unsupported file type: {extension}"
        
        except Exception as e:
            return "", f"Conversion error: {str(e)}"
    
    def _convert_pdf(self, file_path: Path) -> Tuple[str, None]:
        """Convert PDF to Markdown"""
        result = self.md.convert(str(file_path))
        return result.text_content, None
    
    def _convert_powerpoint(self, file_path: Path) -> Tuple[str, None]:
        """
        Convert PowerPoint to Markdown
        Implements both direct conversion and PDF pathway
        """
        results = []
        
        # Method 1: Direct PPTX → Markdown
        if CONVERT_PPTX_DIRECT:
            try:
                result = self.md.convert(str(file_path))
                results.append("# Direct PPTX Conversion\n\n")
                results.append(result.text_content)
            except Exception as e:
                results.append(f"Direct conversion failed: {str(e)}\n\n")
        
        # Method 2: PPTX → PDF → Markdown
        if CONVERT_PPTX_TO_PDF:
            try:
                pdf_content = self._pptx_to_pdf(file_path)
                pdf_path = file_path.with_suffix('.pdf')
                pdf_path.write_bytes(pdf_content)
                
                result = self.md.convert(str(pdf_path))
                results.append("\n\n---\n\n# PDF Pathway Conversion\n\n")
                results.append(result.text_content)
                
                # Clean up temporary PDF
                pdf_path.unlink()
            except Exception as e:
                results.append(f"\n\nPDF pathway failed: {str(e)}")
        
        return "".join(results), None
    
    def _pptx_to_pdf(self, pptx_path: Path) -> bytes:
        """
        Convert PPTX to PDF using reportlab
        Returns PDF as bytes
        """
        prs = Presentation(str(pptx_path))
        
        # Create PDF in memory
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        for i, slide in enumerate(prs.slides):
            # Add slide number
            story.append(Paragraph(f"<b>Slide {i+1}</b>", styles['Heading1']))
            story.append(Spacer(1, 0.2*inch))
            
            # Extract text from shapes
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text:
                    # Clean and format text
                    text = shape.text.strip()
                    if text:
                        story.append(Paragraph(text, styles['Normal']))
                        story.append(Spacer(1, 0.1*inch))
            
            # Add spacing between slides
            story.append(Spacer(1, 0.3*inch))
        
        doc.build(story)
        return pdf_buffer.getvalue()