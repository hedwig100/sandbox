from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
import os 
import google.auth 

os.environ["GOOGLE_API_KEY"] = ""
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"

# credentials, project_id = google.auth.default()

# print(project_id, credentials)

# 埋め込みモデルの準備
# こっちだとGCPの権限ではできない、GOOGLEAISTUIDのほうでやるしかない
# と思っていたがGOOGLE_GENAI_USE_VERTEXAI変数を指定すると使える
embed_model = GoogleGenAIEmbedding(
    model_name="text-embedding-004",
    project="my-sandbox-forever",
    location="asia-northeast1",
    # credentials=credentials,
)
query = "Vertex AIでLlamaIndexを使ってみたい"
embedding_vector = embed_model.get_query_embedding(query)

print(f"Embedding vector (最初の5要素): {embedding_vector[:5]}")


# documents = SimpleDirectoryReader("data").load_data()
# index = VectorStoreIndex.from_documents(documents)
# retriever = index.as_retriever()
# print(retriever.retrieve("こんにちは"))