import os

from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename

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
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f"File {filename} uploaded successfully!"
      
      
    
    return redirect(url_for('index'))


# https://docs.oracle.com/en-us/iaas/api/#/en/document-understanding/20221109/ProcessorJob/CreateProcessorJob

'''
@app.route('/analyze-document', methods=['POST'])
def analyze_document():
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)

    try:
      # Get the file from the request
      file = request.files['document']
      document_content = file.read()

      # Prepare the AnalyzeDocumentDetails payload
      document_details = AnalyzeDocumentDetails(
        features=["TEXT_EXTRACTION"],
        document={"source": "RAW_TEXT", "content": document_content}
      )

      # Call the Document Understanding API
      response = ai_document_client.analyze_document(analyze_document_details=document_details)

      # Return the analysis result as JSON
      return jsonify(response.data), 200
    
    except Exception as e:
      return jsonify({"error": str(e)}), 500

'''
