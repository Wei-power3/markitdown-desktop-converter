#!/usr/bin/env python
"""
Build script for creating standalone Windows executable
Run: python build_exe.py
"""
import PyInstaller.__main__
import sys
from pathlib import Path

# Get project root
root_dir = Path(__file__).parent
src_dir = root_dir / "src"

# PyInstaller arguments
args = [
    str(src_dir / "main.py"),
    "--name=MarkItDownConverter",
    "--onefile",
    "--windowed",
    "--noconfirm",
    f"--distpath={root_dir / 'dist'}",
    f"--workpath={root_dir / 'build'}",
    f"--specpath={root_dir}",
    "--clean",
    # Add hidden imports
    "--hidden-import=markitdown",
    "--hidden-import=customtkinter",
    "--hidden-import=tkinterdnd2",
    "--hidden-import=CTkMessagebox",
    "--hidden-import=reportlab",
    "--hidden-import=pptx",
    "--hidden-import=PIL",
    "--hidden-import=pdfminer",
    "--hidden-import=pdfplumber",
    "--hidden-import=mammoth",
    "--hidden-import=beautifulsoup4",
    # Exclude unnecessary packages
    "--exclude-module=matplotlib",
    "--exclude-module=numpy",
    "--exclude-module=scipy",
    # Console for debugging (remove --windowed above to see console)
    # "--console",
]

print("Building Windows executable...")
print("This may take a few minutes...\n")

try:
    PyInstaller.__main__.run(args)
    print("\n" + "="*60)
    print("Build completed successfully!")
    print(f"Executable location: {root_dir / 'dist' / 'MarkItDownConverter.exe'}")
    print("="*60)
except Exception as e:
    print(f"\nBuild failed: {e}")
    sys.exit(1)