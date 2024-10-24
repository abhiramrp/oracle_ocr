import os

from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename

from oracle_functs import process_with_oci

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'  # Folder to store uploaded files
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max upload size (16 MB)

# Allowed file extensions (for security)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze-document', methods=['POST'])
def analyze_document():
    
    if request.method == 'POST':
      if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
      
      file = request.files['file']

      if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
        
      if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)  # Sanitize the filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        r = process_with_oci(file_path)
        return f"File {filename} uploaded successfully! {r}"
    
    return redirect(url_for('index'))
