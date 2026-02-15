"""
Document conversion logic using MarkItDown with enhanced quality
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
import logging
from config import CONVERT_PPTX_TO_PDF, CONVERT_PPTX_DIRECT
from text_cleaner import MarkdownCleaner
from table_extractor import TableExtractor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentConverter:
    """
    Enhanced document conversion with:
    - Text cleaning (fixes ligatures, spacing, encoding)
    - Structured table extraction
    - Dual PowerPoint conversion
    """
    
    def __init__(self):
        self.md = MarkItDown()
        self.text_cleaner = MarkdownCleaner()
        self.table_extractor = TableExtractor(min_accuracy=0.5)
    
    def convert_file(self, file_path: Path) -> Tuple[str, Optional[str]]:
        """
        Convert file to Markdown with enhanced quality.
        
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
            logger.error(f"Conversion error: {str(e)}", exc_info=True)
            return "", f"Conversion error: {str(e)}"
    
    def _convert_pdf(self, file_path: Path) -> Tuple[str, None]:
        """
        Convert PDF to Markdown with enhanced quality.
        
        Process:
        1. Extract base text using MarkItDown
        2. Clean text artifacts (ligatures, spacing, etc.)
        3. Extract structured tables
        4. Combine all content
        """
        logger.info(f"Converting PDF: {file_path.name}")
        
        # Step 1: Base conversion
        result = self.md.convert(str(file_path))
        base_content = result.text_content
        
        # Step 2: Clean text
        cleaned_content = self.text_cleaner.clean(base_content)
        
        # Log cleaning statistics
        report = self.text_cleaner.get_cleaning_report(base_content, cleaned_content)
        logger.info(f"Text cleaning: {report['encoding_fixes']} encoding fixes, "
                   f"{report['hyphen_fixes']} hyphen fixes, "
                   f"{report['medical_term_fixes']} medical term fixes")
        
        # Step 3: Extract structured tables
        try:
            tables = self.table_extractor.extract_tables(file_path)
            if tables:
                logger.info(f"Extracted {len(tables)} structured table(s)")
                table_section = self.table_extractor.format_tables_for_markdown(tables)
                cleaned_content += table_section
        except Exception as e:
            logger.warning(f"Table extraction failed: {e}")
            # Continue without tables - not critical
        
        return cleaned_content, None
    
    def _convert_powerpoint(self, file_path: Path) -> Tuple[str, None]:
        """
        Convert PowerPoint to Markdown.
        Implements both direct conversion and PDF pathway.
        Text cleaning is applied to all outputs.
        """
        logger.info(f"Converting PowerPoint: {file_path.name}")
        results = []
        
        # Method 1: Direct PPTX → Markdown
        if CONVERT_PPTX_DIRECT:
            try:
                result = self.md.convert(str(file_path))
                direct_content = result.text_content
                
                # Clean the content
                direct_content = self.text_cleaner.clean(direct_content)
                
                results.append("# Direct PPTX Conversion\n\n")
                results.append(direct_content)
                logger.info("Direct PPTX conversion completed")
            except Exception as e:
                logger.warning(f"Direct conversion failed: {str(e)}")
                results.append(f"Direct conversion failed: {str(e)}\n\n")
        
        # Method 2: PPTX → PDF → Markdown
        if CONVERT_PPTX_TO_PDF:
            try:
                pdf_content = self._pptx_to_pdf(file_path)
                pdf_path = file_path.with_suffix('.pdf')
                pdf_path.write_bytes(pdf_content)
                
                result = self.md.convert(str(pdf_path))
                pdf_pathway_content = result.text_content
                
                # Clean the content
                pdf_pathway_content = self.text_cleaner.clean(pdf_pathway_content)
                
                results.append("\n\n---\n\n# PDF Pathway Conversion\n\n")
                results.append(pdf_pathway_content)
                
                # Clean up temporary PDF
                pdf_path.unlink()
                logger.info("PDF pathway conversion completed")
            except Exception as e:
                logger.warning(f"PDF pathway failed: {str(e)}")
                results.append(f"\n\nPDF pathway failed: {str(e)}")
        
        final_content = "".join(results)
        return final_content, None
    
    def _pptx_to_pdf(self, pptx_path: Path) -> bytes:
        """
        Convert PPTX to PDF using reportlab.
        Returns PDF as bytes.
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
