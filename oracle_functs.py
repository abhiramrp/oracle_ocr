import oci 

from oci.generative_ai_inference import GenerativeAiInferenceClient

from oci.ai_document import AIServiceDocumentClient
from oci.ai_document.models import AnalyzeDocumentDetails
from oci.ai_document.models import DocumentClassificationFeature

config = oci.config.from_file()

generative_ai_inference_client = GenerativeAiInferenceClient(config)
doc_client = AIServiceDocumentClient(config)

def analyze_document(file_path):
    with open(file_path, 'rb') as f:
        document_content = f.read()

    # Prepare the document for analysis
    document = Document(content=document_content, content_type="application/pdf")

    # Analyze document details
    analyze_document_details = AnalyzeDocumentDetails(
        document=document,
        features=['TEXT_EXTRACTION']  # You can add more features
    )

    # Call the OCI Document Understanding service
    response = doc_client.analyze_document(analyze_document_details)
    return response.data

@app.route('/analyze-document', methods=['POST'])
def analyze_uploaded_document():
    file = request.files['file']
    file_path = f"./uploads/{file.filename}"
    file.save(file_path)
    
    analysis_result = analyze_document(file_path)
    return jsonify({'text': analysis_result.text})