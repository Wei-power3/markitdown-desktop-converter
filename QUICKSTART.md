# Quick Start Guide

## For End Users (Just Want to Use It)

### 1. Download Executable

**Coming Soon**: Pre-built executable will be available in Releases

**For Now**: Follow "Build Your Own" section below

### 2. Run Application

1. Double-click `MarkItDownConverter.exe`
2. Wait 2-3 seconds for application to load
3. You'll see the main window with a drop zone

### 3. Convert Files

**Method A: Drag and Drop**
1. Open Windows Explorer
2. Find your PDF or PowerPoint file
3. Drag it onto the blue drop zone
4. Click "▶ Start Processing"
5. Wait for conversion to complete (✔ checkmark)

**Method B: Browse**
1. Click "Browse Files" button
2. Select one or more files
3. Click "Open"
4. Click "▶ Start Processing"

### 4. Access Converted Files

1. Click "📄 Processed Folder" button
2. Your Markdown files are there with timestamps
3. Files named like: `14-02-2026_report_markdown.md`

---

## For Developers (Build Your Own)

### Prerequisites Check

```bash
# Check Python version (need 3.10+)
python --version

# If not installed: Download from https://www.python.org/downloads/
```

### 5-Minute Setup

```bash
# 1. Clone repository
git clone https://github.com/Wei-power3/markitdown-desktop-converter.git
cd markitdown-desktop-converter

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate

# 4. Install dependencies (takes 2-3 minutes)
pip install -r requirements.txt

# 5. Run application
python src/main.py
```

### Build Standalone Executable

```bash
# After completing 5-Minute Setup above:

# 1. Build executable (takes 3-5 minutes)
python build_exe.py

# 2. Find your executable
dir dist\MarkItDownConverter.exe

# 3. Test it
dist\MarkItDownConverter.exe

# 4. Share it
# Copy dist\MarkItDownConverter.exe to any Windows computer
# No installation needed - just double-click!
```

---

## Common First-Time Questions

### "What files can I convert?"

- **PDF files** (`.pdf`)
- **PowerPoint presentations** (`.pptx`, `.ppt`)
- More formats coming soon!

### "Where do my files go?"

- **Original files**: `data/originals/` folder (with timestamps)
- **Markdown files**: `data/processed/` folder (with timestamps)
- Both folders created automatically

### "What's the timestamp format?"

```
Original: 14-02-2026_my-report_original.pdf
Markdown: 14-02-2026_my-report_markdown.md
         ││ ││ ││││
         DD-MM-YYYY
```

### "Can I convert multiple files at once?"

Yes! That's the point of the batch queue:
1. Drop/browse multiple files
2. They all appear in the queue
3. Click "▶ Start Processing" once
4. All files convert automatically

### "How long does conversion take?"

- **Small PDF (1-10 pages)**: 5-10 seconds
- **Large PDF (100+ pages)**: 30-60 seconds
- **PowerPoint (10-20 slides)**: 15-30 seconds
- **PowerPoint (50+ slides)**: 1-2 minutes

### "What if conversion fails?"

You'll see a ✖ red X icon. Common causes:
- **Password-protected file**: Remove password first
- **Corrupted file**: Try opening it normally - if it doesn't work, file is bad
- **Unsupported format**: Check file extension (must be PDF, PPTX, or PPT)

### "Can I use this offline?"

Yes! After first run (which downloads some data), works 100% offline.

---

## Visual Guide

### Step 1: Main Window
```
┌──────────────────────────────────┐
│  MarkItDown Desktop Converter  │
│                                │
│     📁 Drop files here        │  ← Drop zone
│    Supported: PDF, PPTX       │
│                                │
│       [Browse Files]          │  ← Or click here
└──────────────────────────────────┘
```

### Step 2: Files in Queue
```
┌────────────────────────────────────────┐
│  Processing Queue (2 files)           │
├────────────────────────────────────────┤
│  ⏸ report.pdf      [--------] Queued  │
│  ⏸ slides.pptx     [--------] Queued  │
├────────────────────────────────────────┤
│  [▶ Start] [Clear] [Folders...]     │  ← Click Start
└────────────────────────────────────────┘
```

### Step 3: Processing
```
┌────────────────────────────────────────────┐
│  Processing Queue (2 files)               │
├────────────────────────────────────────────┤
│  ✔ report.pdf      [========] Complete    │
│  ⏳ slides.pptx     [====----] Processing │  ← In progress
└────────────────────────────────────────────┘
```

### Step 4: Complete
```
┌────────────────────────────────────────────┐
│  Processing Queue (2 files)               │
├────────────────────────────────────────────┤
│  ✔ report.pdf      [========] Complete    │
│  ✔ slides.pptx     [========] Complete    │
├────────────────────────────────────────────┤
│  [📄 Processed Folder]                   │  ← Click to see files
└────────────────────────────────────────────┘
```

---

## Next Steps

1. **Try it out** - Convert a test PDF or PowerPoint
2. **Check output** - Open the Markdown file in Notepad or VS Code
3. **Use in workflow** - Integrate converted Markdown into your tools
4. **Share feedback** - Open an issue if something doesn't work

## Need Help?

- **Documentation**: See [README.md](README.md) for full guide
- **Build Issues**: See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)
- **Bug Reports**: [Open an issue](https://github.com/Wei-power3/markitdown-desktop-converter/issues)

**That's it! You're ready to convert files to Markdown. 🚀**