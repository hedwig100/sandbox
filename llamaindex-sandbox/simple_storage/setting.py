from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding

# LLMの準備
Settings.llm = Gemini(
    model_name="models/gemini-2.5-flash",
)

# 埋め込みモデルの準備
Settings.embed_model = GeminiEmbedding(
    model_name="models/embedding-001", 
)