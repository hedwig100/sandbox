"""SQLite tools: schema discovery, read-only fetch, and keyword search.

Plain functions (no ``RunContext`` needed) that Pydantic AI turns into tools.
They are deliberately read-only:

  * ``db_list_tables`` -> learn the schema (tables + columns) before querying.
  * ``db_query``       -> run an arbitrary ``SELECT`` (the "fetch" power tool);
                          anything that is not a single SELECT is rejected.
  * ``db_search``      -> ``LIKE`` keyword search across a table's text columns.

Table/column identifiers can't be SQL parameters, so where we interpolate them
we validate against the live schema first (allow-list), keeping the surface safe
from injection. The DB is opened read-only as a second line of defense.
"""

from __future__ import annotations

import sqlite3

from agent.config import DB_PATH

MAX_ROWS = 200


def _connect() -> sqlite3.Connection:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"SQLite DB not found at {DB_PATH}. Run `uv run seed` first."
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
    # `table` is validated by the caller against _table_names first.
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


def db_list_tables() -> str:
    """List all tables in the SQLite database with their columns and types.

    Call this first to learn the schema before querying or searching.
    """
    with _connect() as conn:
        parts = []
        for table in _table_names(conn):
            cols = ", ".join(f"{c['name']} {c['type']}" for c in _columns(conn, table))
            parts.append(f"- **{table}**({cols})")
    return "\n".join(parts) if parts else "(database has no tables)"


def db_query(sql: str) -> str:
    """Run a read-only SQL SELECT query against the SQLite database.

    Only a single SELECT/WITH statement is allowed (no INSERT/UPDATE/DELETE/DDL).

    Args:
        sql: The SQL SELECT statement to execute.
    """
    if not _is_read_only_select(sql):
        return "Rejected: only a single read-only SELECT/WITH statement is allowed."
    try:
        with _connect() as conn:
            rows = conn.execute(sql).fetchmany(MAX_ROWS)
    except sqlite3.Error as e:
        return f"SQL error: {e}"
    return _rows_to_markdown(rows)


def db_search(table: str, keyword: str) -> str:
    """Case-insensitive keyword search across all text columns of a table.

    Use db_list_tables first to pick a valid table name.

    Args:
        table: The table to search in.
        keyword: The substring to look for.
    """
    with _connect() as conn:
        if table not in _table_names(conn):  # allow-list the identifier
            return f"Unknown table: {table!r}."
        text_cols = [
            c["name"]
            for c in _columns(conn, table)
            if "char" in c["type"].lower() or "text" in c["type"].lower()
        ]
        if not text_cols:
            return f"{table} has no text columns to search."
        where = " OR ".join(f"{col} LIKE ?" for col in text_cols)
        params = [f"%{keyword}%"] * len(text_cols)
        rows = conn.execute(
            f"SELECT * FROM {table} WHERE {where} LIMIT {MAX_ROWS}", params
        ).fetchall()
    return _rows_to_markdown(rows)


DATABASE_TOOLS = [db_list_tables, db_query, db_search]
