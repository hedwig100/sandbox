from llama_index.core import Document, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import MetadataMode
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
import settings
from typing import Any

documents = [
    Document(id_="doc_0",text="""LlamaIndexは強力な情報検索ライブラリです
LlamaIndexを使うと、様々なデータソースから情報を効率的に検索できます。
例えば、ドキュメント、ウェブページ、データベースなどから情報を抽出できます。
さらに、LlamaIndexは高度な検索アルゴリズムを提供し、ユーザーのクエリに対して最適な結果を返します。
LlamaIndexを使って、あなたのアプリケーションに強力な検索機能を追加しましょう。
"""),
    Document(id_="doc_1",text="""Google Agent Development Kit (ADK) は、
GoogleのAIエージェントを開発するためのツールキットです。
ADKを使用すると、開発者はGoogleの生成AIモデルを活用して、
カスタムAIエージェントを構築できます。
ADKは、エージェントの設計、トレーニング、デプロイメントをサポートし、
効率的な開発プロセスを提供します。
Google ADKを使って、革新的なAIエージェントを作成しましょう。
"""),
    Document(id_="doc_2",text="""Vertex AIとGoogle GenAIの統合。
Vertex AIは、Google Cloud上で機械学習モデルを構築、デプロイ、管理するためのプラットフォームです。
Google GenAIは、生成AIモデルを活用して、テキスト、画像、音声などのコンテンツを生成するためのサービスです。
"""),
]

class SentenceSplitterWithDocument(SentenceSplitter):
    def get_nodes_from_document(self, documents: list[Document], show_progress: bool = False,
        **kwargs: Any) -> list[Document]:
        nodes = super().get_nodes_from_document(documents, show_progress, **kwargs)
        nodes.extend(documents)
        return nodes

chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.get_or_create_collection("example_collection")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

parser = SentenceSplitterWithDocument(chunk_size=100, chunk_overlap=10)
# nodes = parser.get_nodes_from_documents(documents)
# for node in nodes:
#     print(node)
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    transformations=[parser],
    store_nodes_override=True
)
refreshed = index.refresh_ref_docs(documents)
print(f"Refreshed documents: {refreshed}")
retriever = index.as_retriever()
results = retriever.retrieve("AIエージェント開発したい")

for res in results:
    print(f"Doc ID: {res.node.ref_doc_id}")
    print(f"Text: {res.get_text()}")
    x = vector_store.get_nodes(node_ids=[res.node.ref_doc_id])[0]
    print(f"Original Document: {x.get_text()}")

print(chroma_collection.count())
