import os
import oci 

from oci.ai_document import AIServiceDocumentClient
from oci.ai_document.models import AnalyzeDocumentDetails

from flask import Flask, request, jsonify

app = Flask(__name__)
config = oci.config.from_file()

ai_document_client = AIServiceDocumentClient(config)

@app.route("/")
def hello_world():
  return "<p>Hello, World!</p>"

# https://docs.oracle.com/en-us/iaas/api/#/en/document-understanding/20221109/ProcessorJob/CreateProcessorJob

@app.route('/analyze-document', methods=['POST'])
def analyze_document():
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

