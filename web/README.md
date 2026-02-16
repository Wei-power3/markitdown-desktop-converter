# MarkItDown Web Converter

## 🚀 Quick Start

### Production Version (Recommended)

**Download and run locally:**
1. Download **[index.html](index.html)** (v2.2.1 - Clean text extraction)
2. Open it in any modern browser (Chrome, Firefox, Edge, Safari)
3. Drag & drop PDF or PowerPoint files
4. Get clean markdown optimized for embeddings!

**No installation required** - everything runs in your browser with complete privacy.

### Experimental Version (Advanced Features)

**For testing only:**
1. Download **[index_experimental.html](index_experimental.html)** (v2.3.2)
2. Includes footnote detection, H/F removal, multi-column support
3. ⚠️ **Known regressions:** Link pollution, table issues
4. See [VERSION_NOTES.md](VERSION_NOTES.md) for detailed comparison

---

## 🎯 Which Version Should I Use?

### Use Production (index.html) For:
- ✅ **Embedding generation** (Primary use case)
- ✅ **RAG pipeline ingestion**
- ✅ **Semantic search indexing**
- ✅ **LLM knowledge bases**
- ✅ **Clean text extraction**
- ✅ **Production deployments**

### Use Experimental (index_experimental.html) For:
- 🧪 **Testing footnote features**
- 🧪 **Evaluating multi-column detection**
- 🧪 **Research and development**
- ❌ **NOT for production embeddings**

**See [VERSION_NOTES.md](VERSION_NOTES.md) for complete quality analysis**

---

## ✨ Features in v2.2.1 (Production)

### Clean Text Extraction
- 🧹 **Advanced Text Cleaning** - Fixes ligatures, merged words, spacing
- 📐 **AI Structure Detection** - Font analysis for headers, lists, styling
- 🎓 **Academic Document Support** - Recognizes research paper sections
- 📊 **Structured Table Extraction** - Preserves table data accurately
- 🔗 **Selective Link Preservation** - External links without pollution
- 📈 **Quality Metrics** - Text quality, structure score, overall rating

### Why v2.2.1?

**Clean text is paramount for embeddings:**
- ✅ No `[their](https://...)` link pollution
- ✅ Stable table headers
- ✅ Better semantic preservation
- ✅ High-quality token sequences
- ✅ Production-tested reliability

**Example output:**
```markdown
All patients underwent their standard treatment protocols.

| Training Set | Validation Set | Test Set |
|--------------|----------------|----------|
| 1,234        | 456            | 789      |
```

---

## 🧪 Features in v2.3.2 (Experimental)

### Advanced Features (With Regressions)
- 📚 **Complete Footnote Pipeline** - Detect, extract, match, insert footnotes
- 🧹 **Header/Footer Removal** - Removes page numbers, DOIs, running headers
- 📰 **Multi-Column Detection** - Proper reading order for 2-column PDFs

### Known Issues
- ❌ **Link Pollution** - Aggressive inline linking degrades text quality
- ❌ **Table Header Duplication** - Headers duplicated and hyperlinked incorrectly
- ❌ **Word-Splitting Artifacts** - Same ligature issues as v2.2.1

**Example problematic output:**
```markdown
[All patients underwent](https://doi.org/...) [their](https://doi.org/...) treatment.

| [Training Set] [Validation Set] | [Validation Set] |
```

**Status:** Reference only, not recommended for production use.

---

## 📊 Quality Metrics (v2.2.1)

### Three-Dimensional Scoring

**1. Text Quality (60% weight)**
- Measures artifact cleaning:
  - Ligature fixes (ﬁ→fi, ﬂ→fl)
  - Hyphenation repairs
  - Encoding corrections
  - Spacing normalization
- **90-100%** = Excellent, publication-ready
- **70-89%** = Good, minor artifacts
- **50-69%** = Fair, needs review
- **<50%** = Poor, significant issues

**2. Structure Score (40% weight)**
- Evaluates markdown richness:
  - Headers detected (max 30 points)
  - Lists found (max 25 points)
  - Numbered lists (max 20 points)
  - Bold text (max 15 points)
  - Italic text (max 10 points)
- **80-100%** = Rich formatting
- **50-79%** = Moderate structure
- **30-49%** = Basic structure
- **<30%** = Plain text

**3. Overall Score**
- Weighted average: `(Text × 0.6) + (Structure × 0.4)`
- Best indicator of conversion quality

### Example Scores

| Document Type | Text Quality | Structure | Overall | Assessment |
|---------------|--------------|-----------|---------|------------|
| Clean research paper | 100% | 75% | 90% | Excellent |
| Academic journal | 95% | 85% | 91% | Excellent |
| Simple report | 100% | 35% | 74% | Good |
| Technical doc | 90% | 70% | 82% | Excellent |

---

## 🔧 Technical Details

### Architecture

**100% Client-Side Processing:**
- No data uploaded to servers
- Complete privacy
- Works offline after initial load
- No API keys needed

**Libraries Used:**
1. **PDF.js** (Mozilla) - PDF parsing
2. **JSZip** - PowerPoint PPTX extraction
3. **Vanilla JavaScript** - All processing logic

