"""
Flask API for MarkItDown Converter v2.4.2
Provides REST endpoints for the web interface
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import tempfile
import logging
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from pptx_converter_v242 import convert_pptx_v242

app = Flask(__name__)
CORS(app)  # Enable CORS for web interface

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {'pptx', 'ppt'}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'version': '2.4.2',
        'service': 'MarkItDown Converter API'
    })


@app.route('/api/version', methods=['GET'])
def get_version():
    """Get API version and capabilities."""
    return jsonify({
        'version': '2.4.2',
        'features': {
            'tables_preserved': True,
            'list_hierarchy': True,
            'line_breaks_fixed': True,
            'unicode_normalized': True,
            'schema_standardized': True
        },
        'supported_formats': ['pptx', 'ppt'],
        'max_file_size_mb': MAX_FILE_SIZE / (1024 * 1024)
    })


@app.route('/api/convert/pptx', methods=['POST'])
def convert_pptx():
    """
    Convert PPTX file to Markdown with v2.4.2 fixes.
    
    Expects:
        multipart/form-data with 'file' field
    
    Returns:
        JSON with:
        - success: boolean
        - markdown: converted markdown text
        - stats: detailed statistics
        - quality_score: 0-100 quality score
        - filename: original filename
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                'success': False,
                'error': f'File too large. Maximum size: {MAX_FILE_SIZE / (1024 * 1024)}MB'
            }), 400
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pptx') as tmp_file:
            tmp_path = tmp_file.name
            file.save(tmp_path)
        
        try:
            # Convert using v2.4.2
            logger.info(f"Converting {file.filename} with v2.4.2")
            result = convert_pptx_v242(tmp_path)
            
            if result['success']:
                # Calculate quality score
                from pptx_converter_v242 import PPTXConverterV242
                converter = PPTXConverterV242()
                converter.stats = result['stats']
                quality_score = converter.get_quality_score()
                
                logger.info(
                    f"Conversion successful: {file.filename}, "
                    f"{result['stats']['total_fixes']} fixes, "
                    f"quality: {quality_score:.1f}"
                )
                
                return jsonify({
                    'success': True,
                    'markdown': result['markdown'],
                    'stats': result['stats'],
                    'quality_score': quality_score,
                    'filename': file.filename,
                    'version': '2.4.2'
                })
            else:
                logger.error(f"Conversion failed: {result.get('error')}")
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Conversion failed')
                }), 500
        
        finally:
            # Clean up temporary file
            try:
                os.unlink(tmp_path)
            except:
                pass
    
    except Exception as e:
        logger.error(f"API error: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get API usage statistics (placeholder for future implementation).
    """
    return jsonify({
        'total_conversions': 0,
        'total_fixes_applied': 0,
        'average_quality_score': 0.0,
        'note': 'Statistics tracking not yet implemented'
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Development server
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting MarkItDown Converter API v2.4.2 on port {port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
