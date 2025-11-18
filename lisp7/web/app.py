"""
LISP-7 Web Interface
Flask application for compression and decompression.
"""

import sys
import os

# Add root directory for imports (go up 2 levels: web -> lisp7 -> root)
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, root_dir)

from flask import Flask, request, jsonify, render_template
import uuid

from lisp7 import (
    compress,
    compress_and_learn,
    decompress,
    decompress_with_key,
    lookup_sentence
)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In-memory storage for uploaded files
files_storage = {}


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and decompression"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.endswith('.txt'):
        return jsonify({'error': 'Only .txt files allowed'}), 400

    file_id = str(uuid.uuid4())
    compressed_content = file.read().decode('utf-8')

    decompressed_content = decompress(compressed_content)
    if decompressed_content is None:
        decompressed_content = "[Not found in database]"

    files_storage[file_id] = {
        'original_name': file.filename,
        'compressed': compressed_content,
        'decompressed': decompressed_content
    }

    return jsonify({
        'file_id': file_id,
        'original_name': file.filename,
        'decompressed': decompressed_content,
        'compressed_size': len(compressed_content),
        'decompressed_size': len(decompressed_content)
    })


@app.route('/read/<file_id>', methods=['GET'])
def read_file(file_id):
    """Read uploaded file by ID"""
    if file_id not in files_storage:
        return jsonify({'error': 'File not found'}), 404

    file_data = files_storage[file_id]

    return jsonify({
        'file_id': file_id,
        'original_name': file_data['original_name'],
        'decompressed': file_data['decompressed'],
        'compressed': file_data['compressed'],
        'compressed_size': len(file_data['compressed']),
        'decompressed_size': len(file_data['decompressed'])
    })


@app.route('/compress', methods=['POST'])
def compress_text():
    """Compress text at specified level"""
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']
    level = data.get('level', 2)

    # Compress and learn
    compressed = compress_and_learn(text, level)

    file_id = str(uuid.uuid4())
    decompressed = decompress(compressed)

    files_storage[file_id] = {
        'original_name': 'compressed.txt',
        'compressed': compressed,
        'decompressed': decompressed
    }

    # For Level 7, get alphabet key
    alphabet_key = None
    if level == 7:
        _, alphabet_key = lookup_sentence(compressed)

    return jsonify({
        'file_id': file_id,
        'original_text': text,
        'compressed': compressed,
        'decompressed': decompressed,
        'alphabet_key': alphabet_key,
        'level': level,
        'original_size': len(text),
        'compressed_size': len(compressed),
        'compression_ratio': round((1 - len(compressed) / len(text)) * 100, 2) if len(text) > 0 else 0
    })


@app.route('/decompress_manual', methods=['POST'])
def decompress_manual():
    """Manual decompression with alphabet key verification"""
    data = request.get_json()

    if not data or 'compressed_text' not in data:
        return jsonify({'error': 'No compressed text provided'}), 400

    compressed_text = data['compressed_text']
    alphabet_key_provided = data.get('alphabet_key', '').strip()

    result = {
        'compressed': compressed_text,
        'has_alphabet_key': bool(alphabet_key_provided and len(alphabet_key_provided) == 26),
        'decompressed_from_db': None,
        'success': False,
        'key_match': False
    }

    # Check database
    original, alphabet_key_db = lookup_sentence(compressed_text)

    if original is None:
        result['db_decompression_success'] = False
        result['db_decompression_error'] = 'Text not found in database'
        return jsonify(result)

    result['db_decompression_success'] = True

    # For Level 7, verify key match
    if alphabet_key_db:  # Level 7
        if alphabet_key_provided and alphabet_key_provided == alphabet_key_db:
            result['key_match'] = True
            result['decompressed_from_db'] = original
            result['success'] = True
        else:
            result['key_match'] = False
            result['db_decompression_error'] = 'Incorrect or missing alphabet key for this Level 7 text'
            result['success'] = False
    else:  # Not Level 7
        result['decompressed_from_db'] = original
        result['success'] = True
        result['key_match'] = True

    return jsonify(result)


if __name__ == '__main__':
    print("=" * 50)
    print("LISP-7 Web Interface")
    print("=" * 50)
    print("Starting server at http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    app.run(debug=True, port=5000)
