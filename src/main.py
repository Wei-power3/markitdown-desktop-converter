"""
MarkItDown Desktop Converter - Main GUI Application
Version: 2.2.1 (Production)

Enhanced with:
- AI structure detection
- Advanced text cleaning
- Batch processing queue
- Quality metrics
- Link preservation
- Word and Excel support
"""

import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES
from pathlib import Path
import threading
from typing import List, Optional
import subprocess
import platform
from converter import DocumentConverter
from file_manager import FileManager
from config import ORIGINALS_DIR, PROCESSED_DIR
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# CustomTkinter settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Supported file extensions
SUPPORTED_EXTENSIONS = [".pdf", ".pptx", ".ppt", ".docx", ".doc", ".xlsx", ".xls"]


class QueueItem:
    """Represents a file in the processing queue"""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.status = "queued"  # queued, processing, complete, error
        self.progress = 0.0
        self.markdown_content = ""
        self.error_message = None
        self.quality_metrics = {}


class MarkItDownApp:
    """Main application window"""
    
    def __init__(self):
        # Create root using TkinterDnD for drag-and-drop
        self.root = TkinterDnD.Tk()
        self.root.title("MarkItDown Desktop Converter v2.2.1")
        self.root.geometry("900x700")
        
        # Initialize components
        self.converter = DocumentConverter()
        self.file_manager = FileManager()
        self.processing_queue: List[QueueItem] = []
        self.is_processing = False
        
        # Build UI
        self.setup_ui()
        
        logger.info("MarkItDown Desktop Converter v2.2.1 initialized")
    
    def setup_ui(self):
        """Setup the user interface"""
        
        # Title
        title = ctk.CTkLabel(
            self.root, 
            text="MarkItDown Desktop Converter v2.2.1",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)
        
        subtitle = ctk.CTkLabel(
            self.root,
            text="Clean Text Extraction for Embeddings | Quality-First Approach",
            font=("Arial", 12)
        )
        subtitle.pack()
        
        # Drop zone
        self.drop_frame = ctk.CTkFrame(self.root, height=150)
        self.drop_frame.pack(pady=20, padx=40, fill="x")
        self.drop_frame.pack_propagate(False)
        
        drop_label = ctk.CTkLabel(
            self.drop_frame,
            text="📁 Drop files here\nSupported: PDF, PPTX, DOCX, XLSX",
            font=("Arial", 14)
        )
        drop_label.pack(expand=True)
        
        # Enable drag-and-drop
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.on_drop)
        
        # Browse button
        browse_btn = ctk.CTkButton(
            self.root,
            text="📂 Browse Files",
            command=self.browse_files,
            width=200,
            height=40
        )
        browse_btn.pack(pady=10)
        
        # Queue frame
        queue_label = ctk.CTkLabel(
            self.root,
            text="Processing Queue",
            font=("Arial", 16, "bold")
        )
        queue_label.pack(pady=(20, 10))
        
        self.queue_frame = ctk.CTkScrollableFrame(self.root, height=250)
        self.queue_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
        # Control buttons
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=20)
        
        self.start_btn = ctk.CTkButton(
            button_frame,
            text="▶ Start Processing",
            command=self.start_processing,
            width=150,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.start_btn.pack(side="left", padx=5)
        
        clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑 Clear Queue",
            command=self.clear_queue,
            width=150
        )
        clear_btn.pack(side="left", padx=5)
        
        originals_btn = ctk.CTkButton(
            button_frame,
            text="📂 Originals Folder",
            command=lambda: self.open_folder(ORIGINALS_DIR),
            width=150
        )
        originals_btn.pack(side="left", padx=5)
        
        processed_btn = ctk.CTkButton(
            button_frame,
            text="📄 Processed Folder",
            command=lambda: self.open_folder(PROCESSED_DIR),
            width=150
        )
        processed_btn.pack(side="left", padx=5)
    
    def on_drop(self, event):
        """Handle dropped files"""
        files = self.root.tk.splitlist(event.data)
        valid_files = []
        
        for file in files:
            file_path = Path(file)
            if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                valid_files.append(file_path)
            else:
                logger.warning(f"Unsupported file type: {file_path.name}")
        
        if valid_files:
            self.add_to_queue(valid_files)
    
    def browse_files(self):
        """Browse for files to add to queue"""
        from tkinter import filedialog
        
        files = filedialog.askopenfilenames(
            title="Select files to convert",
            filetypes=[
                ("Supported files", "*.pdf;*.pptx;*.ppt;*.docx;*.doc;*.xlsx;*.xls"),
                ("PDF files", "*.pdf"),
                ("PowerPoint files", "*.pptx;*.ppt"),
                ("Word files", "*.docx;*.doc"),
                ("Excel files", "*.xlsx;*.xls"),
                ("All files", "*.*")
            ]
        )
        
        if files:
            file_paths = [Path(f) for f in files]
            self.add_to_queue(file_paths)
    
    def add_to_queue(self, file_paths: List[Path]):
        """Add files to processing queue"""
        for file_path in file_paths:
            # Check if already in queue
            if any(item.file_path == file_path for item in self.processing_queue):
                logger.info(f"File already in queue: {file_path.name}")
                continue
            
            item = QueueItem(file_path)
            self.processing_queue.append(item)
            self.create_queue_item_widget(item)
        
        logger.info(f"Added {len(file_paths)} file(s) to queue")
    
    def create_queue_item_widget(self, item: QueueItem):
        """Create widget for queue item"""
        frame = ctk.CTkFrame(self.queue_frame)
        frame.pack(pady=5, padx=10, fill="x")
        
        # Store reference
        item.widget_frame = frame
        
        # File info
        info_label = ctk.CTkLabel(
            frame,
            text=f"{item.file_path.name}",
            font=("Arial", 12)
        )
        info_label.pack(anchor="w", padx=10, pady=5)
        
        # Progress bar
        progress = ctk.CTkProgressBar(frame)
        progress.pack(fill="x", padx=10, pady=5)
        progress.set(0)
        item.progress_bar = progress
        
        # Status label
        status = ctk.CTkLabel(
            frame,
            text="⏸ Queued",
            font=("Arial", 10)
        )
        status.pack(anchor="w", padx=10, pady=5)
        item.status_label = status
    
    def start_processing(self):
        """Start processing queue"""
        if self.is_processing:
            logger.info("Already processing")
            return
        
        if not self.processing_queue:
            logger.info("Queue is empty")
            return
        
        self.is_processing = True
        self.start_btn.configure(state="disabled")
        
        # Process in separate thread
        thread = threading.Thread(target=self.process_queue, daemon=True)
        thread.start()
    
    def process_queue(self):
        """Process all items in queue"""
        for item in self.processing_queue:
            if item.status != "queued":
                continue
            
            self.process_item(item)
        
        self.is_processing = False
        self.root.after(0, lambda: self.start_btn.configure(state="normal"))
        logger.info("Queue processing complete")
    
    def process_item(self, item: QueueItem):
        """Process a single queue item"""
        # Update status
        item.status = "processing"
        self.root.after(0, lambda: item.status_label.configure(text="⏳ Processing..."))
        self.root.after(0, lambda: item.progress_bar.set(0.3))
        
        try:
            # Convert file
            logger.info(f"Converting: {item.file_path.name}")
            markdown, error = self.converter.convert_file(item.file_path)
            
            if error:
                item.status = "error"
                item.error_message = error
                self.root.after(0, lambda: item.status_label.configure(
                    text=f"✖ Error: {error[:50]}..."
                ))
                self.root.after(0, lambda: item.progress_bar.set(0))
                logger.error(f"Conversion failed: {error}")
                return
            
            self.root.after(0, lambda: item.progress_bar.set(0.7))
            
            # Save files
            self.file_manager.save_original(item.file_path)
            markdown_path = self.file_manager.save_markdown(markdown, item.file_path)
            
            # Success
            item.status = "complete"
            item.markdown_content = markdown
            self.root.after(0, lambda: item.status_label.configure(
                text=f"✔ Complete → {markdown_path.name}"
            ))
            self.root.after(0, lambda: item.progress_bar.set(1.0))
            logger.info(f"Successfully converted: {item.file_path.name}")
            
        except Exception as e:
            item.status = "error"
            item.error_message = str(e)
            self.root.after(0, lambda: item.status_label.configure(
                text=f"✖ Error: {str(e)[:50]}..."
            ))
            self.root.after(0, lambda: item.progress_bar.set(0))
            logger.error(f"Processing error: {str(e)}", exc_info=True)
    
    def clear_queue(self):
        """Clear completed/failed items from queue"""
        if self.is_processing:
            logger.info("Cannot clear queue while processing")
            return
        
        # Remove completed/error items
        items_to_remove = [
            item for item in self.processing_queue 
            if item.status in ["complete", "error"]
        ]
        
        for item in items_to_remove:
            item.widget_frame.destroy()
            self.processing_queue.remove(item)
        
        logger.info(f"Cleared {len(items_to_remove)} item(s) from queue")
    
    def open_folder(self, folder_path: Path):
        """Open folder in file explorer"""
        try:
            if platform.system() == "Windows":
                subprocess.run(["explorer", str(folder_path)])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", str(folder_path)])
            else:  # Linux
                subprocess.run(["xdg-open", str(folder_path)])
        except Exception as e:
            logger.error(f"Could not open folder: {str(e)}")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MarkItDownApp()
    app.run()
