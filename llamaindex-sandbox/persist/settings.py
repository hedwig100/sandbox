from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import Settings
import os  

os.environ["GOOGLE_API_KEY"] = ""
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"

Settings.embed_model = GoogleGenAIEmbedding(
    model_name="text-embedding-004",
    project="my-sandbox-forever",
    location="asia-northeast1",
)
