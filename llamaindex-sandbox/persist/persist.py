from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    Document,
)
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.node_parser import SentenceSplitter
from chromadb import PersistentClient
import os
import settings
from documents import documents

PERSIST_DIR = "./storage"
DOCSTORE_PATH = os.path.join(PERSIST_DIR, "docstore.json")
CHROMA_PATH = os.path.join(PERSIST_DIR, "chroma")


chroma_client = PersistentClient(path=CHROMA_PATH)
chroma_collection = chroma_client.get_or_create_collection("my_persis_collection")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# StorageContext を作成（docstore + vector store）
storage_context = StorageContext.from_defaults(
    vector_store=vector_store,
)

parser = SentenceSplitter(chunk_size=100, chunk_overlap=10)

# Index を作成
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    transformations=[parser],
    store_nodes_override=True
)

# 永続化
storage_context.persist(persist_dir=PERSIST_DIR)

print("Ingestion 完了 & 永続化済み！")
