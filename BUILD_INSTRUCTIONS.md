# Build Instructions for Standalone Executable

## Prerequisites

1. **Windows 10/11** (Required for Windows executable)
2. **Python 3.10 or higher**
3. **Git** (to clone repository)

## Step-by-Step Build Process

### 1. Clone Repository

```bash
git clone https://github.com/Wei-power3/markitdown-desktop-converter.git
cd markitdown-desktop-converter
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Important**: If you encounter issues with `tkinterdnd2`, install it separately:

```bash
pip install tkinterdnd2
```

### 4. Test Application (Optional but Recommended)

```bash
python src/main.py
```

- Verify the GUI launches
- Test drag-and-drop or browse functionality
- Convert a sample PDF to ensure MarkItDown works
- Close the application

### 5. Build Executable

```bash
python build_exe.py
```

**Build Process:**
- Analyzes dependencies
- Bundles Python interpreter
- Creates single `.exe` file
- Takes 3-5 minutes

### 6. Locate Executable

```
dist/MarkItDownConverter.exe
```

**File size**: Approximately 80-150 MB (includes Python runtime)

### 7. Test Executable

```bash
dist\MarkItDownConverter.exe
```

**Test checklist:**
- [ ] Application launches without console window
- [ ] Drag-and-drop works
- [ ] Browse button opens file dialog
- [ ] File conversion completes successfully
- [ ] Files saved to `data/originals/` and `data/processed/`
- [ ] Folder buttons open Windows Explorer

## Distribution

### Option 1: Simple Distribution
1. Copy `MarkItDownConverter.exe` to target computer
2. Double-click to run
3. `data/` folders will be created automatically

### Option 2: Package with Installer (Advanced)

Use **Inno Setup** to create professional installer:

1. Download Inno Setup: https://jrsoftware.org/isinfo.php
2. Create installer script (see `installer_script.iss` template below)
3. Build installer

## Troubleshooting

### Build Fails with "Module not found"

**Solution**: Add missing module to `build_exe.py`:

```python
"--hidden-import=missing_module_name",
```

### Executable Size Too Large

**Solution**: Use `--exclude-module` for unused packages:

```python
"--exclude-module=pandas",
"--exclude-module=openpyxl",
```

### Application Crashes on Startup

**Solution**: Build with console window to see errors:

1. Edit `build_exe.py`
2. Remove `"--windowed"` line
3. Add `"--console"` line
4. Rebuild and check console output

### Drag-and-Drop Doesn't Work

**Solution**: Ensure `tkinterdnd2` installed correctly:

```bash
pip uninstall tkinterdnd2
pip install tkinterdnd2
```

## Advanced: Inno Setup Installer Script

Create `installer_script.iss`:

```ini
[Setup]
AppName=MarkItDown Desktop Converter
AppVersion=1.0.0
DefaultDirName={pf}\MarkItDownConverter
DefaultGroupName=MarkItDown Converter
OutputDir=installer_output
OutputBaseFilename=MarkItDownConverter_Setup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\MarkItDownConverter.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\MarkItDown Converter"; Filename: "{app}\MarkItDownConverter.exe"
Name: "{commondesktop}\MarkItDown Converter"; Filename: "{app}\MarkItDownConverter.exe"

[Run]
Filename: "{app}\MarkItDownConverter.exe"; Description: "Launch MarkItDown Converter"; Flags: postinstall nowait skipifsilent
```

Compile with Inno Setup to create `MarkItDownConverter_Setup.exe`.

## File Structure After Build

```
markitdown-desktop-converter/
├── build/                  # Temporary build files (can delete)
├── dist/
│   └── MarkItDownConverter.exe  # YOUR STANDALONE EXECUTABLE
├── src/                    # Source code
├── data/                   # Created at runtime
├── build_exe.py            # Build script
└── requirements.txt        # Dependencies
```

## Next Steps

1. **Test thoroughly** on your machine
2. **Copy executable** to clean Windows machine for testing
3. **Share** with users or package as installer

## Support

For build issues, check:
- Python version: `python --version` (must be 3.10+)
- PyInstaller version: `pyinstaller --version`
- All dependencies installed: `pip list`
