"""Entry point: a single-shot agent built with Pydantic AI.

Wires three capability groups into one agent:

  1. Web    -> custom `fetch_url` tool (httpx + BeautifulSoup).
  2. DB     -> custom SQLite tools (fetch + search) from `agent.tools.database`.
  3. Office -> custom Excel / PowerPoint readers from `agent.tools.documents`.

Usage:
    uv run agent "your question"
    # or, with no prompt, a demo question is used.
"""

from __future__ import annotations

import sys

from pydantic_ai import Agent

from agent.config import MODEL
from agent.tools import DATABASE_TOOLS, DOCUMENT_TOOLS, WEB_TOOLS

SYSTEM_PROMPT = (
    "あなたはデータアシスタントです。Web の取得（fetch_url）、ローカルの SQLite "
    "データベースへの問い合わせ（db_list_tables / db_query / db_search）、"
    "Excel / PowerPoint ファイルの読み取り（read_excel / read_powerpoint）が"
    "できます。データベースについて聞かれたら、まず db_list_tables を呼んで"
    "スキーマを把握してください。推測ではなくツールを使い、それぞれの事実が"
    "どこから得られたかを示してください。回答は日本語で書いてください。"
)

DEFAULT_PROMPT = (
    "データベースにはどんなテーブルがありますか？また、在庫が少ない商品はどれですか？"
    "あわせて、同梱の PowerPoint 資料も要約してください。"
)


def build_agent() -> Agent:
    return Agent(
        MODEL,
        system_prompt=SYSTEM_PROMPT,
        tools=[*WEB_TOOLS, *DATABASE_TOOLS, *DOCUMENT_TOOLS],
    )


def cli() -> None:
    prompt = " ".join(sys.argv[1:]).strip() or DEFAULT_PROMPT
    result = build_agent().run_sync(prompt)
    print(result.output)


if __name__ == "__main__":
    cli()
