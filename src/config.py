"""
Configuration settings for MarkItDown Desktop Converter
"""
from pathlib import Path

# Application metadata
APP_NAME = "MarkItDown Desktop Converter"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Wei-power3"

# Directory structure
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
ORIGINALS_DIR = DATA_DIR / "originals"
PROCESSED_DIR = DATA_DIR / "processed"

# File naming patterns
TIMESTAMP_FORMAT = "%d-%m-%Y"  # day-month-year
ORIGINAL_SUFFIX = "_original"
MARKDOWN_SUFFIX = "_markdown"

# Supported file types
SUPPORTED_EXTENSIONS = {
    '.pdf': 'PDF Document',
    '.pptx': 'PowerPoint Presentation',
    '.ppt': 'PowerPoint Presentation (Legacy)'
}

# UI Settings
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700
THEME = "dark-blue"  # Options: "blue", "green", "dark-blue"
APPEARANCE_MODE = "dark"  # Options: "light", "dark", "system"

# Conversion settings
CONVERT_PPTX_TO_PDF = True  # Enable PPTX→PDF pathway
CONVERT_PPTX_DIRECT = True   # Enable PPTX→MD pathway

# Queue settings
MAX_QUEUE_DISPLAY = 50  # Maximum items to show in queue
AUTO_SCROLL = True  # Auto-scroll to latest item