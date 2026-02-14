# MarkItDown Desktop Converter

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)](https://www.microsoft.com/windows)

A Windows desktop application for converting PDF and PowerPoint files to Markdown with drag-and-drop simplicity and batch processing queue.

## ✨ Features

- 📂 **Drag & Drop Interface** - Simply drop files to convert
- 📦 **Batch Processing Queue** - Convert multiple files with visual progress tracking
- 📄 **Dual PowerPoint Conversion** - Both direct PPTX→MD and PPTX→PDF→MD pathways
- 🕒 **Automatic Timestamped Naming** - Files organized with date stamps
- 📁 **Organized Folder Structure** - Separate folders for originals and processed files
- 🎨 **Modern Dark Theme UI** - Clean, professional interface
- ⚡ **Standalone Executable** - No installation required, just double-click to run

## 🖼️ Preview

### Main Interface with Batch Queue
```
┌──────────────────────────────────────────────────────┐
│    MarkItDown Desktop Converter                        │
│    Drag & Drop PDF or PowerPoint files                │
├──────────────────────────────────────────────────────┤
│              📁                                       │
│         Drop files here                              │
│    Supported: PDF, PPTX, PPT                         │
├──────────────────────────────────────────────────────┤
│  Processing Queue (3 files)                         │
├──────────────────────────────────────────────────────┤
│  ✔ report.pdf             [========] Complete      │
│  ⏳ presentation.pptx      [====----] Processing   │
│  ⏸ document.pdf           [--------] Queued       │
├──────────────────────────────────────────────────────┤
│ [▶ Start] [Clear] [Originals] [Processed]       │
└──────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Option 1: Download Standalone Executable (Recommended)

1. Go to [Releases](https://github.com/Wei-power3/markitdown-desktop-converter/releases)
2. Download `MarkItDownConverter.exe`
3. Double-click to run - that's it!

### Option 2: Run from Source

```bash
# Clone repository
git clone https://github.com/Wei-power3/markitdown-desktop-converter.git
cd markitdown-desktop-converter

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python src/main.py
```

## 📚 Usage Guide

### Basic Workflow

1. **Launch Application**
   - Double-click `MarkItDownConverter.exe` or run `python src/main.py`

2. **Add Files to Queue**
   - **Method A**: Drag and drop files onto the drop zone
   - **Method B**: Click "Browse Files" button

3. **Start Processing**
   - Click "▶ Start Processing" button
   - Watch real-time progress in the queue

4. **Access Converted Files**
   - Click "📂 Originals Folder" to see source files
   - Click "📄 Processed Folder" to see Markdown outputs

### File Naming Convention

**Original Files:**
```
14-02-2026_quarterly-report_original.pdf
14-02-2026_product-pitch_original.pptx
```

**Markdown Files:**
```
14-02-2026_quarterly-report_markdown.md
14-02-2026_product-pitch_markdown.md
```

Format: `{day}-{month}-{year}_{filename}_{suffix}.{extension}`

### Folder Structure

```
markitdown-desktop-converter/
├── data/
│   ├── originals/       # Your source files with timestamps
│   └── processed/       # Converted Markdown files
├── src/                 # Application source code
└── MarkItDownConverter.exe  # Standalone executable
```

## ⚙️ Features in Detail

### Dual PowerPoint Conversion

The application uses TWO conversion methods for PowerPoint files:

1. **Direct PPTX → Markdown**
   - Preserves slide structure and formatting
   - Best for text-heavy presentations

2. **PPTX → PDF → Markdown**
   - Better text extraction for complex layouts
   - Handles embedded objects more reliably

Both outputs are combined in a single `.md` file with section headers.

### Batch Processing Queue

- **Visual Status Indicators**
  - ⏸ Queued (waiting)
  - ⏳ Processing (active)
  - ✔ Complete (success)
  - ✖ Error (failed)

- **Progress Tracking**
  - Individual progress bars per file
  - Real-time status updates
  - Error messages displayed inline

- **Queue Management**
  - Add multiple files at once
  - Remove individual items (except during processing)
  - Clear completed items
  - Process all queued items with one click

## 🛠️ Building Standalone Executable

See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) for detailed build guide.

### Quick Build

```bash
# Install dependencies
pip install -r requirements.txt

# Build executable
python build_exe.py

# Find executable
dist/MarkItDownConverter.exe
```

## 💻 System Requirements

- **OS**: Windows 10 or 11
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 500 MB
- **Python** (for source): 3.10 or higher

## 📄 Supported File Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | `.pdf` | Full support via pdfminer.six and pdfplumber |
| PowerPoint | `.pptx` | Dual conversion pathway |
| PowerPoint Legacy | `.ppt` | Converted via python-pptx |

## 🧩 Technology Stack

- **Core Conversion**: [MarkItDown](https://github.com/microsoft/markitdown) by Microsoft
- **GUI Framework**: CustomTkinter (modern Tkinter)
- **Drag-and-Drop**: TkinterDnD2
- **PDF Generation**: ReportLab
- **PowerPoint Processing**: python-pptx
- **Packaging**: PyInstaller

## 🐛 Troubleshooting

### Application Won't Start

**Issue**: Double-clicking `.exe` does nothing

**Solution**:
1. Right-click `.exe` → "Run as administrator"
2. Check Windows Defender didn't block it
3. Ensure no antivirus blocking execution

### Drag-and-Drop Not Working

**Issue**: Files don't trigger when dropped

**Solution**:
1. Use "Browse Files" button instead
2. Ensure files are supported formats (PDF, PPTX, PPT)
3. Try running as administrator

### Conversion Fails

**Issue**: File shows error status

**Solution**:
1. Check file isn't password-protected
2. Ensure file isn't corrupted (can you open it?)
3. Check error message in status text
4. Try converting file individually

### Large Files Slow Processing

**Issue**: Processing takes very long

**Solution**:
- PDF: Expected for 100+ page documents
- PPTX: Large presentations (50+ slides) may take 1-2 minutes
- Consider splitting large files before conversion

## 🛣️ Roadmap

- [ ] Add image extraction from PDFs
- [ ] Support Word documents (.docx)
- [ ] Add Excel spreadsheet conversion (.xlsx)
- [ ] Preview pane for Markdown output
- [ ] LLM integration for auto-summaries
- [ ] Custom output folder selection
- [ ] Conversion settings panel
- [ ] macOS and Linux support

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- **Microsoft AutoGen Team** - [MarkItDown](https://github.com/microsoft/markitdown) library
- **CustomTkinter** - Modern UI framework
- **PyInstaller** - Executable packaging

## 📧 Support

For issues, questions, or feature requests:
- Open an issue: [GitHub Issues](https://github.com/Wei-power3/markitdown-desktop-converter/issues)
- Check documentation: [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)

---

**Made with ♥️ by Wei-power3**

[Report Bug](https://github.com/Wei-power3/markitdown-desktop-converter/issues) · [Request Feature](https://github.com/Wei-power3/markitdown-desktop-converter/issues)