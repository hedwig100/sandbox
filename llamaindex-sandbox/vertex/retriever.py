from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
import os  

os.environ["GOOGLE_API_KEY"] = ""
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"

Settings.embed_model = GoogleGenAIEmbedding(
    model_name="text-embedding-004",
    project="my-sandbox-forever",
    location="asia-northeast1",
)

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
retriever = index.as_retriever()
print(retriever.retrieve("こんにちは"))