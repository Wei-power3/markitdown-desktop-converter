#!/usr/bin/env python3
"""
Build Complete Standalone HTML for MarkItDown v2.4.3

This script combines all JavaScript modules into a single self-contained HTML file
that works when double-clicked (no server needed).

Usage:
    python build_standalone.py

Output:
    web/index_v2.4.3_standalone_COMPLETE.html
"""

import os
import re
from pathlib import Path

def read_file(filepath):
    """Read file content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """Write file content"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    print("🔨 Building Complete Standalone HTML for v2.4.3...")
    print("=" * 60)
    
    # Define module paths
    modules = [
        ("web/js/utils/xml-helper.js", "XML Helper"),
        ("web/js/utils/base64-helper.js", "Base64 Helper"),
        ("web/js/modules/pptx-images.js", "PPTX Image Extractor"),
        ("web/js/modules/pptx-charts.js", "PPTX Chart Extractor"),
        ("web/js/modules/pptx-notes.js", "PPTX Notes Extractor"),
        ("web/js/modules/pptx-groups.js", "PPTX Group Handler"),
        ("web/js/converters/excel-v243.js", "Excel Converter v2.4.3"),
        ("web/js/converters/pptx-v243.js", "PPTX Converter v2.4.3"),
    ]
    
    # Read all JavaScript modules
    js_content = ""
    for module_path, module_name in modules:
        if os.path.exists(module_path):
            print(f"✓ Loading {module_name}")
            js_code = read_file(module_path)
            js_content += f"\n\n// ========================================\n"
            js_content += f"// {module_name.upper()}\n"
            js_content += f"// ========================================\n"
            js_content += js_code
        else:
            print(f"✗ Missing: {module_path}")
            return
    
    print(f"\n📦 Total JavaScript size: {len(js_content):,} bytes")
    
    # Read base HTML template
    print("\n📄 Reading HTML template...")
    html_template = read_file("web/index_v2.4.3.html")
    
    # Replace external <script src="..."> with embedded scripts
    print("\n🔄 Embedding JavaScript modules...")
    
    # Remove external script tags for local modules
    html_template = re.sub(
        r'<script\s+src="js/.*?".*?></script>',
        '',
        html_template,
        flags=re.DOTALL
    )
    
    # Find where to insert embedded scripts (before closing </body>)
    insertion_point = html_template.rfind('</body>')
    
    if insertion_point == -1:
        print("✗ Could not find </body> tag")
        return
    
    # Create embedded script block
    embedded_scripts = f"\n\n    <!-- EMBEDDED JAVASCRIPT - All 8 modules inline -->\n"
    embedded_scripts += f"    <script>\n{js_content}\n    </script>\n\n"
    
    # Insert embedded scripts
    html_complete = (
        html_template[:insertion_point] +
        embedded_scripts +
        html_template[insertion_point:]
    )
    
    # Add standalone notice to title
    html_complete = html_complete.replace(
        '<title>MarkItDown v2.4.3',
        '<title>MarkItDown v2.4.3 STANDALONE'
    )
    
    # Add notice in header
    html_complete = html_complete.replace(
        '<span class="version-badge">v2.4.3</span>',
        '<span class="version-badge">v2.4.3 STANDALONE</span>'
    )
    
    # Write output file
    output_path = "web/index_v2.4.3_standalone_COMPLETE.html"
    write_file(output_path, html_complete)
    
    print(f"\n✅ SUCCESS!")
    print(f"📁 Created: {output_path}")
    print(f"📏 File size: {len(html_complete):,} bytes ({len(html_complete)/1024:.1f} KB)")
    print(f"\n🎯 Usage: Just double-click the file to open in your browser!")
    print(f"💡 No server needed, works completely offline.")
    print("=" * 60)

if __name__ == "__main__":
    main()
