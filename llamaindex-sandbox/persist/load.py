from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
import settings

PERSIST_DIR = "./storage"

# 永続化された storage context をロード
storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)

# Index を復元
# db = chromadb.PersistentClient(path="./storage/chroma")
# chroma_collection = db.get_or_create_collection("my_persis_collection")
# vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
# index = VectorStoreIndex.from_vector_store(
#     vector_store=vector_store,
#     storage_context=storage_context,
# )
# retriever = index.as_retriever()
# results = retriever.retrieve("AIエージェント開発したい")

# for res in results:
#     doc = storage_context.docstore.get_document(res.node.ref_doc_id)
#     print(f"Doc ID: {res.node.ref_doc_id}")
#     print(f"Text: {doc.get_text()}")

###########
# print(storage_context.docstore.get_all_ref_doc_info())
nodes = storage_context.docstore.to_dict()["docstore/data"]
child_nodes = storage_context.docstore.get_ref_doc_info("doc_1")
for node_id in child_nodes.node_ids:
    node = nodes[node_id]["__data__"]
    print(f"Text : {node.get('text')}, Start: {node.get('start_char_idx')}, End: {node.get('end_char_idx')}")
    print(len(node.get("text")))