**Code Attribution:**
- List detection patterns: [jzillmann/pdf-to-markdown](https://github.com/jzillmann/pdf-to-markdown) (MIT License)
- Font analysis: Adapted from jzillmann's PageItem.jsx
- Text cleaning: Enhanced MarkItDown engine
- Structure scoring: Original implementation

### Browser Compatibility

✅ **Supported:**
- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+
- Opera 76+

❌ **Not Supported:**
- Internet Explorer (any version)
- Old mobile browsers

---

## 📋 Usage Tips

### Best Results

**PDFs:**
- Text-based PDFs work best (not scanned images)
- Academic papers: Excellent results (85-95% overall)
- Technical docs: Very good (80-90% overall)
- Simple reports: Good (75-85% overall)

**PowerPoint:**
- PPTX format preferred over PPT
- List detection on bullet slides
- Header detection for slide titles

### File Size Limits

- **Recommended:** Under 10 MB
- **Maximum:** 50 MB (browser dependent)
- **Processing time:** ~2-5 seconds per MB

### Downloading the App

**For Desktop Use:**
1. Right-click `index.html`
2. Select "Save As..."
3. Save to your computer
4. Double-click to open anytime
5. Bookmark for quick access

**Advantages:**
- No internet needed after download
- Complete privacy (no network traffic)
- Faster loading
- Works on air-gapped systems

---

## 🆚 Version Comparison

| Feature | v2.2.1 (Production) | v2.3.2 (Experimental) |
|---------|---------------------|------------------------|
| **Clean Text** | ✅ Excellent | ❌ Link pollution |
| **Embedding Quality** | ✅ High | ❌ Degraded |
| **Table Integrity** | ✅ Stable | ❌ Header duplication |
| **Text Cleaning** | ✅ Advanced | ✅ Same |
| **Structure Detection** | ✅ AI-powered | ✅ Same |
| **Link Preservation** | ✅ Selective | ⚠️ Too aggressive |
| **Footnote Support** | ❌ None | ✅ Complete pipeline |
| **H/F Removal** | ❌ None | ✅ Automatic |
| **Multi-Column** | ❌ None | ✅ 2-column detection |
| **Production Ready** | ✅ Yes | ❌ No (regressions) |
| **Structure Score** | 70-85% | 70-85% (same) |
| **Overall Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ (noise) |

**Full analysis:** See [VERSION_NOTES.md](VERSION_NOTES.md)

---

## 📁 File Guide

| File | Version | Status | Use Case |
|------|---------|--------|----------|
| **index.html** | v2.2.1 | ✅ **Production** | **Clean text extraction, embeddings, NLP** |
| index_experimental.html | v2.3.2 | ⚠️ Experimental | Testing footnote features, reference |
| index_v2.2.1.html | v2.2.1 | 📚 Archive | Backup of production version |
| index_v2.3.1.html | v2.3.2 | 📚 Archive | Complete v2.3.2 code |
| VERSION_NOTES.md | - | 📝 Documentation | Complete rationale & comparison |

---

## 🎯 Expected Quality (v2.2.1)

### Before MarkItDown
- **Text quality:** Variable, many artifacts
- **Structure:** Lost or minimal
- **Tables:** Unformatted text blocks
- **Overall:** ⭐⭐

### After v2.2.1
- **Text quality:** 90-100% (excellent cleaning)
- **Structure:** 70-85% (intelligent detection)
- **Tables:** Properly formatted markdown
- **Overall:** ⭐⭐⭐⭐⭐

**Net improvement:** +60-70 percentage points in overall quality

---

## 🔮 Future Roadmap

### v2.4 (Planned) - Hybrid Approach
- Start from v2.2.1 clean base
- Optional footnote detection (toggle)
- Optional link preservation (toggle)
- Fix remaining ligature issues
- Features as opt-in, not forced
- Maintain clean text as default

### Design Principles:
1. **Clean text is paramount** for embeddings
2. **Link pollution corrupts semantic meaning**
3. **Table headers should never be hyperlinked**
4. **Footnotes are nice-to-have, not essential**
5. **Features must not degrade base quality**

---

## 📄 License

MIT License - Free for personal and commercial use

**Third-party code credits:**
- List detection logic adapted from [jzillmann/pdf-to-markdown](https://github.com/jzillmann/pdf-to-markdown) (MIT)
- PDF.js by Mozilla Foundation (Apache 2.0)
- JSZip by Stuart Knightley (MIT)

---

## 🤝 Contributing

Found a bug or have suggestions? Open an issue on the main repository!

**Repository:** [Wei-power3/markitdown-desktop-converter](https://github.com/Wei-power3/markitdown-desktop-converter)

---

## 📧 Support

For issues or questions:
- See [VERSION_NOTES.md](VERSION_NOTES.md) for version comparison
- Check main repository README
- Open an issue on GitHub

---

**Made with ♥️ by Wei-power3**

**Version 2.2.1** - Production: Clean Text Extraction for Embeddings

[Try Now](index.html) · [Experimental Version](index_experimental.html) · [Version Comparison](VERSION_NOTES.md) · [Main Repository](https://github.com/Wei-power3/markitdown-desktop-converter)
