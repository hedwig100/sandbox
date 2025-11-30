from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
import settings
from documents import documents

PERSIST_DIR = "./storage"

db = chromadb.PersistentClient(path="./storage/chroma")
chroma_collection = db.get_or_create_collection("my_persis_collection")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# 永続化された storage context をロード
storage_context = StorageContext.from_defaults(vector_store=vector_store,persist_dir=PERSIST_DIR)

# Index を復元
index = VectorStoreIndex(
    nodes=[],
    storage_context=storage_context,
    store_nodes_override=True
)

print(index._docstore.get_all_ref_doc_info())
refreshed = index.refresh_ref_docs(documents)
print(f"Refreshed documents: {refreshed}")
print(f"Count: {chroma_collection.count()}")
storage_context.persist(persist_dir=PERSIST_DIR)
