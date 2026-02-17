# MarkItDown Desktop Converter

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://www.microsoft.com/windows)
[![Version](https://img.shields.io/badge/version-2.4.3-orange)](https://github.com/Wei-power3/markitdown-desktop-converter/releases)
[![Tests](https://img.shields.io/badge/tests-45%2B%20Excel%20tests-success)](tests/)

A cross-platform desktop application for converting **PDF, PowerPoint, Word, and Excel** files to **clean, high-quality** Markdown optimized for embeddings, RAG pipelines, and NLP tasks.

## 🎉 Current Version: v2.4.3 - Enhanced PPTX & Excel!

**NEW:** Advanced PPTX features with images, charts, and speaker notes extraction! Plus enhanced Excel multi-sheet processing!

### ✨ What's New in v2.4.3?

🖼️ **PPTX Image Extraction**
- Extract images from PowerPoint presentations
- Preserve alt text from slide XML
- Base64 embedding option for self-contained markdown
- Support for all image formats (PNG, JPEG, GIF, etc.)

📊 **PPTX Chart Extraction**
- Convert PowerPoint charts to markdown tables
- Support for 8+ chart types (bar, line, pie, area, scatter, radar, etc.)
- Extract series data and category labels
- Preserve chart metadata and structure

📝 **PPTX Speaker Notes**
- Extract speaker notes from each slide
- Per-slide caching for performance
- Search and filter notes
- Clean markdown formatting

📈 **Enhanced Excel Processing**
- Multi-sheet processing with sheet name headers
- Formula preservation (displayed as markdown code)
- Merged cell detection and reporting
- Enhanced statistics (sheets, formulas, merged cells)
- Better empty cell handling
- Document summary generation

🎛️ **Configurable Options**
- Toggle image extraction on/off
- Toggle chart extraction on/off
- Toggle speaker notes inclusion
- Choose base64 embedding or links
- Control metadata output

📊 **Comprehensive Statistics**
- Track images, charts, notes extracted
- Monitor processing time
- Quality metrics per file
- Real-time progress indicators

---

## 🌐 Web Version (Recommended)

**NEW v2.4.3:** Browser-based converter with enhanced PPTX & Excel features:
- 📂 **[Download web/index_v2.4.3.html](web/index_v2.4.3.html)** - Latest version with all features!
- 🖼️ **PPTX Images** - Extract images with alt text **NEW!**
- 📊 **PPTX Charts** - Convert to markdown tables **NEW!**
- 📝 **Speaker Notes** - Include presenter notes **NEW!**
- 📈 **Excel Multi-Sheet** - Enhanced processing with formulas **NEW!**
- 🔧 **Feature Toggles** - Enable/disable features as needed **NEW!**
- 📄 **Word Documents** - .docx and .doc support
- 📑 **PDF Support** - Clean text extraction
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

### Document Conversion (v2.4.3)
- 📄 **PDF to Markdown** - Clean text extraction with structure detection
- 📊 **PowerPoint to Markdown** - Full image, chart, and notes extraction **ENHANCED!**
- 📝 **Word to Markdown** - Full .docx and .doc support
- 📈 **Excel to Markdown** - Multi-sheet with formula preservation **ENHANCED!**
- 📂 **Drag & Drop Interface** - Simply drop files to convert
- 📦 **Batch Processing Queue** - Convert multiple files with visual progress tracking
- ⚙️ **Configurable Options** - Toggle features on/off **NEW!**

### PPTX Enhancements (v2.4.3) 🆕
- 🖼️ **Image Extraction** - Extract images from media folder with alt text
- 📊 **Chart Conversion** - Convert charts to structured markdown tables
- 📝 **Speaker Notes** - Extract presenter notes per slide
- 🔲 **Shape Grouping** - Handle grouped shapes with spatial sorting
- 🔐 **Base64 Embedding** - Optional self-contained image embedding
- 📊 **Statistics Tracking** - Count images, charts, notes extracted

### Excel Enhancements (v2.4.3) 🆕
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

### User Experience
- 🕒 **Automatic Timestamped Naming** - Files organized with date stamps
- 📁 **Organized Folder Structure** - Separate folders for originals and processed files
- 🎨 **Modern Dark Theme UI** - Clean, professional interface
- ⚡ **Standalone Executable** - No installation required, just double-click to run
- 📊 **Quality Metrics** - Text quality, structure score, features extracted

---

## 🖼️ Preview

### Main Interface with Feature Toggles (v2.4.3)
```
┌──────────────────────────────────────────────────────┐
│    MarkItDown Converter v2.4.3                       │
│    Enhanced Excel & PPTX - Images, Charts, Notes     │
├──────────────────────────────────────────────────────┤
│  ⚙️ Conversion Options                               │
│  ☑ Extract Images         ☑ Extract Charts          │
│  ☑ Speaker Notes          ☑ Embed as Base64         │
│  ☑ Include Metadata                                  │
├──────────────────────────────────────────────────────┤
│              📁                                       │
│         Drop files here                              │
│    PPTX ✨ • XLSX ✨ • PDF • DOCX                   │
├──────────────────────────────────────────────────────┤
│  Statistics: 12 files • 47 images • 8 charts         │
├──────────────────────────────────────────────────────┤
│  ✔ presentation.pptx      [========] Complete      │
│     → 15 slides • 8 images • 3 charts • 12 notes    │
│  ✔ financial.xlsx         [========] Complete      │
│     → 4 sheets • 45 formulas • 12 merged cells      │
│  ⏳ report.docx           [====----] Processing   │
└──────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Option 1: Web Version (Recommended) ⭐

1. Download [web/index_v2.4.3.html](web/index_v2.4.3.html)
2. Double-click to open in browser
3. Configure options (images, charts, notes)
4. Drag & drop PPTX/Excel/Word/PDF files
5. All processing happens locally in your browser!
6. **Best for:** Enhanced PPTX/Excel, all platforms, privacy

### Option 2: Previous Stable Version

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

### Basic Workflow (v2.4.3)

1. **Launch Application**
   - Open `web/index_v2.4.3.html` in browser (recommended)
   - Or double-click `MarkItDownConverter.exe`
   - Or run `python src/main.py`

2. **Configure Options** (Web version)
   - ☑️ Extract Images - Get images from PPTX with alt text
   - ☑️ Extract Charts - Convert PPTX charts to markdown tables
   - ☑️ Speaker Notes - Include presenter notes
   - ☑️ Embed as Base64 - Self-contained markdown (larger files)
   - ☑️ Include Metadata - Show conversion statistics

3. **Add Files to Queue**
   - **Method A**: Drag and drop files onto the drop zone
   - **Method B**: Click to browse files
   - **Supported**: PDF, PPTX, PPT, DOCX, DOC, XLSX, XLS

4. **Start Processing**
   - Processing starts automatically (web version)
   - Watch real-time progress and statistics
   - See metrics: images, charts, notes, sheets, formulas

5. **Download Results**
   - Click "⬇ Download Markdown" button
   - Files saved with `_v243.md` suffix
   - Or click "👁 Preview" to view in browser

### File Naming Convention

**Web Version (v2.4.3):**
```
research-presentation_v243.md
financial-report_v243.md
business-plan_v243.md
```

**Desktop Version:**
```
16-02-2026_research-presentation_v2.4.3_clean.md
16-02-2026_financial-report_v2.4.3_clean.md
```

### Folder Structure

```
markitdown-desktop-converter/
├── web/
│   ├── index_v2.4.3.html    # Latest: Enhanced PPTX & Excel ⭐
│   ├── index_v2.4.0.html    # Previous: Word & Excel
│   ├── index_v2.2.1.html    # Legacy: PDF & PPTX only
│   ├── js/
│   │   ├── converters/
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
│   ├── VERSION_NOTES.md     # Version comparison
│   └── README.md            # Web documentation
├── docs/
│   ├── v2.4.3-progress.md         # Implementation log
│   └── v2.4.3-implementation-guide.md  # Technical details
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

## ⚙️ Features in Detail

### 🖼️ PPTX Image Extraction (NEW in v2.4.3)

**What Gets Extracted:**
- ✅ All images from `ppt/media/` folder
- ✅ Alt text from slide XML (`p:cNvPr descr` attribute)
- ✅ Image metadata (size, format, dimensions)
- ✅ Slide-to-image mapping
- ✅ Base64 encoding option
- ✅ Statistics (total images, images per slide)

**Example:**

**Input (PPTX):**
```
Slide 1:
- Title: Product Overview
- Image: product-photo.png (Alt text: "Red smartphone with curved display")
```

**Output (Markdown):**
```markdown
## Slide 1

### Product Overview

### Images

![Red smartphone with curved display](data:image/png;base64,iVBOR...)
*Size: 245.3 KB*
```

### 📊 PPTX Chart Extraction (NEW in v2.4.3)

**Supported Chart Types:**
- ✅ Bar charts (horizontal/vertical)
- ✅ Line charts
- ✅ Pie charts
- ✅ Area charts
- ✅ Scatter plots
- ✅ Radar charts
- ✅ Combo charts (mixed types)
- ✅ Multi-series charts

**What Gets Converted:**
- ✅ Chart title
- ✅ Series names and data
- ✅ Category labels (X-axis)
- ✅ Values (Y-axis)
- ✅ Multiple data series
- ✅ Formatted as markdown tables

**Example:**

**Input (PPTX Chart):**
```
Chart: Quarterly Revenue
Type: Bar Chart

Series: Revenue
Q1: $500,000
Q2: $550,000
Q3: $600,000
Q4: $650,000
```

**Output (Markdown):**
```markdown
### Chart: Quarterly Revenue

**Type:** Bar Chart

| Category | Revenue |
|----------|----------|
| Q1 | 500000 |
| Q2 | 550000 |
| Q3 | 600000 |
| Q4 | 650000 |

*Chart contains 1 series with 4 data points*
```

### 📝 PPTX Speaker Notes (NEW in v2.4.3)

**What Gets Extracted:**
- ✅ Speaker notes from each slide
- ✅ Clean text (no XML artifacts)
- ✅ Per-slide organization
- ✅ Search and filter capability
- ✅ Statistics (slides with notes)

**Example:**

**Input (PPTX with Notes):**
```
Slide 1: Introduction
Notes: "Welcome the audience. Mention the agenda. Allow 2 minutes for questions."

Slide 2: Overview
Notes: "Emphasize the key benefits. Show demo if time permits."
```

**Output (Markdown):**
```markdown
## Slide 1: Introduction

[slide content]

### 📝 Speaker Notes

Welcome the audience. Mention the agenda. Allow 2 minutes for questions.

---

## Slide 2: Overview

[slide content]

### 📝 Speaker Notes

Emphasize the key benefits. Show demo if time permits.
```

### 📈 Enhanced Excel Processing (v2.4.3)

**Supported Formats:** .xlsx, .xls

**What Gets Converted:**
- ✅ All sheets in workbook with clear headers
- ✅ Sheet names preserved
- ✅ Cell values (numbers, text, dates)
- ✅ **Formulas preserved** as markdown code (NEW!)
- ✅ **Merged cells detected** and reported (NEW!)
- ✅ Empty cells handled gracefully
- ✅ Multiple data types
- ✅ **Enhanced statistics** (sheets, formulas, merged cells) (NEW!)
- ✅ **Document summary** at the beginning (NEW!)

**Example:**

**Input (Excel):**
```
Sheet: Financial Summary

| Quarter | Revenue | Expenses | Profit (Formula: =B2-C2) |
| Q1 2024 | $500,000 | $300,000 | $200,000 |
| Q2 2024 | $550,000 | $320,000 | $230,000 |
```

**Output (Markdown):**
```markdown
# financial-report.xlsx

Converted with MarkItDown v2.4.3

**Summary:**
- Total Sheets: 2
- Formulas: 8
- Merged Cells: 3

---

## Sheet: Financial Summary

| Quarter | Revenue | Expenses | Profit |
|---------|---------|----------|--------|
| Q1 2024 | 500000 | 300000 | 200000 `=B2-C2` |
| Q2 2024 | 550000 | 320000 | 230000 `=B3-C3` |

*Formulas preserved as markdown code*
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

---

## 🎯 Use Cases

### Ideal For:
- ✅ **Embedding generation** (Primary use case)
- ✅ **RAG pipeline ingestion**
- ✅ **Semantic search indexing**
- ✅ **LLM knowledge bases**
- ✅ **Academic paper processing** (PDF)
- ✅ **Financial data with formulas** (Excel) **ENHANCED!**
- ✅ **Presentation analysis** (PPTX with images/charts) **NEW!**
- ✅ **Training material conversion** (PPTX with notes) **NEW!**
- ✅ **Business intelligence** (Excel multi-sheet) **ENHANCED!**
- ✅ **Healthcare documentation** (Word)
- ✅ **Technical documentation** (All formats)
- ✅ **Data visualization extraction** (PPTX charts) **NEW!**

### Quality by Use Case:

| Use Case | v2.4.3 Quality | Key Features |
|----------|----------------|---------------|
| Embedding Generation | ⭐⭐⭐⭐⭐ | All formats, clean text |
| RAG Pipeline | ⭐⭐⭐⭐⭐ | Structured output |
| Presentation Analysis | ⭐⭐⭐⭐⭐ | Images, charts, notes **NEW!** |
| Financial Data | ⭐⭐⭐⭐⭐ | Formulas, multi-sheet **NEW!** |
| Training Materials | ⭐⭐⭐⭐⭐ | Speaker notes **NEW!** |
| Academic Papers | ⭐⭐⭐⭐⭐ | Structure detection |
| Healthcare Docs | ⭐⭐⭐⭐⭐ | PDF, Word support |
| Business Reports | ⭐⭐⭐⭐ | Word, Excel |

---

## 📄 Supported File Formats

| Format | Extension | Quality | v2.4.3 Features |
|--------|-----------|---------|------------------|
| PDF | `.pdf` | ⭐⭐⭐⭐⭐ | Full support, clean text |
| PowerPoint | `.pptx` | ⭐⭐⭐⭐⭐ | **Images, charts, notes** ✨ |
| PowerPoint Legacy | `.ppt` | ⭐⭐⭐⭐ | Basic support |
| Word Document | `.docx` | ⭐⭐⭐⭐⭐ | Formatting, hyperlinks |
| Word Legacy | `.doc` | ⭐⭐⭐⭐ | Basic support |
| Excel Spreadsheet | `.xlsx` | ⭐⭐⭐⭐⭐ | **Multi-sheet, formulas** ✨ |
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

### Web Version (v2.4.3) - Client-Side Only
- **PDF Processing**: [PDF.js](https://mozilla.github.io/pdf.js/) by Mozilla
- **PowerPoint Processing**: [JSZip](https://stuk.github.io/jszip/)
- **Word Processing**: [Mammoth.js](https://github.com/mwilliamson/mammoth.js)
- **Excel Processing**: [SheetJS (XLSX)](https://sheetjs.com/)
- **Image Extraction**: Custom PPTXImageExtractor module **NEW!**
- **Chart Extraction**: Custom PPTXChartExtractor module **NEW!**
- **Notes Extraction**: Custom PPTXNotesExtractor module **NEW!**
- **XML Parsing**: Custom XMLHelper utility **NEW!**
- **Base64 Encoding**: Custom Base64Helper utility **NEW!**
- **Client-Side Only**: Zero server uploads, 100% privacy

### Desktop Application
- **Core Conversion**: [MarkItDown](https://github.com/microsoft/markitdown) by Microsoft
- **GUI Framework**: CustomTkinter
- **Drag-and-Drop**: TkinterDnD2
- **Table Extraction**: Camelot + Tabula
- **Packaging**: PyInstaller

---

## 🐛 Troubleshooting

### PPTX Image Extraction Issues

**Issue**: Images not extracting from PPTX

**Solution**:
1. Ensure using .pptx format (not .ppt)
2. Check "Extract Images" option is enabled
3. Verify images are embedded (not linked externally)
4. Check console logs (F12) for detailed errors
5. Try re-saving PPTX in PowerPoint

### PPTX Chart Extraction Issues

**Issue**: Charts not converting

**Solution**:
1. Ensure using .pptx format
2. Check "Extract Charts" option is enabled
3. Charts must be native PowerPoint charts (not images)
4. Check console logs for unsupported chart types
5. Try simplifying complex charts

### Excel Formula Issues

**Issue**: Formulas not showing in output

**Solution**:
1. Formulas are shown as markdown code (`` `=FORMULA()` ``)
2. Look for backtick-wrapped formulas in cells
3. Check console logs for parsing errors
4. Very complex formulas may need simplification

### Web Version Issues

**Issue**: Web version not working

**Solution**:
1. Ensure JavaScript is enabled
2. Use modern browser (Chrome 90+, Firefox 88+, Safari 14+)
3. Check browser console for errors (F12)
4. Clear browser cache and reload
5. Try different browser
6. Ensure files are not too large (>50MB may be slow)

---

## 💻 System Requirements

### Web Version (v2.4.3)
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

### v2.4.3 (Current) - Enhanced PPTX & Excel ✅
- [x] PPTX image extraction with alt text
- [x] PPTX chart-to-markdown conversion
- [x] PPTX speaker notes extraction
- [x] Excel formula preservation
- [x] Excel merged cell detection
- [x] Configurable feature toggles
- [x] Comprehensive statistics tracking
- [x] 9 modular JavaScript files
- [x] Full client-side processing

### v2.5.0 (Future) - Integration & Testing
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

See [docs/v2.4.3-progress.md](docs/v2.4.3-progress.md) for recent implementation details.

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
- Test documentation: [tests/README.md](tests/README.md)
- Implementation guide: [docs/v2.4.3-implementation-guide.md](docs/v2.4.3-implementation-guide.md)

---

**Made with ♥️ by Wei-power3**

**Version 2.4.3** - Enhanced PPTX & Excel with Images, Charts, Notes, and Formulas

[Report Bug](https://github.com/Wei-power3/markitdown-desktop-converter/issues) · [Request Feature](https://github.com/Wei-power3/markitdown-desktop-converter/issues) · [Try v2.4.3](web/index_v2.4.3.html) · [View Docs](docs/) · [Run Tests](tests/)
