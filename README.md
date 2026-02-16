# MarkItDown Desktop Converter

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)](https://www.microsoft.com/windows)
[![Version](https://img.shields.io/badge/version-2.2.1-brightgreen)](https://github.com/Wei-power3/markitdown-desktop-converter/releases)

A Windows desktop application for converting PDF and PowerPoint files to **clean, high-quality** Markdown optimized for embeddings, RAG pipelines, and NLP tasks.

## 🎯 Current Version: v2.2.1 (Production)

**Focus:** Clean text extraction for embeddings and semantic search

### Why v2.2.1?

After extensive testing, **v2.2.1 provides the cleanest text output** for embedding generation and NLP use cases:

✅ **Clean inline text** - No link pollution or noise  
✅ **Stable table structure** - Headers preserved correctly  
✅ **Better semantic quality** - Word integrity maintained  
✅ **Optimal for embeddings** - High-quality token sequences  
✅ **Production-tested** - Reliable and consistent  

**See [web/VERSION_NOTES.md](web/VERSION_NOTES.md) for detailed comparison between v2.2.1 and experimental v2.3.2**

---

## 🌐 Web Version (Recommended)

**PRODUCTION:** Browser-based converter with v2.2.1 quality:
- 📂 **[Download web/index.html](web/index.html)** - Production version (v2.2.1)
- 🔒 100% client-side processing (no uploads)
- ✨ AI structure detection + advanced text cleaning
- 🚀 Run offline after download
- 📱 Works on any OS with modern browser
- 📊 Quality metrics with scoring

**EXPERIMENTAL:** Advanced features (use with caution):
- 📂 [Download web/index_experimental.html](web/index_experimental.html) - v2.3.2 with footnotes
- ⚠️ Known regressions: link pollution, table issues
- 🧪 For testing advanced features only
- 📝 See [VERSION_NOTES.md](web/VERSION_NOTES.md) for details

**Perfect for:**
- Clean text extraction for embeddings
- RAG pipeline document ingestion
- Semantic search indexing
- LLM knowledge base creation
- Academic paper processing
- Sensitive documents (zero data uploads)

[See web/README.md for details](web/README.md)

---

## ✨ Core Features

### Production (v2.2.1)
- 📂 **Drag & Drop Interface** - Simply drop files to convert
- 📦 **Batch Processing Queue** - Convert multiple files with visual progress tracking
- ✨ **Advanced Text Cleaning** - Fixes ligatures, merged words, spacing
- 📐 **AI Structure Detection** - Font analysis for headers, lists, styling
- 🎓 **Academic Document Support** - Recognizes research paper sections
- 📊 **Structured Table Extraction** - Preserve table data accurately
- 🔗 **Selective Link Preservation** - External links without pollution
- 📄 **Dual PowerPoint Conversion** - Both direct PPTX→MD and PPTX→PDF→MD pathways
- 🕒 **Automatic Timestamped Naming** - Files organized with date stamps
- 📁 **Organized Folder Structure** - Separate folders for originals and processed files
- 🎨 **Modern Dark Theme UI** - Clean, professional interface
- ⚡ **Standalone Executable** - No installation required, just double-click to run

### Experimental (v2.3.2)
- 📚 **Complete Footnote Pipeline** - Detect, extract, match, insert footnotes
- 🧹 **Header/Footer Removal** - Removes page numbers, DOIs, running headers
- 📰 **Multi-Column Detection** - Proper reading order for 2-column PDFs
- ⚠️ **Known Issues** - Link pollution, table duplication, word-splitting artifacts
- 📝 **Status** - Reference only, not recommended for production

---

## 🖼️ Preview

### Main Interface with Batch Queue
```
┌──────────────────────────────────────────────────────┐
│    MarkItDown Desktop Converter v2.2.1                │
│    Clean Text Extraction for Embeddings               │
├──────────────────────────────────────────────────────┤
│              📁                                       │
│         Drop files here                              │
│    Supported: PDF, PPTX, PPT                         │
├──────────────────────────────────────────────────────┤
│  Processing Queue (3 files)                         │
├──────────────────────────────────────────────────────┤
│  ✔ research-paper.pdf     [========] Complete      │
│     → Text: 95% • Structure: 85% • Overall: 91%     │
│     → Links: 12 • Fixed 15 artifacts                │
│  ⏳ journal-article.pdf   [====----] Processing   │
│  ⏸ presentation.pptx      [--------] Queued       │
├──────────────────────────────────────────────────────┤
│ [▶ Start] [Clear] [Originals] [Processed]       │
└──────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Option 1: Web Version (Recommended)

1. Download [web/index.html](web/index.html) (Production v2.2.1)
2. Double-click to open in browser
3. Drag & drop PDFs - all processing happens locally!
4. **Best for:** Clean embeddings and NLP tasks

### Option 2: Download Standalone Executable

1. Go to [Releases](https://github.com/Wei-power3/markitdown-desktop-converter/releases)
2. Download `MarkItDownConverter.exe` (v2.2.1)
3. Download and install [Ghostscript](https://ghostscript.com/releases/gsdnld.html) (required for table extraction)
4. Double-click to run - that's it!

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

---

## 📚 Usage Guide

### Basic Workflow

1. **Launch Application**
   - Double-click `MarkItDownConverter.exe` or run `python src/main.py`
   - Or use web version: open `web/index.html` in browser

2. **Add Files to Queue**
   - **Method A**: Drag and drop files onto the drop zone
   - **Method B**: Click "Browse Files" button

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
16-02-2026_presentation_original.pptx
```

**Markdown Files:**
```
16-02-2026_research-paper_v2.2.1_clean.md
16-02-2026_presentation_v2.2.1_clean.md
```

Format: `{day}-{month}-{year}_{filename}_v2.2.1_clean.md`

### Folder Structure

```
markitdown-desktop-converter/
├── web/
│   ├── index.html              # Production v2.2.1 (Clean text)
│   ├── index_experimental.html # Experimental v2.3.2 (Advanced features)
│   ├── VERSION_NOTES.md        # Detailed version comparison
│   └── README.md               # Web version documentation
├── data/
│   ├── originals/       # Your source files with timestamps
│   └── processed/       # Clean Markdown optimized for embeddings
├── src/                 # Application source code
│   ├── text_cleaner.py  # Text cleaning engine
│   ├── structure_detector.py  # AI structure analysis
│   ├── link_extractor.py  # Link preservation
│   ├── table_extractor.py  # Table extraction engine
│   └── converter.py     # Enhanced converter logic
└── MarkItDownConverter.exe  # Standalone executable
```

---

## ⚙️ Features in Detail

### ✨ Advanced Text Cleaning (v2.2.1)

Fixes common PDF extraction artifacts for clean embeddings:

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

**Before structure detection:**
```markdown
Introduction
Artificial intelligence has transformed healthcare.
```

**After structure detection:**
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

### 🔗 Link Preservation (v2.2.0)

Maintains clickable hyperlinks without pollution:

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
- ✅ External URLs (HTTP/HTTPS) when explicitly linked
- ✅ Email links (mailto:)
- ✅ DOI links in reference sections
- ❌ Aggressive inline linking (removed for clean text)

### 📊 Structured Table Extraction

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

### Batch Processing Queue

- **Visual Status Indicators**
  - ⏸ Queued (waiting)
  - ⏳ Processing (active)
  - ✔ Complete (success)
  - ✖ Error (failed)

- **Progress Tracking**
  - Individual progress bars per file
  - Real-time status updates
  - Quality scores: text quality, structure, overall
  - Link preservation count
  - Artifact fix count
  - Error messages with details

- **Queue Management**
  - Add multiple files at once
  - Remove individual items (except during processing)
  - Clear completed items
  - Process all queued items with one click

---

## 🎯 Use Cases

### Ideal For:
- ✅ **Embedding generation** (Primary use case)
- ✅ **RAG pipeline ingestion**
- ✅ **Semantic search indexing**
- ✅ **LLM knowledge bases**
- ✅ **Academic paper processing**
- ✅ **Scientific literature review**
- ✅ **Medical documentation**
- ✅ **Research data extraction**
- ✅ **Technical documentation**
- ✅ **Patent document processing**

### Quality by Use Case:

| Use Case | v2.2.1 Quality | Notes |
|----------|----------------|-------|
| Embedding Generation | ⭐⭐⭐⭐⭐ | Clean text, no noise |
| RAG Pipeline Ingestion | ⭐⭐⭐⭐⭐ | Optimal semantic preservation |
| Semantic Search Indexing | ⭐⭐⭐⭐⭐ | High token quality |
| LLM Knowledge Base | ⭐⭐⭐⭐⭐ | Clean, structured input |
| Academic Papers | ⭐⭐⭐⭐⭐ | Excellent structure detection |
| Scientific Literature | ⭐⭐⭐⭐⭐ | Clean references, tables |
| Medical Documentation | ⭐⭐⭐⭐ | Preserves medical terminology |
| General Document Conversion | ⭐⭐⭐⭐ | Reliable and consistent |

---

## 📊 Version Comparison

| Feature | v2.2.1 (Production) | v2.3.2 (Experimental) |
|---------|---------------------|------------------------|
| **Clean Text** | ✅ Excellent | ❌ Link pollution |
| **Embedding Quality** | ✅ High | ❌ Degraded |
| **Table Integrity** | ✅ Stable | ❌ Header duplication |
| **Link Preservation** | ✅ Selective | ⚠️ Too aggressive |
| **Footnote Support** | ❌ None | ✅ Complete pipeline |
| **H/F Removal** | ❌ None | ✅ Automatic |
| **Multi-Column** | ❌ None | ✅ 2-column detection |
| **Production Ready** | ✅ Yes | ❌ No (regressions) |
| **Best For** | Embeddings, NLP | Testing, reference |

**Full comparison:** See [web/VERSION_NOTES.md](web/VERSION_NOTES.md)

---

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

---

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

---

## 📄 Supported File Formats

| Format | Extension | Quality | Notes |
|--------|-----------|---------|-------|
| PDF | `.pdf` | ⭐⭐⭐⭐⭐ | Full support, clean text extraction |
| PowerPoint | `.pptx` | ⭐⭐⭐⭐ | Link preservation, structure detection |
| PowerPoint Legacy | `.ppt` | ⭐⭐⭐⭐ | Link preservation, structure detection |

---

## 🧩 Technology Stack

### Desktop Application
- **Core Conversion**: [MarkItDown](https://github.com/microsoft/markitdown) by Microsoft
- **Structure Detection**: Custom font analysis + patterns from [jzillmann/pdf-to-markdown](https://github.com/jzillmann/pdf-to-markdown)
- **Text Cleaning**: Custom regex-based engine
- **Link Extraction**: Custom PDF.js-based extraction
- **Table Extraction**: [Camelot](https://camelot-py.readthedocs.io/) + [Tabula](https://tabula-py.readthedocs.io/)
- **Data Processing**: [Pandas](https://pandas.pydata.org/)
- **GUI Framework**: CustomTkinter
- **Drag-and-Drop**: TkinterDnD2
- **PDF Generation**: ReportLab
- **PowerPoint Processing**: python-pptx
- **Packaging**: PyInstaller

### Web Version
- **PDF Processing**: [PDF.js](https://mozilla.github.io/pdf.js/) by Mozilla
- **PowerPoint Processing**: [JSZip](https://stuk.github.io/jszip/)
- **Structure Detection**: JavaScript port of v2.1 algorithms
- **Text Cleaning**: JavaScript port of v2.2 algorithms
- **Client-Side Only**: Zero server uploads

---

## 🐛 Troubleshooting

### Application Won't Start

**Issue**: Double-clicking `.exe` does nothing

**Solution**:
1. Right-click `.exe` → "Run as administrator"
2. Check Windows Defender didn't block it
3. Ensure no antivirus blocking execution

### Structure Detection Not Working

**Issue**: Headers not detected, structure score still low

**Solution**:
1. Ensure using v2.2.1 (check version badge)
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

### Large Files Slow Processing

**Issue**: Processing takes very long

**Solution**:
- PDF: Expected for 100+ page documents
- PPTX: Large presentations (50+ slides) may take 1-2 minutes
- Table extraction adds 2-5 seconds per PDF
- Consider splitting large files before conversion

---

## 🛣️ Roadmap

### v2.2.1 (Current) - Production ✅
- [x] Clean text extraction for embeddings
- [x] Advanced text cleaning
- [x] AI structure detection
- [x] Selective link preservation
- [x] Quality metrics
- [x] Production-tested stability

### v2.4 (Future) - Hybrid Approach
- [ ] Start from v2.2.1 clean base
- [ ] Optional footnote detection (toggle)
- [ ] Optional link preservation (toggle)
- [ ] Fix remaining ligature issues
- [ ] Features as opt-in, not forced
- [ ] Maintain clean text as default

### v3.0 (Future) - Visual Intelligence
- [ ] Figure/image extraction
- [ ] AI-powered figure descriptions
- [ ] OCR for scanned documents
- [ ] Chart data extraction

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
- **jzillmann** - [pdf-to-markdown](https://github.com/jzillmann/pdf-to-markdown) for structure detection patterns (MIT License)
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
- Version comparison: [web/VERSION_NOTES.md](web/VERSION_NOTES.md)

---

**Made with ♥️ by Wei-power3**

**Version 2.2.1** - Production: Clean Text Extraction for Embeddings

[Report Bug](https://github.com/Wei-power3/markitdown-desktop-converter/issues) · [Request Feature](https://github.com/Wei-power3/markitdown-desktop-converter/issues) · [View Changelog](CHANGELOG.md) · [Try Web Version](web/index.html) · [Version Comparison](web/VERSION_NOTES.md)
