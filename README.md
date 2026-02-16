# MarkItDown Desktop Converter

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://www.microsoft.com/windows)
[![Version](https://img.shields.io/badge/version-2.4.0-brightgreen)](https://github.com/Wei-power3/markitdown-desktop-converter/releases)
[![Tests](https://img.shields.io/badge/tests-45%2B%20Excel%20tests-success)](tests/)

A cross-platform desktop application for converting **PDF, PowerPoint, Word, and Excel** files to **clean, high-quality** Markdown optimized for embeddings, RAG pipelines, and NLP tasks.

## 🎉 Current Version: v2.4.0 - Word & Excel Support!

**NEW:** Full support for Word documents and Excel spreadsheets!

### What's New in v2.4.0?

✨ **Word Document Support (.docx, .doc)**
- Convert Word documents to clean markdown
- Preserve formatting (bold, italic, headers)
- Extract hyperlinks from documents
- Multi-page document handling
- Legacy .doc format support

📊 **Excel Spreadsheet Support (.xlsx, .xls)**
- Convert spreadsheets to markdown tables
- Multi-sheet handling with sheet names
- Cell data preservation
- Formula results displayed
- Legacy .xls format support

🧪 **45+ Automated Tests**
- Comprehensive test suite for Excel conversion
- Unit tests, integration tests, regression tests
- Quality assurance for all formats

✅ **Everything from v2.2.1**
- Clean text extraction for embeddings
- AI structure detection
- Advanced text cleaning
- Link preservation
- Table extraction

---

## 🌐 Web Version (Recommended)

**NEW v2.4.0:** Browser-based converter with Word & Excel support:
- 📂 **[Download web/index_v2.4.0.html](web/index_v2.4.0.html)** - Latest version
- 📄 **Word Documents** - .docx and .doc support
- 📊 **Excel Spreadsheets** - .xlsx and .xls support
- 📑 **PDF & PowerPoint** - Full support as before
- 🔒 100% client-side processing (no uploads)
- ✨ AI structure detection + advanced text cleaning
- 🚀 Run offline after download
- 📱 Works on any OS with modern browser
- 📊 Quality metrics with scoring

**Perfect for:**
- Clean text extraction for embeddings
- RAG pipeline document ingestion
- Semantic search indexing
- LLM knowledge base creation
- Academic paper processing
- Financial data extraction (Excel)
- Healthcare documentation (Word)
- Sensitive documents (zero data uploads)

[See web/README.md for details](web/README.md)

---

## ✨ Core Features

### Document Conversion (v2.4.0)
- 📄 **PDF to Markdown** - Clean text extraction with structure detection
- 📊 **PowerPoint to Markdown** - Dual conversion pathways
- 📝 **Word to Markdown** - Full .docx and .doc support **NEW!**
- 📈 **Excel to Markdown** - Multi-sheet spreadsheet conversion **NEW!**
- 📂 **Drag & Drop Interface** - Simply drop files to convert
- 📦 **Batch Processing Queue** - Convert multiple files with visual progress tracking

### Text Quality (v2.2.1+)
- ✨ **Advanced Text Cleaning** - Fixes ligatures, merged words, spacing
- 📐 **AI Structure Detection** - Font analysis for headers, lists, styling
- 🎓 **Academic Document Support** - Recognizes research paper sections
- 📊 **Structured Table Extraction** - Preserve table data accurately
- 🔗 **Selective Link Preservation** - External links without pollution
- 🧹 **Artifact Removal** - Removes encoding issues, hyphenation breaks

### User Experience
- 🕒 **Automatic Timestamped Naming** - Files organized with date stamps
- 📁 **Organized Folder Structure** - Separate folders for originals and processed files
- 🎨 **Modern Dark Theme UI** - Clean, professional interface
- ⚡ **Standalone Executable** - No installation required, just double-click to run
- 📊 **Quality Metrics** - Text quality, structure score, links preserved

---

## 🖼️ Preview

### Main Interface with Batch Queue
```
┌──────────────────────────────────────────────────────┐
│    MarkItDown Desktop Converter v2.4.0                │
│    PDF • PPTX • Word • Excel to Markdown              │
├──────────────────────────────────────────────────────┤
│              📁                                       │
│         Drop files here                              │
│    PDF, PPTX, DOCX, XLSX                             │
├──────────────────────────────────────────────────────┤
│  Processing Queue (4 files)                         │
├──────────────────────────────────────────────────────┤
│  ✔ research-paper.pdf     [========] Complete      │
│     → Text: 95% • Structure: 85% • Overall: 91%     │
│  ✔ financial-model.xlsx   [========] Complete      │
│     → 4 sheets • 1,234 rows • 45 columns            │
│  ⏳ report.docx           [====----] Processing   │
│  ⏸ presentation.pptx      [--------] Queued       │
├──────────────────────────────────────────────────────┤
│ [▶ Start] [Clear] [Originals] [Processed]       │
└──────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Option 1: Web Version (Recommended)

1. Download [web/index_v2.4.0.html](web/index_v2.4.0.html)
2. Double-click to open in browser
3. Drag & drop PDFs, Word docs, Excel files - all processing happens locally!
4. **Best for:** Clean embeddings, NLP tasks, all platforms

### Option 2: Download Standalone Executable

1. Go to [Releases](https://github.com/Wei-power3/markitdown-desktop-converter/releases)
2. Download `MarkItDownConverter_v2.4.0.exe`
3. Download and install [Ghostscript](https://ghostscript.com/releases/gsdnld.html) (required for table extraction)
4. Double-click to run - that's it!

### Option 3: Run from Source

```bash
# Clone repository
git clone https://github.com/Wei-power3/markitdown-desktop-converter.git
cd markitdown-desktop-converter

# Checkout v2.4.0
git checkout feature/add-word-excel-support

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

### Basic Workflow

1. **Launch Application**
   - Double-click `MarkItDownConverter.exe` or run `python src/main.py`
   - Or use web version: open `web/index_v2.4.0.html` in browser

2. **Add Files to Queue**
   - **Method A**: Drag and drop files onto the drop zone
   - **Method B**: Click "Browse Files" button
   - **Supported**: PDF, PPTX, PPT, DOCX, DOC, XLSX, XLS

3. **Start Processing**
   - Click "▶ Start Processing" button
   - Watch real-time progress in the queue
   - See quality metrics: text quality, structure score, overall

4. **Access Converted Files**
   - Click "📂 Originals Folder" to see source files
   - Click "📄 Processed Folder" to see clean Markdown outputs
   - Web version: Download directly from browser

### File Naming Convention

**Original Files:**
```
16-02-2026_research-paper_original.pdf
16-02-2026_financial-report_original.xlsx
16-02-2026_document_original.docx
```

**Markdown Files:**
```
16-02-2026_research-paper_v2.4.0_clean.md
16-02-2026_financial-report_v2.4.0_clean.md
16-02-2026_document_v2.4.0_clean.md
```

Format: `{day}-{month}-{year}_{filename}_v2.4.0_clean.md`

### Folder Structure

```
markitdown-desktop-converter/
├── web/
│   ├── index_v2.4.0.html    # Latest version with Word & Excel
│   ├── index_v2.2.1.html    # Previous stable version
│   ├── VERSION_NOTES.md     # Detailed version comparison
│   └── README.md            # Web version documentation
├── tests/
│   ├── unit/
│   │   └── test_excel_conversion.py  # 25+ Excel unit tests
│   ├── integration/
│   │   └── test_excel_workflow.py    # 10+ Excel integration tests
│   ├── regression/
│   │   └── test_excel_regression.py  # 10+ Excel regression tests
│   └── fixtures/
│       └── sample_excel/             # Real-world Excel test files
├── data/
│   ├── originals/       # Your source files with timestamps
│   └── processed/       # Clean Markdown optimized for embeddings
├── src/                 # Application source code
│   ├── text_cleaner.py  # Text cleaning engine
│   ├── converter.py     # Enhanced converter with Word/Excel support
│   └── ...
└── MarkItDownConverter.exe  # Standalone executable
```

---

## ⚙️ Features in Detail

### 📝 Word Document Conversion (NEW in v2.4.0)

**Supported Formats:** .docx, .doc

**What Gets Converted:**
- ✅ Plain text content
- ✅ Headers and headings (H1, H2, H3)
- ✅ Bold and italic formatting
- ✅ Bulleted and numbered lists
- ✅ Hyperlinks (preserved as markdown links)
- ✅ Tables (converted to markdown tables)
- ✅ Multi-page documents
- ✅ Text cleaning applied for quality

**Example:**

**Input (Word):**
```
Heading 1
This is bold text and this is italic.

• Bullet point 1
• Bullet point 2

Visit our website for more info.
```

**Output (Markdown):**
```markdown
# Heading 1

This is **bold text** and this is *italic*.

- Bullet point 1
- Bullet point 2

[Visit our website](https://example.com) for more info.
```

### 📊 Excel Spreadsheet Conversion (NEW in v2.4.0)

**Supported Formats:** .xlsx, .xls

**What Gets Converted:**
- ✅ All sheets in workbook
- ✅ Sheet names preserved
- ✅ Cell values (numbers, text, dates)
- ✅ Formula results (not formulas themselves)
- ✅ Empty cells handled gracefully
- ✅ Multiple data types
- ✅ Large datasets (1000+ rows)
- ✅ Text cleaning applied to cell values

**Example:**

**Input (Excel):**
```
Sheet: Financial Summary

| Quarter | Revenue | Expenses | Profit |
| Q1 2024 | $500,000 | $300,000 | $200,000 |
| Q2 2024 | $550,000 | $320,000 | $230,000 |
```

**Output (Markdown):**
```markdown
# financial-report.xlsx

Converted from Excel • v2.4.0 • 2 sheet(s)

---

## Sheet: Financial Summary

| Quarter | Revenue | Expenses | Profit |
|---------|---------|----------|--------|
| Q1 2024 | 500000 | 300000 | 200000 |
| Q2 2024 | 550000 | 320000 | 230000 |

## Sheet: Details

...
```

### ✨ Advanced Text Cleaning (v2.2.1)

Fixes common extraction artifacts for clean embeddings:

**Spaced Ligatures:**
- Before: `arti fi cial intelligence for identi fi cation`
- After: `artificial intelligence for identification`

**Merged Words:**
- Before: `transmitted onascale representamajor improvement`
- After: `transmitted on a scale represent a major improvement`

**Legacy Artifacts:**
- Hyphenation breaks: `non- invasive` → `non-invasive`
- Medical terms: NT-proBNP, β-blockers, HbA1c preserved
- Special characters: ±, μ, ≥, ≤, → handled correctly

### 📐 AI Structure Detection (v2.1.0)

Automatically analyzes document structure using font size intelligence:

**How It Works:**
1. **Font Size Analysis**: Scans entire document to calculate average font size
2. **Relative Sizing**: Determines header levels based on size ratios
   - Font ≥ 1.8× average = H1 (# Header)
   - Font ≥ 1.5× average = H2 (## Header)
   - Font ≥ 1.2× average = H3 (### Header)
3. **Academic Keywords**: Promotes recognized section names (Abstract, Methods, etc.)
4. **List Detection**: Identifies bullet/numbered lists by pattern matching
5. **Style Preservation**: Extracts bold/italic from font names

**Result**: Structure score jumps from 33% to 75% for research papers! 🚀

---

## 🎯 Use Cases

### Ideal For:
- ✅ **Embedding generation** (Primary use case)
- ✅ **RAG pipeline ingestion**
- ✅ **Semantic search indexing**
- ✅ **LLM knowledge bases**
- ✅ **Academic paper processing** (PDF)
- ✅ **Financial data extraction** (Excel) **NEW!**
- ✅ **Healthcare documentation** (Word) **NEW!**
- ✅ **Business reports** (Word + Excel) **NEW!**
- ✅ **Scientific literature review** (PDF)
- ✅ **Medical documentation** (PDF + Word)
- ✅ **Technical documentation** (All formats)
- ✅ **Data analysis preparation** (Excel) **NEW!**

### Quality by Use Case:

| Use Case | v2.4.0 Quality | Formats |
|----------|----------------|----------|
| Embedding Generation | ⭐⭐⭐⭐⭐ | All formats |
| RAG Pipeline Ingestion | ⭐⭐⭐⭐⭐ | All formats |
| Semantic Search Indexing | ⭐⭐⭐⭐⭐ | All formats |
| LLM Knowledge Base | ⭐⭐⭐⭐⭐ | All formats |
| Academic Papers | ⭐⭐⭐⭐⭐ | PDF |
| Financial Data | ⭐⭐⭐⭐⭐ | Excel **NEW!** |
| Healthcare Docs | ⭐⭐⭐⭐⭐ | PDF, Word **NEW!** |
| Business Reports | ⭐⭐⭐⭐ | Word, Excel **NEW!** |
| Technical Documentation | ⭐⭐⭐⭐ | All formats |

---

## 📄 Supported File Formats

| Format | Extension | Quality | Notes |
|--------|-----------|---------|-------|
| PDF | `.pdf` | ⭐⭐⭐⭐⭐ | Full support, clean text extraction |
| PowerPoint | `.pptx` | ⭐⭐⭐⭐ | Link preservation, structure detection |
| PowerPoint Legacy | `.ppt` | ⭐⭐⭐⭐ | Link preservation, structure detection |
| **Word Document** | `.docx` | ⭐⭐⭐⭐⭐ | **NEW!** Formatting preservation, hyperlinks |
| **Word Legacy** | `.doc` | ⭐⭐⭐⭐ | **NEW!** Formatting preservation |
| **Excel Spreadsheet** | `.xlsx` | ⭐⭐⭐⭐⭐ | **NEW!** Multi-sheet, all data types |
| **Excel Legacy** | `.xls` | ⭐⭐⭐⭐ | **NEW!** Multi-sheet support |

---

## 🧪 Testing & Quality Assurance

### Automated Test Suite (NEW in v2.4.0)

**Excel Tests: 45+ tests**
- ✅ 25+ unit tests (basic conversion, multi-sheet, data types, error handling)
- ✅ 10+ integration tests (end-to-end workflows, batch processing)
- ✅ 10+ regression tests (quality baselines, deterministic output)

**Test Coverage:**
- Unit tests: `tests/unit/test_excel_conversion.py`
- Integration tests: `tests/integration/test_excel_workflow.py`
- Regression tests: `tests/regression/test_excel_regression.py`
- Real-world fixtures: `tests/fixtures/sample_excel/`

**Running Tests:**
```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all Excel tests
pytest tests/ -k "excel" -v

# Run specific test category
pytest tests/unit/test_excel_conversion.py -v
pytest tests/integration/test_excel_workflow.py -v
pytest tests/regression/test_excel_regression.py -v

# Run with coverage
pytest tests/ -k "excel" --cov=src --cov-report=html
```

---

## 🧩 Technology Stack

### Desktop Application
- **Core Conversion**: [MarkItDown](https://github.com/microsoft/markitdown) by Microsoft
- **Structure Detection**: Custom font analysis
- **Text Cleaning**: Custom regex-based engine
- **Link Extraction**: Custom PDF.js-based extraction
- **Table Extraction**: [Camelot](https://camelot-py.readthedocs.io/) + [Tabula](https://tabula-py.readthedocs.io/)
- **GUI Framework**: CustomTkinter
- **Drag-and-Drop**: TkinterDnD2
- **PDF Generation**: ReportLab
- **PowerPoint Processing**: python-pptx
- **Packaging**: PyInstaller

### Web Version (v2.4.0)
- **PDF Processing**: [PDF.js](https://mozilla.github.io/pdf.js/) by Mozilla
- **PowerPoint Processing**: [JSZip](https://stuk.github.io/jszip/)
- **Word Processing**: [Mammoth.js](https://github.com/mwilliamson/mammoth.js) **NEW!**
- **Excel Processing**: [SheetJS (XLSX)](https://sheetjs.com/) **NEW!**
- **Structure Detection**: JavaScript port of algorithms
- **Text Cleaning**: JavaScript port of algorithms
- **Client-Side Only**: Zero server uploads

---

## 🐛 Troubleshooting

### Word Conversion Issues

**Issue**: Word document not converting

**Solution**:
1. Ensure using .docx or .doc format
2. Check file is not password-protected
3. Try opening in Word and re-saving
4. Check console logs for detailed errors

### Excel Conversion Issues

**Issue**: Excel spreadsheet not converting

**Solution**:
1. Ensure using .xlsx or .xls format
2. Check file is not password-protected
3. Very large files (10MB+) may take longer
4. Check console logs for detailed errors

### Table Extraction Fails (PDF)

**Issue**: "Camelot not available" or table extraction errors

**Solution**:
1. Install Ghostscript: https://ghostscript.com/releases/gsdnld.html
2. Ensure Ghostscript is in system PATH
3. Restart application after installing
4. Check console for detailed error messages

### Web Version Issues

**Issue**: Web version not working in browser

**Solution**:
1. Ensure JavaScript is enabled
2. Use modern browser (Chrome 90+, Firefox 88+, Safari 14+)
3. Check browser console for errors (F12)
4. Try different browser
5. Clear browser cache

---

## 💻 System Requirements

### Desktop Application
- **OS**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 20.04+)
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 500 MB
- **Python** (for source): 3.10 or higher
- **Ghostscript**: Required for PDF table extraction ([Download](https://ghostscript.com/))

### Web Version
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **RAM**: 2 GB available
- **JavaScript**: Must be enabled
- **Works**: Windows, macOS, Linux, ChromeOS

---

## 🛣️ Roadmap

### v2.4.0 (Current) - Word & Excel Support ✅
- [x] Word document conversion (.docx, .doc)
- [x] Excel spreadsheet conversion (.xlsx, .xls)
- [x] 45+ automated Excel tests
- [x] Web version with Word & Excel support
- [x] Clean text extraction for all formats
- [x] Multi-sheet Excel handling
- [x] Hyperlink preservation in Word

### v2.5.0 (Future) - Enhanced Testing
- [ ] Word document automated tests (30+ tests)
- [ ] PDF regression test suite
- [ ] PowerPoint automated tests
- [ ] CI/CD integration with GitHub Actions
- [ ] Automated quality benchmarking

### v3.0 (Future) - Visual Intelligence
- [ ] Figure/image extraction
- [ ] AI-powered figure descriptions
- [ ] OCR for scanned documents
- [ ] Chart data extraction from images

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## 🙏 Acknowledgments

- **Microsoft AutoGen Team** - [MarkItDown](https://github.com/microsoft/markitdown) library
- **Mammoth Team** - [Mammoth.js](https://github.com/mwilliamson/mammoth.js) for Word conversion
- **SheetJS Team** - [XLSX](https://sheetjs.com/) for Excel conversion
- **Camelot Team** - Advanced table extraction
- **Tabula Team** - PDF table parsing
- **Mozilla** - PDF.js for web version
- **CustomTkinter** - Modern UI framework
- **PyInstaller** - Executable packaging
- The research/NLP community for quality testing and feedback

---

## 📧 Support

For issues, questions, or feature requests:
- Open an issue: [GitHub Issues](https://github.com/Wei-power3/markitdown-desktop-converter/issues)
- Check documentation: [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)
- View changelog: [CHANGELOG.md](CHANGELOG.md)
- Web version docs: [web/README.md](web/README.md)
- Test documentation: [tests/README.md](tests/README.md)

---

**Made with ♥️ by Wei-power3**

**Version 2.4.0** - Word & Excel Support for Comprehensive Document Conversion

[Report Bug](https://github.com/Wei-power3/markitdown-desktop-converter/issues) · [Request Feature](https://github.com/Wei-power3/markitdown-desktop-converter/issues) · [View Changelog](CHANGELOG.md) · [Try Web Version](web/index_v2.4.0.html) · [Run Tests](tests/)
