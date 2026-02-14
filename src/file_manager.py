"""
File management operations: naming, saving, organizing
"""
from pathlib import Path
from datetime import datetime
import shutil
from config import (
    ORIGINALS_DIR, 
    PROCESSED_DIR, 
    TIMESTAMP_FORMAT,
    ORIGINAL_SUFFIX,
    MARKDOWN_SUFFIX
)


class FileManager:
    """Handles all file system operations"""
    
    def __init__(self):
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        ORIGINALS_DIR.mkdir(parents=True, exist_ok=True)
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    def generate_filename(self, original_path: Path, suffix: str) -> str:
        """
        Generate timestamped filename
        Format: day-month-year_filename_suffix.extension
        
        Args:
            original_path: Path to original file
            suffix: Either ORIGINAL_SUFFIX or MARKDOWN_SUFFIX
        
        Returns:
            Formatted filename string
        """
        timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
        base_name = original_path.stem  # filename without extension
        
        if suffix == MARKDOWN_SUFFIX:
            extension = ".md"
        else:
            extension = original_path.suffix
        
        return f"{timestamp}_{base_name}{suffix}{extension}"
    
    def save_original(self, source_path: Path) -> Path:
        """
        Copy original file to originals directory with timestamp
        
        Args:
            source_path: Path to source file
        
        Returns:
            Path to saved file
        """
        new_filename = self.generate_filename(source_path, ORIGINAL_SUFFIX)
        destination = ORIGINALS_DIR / new_filename
        
        # Handle duplicate filenames
        counter = 1
        while destination.exists():
            stem = destination.stem
            new_filename = f"{stem}_{counter}{destination.suffix}"
            destination = ORIGINALS_DIR / new_filename
            counter += 1
        
        shutil.copy2(source_path, destination)
        return destination
    
    def save_markdown(self, content: str, original_path: Path) -> Path:
        """
        Save markdown content to processed directory
        
        Args:
            content: Markdown text content
            original_path: Path to original file (for naming)
        
        Returns:
            Path to saved markdown file
        """
        new_filename = self.generate_filename(original_path, MARKDOWN_SUFFIX)
        destination = PROCESSED_DIR / new_filename
        
        # Handle duplicate filenames
        counter = 1
        while destination.exists():
            stem = destination.stem
            new_filename = f"{stem}_{counter}.md"
            destination = PROCESSED_DIR / new_filename
            counter += 1
        
        destination.write_text(content, encoding='utf-8')
        return destination
    
    def get_recent_files(self, limit: int = 10) -> list:
        """
        Get most recently processed files
        
        Args:
            limit: Maximum number of files to return
        
        Returns:
            List of (original_path, markdown_path) tuples
        """
        processed_files = sorted(
            PROCESSED_DIR.glob("*.md"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )[:limit]
        
        return [(f, f.stem) for f in processed_files]