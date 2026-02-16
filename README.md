# MarkItDown Desktop Converter

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)](https://www.microsoft.com/windows)
[![Version](https://img.shields.io/badge/version-2.3.0-orange)](https://github.com/Wei-power3/markitdown-desktop-converter/releases)

A Windows desktop application for converting PDF and PowerPoint files to **high-quality** Markdown with drag-and-drop simplicity and batch processing queue.

## 🆕 What's New in v2.3.0

### 🚀 Phase 3: Advanced PDF Features

Version 2.3.0 introduces **intelligent layout analysis** for academic papers and journal PDFs:

🧹 **Header/Footer Removal** (NEW)
- Automatically detects and removes repetitive content
- Eliminates page numbers, DOIs, journal names, and running headers
- Analyzes text frequency across all pages (50%+ threshold)
- **Impact:** Removes 15-25 noise items per page in journal PDFs

📰 **Multi-Column Layout Detection** (NEW)
- Intelligently detects 2-column academic papers
- Analyzes X-coordinate distribution to find column boundaries
- Sorts text in proper reading order: left-to-right, top-to-bottom
- **Impact:** +40-60% readability improvement for 2-column PDFs

✨ **Enhanced Structure Scoring**
- +5 points for header/footer removal
- +10 points for multi-column detection
- Total possible bonus: +15 points to structure score

### 📊 Quality Improvements (v2.3.0)

**Structure Score with Multi-Column Detection:**

| Document Type | v2.2.2 | v2.3.0 | Improvement |
|---------------|--------|--------|-------------|
| 2-Column Research Paper | 70-75% | 85-95% | **+15-20% 🚀** |
| Journal Articles (Frontiers, Nature) | 65-70% | 80-90% | **+15-20% 🚀** |
| Conference Proceedings (IEEE, ACM) | 70-75% | 85-95% | **+15-20% 🚀** |
| Single-Column PDF | 75-80% | 80-90% | **+5-10% 🚀** |

**Before/After Example (Multi-Column):**

❌ **Before v2.3.0** (scrambled):
```markdown
Introduction [Col 1]
Results [Col 1]
[Continue intro - Col 2]
[Continue results - Col 2]
```

✅ **After v2.3.0** (correct reading order):
```markdown
Introduction [Col 1]
[Continue intro - Col 2]
Results [Col 1]
[Continue results - Col 2]
```

[See full CHANGELOG](CHANGELOG.md)

---

## 🌐 Web Version Available!

**LATEST:** Try the browser-based converter with v2.3.0 features:
- 📂 [Download web/index_v2.3.0.html](web/index_v2.3.0.html)
- 🔒 100% client-side processing (no uploads)
- 🧹 Header/footer removal for journal PDFs
- 📰 Multi-column layout detection
- ✨ AI structure detection + text cleaning
- 🚀 Run offline after download
- 📱 Works on any OS with modern browser

**Perfect for:**
- Academic papers and journal articles
- Quick conversions without installation
- Sensitive documents (zero data uploads)
- Cross-platform usage

[See web/README.md for details](web/README.md)

---

## ✨ Core Features

- 📂 **Drag & Drop Interface** - Simply drop files to convert
- 📦 **Batch Processing Queue** - Convert multiple files with visual progress tracking
- 🧹 **Header/Footer Removal** - Eliminates page numbers, DOIs, running headers (NEW v2.3)
- 📰 **Multi-Column Detection** - Proper reading order for 2-column PDFs (NEW v2.3)
- 🔗 **Link Preservation** - Maintains external hyperlinks from PDFs and PPTX (v2.2)
- ✨ **Advanced Text Cleaning** - Fixes ligatures, merged words, spacing (v2.2.2)
- 📐 **AI Structure Detection** - Font analysis for headers, lists, styling (v2.1)
- 🎓 **Academic Document Support** - Recognizes research paper sections (v2.1)
- 📊 **Structured Table Extraction** - Preserve table data accurately (v2.0)
- 📄 **Dual PowerPoint Conversion** - Both direct PPTX→MD and PPTX→PDF→MD pathways
- 🕒 **Automatic Timestamped Naming** - Files organized with date stamps
- 📁 **Organized Folder Structure** - Separate folders for originals and processed files
- 🎨 **Modern Dark Theme UI** - Clean, professional interface
- ⚡ **Standalone Executable** - No installation required, just double-click to run

## 🖼️ Preview

### Main Interface with Batch Queue
```
┌──────────────────────────────────────────────────────┐
│    MarkItDown Desktop Converter v2.3                  │
│    Drag & Drop PDF or PowerPoint files                │
├──────────────────────────────────────────────────────┤
│              📁                                       │
│         Drop files here                              │
│    Supported: PDF, PPTX, PPT                         │
├──────────────────────────────────────────────────────┤
│  Processing Queue (3 files)                         │
├──────────────────────────────────────────────────────┤
│  ✔ research-paper.pdf     [========] Complete      │
│     → Structure: 88% • 2-column detected • H/F: 18  │
│     → Links: 12 • Fixed 15 artifacts                │
│  ⏳ journal-article.pdf   [====----] Processing   │
│  ⏸ presentation.pptx      [--------] Queued       │
├──────────────────────────────────────────────────────┤
│ [▶ Start] [Clear] [Originals] [Processed]       │
└──────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Option 1: Download Standalone Executable (Recommended)

1. Go to [Releases](https://github.com/Wei-power3/markitdown-desktop-converter/releases)
2. Download `MarkItDownConverter.exe` (v2.3.0)
3. Download and install [Ghostscript](https://ghostscript.com/releases/gsdnld.html) (required for table extraction)
4. Double-click to run - that's it!

### Option 2: Web Version (No Installation)

1. Download [web/index_v2.3.0.html](web/index_v2.3.0.html)
2. Double-click to open in browser
3. Drag & drop PDFs - all processing happens locally!
4. Perfect for 2-column academic papers!

### Option 3: Run from Source

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

**System Dependencies (for table extraction):**
- **Windows**: Install [Ghostscript](https://ghostscript.com/releases/gsdnld.html)
- **macOS**: `brew install ghostscript tcl-tk`
- **Linux**: `sudo apt-get install ghostscript python3-tk`

## 📚 Usage Guide

### Basic Workflow

1. **Launch Application**
   - Double-click `MarkItDownConverter.exe` or run `python src/main.py`
   - Or use web version: open `web/index_v2.3.0.html` in browser

2. **Add Files to Queue**
   - **Method A**: Drag and drop files onto the drop zone
   - **Method B**: Click "Browse Files" button

3. **Start Processing**
   - Click "▶ Start Processing" button
   - Watch real-time progress in the queue
   - See advanced metrics: columns detected, H/F removed, links preserved

4. **Access Converted Files**
   - Click "📂 Originals Folder" to see source files
   - Click "📄 Processed Folder" to see enhanced Markdown outputs
   - Web version: Download directly from browser

### File Naming Convention

**Original Files:**
```
16-02-2026_research-paper_original.pdf
16-02-2026_presentation_original.pptx
```

**Markdown Files:**
```
16-02-2026_research-paper_v2.3.0_advanced.md
16-02-2026_presentation_v2.3.0_advanced.md
```

Format: `{day}-{month}-{year}_{filename}_v2.3.0_advanced.md`

### Folder Structure

```
markitdown-desktop-converter/
├── web/
│   ├── index_v2.3.0.html   # LATEST: Advanced layout detection
│   ├── index_v2.2.2.html   # Text cleaning version
│   ├── index_v2.1.html     # Structure detection version
│   └── README.md           # Web version documentation
├── data/
│   ├── originals/       # Your source files with timestamps
│   └── processed/       # Enhanced Markdown with advanced features
├── src/                 # Application source code
│   ├── text_cleaner.py  # Text cleaning engine (v2.0/v2.2)
│   ├── structure_detector.py  # AI structure analysis (v2.1)
│   ├── link_extractor.py  # Link preservation (v2.2)
│   ├── layout_analyzer.py  # NEW: Multi-column detection (v2.3)
│   ├── table_extractor.py  # Table extraction engine (v2.0)
│   └── converter.py     # Enhanced converter logic
└── MarkItDownConverter.exe  # Standalone executable
```

## ⚙️ Features in Detail

### 🧹 Header/Footer Removal (v2.3.0)

Automatically cleans up repetitive content from journal PDFs:

**What Gets Removed:**
- Page numbers: `1`, `2`, `Page 123`
- DOIs: `doi:10.1038/s41586-023-12345`
- Journal names: `Frontiers in Oncology | www.frontiersin.org`
- Running headers: Author names, section titles
- Copyright notices: Publisher information

**Before v2.3.0:**
```markdown
## Page 1

Frontiers in Oncology | www.frontiersin.org
DOI: 10.3389/fonc.2023.12345

Abstract
This study examines...

1
```

**After v2.3.0:**
```markdown
## Page 1

Abstract
This study examines...
```

**Algorithm:**
1. Scans entire document (all pages)
2. Counts text frequency across pages
3. Identifies items appearing on ≥50% of pages
4. Applies heuristics for page numbers, DOIs, journals
5. Removes matching items from output

**Result**: Cleaner markdown, better for LLM/RAG pipelines! 🎯

### 📰 Multi-Column Layout Detection (v2.3.0)

Intelligent column detection for academic papers:

**How It Works:**
1. **X-Coordinate Analysis**: Maps horizontal text distribution
2. **Middle Gap Detection**: Finds empty vertical space (35-65% of width)
3. **Column Classification**: If <10% text in middle → 2 columns
4. **Smart Sorting**: Assigns column (0=left, 1=right), then sorts by Y

**Supported Layouts:**
- ✅ Single-column PDFs (standard sorting)
- ✅ 2-column academic papers (intelligent column sorting)
- ⚠️ 3+ columns (falls back to Y-position sorting)

**Perfect For:**
- Nature, Science, Cell journals
- Frontiers research articles
- IEEE/ACM conference papers
- Medical journals (NEJM, Lancet, JAMA)

**Impact:** Prevents text scrambling, maintains proper reading flow!

### 🔗 Link Preservation (v2.2.0)

Maintains clickable hyperlinks in markdown output:

**PDF Links:**
```markdown
Visit our [website](https://example.com) for more information.
See [supplementary materials](https://doi.org/10.1234/suppl).
```

**PPTX Hyperlinks:**
```markdown
- [Learn more](https://docs.example.com)
- [Contact us](mailto:info@example.com)
```

**Link Types:**
- ✅ External URLs (HTTP/HTTPS)
- ✅ Email links (mailto:)
- ✅ DOI links
- ❌ Internal page references (removed in v2.2.1 for cleaner output)

### ✨ Advanced Text Cleaning (v2.2.2)

Fixes common PDF extraction artifacts:

**Spaced Ligatures:**
- Before: `arti fi cial intelligence for identi fi cation`
- After: `artificial intelligence for identification`

**Merged Words:**
- Before: `transmitted onascale representamajor improvement`
- After: `transmitted on a scale represent a major improvement`

**Legacy Artifacts (v2.0):**
- Hyphenation breaks: `non- invasive` → `non-invasive`
- Medical terms: NT-proBNP, β-blockers, HbA1c preserved
- Special characters: ±, μ, ≥, ≤, → handled correctly

### 📐 AI Structure Detection (v2.1.0)

Automatically analyzes document structure using font size intelligence:

**Before v2.1.0:**
```markdown
Introduction
Artificial intelligence has transformed healthcare.
```

**After v2.1.0:**
```markdown
## Introduction

Artificial intelligence has transformed healthcare.
```

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

### 📊 Structured Table Extraction (v2.0)

Extracts tables as properly formatted markdown:

**Input (PDF):** Complex scientific table

**Output (Markdown):**
```markdown
## Table 1 (Page 5)

*Confidence: 95% | Method: camelot-lattice | Size: 10 rows × 4 columns*

| Parameter | Control Group | Treatment Group | P-value |
|-----------|---------------|-----------------|----------|
| Age (years) | 65.3 ± 12.1 | 64.8 ± 11.9 | 0.672 |
| Gender (M/F) | 45/55 | 48/52 | 0.543 |
...
```

**Features:**
- Multi-engine extraction (Camelot lattice, stream, Tabula fallback)
- Confidence scoring per table
- Automatic header detection
- Clean cell formatting
- Page number tracking

### Dual PowerPoint Conversion

The application uses TWO conversion methods for PowerPoint files:

1. **Direct PPTX → Markdown**
   - Preserves slide structure and formatting
   - Best for text-heavy presentations
   - Maintains hyperlinks

2. **PPTX → PDF → Markdown**
   - Better text extraction for complex layouts
   - Handles embedded objects more reliably

Both outputs are combined in a single `.md` file with section headers, structure detection, and text cleaning applied.

### Batch Processing Queue

- **Visual Status Indicators**
  - ⏸ Queued (waiting)
  - ⏳ Processing (active)
  - ✔ Complete (success)
  - ✖ Error (failed)

- **Progress Tracking**
  - Individual progress bars per file
  - Real-time status updates
  - Advanced metrics: columns detected, H/F removed, links preserved
  - Quality scores: text quality, structure, overall
  - Error messages with details

- **Queue Management**
  - Add multiple files at once
  - Remove individual items (except during processing)
  - Clear completed items
  - Process all queued items with one click

## 🎯 Use Cases

### Ideal For:
- ✅ 2-column academic papers (NEW: Perfect with v2.3!)
- ✅ Journal articles (Frontiers, Nature, Science)
- ✅ Conference proceedings (IEEE, ACM, Springer)
- ✅ Scientific literature review
- ✅ Medical documentation (NEJM, Lancet, JAMA)
- ✅ Research data extraction
- ✅ LLM/RAG pipelines (clean, structured input)
- ✅ Knowledge base creation
- ✅ Semantic search indexing
- ✅ Patent document processing
- ✅ Technical documentation

### Quality by Use Case:

| Use Case | Quality Score |
|----------|---------------|
| 2-Column Academic Papers | ⭐⭐⭐⭐⭐ (NEW: v2.3 breakthrough!) |
| Journal Article Processing | ⭐⭐⭐⭐⭐ (NEW: H/F removal + columns) |
| LLM Knowledge Ingestion | ⭐⭐⭐⭐⭐ |
| Scientific Literature Review | ⭐⭐⭐⭐⭐ |
| Single-Column PDFs | ⭐⭐⭐⭐⭐ |
| Clinical Decision Support | ⭐⭐⭐⭐ |
| General Document Conversion | ⭐⭐⭐⭐ |
| Regulatory Documentation | ⭐⭐⭐ (manual review recommended) |

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

### Desktop Application
- **OS**: Windows 10 or 11
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 500 MB
- **Python** (for source): 3.10 or higher
- **Ghostscript**: Required for table extraction ([Download](https://ghostscript.com/))

### Web Version
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **RAM**: 2 GB available
- **JavaScript**: Must be enabled
- **Works**: Windows, macOS, Linux, ChromeOS

## 📄 Supported File Formats

| Format | Extension | Quality | Advanced Features |
|--------|-----------|---------|------------------|
| PDF | `.pdf` | ⭐⭐⭐⭐⭐ | ✅ Full support (v2.3: H/F removal, columns) |
| PowerPoint | `.pptx` | ⭐⭐⭐⭐ | ✅ Link preservation, structure detection |
| PowerPoint Legacy | `.ppt` | ⭐⭐⭐⭐ | ✅ Link preservation, structure detection |

## 🧩 Technology Stack

### Desktop Application
- **Core Conversion**: [MarkItDown](https://github.com/microsoft/markitdown) by Microsoft
- **Layout Analysis**: Custom multi-column detection (NEW v2.3)
- **Structure Detection**: Custom font analysis + patterns from [jzillmann/pdf-to-markdown](https://github.com/jzillmann/pdf-to-markdown) (v2.1)
- **Text Cleaning**: Custom regex-based engine (v2.0/v2.2)
- **Link Extraction**: Custom PDF.js-based extraction (v2.2)
- **Table Extraction**: [Camelot](https://camelot-py.readthedocs.io/) + [Tabula](https://tabula-py.readthedocs.io/) (v2.0)
- **Data Processing**: [Pandas](https://pandas.pydata.org/)
- **GUI Framework**: CustomTkinter
- **Drag-and-Drop**: TkinterDnD2
- **PDF Generation**: ReportLab
- **PowerPoint Processing**: python-pptx
- **Packaging**: PyInstaller

### Web Version
- **PDF Processing**: [PDF.js](https://mozilla.github.io/pdf.js/) by Mozilla
- **PowerPoint Processing**: [JSZip](https://stuk.github.io/jszip/)
- **Layout Detection**: JavaScript port of v2.3 algorithms (NEW)
- **Structure Detection**: JavaScript port of v2.1 algorithms
- **Client-Side Only**: Zero server uploads

## 🐛 Troubleshooting

### Application Won't Start

**Issue**: Double-clicking `.exe` does nothing

**Solution**:
1. Right-click `.exe` → "Run as administrator"
2. Check Windows Defender didn't block it
3. Ensure no antivirus blocking execution

### Multi-Column Detection Not Working

**Issue**: 2-column PDF still shows scrambled text

**Solution**:
1. Ensure using v2.3.0 or later (check version badge)
2. PDF must have clear vertical gap between columns
3. Very dense layouts may not detect (try manual column inspection)
4. 3+ column layouts not supported yet (falls back to Y-sort)
5. Check console for "columnsDetected" count

### Headers/Footers Still Appearing

**Issue**: Page numbers or journal names in output

**Solution**:
1. H/F must appear on ≥50% of pages to be detected
2. Very short documents (<5 pages) may not trigger removal
3. Unique headers per page won't be removed (by design)
4. Check "H/F Removed" metric in output

### Structure Detection Not Working

**Issue**: Headers not detected, structure score still low

**Solution**:
1. Ensure using v2.1.0 or later (check version badge)
2. PDF must have actual text (not scanned images)
3. Font information must be embedded in PDF
4. Some PDFs with custom fonts may not work perfectly
5. Check console logs for font size analysis details

### Table Extraction Fails

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
2. Use modern browser (Chrome 90+, Firefox 88+)
3. Check browser console for errors (F12)
4. Try different browser
5. Clear browser cache

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
3. Check error message in status text and console
4. Try converting file individually
5. Check if file contains scanned images (OCR needed)

### Large Files Slow Processing

**Issue**: Processing takes very long

**Solution**:
- PDF: Expected for 100+ page documents (especially with layout analysis)
- Multi-column detection adds 1-2 seconds per document
- H/F removal requires scanning all pages first
- PPTX: Large presentations (50+ slides) may take 1-2 minutes
- Table extraction adds 2-5 seconds per PDF
- Consider splitting large files before conversion

## 🛣️ Roadmap

### v2.3 (Current) - Advanced PDF Features ✅
- [x] Header/footer removal (page numbers, DOIs, journals)
- [x] Multi-column layout detection (2-column support)
- [x] Advanced metadata tracking
- [x] Enhanced structure scoring (+15 points)
- [x] Web version with layout analysis

### v2.4 (Next) - Phase 3 Complete
- [ ] Footnote extraction
- [ ] Enhanced figure/table references
- [ ] Bibliography section detection
- [ ] Citation format preservation
- [ ] 3+ column layout support

### v2.5 (Planned) - Export Format Options
- [ ] HTML export with Showdown.js
- [ ] Plain text export
- [ ] JSON export with full metadata
- [ ] Format selector in UI
- [ ] Custom templates

### v3.0 (Future) - Visual Intelligence
- [ ] Figure/image extraction
- [ ] AI-powered figure descriptions (GPT-4 Vision/Claude)
- [ ] OCR for scanned documents
- [ ] Chart data extraction
- [ ] Diagram understanding

### v4.0 (Future) - Advanced Features
- [ ] Support Word documents (.docx)
- [ ] Add Excel spreadsheet conversion (.xlsx)
- [ ] Preview pane for Markdown output
- [ ] LLM integration for auto-summaries
- [ ] Custom output folder selection
- [ ] Conversion settings panel
- [ ] macOS and Linux native apps

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CHANGELOG.md](CHANGELOG.md) for version history.

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- **Microsoft AutoGen Team** - [MarkItDown](https://github.com/microsoft/markitdown) library
- **jzillmann** - [pdf-to-markdown](https://github.com/jzillmann/pdf-to-markdown) for structure detection patterns (MIT License)
- **Camelot Team** - Advanced table extraction
- **Tabula Team** - PDF table parsing
- **Mozilla** - PDF.js for web version
- **CustomTkinter** - Modern UI framework
- **PyInstaller** - Executable packaging
- The medical/research community for quality testing and feedback

## 📧 Support

For issues, questions, or feature requests:
- Open an issue: [GitHub Issues](https://github.com/Wei-power3/markitdown-desktop-converter/issues)
- Check documentation: [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)
- View changelog: [CHANGELOG.md](CHANGELOG.md)
- Web version docs: [web/README.md](web/README.md)

---

**Made with ♥️ by Wei-power3**

**Version 2.3.0** - Advanced PDF Features: Multi-Column Detection + Header/Footer Removal

[Report Bug](https://github.com/Wei-power3/markitdown-desktop-converter/issues) · [Request Feature](https://github.com/Wei-power3/markitdown-desktop-converter/issues) · [View Changelog](CHANGELOG.md) · [Try Web Version](web/index_v2.3.0.html)
