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
)

retriever = index.as_retriever()
results = retriever.retrieve("AIエージェント開発したい")

nodes = storage_context.docstore.to_dict()["docstore/data"]
for result in results:
    child_nodes = storage_context.docstore.get_ref_doc_info(result.node.ref_doc_id)
    for node_id in child_nodes.node_ids:
        node = nodes[node_id]["__data__"]
        print(f"Text : {node.get('text')}, Start: {node.get('start_char_idx')}, End: {node.get('end_char_idx')}")
        print(len(node.get("text")))