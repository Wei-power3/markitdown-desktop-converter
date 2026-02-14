# Testing Guide

## Pre-Build Testing

### 1. Test Core Conversion

```bash
# Activate virtual environment
venv\Scripts\activate

# Test PDF conversion
python -c "from markitdown import MarkItDown; md = MarkItDown(); result = md.convert('sample.pdf'); print('PDF OK')"

# Test PPTX conversion
python -c "from markitdown import MarkItDown; md = MarkItDown(); result = md.convert('sample.pptx'); print('PPTX OK')"
```

### 2. Test GUI Launch

```bash
python src/main.py
```

**Checklist:**
- [ ] Window opens without errors
- [ ] Drop zone visible
- [ ] All buttons render correctly
- [ ] No console errors

### 3. Test File Operations

**Test drag-and-drop:**
1. Drag a PDF onto drop zone
2. Verify file appears in queue
3. Click "Start Processing"
4. Wait for completion
5. Verify files in `data/` folders

**Test browse:**
1. Click "Browse Files"
2. Select multiple files
3. Verify all added to queue
4. Process and verify outputs

### 4. Test Edge Cases

**Large files:**
- Test 100+ page PDF
- Test 50+ slide PowerPoint
- Verify progress updates correctly

**Unsupported files:**
- Try dropping .txt file
- Should show warning message

**Empty queue:**
- Click "Start Processing" with no files
- Should show info message

**Duplicate files:**
- Add same file twice
- Process both
- Verify unique filenames (counter added)

## Post-Build Testing

### 1. Executable Integrity

```bash
# Check file exists
dir dist\MarkItDownConverter.exe

# Check size (should be 80-150 MB)
```

### 2. Fresh Machine Test (CRITICAL)

**Test on a computer that:**
- Never had Python installed
- Never ran this application
- Clean Windows 10/11

**Test procedure:**
1. Copy only the `.exe` to test machine
2. Double-click to run
3. Test full conversion workflow
4. Verify no dependency errors

### 3. Antivirus Compatibility

**Test with:**
- Windows Defender (default)
- Popular third-party antivirus

**Check:**
- [ ] Executable not flagged as malware
- [ ] Can run without admin rights
- [ ] Can access file system

### 4. Performance Benchmarks

**Record conversion times:**

| File Type | Size | Pages/Slides | Time |
|-----------|------|--------------|------|
| PDF | 1 MB | 10 | ___ sec |
| PDF | 10 MB | 100 | ___ sec |
| PPTX | 5 MB | 20 | ___ sec |
| PPTX | 20 MB | 50 | ___ sec |

**Acceptance criteria:**
- Small files (< 5 MB): Under 30 seconds
- Medium files (5-20 MB): Under 2 minutes
- Large files (> 20 MB): Under 5 minutes

## Automated Testing (Optional)

### Unit Tests

```python
# test_file_manager.py
import pytest
from pathlib import Path
from src.file_manager import FileManager

def test_filename_generation():
    fm = FileManager()
    test_path = Path("test.pdf")
    filename = fm.generate_filename(test_path, "_original")
    assert "_original.pdf" in filename
    assert len(filename.split("-")) == 3  # Date format

def test_save_original():
    fm = FileManager()
    # Create temp file
    temp = Path("temp_test.pdf")
    temp.write_text("test")
    
    saved = fm.save_original(temp)
    assert saved.exists()
    assert "_original" in saved.name
    
    # Cleanup
    saved.unlink()
    temp.unlink()
```

### Integration Tests

```python
# test_converter.py
import pytest
from src.converter import DocumentConverter
from pathlib import Path

def test_pdf_conversion():
    converter = DocumentConverter()
    test_pdf = Path("samples/test.pdf")
    
    if test_pdf.exists():
        content, error = converter.convert_file(test_pdf)
        assert error is None
        assert len(content) > 0
        assert "#" in content  # Should have markdown headers

def test_pptx_conversion():
    converter = DocumentConverter()
    test_pptx = Path("samples/test.pptx")
    
    if test_pptx.exists():
        content, error = converter.convert_file(test_pptx)
        assert error is None
        assert "Direct PPTX Conversion" in content
        assert "PDF Pathway Conversion" in content
```

## Regression Testing

**After each code change, retest:**

1. [ ] GUI launches correctly
2. [ ] File drag-and-drop works
3. [ ] Browse button works
4. [ ] Queue displays correctly
5. [ ] Processing completes without errors
6. [ ] Files saved to correct folders
7. [ ] Folder buttons open Explorer
8. [ ] Clear queue works
9. [ ] Remove individual items works
10. [ ] Executable still builds

## Sample Test Files

**Create these test files:**

### Small PDF (test_small.pdf)
- 1-2 pages
- Text content
- No images
- Quick conversion test

### Large PDF (test_large.pdf)
- 50+ pages
- Mixed content (text, images, tables)
- Performance test

### Simple PowerPoint (test_simple.pptx)
- 5-10 slides
- Text-only content
- Basic conversion test

### Complex PowerPoint (test_complex.pptx)
- 30+ slides
- Images, charts, tables
- Advanced layout test

## Bug Reporting Template

When reporting issues:

```markdown
**Bug Description:**
Clear description of what went wrong

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What should have happened

**Actual Behavior:**
What actually happened

**Environment:**
- Windows Version: Windows 10/11
- Python Version (if from source): 3.x.x
- Executable or Source: Executable/Source
- File Type: PDF/PPTX
- File Size: X MB

**Error Message:**
```
Paste any error messages here
```

**Screenshots:**
Attach if helpful
```

## Continuous Improvement

**Track these metrics:**

1. **Conversion Success Rate**
   - Target: > 95%
   - Measure: Successful conversions / Total attempts

2. **Average Conversion Time**
   - Target: < 30 seconds for typical files
   - Measure: Sum of times / Number of conversions

3. **User-Reported Bugs**
   - Target: < 5 per month
   - Track via GitHub Issues

4. **Crash Rate**
   - Target: 0%
   - Monitor application crashes

## Final Release Checklist

Before releasing new version:

- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing complete
- [ ] Fresh machine test successful
- [ ] Performance benchmarks met
- [ ] No known critical bugs
- [ ] Documentation updated
- [ ] Version number incremented
- [ ] Git tag created
- [ ] Release notes written
- [ ] Executable uploaded to Releases