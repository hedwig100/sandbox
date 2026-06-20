"""SQLite tools: schema discovery, read-only fetch, and keyword search.

These are *custom* tools (the `@tool` decorator) bundled into one in-process MCP
server. They are deliberately read-only:

  * ``db_list_tables`` -> the agent first learns the schema (table + column
    names) so it can write correct queries / pick the right table.
  * ``db_query``       -> run an arbitrary ``SELECT`` (the "fetch" power tool).
                          Anything that is not a single SELECT is rejected.
  * ``db_search``      -> ``LIKE`` keyword search across a table's text columns
                          (the "search" tool) without the agent having to know
                          which columns are text.

Table/column identifiers can't be passed as SQL parameters, so where we have to
interpolate them we validate against the live schema first (allow-list), which
keeps the surface safe from injection.
"""

from __future__ import annotations

import sqlite3
from typing import Any

from claude_agent_sdk import create_sdk_mcp_server, tool

from agent.config import DB_PATH

MAX_ROWS = 200


def _connect() -> sqlite3.Connection:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"SQLite DB not found at {DB_PATH}. Run `poetry run seed` first."
        )
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _table_names(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'sqlite_%' ORDER BY name"
    ).fetchall()
    return [r["name"] for r in rows]


def _columns(conn: sqlite3.Connection, table: str) -> list[sqlite3.Row]:
    # `table` is validated by the caller against _table_names before we reach
    # here, so the f-string interpolation is safe.
    return conn.execute(f"PRAGMA table_info({table})").fetchall()


def _rows_to_markdown(rows: list[sqlite3.Row]) -> str:
    if not rows:
        return "(no rows)"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row[h]) for h in headers) + " |")
    return "\n".join(lines)


def _is_read_only_select(sql: str) -> bool:
    """Allow exactly one statement that begins with SELECT or WITH."""
    stripped = sql.strip().rstrip(";").strip()
    if ";" in stripped:  # reject stacked statements
        return False
    head = stripped.lstrip("(").split(None, 1)
    return bool(head) and head[0].lower() in {"select", "with"}


@tool(
    "db_list_tables",
    "List all tables in the SQLite database with their columns and types. "
    "Call this first to learn the schema before querying or searching.",
    {},
)
async def db_list_tables(args: dict[str, Any]) -> dict[str, Any]:
    with _connect() as conn:
        parts = []
        for table in _table_names(conn):
            cols = ", ".join(f"{c['name']} {c['type']}" for c in _columns(conn, table))
            parts.append(f"- **{table}**({cols})")
    body = "\n".join(parts) if parts else "(database has no tables)"
    return {"content": [{"type": "text", "text": body}]}


@tool(
    "db_query",
    "Run a read-only SQL SELECT query against the SQLite database and return the "
    "rows. Only a single SELECT/WITH statement is allowed (no INSERT/UPDATE/"
    "DELETE/DDL).",
    {"sql": str},
)
async def db_query(args: dict[str, Any]) -> dict[str, Any]:
    sql = str(args.get("sql", ""))
    if not _is_read_only_select(sql):
        return {
            "content": [
                {
                    "type": "text",
                    "text": "Rejected: only a single read-only SELECT/WITH "
                    "statement is allowed.",
                }
            ],
            "is_error": True,
        }
    try:
        with _connect() as conn:
            rows = conn.execute(sql).fetchmany(MAX_ROWS)
    except sqlite3.Error as e:
        return {
            "content": [{"type": "text", "text": f"SQL error: {e}"}],
            "is_error": True,
        }
    return {"content": [{"type": "text", "text": _rows_to_markdown(rows)}]}


@tool(
    "db_search",
    "Case-insensitive keyword search across all text columns of a table. "
    "Use db_list_tables first to pick a valid table name.",
    {"table": str, "keyword": str},
)
async def db_search(args: dict[str, Any]) -> dict[str, Any]:
    table = str(args.get("table", ""))
    keyword = str(args.get("keyword", ""))
    with _connect() as conn:
        if table not in _table_names(conn):  # allow-list the identifier
            return {
                "content": [
                    {"type": "text", "text": f"Unknown table: {table!r}."}
                ],
                "is_error": True,
            }
        text_cols = [
            c["name"]
            for c in _columns(conn, table)
            if "char" in c["type"].lower() or "text" in c["type"].lower()
        ]
        if not text_cols:
            return {
                "content": [
                    {"type": "text", "text": f"{table} has no text columns to search."}
                ]
            }
        where = " OR ".join(f"{col} LIKE ?" for col in text_cols)
        params = [f"%{keyword}%"] * len(text_cols)
        rows = conn.execute(
            f"SELECT * FROM {table} WHERE {where} LIMIT {MAX_ROWS}", params
        ).fetchall()
    return {"content": [{"type": "text", "text": _rows_to_markdown(rows)}]}


DATABASE_SERVER = create_sdk_mcp_server(
    name="database",
    version="0.1.0",
    tools=[db_list_tables, db_query, db_search],
)

DATABASE_TOOL_NAMES = [
    "mcp__database__db_list_tables",
    "mcp__database__db_query",
    "mcp__database__db_search",
]
