# MarkItDown v2.4.3 Standalone HTML

## 🔥 Problem Solved: CORS Issues with Local Files

### The Issue
When you **double-click** `index_v2.4.3.html` to open it directly in your browser, it uses the `file://` protocol which triggers browser security (CORS) that blocks loading external JavaScript files. This causes the converter to fail with:

```
Access to script at 'file:///path/to/js/converters/excel-v243.js' 
from origin 'null' has been blocked by CORS policy
```

### The Solution
**Embed ALL JavaScript inline** into a single HTML file, so there are no external file dependencies (except CDN libraries which are allowed).

---

## 🚀 Quick Start

### Option 1: Build Your Own (Recommended)

Run the Python build script to generate the complete standalone HTML:

```bash
cd markitdown-desktop-converter
python web/build_standalone.py
```

This creates: `web/index_v2.4.3_standalone_COMPLETE.html`

**Then just double-click that file!** ✨

---

### Option 2: Use Pre-Built (If Available)

If a pre-built standalone file is available, just download and double-click:
- `index_v2.4.3_standalone_COMPLETE.html` (~60-80 KB)

---

## 📊 What's Different in Standalone?

| Feature | index_v2.4.3.html | Standalone COMPLETE |
|---------|-------------------|----------------------|
| **JavaScript Loading** | External files (8 files) | ALL embedded inline |
| **Server Required** | ✅ YES (local server) | ❌ NO |
| **Double-Click Works** | ❌ NO (CORS errors) | ✅ YES |
| **File Size** | ~20 KB + 8 files | ~60-80 KB single file |
| **Excel Support** | ✅ Full v2.4.3 | ✅ Full v2.4.3 |
| **PPTX Support** | ✅ Full v2.4.3 | ✅ Full v2.4.3 |
| **Images** | ✅ Extract + Embed | ✅ Extract + Embed |
| **Charts** | ✅ To Markdown Tables | ✅ To Markdown Tables |
| **Speaker Notes** | ✅ Included | ✅ Included |

---

## 🛠️ Build Script Details

### What It Does

`build_standalone.py` performs these steps:

1. ✓ Reads all 8 JavaScript modules from `web/js/`
2. ✓ Reads the base HTML template (`index_v2.4.3.html`)
3. ✓ Removes external `<script src="...">` tags
4. ✓ Embeds all JavaScript inline in a single `<script>` block
5. ✓ Writes output: `index_v2.4.3_standalone_COMPLETE.html`

### Modules Embedded

1. `js/utils/xml-helper.js` - XML parsing utilities
2. `js/utils/base64-helper.js` - Base64 encoding utilities
3. `js/modules/pptx-images.js` - Image extraction
4. `js/modules/pptx-charts.js` - Chart extraction
5. `js/modules/pptx-notes.js` - Speaker notes extraction
6. `js/modules/pptx-groups.js` - Grouped shapes handling
7. `js/converters/excel-v243.js` - Excel converter
8. `js/converters/pptx-v243.js` - PPTX converter

---

## ✅ Verification

### Test the Standalone File

1. **Double-click** `index_v2.4.3_standalone_COMPLETE.html`
2. Browser opens (no server needed!)
3. Drag & drop an Excel or PowerPoint file
4. Should work perfectly! ✨

### Check Console (F12)

You should see **NO CORS errors**:
- ✅ No "Access to script blocked by CORS policy"
- ✅ Files convert successfully
- ✅ All features work (images, charts, notes)

---

## 📝 Comparison with Server Version

### When to Use Server Version (`index_v2.4.3.html`)

✅ **Use if:**
- Running with `python -m http.server`
- Developing/debugging (easier to update individual modules)
- File size matters (smaller base HTML)

### When to Use Standalone Version

✅ **Use if:**
- Can't run a local server
- Need to double-click to open
- Want a single self-contained file
- Distributing to non-technical users
- Working offline without server setup

---

## 🐞 Troubleshooting

### Build Script Fails

**Error:** `FileNotFoundError: web/js/converters/excel-v243.js`

**Solution:** Make sure you're running from the repository root:
```bash
python web/build_standalone.py
```

### Standalone File Still Shows Errors

**Check:**
1. Open browser DevTools (F12)
2. Check Console tab for errors
3. Verify all 8 modules are embedded (view page source)

### File Won't Open

**Check:**
- File extension is `.html` not `.txt`
- Default browser is set
- Try right-click → Open With → Browser

---

## 💾 File Sizes

| File | Size | Description |
|------|------|-------------|
| `index_v2.4.3.html` | ~20 KB | Base HTML (requires server) |
| `build_standalone.py` | ~4 KB | Build script |
| `index_v2.4.3_standalone_COMPLETE.html` | ~60-80 KB | Complete standalone (all JS embedded) |

**Total JavaScript embedded:** ~40-50 KB across 8 modules

---

## 🎯 Summary

### Before (v2.4.3 with server)
```
index_v2.4.3.html (20 KB)
├── js/utils/xml-helper.js
├── js/utils/base64-helper.js
├── js/modules/pptx-images.js
├── js/modules/pptx-charts.js
├── js/modules/pptx-notes.js
├── js/modules/pptx-groups.js
├── js/converters/excel-v243.js
└── js/converters/pptx-v243.js

⚠️ Requires: python -m http.server
```

### After (Standalone)
```
index_v2.4.3_standalone_COMPLETE.html (60-80 KB)
└── ALL 8 modules embedded inline

✨ Works: Just double-click!
```

---

## 🔗 Links

- **Original HTML:** `web/index_v2.4.3.html`
- **Build Script:** `web/build_standalone.py`
- **Output:** `web/index_v2.4.3_standalone_COMPLETE.html` (after build)
- **Repository:** [Wei-power3/markitdown-desktop-converter](https://github.com/Wei-power3/markitdown-desktop-converter)

---

## 💬 Questions?

**Q: Why not always use standalone?**

A: Standalone is great for end-users, but development is easier with separate modules (easier debugging, smaller files, faster updates).

**Q: Does it still support all v2.4.3 features?**

A: YES! 100% of v2.4.3 features work:
- ✅ Excel multi-sheet with formulas
- ✅ PPTX image extraction with alt text
- ✅ PPTX chart to markdown conversion
- ✅ Speaker notes extraction
- ✅ All processing is client-side

**Q: Is it safe?**

A: YES! Nothing changes except how JavaScript is loaded. All processing stays in your browser. No uploads, no tracking, 100% private.

---

**Created:** February 17, 2026  
**Version:** 2.4.3 Standalone  
**Author:** Wei-power3
