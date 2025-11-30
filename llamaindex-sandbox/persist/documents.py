from llama_index.core import Document

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