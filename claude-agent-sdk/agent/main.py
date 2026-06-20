"""Entry point: a single-shot agent over `query()`.

Wires three capability groups into one agent:

  1. Web    -> the SDK's built-in ``WebFetch`` / ``WebSearch`` tools.
  2. DB     -> custom SQLite tools (fetch + search) from `agent.tools.database`.
  3. Office -> custom Excel / PowerPoint readers from `agent.tools.documents`.

Usage:
    poetry run agent "your question"
    # or, with no prompt, a demo question is used.
"""

from __future__ import annotations

import asyncio
import sys

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    query,
)

from agent.config import MODEL, bedrock_env
from agent.tools import (
    DATABASE_SERVER,
    DATABASE_TOOL_NAMES,
    DOCUMENTS_SERVER,
    DOCUMENTS_TOOL_NAMES,
)

BUILTIN_WEB_TOOLS = ["WebFetch", "WebSearch"]

SYSTEM_PROMPT = (
    "あなたはデータアシスタントです。Web の取得・検索（WebFetch / WebSearch）、"
    "ローカルの SQLite データベースへの問い合わせ、Excel / PowerPoint ファイルの"
    "読み取りができます。データベースについて聞かれたら、まず db_list_tables を"
    "呼んでスキーマを把握してください。推測ではなくツールを使い、それぞれの事実が"
    "どこから得られたかを示してください。回答は日本語で書いてください。"
)

DEFAULT_PROMPT = (
    "データベースにはどんなテーブルがありますか？また、在庫が少ない商品はどれですか？"
    "あわせて、同梱の PowerPoint 資料も要約してください。"
)


def build_options() -> ClaudeAgentOptions:
    return ClaudeAgentOptions(
        model=MODEL,
        system_prompt=SYSTEM_PROMPT,
        env=bedrock_env(),  # {} for the API-key path; Bedrock vars when enabled
        mcp_servers={
            "database": DATABASE_SERVER,
            "documents": DOCUMENTS_SERVER,
        },
        allowed_tools=[
            *BUILTIN_WEB_TOOLS,
            *DATABASE_TOOL_NAMES,
            *DOCUMENTS_TOOL_NAMES,
        ],
    )


async def run(prompt: str) -> None:
    async for message in query(prompt=prompt, options=build_options()):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
                elif isinstance(block, ToolUseBlock):
                    print(f"\n  [tool] {block.name} {block.input}\n")
        elif isinstance(message, ResultMessage):
            cost = getattr(message, "total_cost_usd", None)
            if cost is not None:
                print(f"\n--- done (cost: ${cost:.4f}) ---")


def cli() -> None:
    prompt = " ".join(sys.argv[1:]).strip() or DEFAULT_PROMPT
    asyncio.run(run(prompt))


if __name__ == "__main__":
    cli()
