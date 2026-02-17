# Changelog

All notable changes to MarkItDown Desktop Converter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.4.4] - 2026-02-17

### Added
- **Copy to Clipboard Button**: One-click markdown copy with toast notification
- **Toast Notifications**: Smooth slide-in/out animations for user feedback
- **PDF Support**: Client-side PDF text extraction using PDF.js
- **DOCX Support**: Full Word document conversion using Mammoth.js
- **4-Button Layout**: Download | Preview | Copy | Delete action buttons

### Changed
- **Stats Display**: Replaced 4-6 stat cards with single-line summary (e.g., "2 of 3 files converted, 42 pages processed")
- **UI Polish**: Improved button styling and layout consistency
- **Toast Animation**: Added green toast notifications for clipboard actions
- **File Naming**: Updated suffix from `_v243.md` to `_v244.md`

### Maintained
- All v2.4.3 PPTX features (images, charts, notes)
- All v2.4.3 Excel features (multi-sheet, formulas)
- Per-job detailed metrics display
- Dark theme and existing styling
- Auto-loading from GitHub for offline use

### Technical
- Added `navigator.clipboard` API for copy functionality
- Implemented toast notification system with CSS animations
- Simplified stats calculation logic
- Maintained all 10 JavaScript modules
- File size: 29 KB (standalone HTML)

---

## [2.4.3] - 2026-02-17

### Added - PPTX Enhancements
- **Image Extraction**: Extract images from `ppt/media/` with alt text
- **Chart Conversion**: Convert 8+ chart types to markdown tables
- **Speaker Notes**: Extract and format presenter notes per slide
- **Shape Grouping**: Handle grouped shapes with spatial sorting
- **Base64 Embedding**: Optional self-contained image embedding
- **Statistics Tracking**: Comprehensive metrics for PPTX processing

### Added - Excel Enhancements
- **Multi-Sheet Headers**: Clear sheet name labels
- **Formula Preservation**: Display formulas as markdown code (`` `=FORMULA()` ``)
- **Merged Cell Detection**: Report and handle merged cells
- **Document Summary**: Overview of entire workbook
- **Enhanced Statistics**: Track sheets, formulas, merged cells

### Added - Modules
- `xml-helper.js`: XML parsing utilities
- `base64-helper.js`: Base64 encoding utilities
- `pptx-images.js`: Image extraction (15KB)
- `pptx-charts.js`: Chart extraction (14KB)
- `pptx-notes.js`: Notes extraction (12KB)
- `pptx-groups.js`: Shape grouping (6KB)
- `excel-v243.js`: Enhanced Excel converter (8KB)
- `pptx-v243.js`: Integrated PPTX converter (11KB)

### Added - UI Features
- **Options Panel**: Toggle images, charts, notes, base64, metadata
- **Enhanced Stats Cards**: 6 metrics (files, completed, images, charts, notes, sheets)
- **Per-Job Metrics**: Detailed statistics per converted file
- **v2.4.3 Banner**: Highlight new features

### Changed
- Migrated from monolithic to modular architecture (9 files)
- Updated UI to show enhanced metrics
- Improved error handling and logging
- Enhanced progress tracking

### Technical
- Total codebase: 2,330+ lines across 9 files
- Modular JavaScript architecture
- Client-side ZIP file handling
- XML parsing for PPTX relationships
- Statistics engine for tracking features

---

## [2.4.2] - Previous

### Fixed
- PPTX table extraction improvements
- PPTX list formatting fixes
- Enhanced text processing

---

## [2.4.1] - Previous

### Added
- Basic PPTX support
- Basic Excel support

---

## [2.4.0] - Previous

### Added
- Word document support (.docx, .doc)
- Excel spreadsheet support (.xlsx, .xls)
- Web-based converter interface

---

## [2.2.1] - Previous

### Added
- Advanced text cleaning
- AI structure detection
- Academic document support
- Ligature fixing
- Word merging correction

---

## [2.0.0] - Initial

### Added
- PDF to Markdown conversion
- PowerPoint to Markdown conversion
- Desktop application interface
- Drag & drop support
- Batch processing queue

---

## Version Comparison

| Version | Released | Key Features | File Size | Modules |
|---------|----------|--------------|-----------|----------|
| 2.4.4 | 2026-02-17 | Copy button, simplified stats, PDF, DOCX | 29 KB | 10 |
| 2.4.3 | 2026-02-17 | PPTX images/charts/notes, Excel formulas | 25 KB | 8 |
| 2.4.0 | Previous | Word & Excel support | 20 KB | 2 |
| 2.2.1 | Previous | Text cleaning, AI structure | 15 KB | 1 |
| 2.0.0 | Initial | PDF & PPTX basic | 12 KB | 1 |

---

## Migration Guide

### From v2.4.3 to v2.4.4

**What's New:**
- Copy button for clipboard operations
- PDF support (text extraction)
- DOCX support (full conversion)
- Simplified stats display

**Breaking Changes:**
- None - fully backward compatible

**Action Required:**
- None - just download the new HTML file

**File Naming:**
- Old: `document_v243.md`
- New: `document_v244.md`

### From v2.4.0 to v2.4.3+

**What's New:**
- PPTX: Images, charts, speaker notes extraction
- Excel: Formula preservation, merged cells
- Modular architecture (8+ modules)

**Breaking Changes:**
- None - options are additive

**Action Required:**
- Enable/disable new features via options panel

---

## Upgrade Instructions

### Web Version

1. Download latest `index_v2.4.4.html`
2. Delete old version (optional)
3. Double-click new file to use
4. Browser caches modules automatically

### Desktop Application

1. Download latest release
2. Extract to new folder
3. Run executable
4. Previous settings preserved

---

## Deprecation Notices

### Current
- None

### Planned
- v2.2.1 and earlier will be archived in v3.0
- Desktop application may transition to Electron in v3.0

---

## Known Issues

### v2.4.4
- Very large PDF files (>100 MB) may be slow
- Complex DOCX formatting may not preserve perfectly
- Browser clipboard API requires HTTPS or localhost

### v2.4.3
- Some complex PPTX charts may not convert perfectly
- Very large images may slow processing
- Grouped shapes in groups may have incorrect ordering

### Workarounds
- For large files: Split into smaller chunks
- For complex charts: Simplify before conversion
- For clipboard issues: Use HTTPS or localhost

---

## Support

For issues, questions, or feature requests:
- [GitHub Issues](https://github.com/Wei-power3/markitdown-desktop-converter/issues)
- [Documentation](docs/)
- [Web README](web/README.md)

---

## License

MIT License - see [LICENSE](LICENSE) file

---

**Maintained by Wei-power3**  
**Latest Version:** 2.4.4 (February 17, 2026)
