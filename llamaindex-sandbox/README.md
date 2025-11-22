# Lalama index

- `uv add llama-index`
- まずはモデルを設定する(embeddingモデルが必要なので)
    - たぶんvertex aiでgeminiが楽そう
    - [LlamaIndex + Gemini](https://www.llamaindex.ai/blog/llamaindex-gemini-8d7c3b9ea97e)
    - `uv add llama-index-llms-gemini`
    - `uv add llama-index-embeddings-gemini`
    - GCP Vertex AIでgemini api keyを発行する
    - 上のではAPIの種類がちがくてできないので[Google AI Studio](https://aistudio.google.com/api-keys)の方でAPIキーを発行する、請求はGCPに紐づくっポイ。
    - うごいた
