import oci 

from oci.generative_ai_inference import GenerativeAiInferenceClient

from oci.ai_document import AIServiceDocumentClient
from oci.ai_document.models import AnalyzeDocumentDetails
from oci.ai_document.models import DocumentClassificationFeature

config = oci.config.from_file()

generative_ai_inference_client = GenerativeAiInferenceClient(config)