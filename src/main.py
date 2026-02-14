"""
Main application entry point
MarkItDown Desktop Converter - Windows GUI Application with Batch Processing Queue
"""
import customtkinter as ctk
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False
    print("Warning: tkinterdnd2 not available. Drag-and-drop disabled.")
from CTkMessagebox import CTkMessagebox
from pathlib import Path
import threading
from typing import List
from datetime import datetime
import sys

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    APP_NAME,
    APP_VERSION,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    THEME,
    APPEARANCE_MODE,
    SUPPORTED_EXTENSIONS
)
from file_manager import FileManager
from converter import DocumentConverter


class QueueItem:
    """Represents a file in the processing queue"""
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.status = "Queued"  # Queued, Processing, Complete, Error
        self.progress = 0.0
        self.message = ""
        self.start_time = None
        self.end_time = None


class MarkItDownApp:
    """Main application class with batch processing queue"""
    
    def __init__(self):
        # Initialize TkinterDnD for drag-and-drop
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = ctk.CTk()
        
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        # Set theme
        ctk.set_appearance_mode(APPEARANCE_MODE)
        ctk.set_default_color_theme(THEME)
        
        # Initialize managers
        self.file_manager = FileManager()
        self.converter = DocumentConverter()
        
        # Processing queue
        self.queue: List[QueueItem] = []
        self.processing = False
        self.queue_widgets = {}  # Map queue items to UI widgets
        
        # Build UI
        self.setup_ui()
        
    def setup_ui(self):
        """Create the user interface with batch queue"""
        
        # Main container with grid layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        main_container = ctk.CTkFrame(self.root)
        main_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # ===== TOP SECTION: Title and Drop Zone =====
        top_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Title
        title_label = ctk.CTkLabel(
            top_frame,
            text="MarkItDown Desktop Converter",
            font=("Arial", 26, "bold")
        )
        title_label.pack(pady=(10, 5))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            top_frame,
            text="Drag & Drop PDF or PowerPoint files to convert to Markdown",
            font=("Arial", 13)
        )
        subtitle_label.pack(pady=(0, 10))
        
        # Drop zone
        self.drop_frame = ctk.CTkFrame(
            top_frame,
            height=150,
            border_width=3,
            border_color="#3B8ED0"
        )
        self.drop_frame.pack(fill="x", padx=20, pady=5)
        self.drop_frame.pack_propagate(False)
        
        # Drop zone content
        drop_content = ctk.CTkFrame(self.drop_frame, fg_color="transparent")
        drop_content.place(relx=0.5, rely=0.5, anchor="center")
        
        drop_icon = ctk.CTkLabel(
            drop_content,
            text="📁",
            font=("Arial", 48)
        )
        drop_icon.pack()
        
        self.drop_label = ctk.CTkLabel(
            drop_content,
            text="Drop files here or click Browse",
            font=("Arial", 16)
        )
        self.drop_label.pack(pady=5)
        
        supported_text = ctk.CTkLabel(
            drop_content,
            text="Supported: PDF, PPTX, PPT",
            font=("Arial", 11),
            text_color="gray"
        )
        supported_text.pack()
        
        # Enable drag and drop
        if DND_AVAILABLE:
            self.drop_frame.drop_target_register(DND_FILES)
            self.drop_frame.dnd_bind('<<Drop>>', self.on_drop)
        
        # Browse button
        browse_btn = ctk.CTkButton(
            drop_content,
            text="Browse Files",
            command=self.browse_files,
            width=140,
            height=35
        )
        browse_btn.pack(pady=10)
        
        # ===== MIDDLE SECTION: Processing Queue =====
        queue_frame = ctk.CTkFrame(main_container)
        queue_frame.grid(row=1, column=0, sticky="nsew", pady=5)
        queue_frame.grid_rowconfigure(1, weight=1)
        queue_frame.grid_columnconfigure(0, weight=1)
        
        # Queue header
        queue_header = ctk.CTkFrame(queue_frame, fg_color="transparent")
        queue_header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        queue_title = ctk.CTkLabel(
            queue_header,
            text="Processing Queue",
            font=("Arial", 18, "bold")
        )
        queue_title.pack(side="left")
        
        self.queue_count_label = ctk.CTkLabel(
            queue_header,
            text="0 files",
            font=("Arial", 14),
            text_color="gray"
        )
        self.queue_count_label.pack(side="left", padx=10)
        
        # Queue scrollable frame
        self.queue_scroll = ctk.CTkScrollableFrame(
            queue_frame,
            fg_color="transparent"
        )
        self.queue_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.queue_scroll.grid_columnconfigure(0, weight=1)
        
        # Empty queue message
        self.empty_queue_label = ctk.CTkLabel(
            self.queue_scroll,
            text="No files in queue. Drop files to begin.",
            font=("Arial", 13),
            text_color="gray"
        )
        self.empty_queue_label.grid(row=0, column=0, pady=50)
        
        # ===== BOTTOM SECTION: Controls =====
        bottom_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        bottom_frame.grid(row=2, column=0, sticky="ew", pady=(5, 10))
        
        # Action buttons
        btn_container = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        btn_container.pack(fill="x", padx=20)
        
        self.process_btn = ctk.CTkButton(
            btn_container,
            text="▶ Start Processing",
            command=self.start_processing,
            width=160,
            height=40,
            font=("Arial", 14, "bold")
        )
        self.process_btn.pack(side="left", padx=5)
        
        self.clear_btn = ctk.CTkButton(
            btn_container,
            text="🗑 Clear Queue",
            command=self.clear_queue,
            width=140,
            height=40,
            fg_color="#D32F2F",
            hover_color="#B71C1C"
        )
        self.clear_btn.pack(side="left", padx=5)
        
        # Folder buttons
        self.open_originals_btn = ctk.CTkButton(
            btn_container,
            text="📂 Originals Folder",
            command=self.open_originals_folder,
            width=160,
            height=40
        )
        self.open_originals_btn.pack(side="right", padx=5)
        
        self.open_processed_btn = ctk.CTkButton(
            btn_container,
            text="📄 Processed Folder",
            command=self.open_processed_folder,
            width=160,
            height=40
        )
        self.open_processed_btn.pack(side="right", padx=5)
    
    def browse_files(self):
        """Open file browser dialog"""
        from tkinter import filedialog
        
        filetypes = [(desc, f"*{ext}") for ext, desc in SUPPORTED_EXTENSIONS.items()]
        filetypes.append(("All Files", "*.*"))
        
        files = filedialog.askopenfilenames(
            title="Select files to convert",
            filetypes=filetypes
        )
        
        if files:
            self.add_files_to_queue([Path(f) for f in files])
    
    def on_drop(self, event):
        """Handle file drop event"""
        files = self.parse_drop_data(event.data)
        supported_files = [
            Path(f) for f in files 
            if Path(f).suffix.lower() in SUPPORTED_EXTENSIONS
        ]
        
        if not supported_files:
            CTkMessagebox(
                title="No Supported Files",
                message="Please drop PDF or PowerPoint files only.",
                icon="warning"
            )
            return
        
        self.add_files_to_queue(supported_files)
    
    def parse_drop_data(self, data: str) -> List[str]:
        """Parse TkinterDnD drop data into file paths"""
        files = []
        current = ""
        in_braces = False
        
        for char in data:
            if char == '{':
                in_braces = True
            elif char == '}':
                in_braces = False
                if current:
                    files.append(current.strip())
                    current = ""
            elif char == ' ' and not in_braces:
                if current:
                    files.append(current.strip())
                    current = ""
            else:
                current += char
        
        if current:
            files.append(current.strip())
        
        return files
    
    def add_files_to_queue(self, files: List[Path]):
        """Add files to processing queue"""
        for file_path in files:
            # Check if already in queue
            if any(item.file_path == file_path for item in self.queue):
                continue
            
            queue_item = QueueItem(file_path)
            self.queue.append(queue_item)
            self.create_queue_widget(queue_item)
        
        self.update_queue_count()
        self.empty_queue_label.grid_remove()
    
    def create_queue_widget(self, item: QueueItem):
        """Create UI widget for queue item"""
        row = len(self.queue_widgets)
        
        # Item container
        item_frame = ctk.CTkFrame(self.queue_scroll)
        item_frame.grid(row=row, column=0, sticky="ew", pady=3, padx=5)
        item_frame.grid_columnconfigure(1, weight=1)
        
        # Status indicator
        status_label = ctk.CTkLabel(
            item_frame,
            text="⏸",
            font=("Arial", 20),
            width=40
        )
        status_label.grid(row=0, column=0, padx=5, pady=5)
        
        # File info
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="ew", padx=5)
        
        filename_label = ctk.CTkLabel(
            info_frame,
            text=item.file_path.name,
            font=("Arial", 13, "bold"),
            anchor="w"
        )
        filename_label.pack(anchor="w")
        
        status_text = ctk.CTkLabel(
            info_frame,
            text="Queued",
            font=("Arial", 11),
            text_color="gray",
            anchor="w"
        )
        status_text.pack(anchor="w")
        
        # Progress bar
        progress = ctk.CTkProgressBar(item_frame, width=150)
        progress.grid(row=0, column=2, padx=10)
        progress.set(0)
        
        # Remove button
        remove_btn = ctk.CTkButton(
            item_frame,
            text="✕",
            width=30,
            height=30,
            command=lambda: self.remove_from_queue(item),
            fg_color="transparent",
            hover_color="#D32F2F"
        )
        remove_btn.grid(row=0, column=3, padx=5)
        
        # Store references
        self.queue_widgets[item] = {
            'frame': item_frame,
            'status_icon': status_label,
            'status_text': status_text,
            'progress': progress,
            'remove_btn': remove_btn
        }
    
    def remove_from_queue(self, item: QueueItem):
        """Remove item from queue"""
        if item.status == "Processing":
            return  # Can't remove while processing
        
        # Remove from queue
        self.queue.remove(item)
        
        # Destroy widget
        widgets = self.queue_widgets.pop(item)
        widgets['frame'].destroy()
        
        # Reorder remaining widgets
        for i, queue_item in enumerate(self.queue):
            self.queue_widgets[queue_item]['frame'].grid(row=i)
        
        self.update_queue_count()
        
        if not self.queue:
            self.empty_queue_label.grid(row=0, column=0, pady=50)
    
    def clear_queue(self):
        """Clear all items from queue"""
        if self.processing:
            CTkMessagebox(
                title="Cannot Clear",
                message="Please wait for current processing to complete.",
                icon="warning"
            )
            return
        
        # Remove all completed/error items
        to_remove = [item for item in self.queue if item.status != "Processing"]
        
        for item in to_remove:
            widgets = self.queue_widgets.pop(item)
            widgets['frame'].destroy()
            self.queue.remove(item)
        
        self.update_queue_count()
        
        if not self.queue:
            self.empty_queue_label.grid(row=0, column=0, pady=50)
    
    def update_queue_count(self):
        """Update queue count label"""
        count = len(self.queue)
        self.queue_count_label.configure(text=f"{count} file{'s' if count != 1 else ''}")
    
    def start_processing(self):
        """Start processing queue"""
        if self.processing:
            return
        
        queued_items = [item for item in self.queue if item.status == "Queued"]
        
        if not queued_items:
            CTkMessagebox(
                title="No Files",
                message="No files to process. Add files to queue first.",
                icon="info"
            )
            return
        
        # Disable process button
        self.process_btn.configure(state="disabled", text="⏸ Processing...")
        
        # Start processing thread
        thread = threading.Thread(
            target=self.process_queue,
            daemon=True
        )
        thread.start()
    
    def process_queue(self):
        """Process all queued items"""
        self.processing = True
        
        queued_items = [item for item in self.queue if item.status == "Queued"]
        
        for item in queued_items:
            self.process_item(item)
        
        self.processing = False
        self.root.after(0, self.process_btn.configure, 
                       state="normal", text="▶ Start Processing")
    
    def process_item(self, item: QueueItem):
        """Process a single queue item"""
        item.status = "Processing"
        item.start_time = datetime.now()
        
        # Update UI
        widgets = self.queue_widgets[item]
        self.root.after(0, widgets['status_icon'].configure, text="⏳")
        self.root.after(0, widgets['status_text'].configure, 
                       text="Processing...", text_color="#3B8ED0")
        self.root.after(0, widgets['progress'].set, 0.3)
        self.root.after(0, widgets['remove_btn'].configure, state="disabled")
        
        try:
            # Save original
            saved_original = self.file_manager.save_original(item.file_path)
            self.root.after(0, widgets['progress'].set, 0.5)
            
            # Convert to Markdown
            markdown_content, error = self.converter.convert_file(item.file_path)
            
            if error:
                raise Exception(error)
            
            self.root.after(0, widgets['progress'].set, 0.8)
            
            # Save Markdown
            saved_markdown = self.file_manager.save_markdown(
                markdown_content, 
                item.file_path
            )
            
            # Success
            item.status = "Complete"
            item.end_time = datetime.now()
            item.message = f"Saved to {saved_markdown.name}"
            
            self.root.after(0, widgets['status_icon'].configure, text="✔")
            self.root.after(0, widgets['status_text'].configure, 
                           text="Complete", text_color="#4CAF50")
            self.root.after(0, widgets['progress'].set, 1.0)
            
        except Exception as e:
            # Error
            item.status = "Error"
            item.end_time = datetime.now()
            item.message = str(e)
            
            self.root.after(0, widgets['status_icon'].configure, text="✖")
            self.root.after(0, widgets['status_text'].configure, 
                           text=f"Error: {str(e)[:50]}", text_color="#D32F2F")
            self.root.after(0, widgets['progress'].set, 0)
        
        finally:
            self.root.after(0, widgets['remove_btn'].configure, state="normal")
    
    def open_originals_folder(self):
        """Open originals folder in file explorer"""
        import os
        os.startfile(self.file_manager.ORIGINALS_DIR)
    
    def open_processed_folder(self):
        """Open processed folder in file explorer"""
        import os
        os.startfile(self.file_manager.PROCESSED_DIR)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Application entry point"""
    app = MarkItDownApp()
    app.run()


if __name__ == "__main__":
    main()