#!/usr/bin/env python
"""
MarkItDown Web Application
Flask-based browser interface for converting PDF and PowerPoint to Markdown
"""
from flask import Flask, render_template, request, send_file, jsonify, session
from werkzeug.utils import secure_filename
import os
import sys
from pathlib import Path
from datetime import datetime
import uuid
import shutil

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.converter import DocumentConverter
from src.file_manager import FileManager
from src.config import SUPPORTED_EXTENSIONS, TIMESTAMP_FORMAT

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Create upload and output directories
UPLOAD_FOLDER = Path('web/uploads')
OUTPUT_FOLDER = Path('web/outputs')
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Initialize converter
converter = DocumentConverter()
file_manager = FileManager()


def allowed_file(filename):
    """Check if file extension is supported"""
    return Path(filename).suffix.lower() in SUPPORTED_EXTENSIONS


def get_session_folder(folder_type='upload'):
    """Get or create session-specific folder"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    base_folder = UPLOAD_FOLDER if folder_type == 'upload' else OUTPUT_FOLDER
    session_folder = base_folder / session['session_id']
    session_folder.mkdir(parents=True, exist_ok=True)
    return session_folder


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files[]')
    uploaded_files = []
    errors = []
    
    for file in files:
        if file.filename == '':
            continue
        
        if not allowed_file(file.filename):
            errors.append(f'{file.filename}: Unsupported file type')
            continue
        
        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            upload_folder = get_session_folder('upload')
            file_path = upload_folder / filename
            
            # Handle duplicate filenames
            counter = 1
            while file_path.exists():
                stem = Path(filename).stem
                ext = Path(filename).suffix
                filename = f"{stem}_{counter}{ext}"
                file_path = upload_folder / filename
                counter += 1
            
            file.save(str(file_path))
            
            uploaded_files.append({
                'id': str(uuid.uuid4()),
                'filename': filename,
                'size': file_path.stat().st_size,
                'path': str(file_path)
            })
        
        except Exception as e:
            errors.append(f'{file.filename}: {str(e)}')
    
    return jsonify({
        'uploaded': uploaded_files,
        'errors': errors
    })


@app.route('/convert', methods=['POST'])
def convert_file():
    """Convert uploaded file to Markdown"""
    data = request.json
    file_path = Path(data.get('path'))
    
    if not file_path.exists():
        return jsonify({'error': 'File not found'}), 404
    
    try:
        # Convert file
        markdown_content, error = converter.convert_file(file_path)
        
        if error:
            return jsonify({'error': error}), 500
        
        # Generate output filename
        timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
        base_name = file_path.stem
        output_filename = f"{timestamp}_{base_name}_markdown.md"
        
        # Save markdown
        output_folder = get_session_folder('output')
        output_path = output_folder / output_filename
        
        output_path.write_text(markdown_content, encoding='utf-8')
        
        return jsonify({
            'success': True,
            'output_filename': output_filename,
            'output_path': str(output_path),
            'size': len(markdown_content)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>')
def download_file(filename):
    """Download converted markdown file"""
    output_folder = get_session_folder('output')
    file_path = output_folder / secure_filename(filename)
    
    if not file_path.exists():
        return "File not found", 404
    
    return send_file(
        str(file_path),
        as_attachment=True,
        download_name=filename
    )


@app.route('/cleanup', methods=['POST'])
def cleanup():
    """Clean up session files"""
    if 'session_id' in session:
        session_id = session['session_id']
        
        # Remove upload folder
        upload_folder = UPLOAD_FOLDER / session_id
        if upload_folder.exists():
            shutil.rmtree(upload_folder)
        
        # Remove output folder
        output_folder = OUTPUT_FOLDER / session_id
        if output_folder.exists():
            shutil.rmtree(output_folder)
        
        session.pop('session_id', None)
    
    return jsonify({'success': True})


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 MarkItDown Web Converter Starting...")
    print("="*60)
    print("\n📍 Open your browser and go to:\n")
    print("   http://localhost:5000")
    print("   http://127.0.0.1:5000")
    print("\n💡 Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)