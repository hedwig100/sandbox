# claude-agent-sdk sandbox

An agent built with the [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/python)
that can:

| Capability | Tool(s) | Kind |
| --- | --- | --- |
| Fetch / search the web | `WebFetch`, `WebSearch` | SDK built-in |
| Fetch data from a DB | `db_query` (read-only SELECT) | custom (SQLite) |
| Search a DB | `db_search` (keyword `LIKE`) | custom (SQLite) |
| Discover the schema | `db_list_tables` | custom (SQLite) |
| Read unstructured Office files | `read_excel`, `read_powerpoint` | custom (openpyxl / python-pptx) |

## How it's wired

Custom tools are plain `async def`s decorated with `@tool(...)`, grouped into
**in-process MCP servers** via `create_sdk_mcp_server(...)`. The servers and the
allow-listed tool names are passed to `ClaudeAgentOptions`, and `query()` runs a
single turn. See:

- `agent/tools/database.py` — the SQLite tools (simple `{"name": type}` schema)
- `agent/tools/documents.py` — the Office readers (full JSON-Schema for optional args)
- `agent/main.py` — builds `ClaudeAgentOptions` and runs `query()`
- `agent/seed.py` — generates the sample `data/` (DB + xlsx + pptx)

```
WebFetch / WebSearch ─┐
db_* (SQLite)        ─┼─► ClaudeAgentOptions.allowed_tools ─► query()
read_* (Office)      ─┘
```

## Prerequisites

- Python 3.10+ and [uv](https://docs.astral.sh/uv/) (`uv` manages the venv/deps)
- Node.js — the SDK drives the Claude Code runtime, which is a Node CLI
- Auth — either `ANTHROPIC_API_KEY`, **or** Amazon Bedrock (see below)

## Setup & run

```bash
cd claude-agent-sdk
uv sync                              # create .venv and install deps
uv run seed                          # create data/sample.{db,xlsx,pptx}
export ANTHROPIC_API_KEY=sk-...
uv run agent "Which products are out of stock?"
uv run agent                         # uses the built-in demo prompt
```

### Auth via Amazon Bedrock (no API key)

Set `AGENT_USE_BEDROCK=1` and use your normal AWS credentials — `config.py` then
forces `CLAUDE_CODE_USE_BEDROCK=1` into the SDK's CLI process and lets the
standard AWS chain (`AWS_PROFILE` / SSO / env vars / instance role) resolve
credentials. The default model switches to a Bedrock model id.

```bash
export AGENT_USE_BEDROCK=1
export AWS_REGION=ap-northeast-1
export AWS_PROFILE=your-profile       # or AWS SSO / env keys / instance role
# Override if your account enables a different model / inference profile:
# export AGENT_MODEL=us.anthropic.claude-sonnet-4-5-20250929-v1:0
uv run agent "Which products are out of stock?"
```

> The default Bedrock model id (`apac.anthropic.claude-sonnet-4-5-20250929-v1:0`,
> the APAC inference profile for `ap-northeast-1`) must be enabled in your
> account/region. Use the `us.` prefix for `us-*` regions, or set `AGENT_MODEL`
> to whatever model / inference profile you actually have access to.

## Configuration

Paths and the model are read from the environment (see `agent/config.py`):

| Var | Default |
| --- | --- |
| `AGENT_DATA_DIR` | `./data` |
| `AGENT_DB_PATH` | `./data/sample.db` |
| `AGENT_XLSX_PATH` | `./data/sample.xlsx` |
| `AGENT_PPTX_PATH` | `./data/sample.pptx` |
| `AGENT_USE_BEDROCK` | `0` (set `1` to auth via Bedrock) |
| `AGENT_MODEL` | `claude-sonnet-4-5` (Bedrock: `jp.anthropic.claude-sonnet-4-5-20250929-v1:0`) |

## Safety notes

- DB access is opened `mode=ro`; `db_query` accepts only a single `SELECT`/`WITH`
  statement and `db_search` allow-lists table/column names against the live
  schema, so neither can mutate data or be SQL-injected.
- Only the tools listed in `allowed_tools` are exposed to the model; nothing else
  (no `Bash`, `Write`, etc.) is available.
