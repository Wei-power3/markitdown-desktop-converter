# MarkItDown Desktop Converter

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://www.microsoft.com/windows)
[![Version](https://img.shields.io/badge/version-2.4.4-orange)](https://github.com/Wei-power3/markitdown-desktop-converter/releases)
[![Tests](https://img.shields.io/badge/tests-45%2B%20Excel%20tests-success)](tests/)

A cross-platform desktop application for converting **PDF, PowerPoint, Word, and Excel** files to **clean, high-quality** Markdown optimized for embeddings, RAG pipelines, and NLP tasks.

## 🎉 Current Version: v2.4.4 - UI Update with Copy Button!

**NEW:** Enhanced user interface with Copy button, toast notifications, and simplified stats display! All 4 formats fully supported!

### ✨ What's New in v2.4.4?

📋 **Copy Button**
- One-click copy to clipboard
- Toast notification confirmation
- Seamless workflow integration
- All 4 action buttons: Download | Preview | Copy | Delete

📊 **Simplified Stats**
- Clean single-line statistics display
- "X of Y files converted, Z pages processed"
- Less clutter, more focus on content
- Per-job detailed metrics retained

✨ **Complete Format Support**
- PDF text extraction (PDF.js)
- DOCX full conversion (Mammoth.js)
- PPTX with images/charts/notes (v2.4.3 features)
- XLSX multi-sheet with formulas (v2.4.3 features)

🎨 **Polished User Experience**
- Modern dark theme maintained
- Responsive button layout
- Toast notifications (slide-in/out animations)
- All previous features preserved

---

## 🌐 Web Version (Recommended)

**v2.4.4:** Complete edition with all formats and new UI:
- 📂 **[Download web/index_v2.4.4.html](web/index_v2.4.4.html)** - Latest version! ⭐
- 📋 **Copy Button** - One-click copy to clipboard **NEW!**
- 📊 **Simplified Stats** - Clean single-line display **NEW!**
- 📄 **PDF Support** - Text extraction from PDFs
- 📝 **DOCX Support** - Full Word document conversion
- 🖼️ **PPTX Images** - Extract images with alt text
- 📈 **PPTX Charts** - Convert to markdown tables
- 📝 **Speaker Notes** - Include presenter notes
- 📊 **Excel Multi-Sheet** - Enhanced processing with formulas
- 🔒 100% client-side processing (no uploads)
- ✨ AI structure detection + advanced text cleaning
- 🚀 Run offline after download
- 📱 Works on any OS with modern browser

**Perfect for:**
- Clean text extraction for embeddings
- RAG pipeline document ingestion
- Semantic search indexing
- LLM knowledge base creation
- Academic paper processing
- Financial data extraction (Excel with formulas)
- Healthcare documentation (Word)
- Presentation analysis (PPTX with images/charts)
- Sensitive documents (zero data uploads)

[See web/README.md for details](web/README.md)

---

## ✨ Core Features

### Document Conversion (v2.4.4)
- 📄 **PDF to Markdown** - Clean text extraction with structure detection
- 📊 **PowerPoint to Markdown** - Full image, chart, and notes extraction
- 📝 **Word to Markdown** - Full .docx and .doc support
- 📈 **Excel to Markdown** - Multi-sheet with formula preservation
- 📂 **Drag & Drop Interface** - Simply drop files to convert
- 📦 **Batch Processing Queue** - Convert multiple files with visual progress tracking
- 📋 **Copy to Clipboard** - One-click copy with notification **NEW!**
- 📊 **Simplified Stats** - Clean single-line display **NEW!**

### PPTX Enhancements (v2.4.3+)
- 🖼️ **Image Extraction** - Extract images from media folder with alt text
- 📊 **Chart Conversion** - Convert charts to structured markdown tables
- 📝 **Speaker Notes** - Extract presenter notes per slide
- 🔲 **Shape Grouping** - Handle grouped shapes with spatial sorting
- 🔐 **Base64 Embedding** - Optional self-contained image embedding
- 📊 **Statistics Tracking** - Count images, charts, notes extracted

### Excel Enhancements (v2.4.3+)
- 📄 **Multi-Sheet Headers** - Each sheet clearly labeled
- 🧮 **Formula Preservation** - Formulas shown as `` `=FORMULA()` ``
- 🔗 **Merged Cell Detection** - Report and handle merged cells
- 📊 **Enhanced Statistics** - Track sheets, formulas, merged cells
- 🗑️ **Empty Cell Handling** - Better handling of sparse data
- 📋 **Document Summary** - Overview of entire workbook

### Text Quality (v2.2.1+)
- ✨ **Advanced Text Cleaning** - Fixes ligatures, merged words, spacing
- 📐 **AI Structure Detection** - Font analysis for headers, lists, styling
- 🎓 **Academic Document Support** - Recognizes research paper sections
- 📊 **Structured Table Extraction** - Preserve table data accurately
- 🔗 **Selective Link Preservation** - External links without pollution
- 🧹 **Artifact Removal** - Removes encoding issues, hyphenation breaks

### User Experience (v2.4.4)
- 📋 **Copy to Clipboard** - Quick copy with toast notification **NEW!**
- 📊 **Single-Line Stats** - Clean, focused display **NEW!**
- 🕒 **Automatic Timestamped Naming** - Files organized with date stamps
- 📁 **Organized Folder Structure** - Separate folders for originals and processed files
- 🎨 **Modern Dark Theme UI** - Clean, professional interface
- ⚡ **Standalone Executable** - No installation required, just double-click to run
- 📊 **Quality Metrics** - Text quality, structure score, features extracted

---

## 🖼️ Preview

### Main Interface (v2.4.4)
```
┌──────────────────────────────────────────────────────┐
│    MarkItDown Converter v2.4.4                       │
│    Complete Edition: PDF • DOCX • PPTX • XLSX        │
├──────────────────────────────────────────────────────┤
│  🎉 v2.4.4: New Copy Button + Simplified Stats!     │
│  Now with 4 action buttons: Download, Preview,      │
│  Copy, Delete. All formats supported!                │
├──────────────────────────────────────────────────────┤
│              📁                                       │
│         Drop files here                              │
│    PDF ✨ • DOCX ✨ • PPTX ✨ • XLSX ✨             │
├──────────────────────────────────────────────────────┤
│  2 of 3 files converted, 42 pages processed         │
├──────────────────────────────────────────────────────┤
│  ✔ presentation.pptx      [========] Completed      │
│     → 15 slides • 8 images • 3 charts • 12 notes    │
│  [⬇ Download] [👁 Preview] [📋 Copy] [🗑 Delete]   │
│                                                      │
│  ✔ financial.xlsx         [========] Completed      │
│     → 4 sheets • 45 formulas • 12 merged cells      │
│  [⬇ Download] [👁 Preview] [📋 Copy] [🗑 Delete]   │
└──────────────────────────────────────────────────────┘

           ┌─────────────────────────┐
           │ ✓ Copied to clipboard! │ ← Toast notification
           └─────────────────────────┘
```

---

## 🚀 Quick Start

### Option 1: Web Version (Recommended) ⭐

1. Download [web/index_v2.4.4.html](web/index_v2.4.4.html)
2. Double-click to open in browser
3. Drag & drop PDF/DOCX/PPTX/XLSX files
4. Click "📋 Copy" to copy markdown to clipboard
5. All processing happens locally in your browser!
6. **Best for:** All formats, one-click copy, privacy

### Option 2: Previous Versions

- [web/index_v2.4.3.html](web/index_v2.4.3.html) - PPTX & Excel enhancements
- [web/index_v2.4.0.html](web/index_v2.4.0.html) - Word & Excel support
- [web/index_v2.2.1.html](web/index_v2.2.1.html) - PDF & PPTX only

### Option 3: Run from Source

```bash
# Clone repository
git clone https://github.com/Wei-power3/markitdown-desktop-converter.git
cd markitdown-desktop-converter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python src/main.py
```

**System Dependencies (for table extraction):**
- **Windows**: Install [Ghostscript](https://ghostscript.com/releases/gsdnld.html)
- **macOS**: `brew install ghostscript tcl-tk`
- **Linux**: `sudo apt-get install ghostscript python3-tk`

---

## 📚 Usage Guide

### Basic Workflow (v2.4.4)

1. **Launch Application**
   - Open `web/index_v2.4.4.html` in browser (recommended)
   - Or double-click `MarkItDownConverter.exe`
   - Or run `python src/main.py`

2. **Add Files to Queue**
   - **Method A**: Drag and drop files onto the drop zone
   - **Method B**: Click to browse files
   - **Supported**: PDF, PPTX, PPT, DOCX, DOC, XLSX, XLS

3. **Start Processing**
   - Processing starts automatically (web version)
   - Watch real-time progress and statistics
   - See simplified stats: "X of Y files converted"

4. **Use Results**
   - Click "⬇ Download" to save as .md file
   - Click "👁 Preview" to view in browser
   - Click "📋 Copy" to copy to clipboard **NEW!**
   - See toast notification: "✓ Copied to clipboard!"
   - Click "🗑 Delete" to remove from queue

### File Naming Convention

**Web Version (v2.4.4):**
```
research-presentation_v244.md
financial-report_v244.md
business-plan_v244.md
```

**Desktop Version:**
```
17-02-2026_research-presentation_v2.4.4_clean.md
17-02-2026_financial-report_v2.4.4_clean.md
```

### Folder Structure

```
markitdown-desktop-converter/
├── web/
│   ├── index_v2.4.4.html    # Latest: Copy button + Simplified stats ⭐
│   ├── index_v2.4.3.html    # Previous: Enhanced PPTX & Excel
│   ├── index_v2.4.0.html    # Legacy: Word & Excel
│   ├── js/
│   │   ├── converters/
│   │   │   ├── pdf-converter.js   # PDF text extraction
│   │   │   ├── docx-converter.js  # Word conversion
│   │   │   ├── excel-v243.js      # Enhanced Excel converter
│   │   │   └── pptx-v243.js       # Enhanced PPTX converter
│   │   ├── modules/
│   │   │   ├── pptx-images.js     # Image extraction
│   │   │   ├── pptx-charts.js     # Chart extraction
│   │   │   ├── pptx-notes.js      # Speaker notes
│   │   │   └── pptx-groups.js     # Shape grouping
│   │   └── utils/
│   │       ├── xml-helper.js      # XML parsing
│   │       └── base64-helper.js   # Base64 encoding
│   └── README.md            # Web documentation
├── docs/
│   └── CHANGELOG.md         # Version history
├── tests/
│   ├── unit/               # 25+ Excel unit tests
│   ├── integration/        # 10+ integration tests
│   └── regression/         # 10+ regression tests
├── data/
│   ├── originals/          # Source files with timestamps
│   └── processed/          # Clean Markdown outputs
└── src/                    # Application source code
```

---

## 🎯 Use Cases

### Ideal For:
- ✅ **Embedding generation** (Primary use case)
- ✅ **RAG pipeline ingestion**
- ✅ **Semantic search indexing**
- ✅ **LLM knowledge bases**
- ✅ **Academic paper processing** (PDF)
- ✅ **Financial data with formulas** (Excel)
- ✅ **Presentation analysis** (PPTX with images/charts)
- ✅ **Training material conversion** (PPTX with notes)
- ✅ **Business intelligence** (Excel multi-sheet)
- ✅ **Healthcare documentation** (Word)
- ✅ **Technical documentation** (All formats)
- ✅ **Data visualization extraction** (PPTX charts)
- ✅ **Quick clipboard workflow** (Copy button) **NEW!**

### Quality by Use Case:

| Use Case | v2.4.4 Quality | Key Features |
|----------|----------------|---------------|
| Embedding Generation | ⭐⭐⭐⭐⭐ | All formats, clean text |
| RAG Pipeline | ⭐⭐⭐⭐⭐ | Structured output |
| Presentation Analysis | ⭐⭐⭐⭐⭐ | Images, charts, notes |
| Financial Data | ⭐⭐⭐⭐⭐ | Formulas, multi-sheet |
| Quick Workflow | ⭐⭐⭐⭐⭐ | Copy button **NEW!** |
| Academic Papers | ⭐⭐⭐⭐⭐ | Structure detection |
| Healthcare Docs | ⭐⭐⭐⭐⭐ | PDF, Word support |
| Business Reports | ⭐⭐⭐⭐ | Word, Excel |

---

## 📄 Supported File Formats

| Format | Extension | Quality | v2.4.4 Features |
|--------|-----------|---------|------------------|
| PDF | `.pdf` | ⭐⭐⭐⭐⭐ | Text extraction |
| Word Document | `.docx` | ⭐⭐⭐⭐⭐ | Full conversion |
| Word Legacy | `.doc` | ⭐⭐⭐⭐ | Basic support |
| PowerPoint | `.pptx` | ⭐⭐⭐⭐⭐ | Images, charts, notes |
| PowerPoint Legacy | `.ppt` | ⭐⭐⭐⭐ | Basic support |
| Excel Spreadsheet | `.xlsx` | ⭐⭐⭐⭐⭐ | Multi-sheet, formulas |
| Excel Legacy | `.xls` | ⭐⭐⭐⭐ | Multi-sheet support |

---

## 🧪 Testing & Quality Assurance

### Automated Test Suite

**Excel Tests: 45+ tests**
- ✅ 25+ unit tests (conversion, multi-sheet, data types)
- ✅ 10+ integration tests (end-to-end workflows)
- ✅ 10+ regression tests (quality baselines)

**Running Tests:**
```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
pytest tests/ -v

# Run Excel tests only
pytest tests/ -k "excel" -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

---

## 🧩 Technology Stack

### Web Version (v2.4.4) - Client-Side Only
- **PDF Processing**: [PDF.js](https://mozilla.github.io/pdf.js/) by Mozilla
- **Word Processing**: [Mammoth.js](https://github.com/mwilliamson/mammoth.js)
- **PowerPoint Processing**: [JSZip](https://stuk.github.io/jszip/)
- **Excel Processing**: [SheetJS (XLSX)](https://sheetjs.com/)
- **Image Extraction**: Custom PPTXImageExtractor module
- **Chart Extraction**: Custom PPTXChartExtractor module
- **Notes Extraction**: Custom PPTXNotesExtractor module
- **XML Parsing**: Custom XMLHelper utility
- **Base64 Encoding**: Custom Base64Helper utility
- **Client-Side Only**: Zero server uploads, 100% privacy

### Desktop Application
- **Core Conversion**: [MarkItDown](https://github.com/microsoft/markitdown) by Microsoft
- **GUI Framework**: CustomTkinter
- **Drag-and-Drop**: TkinterDnD2
- **Table Extraction**: Camelot + Tabula
- **Packaging**: PyInstaller

---

## 💻 System Requirements

### Web Version (v2.4.4)
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **RAM**: 2 GB available (4 GB for large PPTX with images)
- **JavaScript**: Must be enabled
- **Storage**: Temp space for file processing
- **Works**: Windows, macOS, Linux, ChromeOS

### Desktop Application
- **OS**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 20.04+)
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 500 MB
- **Python** (for source): 3.10 or higher
- **Ghostscript**: Required for PDF table extraction

---

## 🛣️ Roadmap

### v2.4.4 (Current) - UI Update ✅
- [x] Copy to clipboard button
- [x] Toast notification for copy action
- [x] Simplified single-line stats
- [x] PDF support (PDF.js)
- [x] DOCX support (Mammoth.js)
- [x] All v2.4.3 PPTX features
- [x] All v2.4.3 Excel features
- [x] 4-button action layout

### v2.5.0 (Planned) - Integration & Testing
- [ ] Integrate v2.4.2 PPTX table/list fixes
- [ ] Word document automated tests
- [ ] PPTX automated test suite
- [ ] Image preview thumbnails
- [ ] Chart preview visualization
- [ ] Export images as separate files (ZIP)
- [ ] CI/CD with GitHub Actions

### v3.0 (Future) - AI Intelligence
- [ ] Figure/image description generation (AI)
- [ ] OCR for scanned documents
- [ ] Chart data extraction from images
- [ ] Automatic content summarization
- [ ] Multi-language support

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CHANGELOG.md](docs/CHANGELOG.md) for recent changes.

---

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## 🙏 Acknowledgments

- **Microsoft AutoGen Team** - [MarkItDown](https://github.com/microsoft/markitdown) library
- **Mozilla** - PDF.js for web version
- **Mammoth Team** - Word conversion
- **SheetJS Team** - Excel conversion
- **JSZip Team** - PowerPoint ZIP handling
- **Camelot/Tabula Teams** - Table extraction
- **CustomTkinter** - Modern UI framework
- The research/NLP community for quality testing and feedback

---

## 📧 Support

For issues, questions, or feature requests:
- Open an issue: [GitHub Issues](https://github.com/Wei-power3/markitdown-desktop-converter/issues)
- View documentation: [docs/](docs/)
- Web version docs: [web/README.md](web/README.md)
- Changelog: [docs/CHANGELOG.md](docs/CHANGELOG.md)

---

**Made with ♥️ by Wei-power3**

**Version 2.4.4** - Copy Button + Simplified Stats + All Formats

[Report Bug](https://github.com/Wei-power3/markitdown-desktop-converter/issues) · [Request Feature](https://github.com/Wei-power3/markitdown-desktop-converter/issues) · [Try v2.4.4](web/index_v2.4.4.html) · [View Docs](docs/) · [Run Tests](tests/)
