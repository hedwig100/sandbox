# pydantic-ai sandbox

An agent built with [Pydantic AI](https://ai.pydantic.dev/) that can:

| Capability | Tool(s) | Kind |
| --- | --- | --- |
| Fetch a web page | `fetch_url` | custom (httpx + BeautifulSoup) |
| Fetch data from a DB | `db_query` (read-only SELECT) | custom (SQLite) |
| Search a DB | `db_search` (keyword `LIKE`) | custom (SQLite) |
| Discover the schema | `db_list_tables` | custom (SQLite) |
| Read unstructured Office files | `read_excel`, `read_powerpoint` | custom (openpyxl / python-pptx) |

This is the Pydantic AI counterpart of the `../claude-agent-sdk` sandbox — same
tools and sample data, different framework.

## How it's wired

Tools are plain functions; Pydantic AI builds each tool's JSON schema from the
function signature + docstring. They're collected and passed to
`Agent(tools=...)`, and `agent.run_sync(prompt)` runs a single turn.

- `agent/tools/database.py` — the SQLite tools (read-only)
- `agent/tools/documents.py` — the Office readers (openpyxl / python-pptx)
- `agent/tools/web.py` — the custom web-fetch tool
- `agent/main.py` — builds the `Agent` and runs `run_sync()`
- `agent/seed.py` — generates the sample `data/` (DB + xlsx + pptx)

```
fetch_url (web)      ─┐
db_* (SQLite)        ─┼─► Agent(tools=[...]) ─► run_sync(prompt).output
read_* (Office)      ─┘
```

> Pydantic AI has no built-in WebFetch (unlike the Claude Agent SDK), so web
> access is the custom `fetch_url` tool. For web *search*, add Pydantic AI's
> first-class `duckduckgo_search_tool` / Tavily tool to the agent.

## Prerequisites

- Python 3.10+ and [uv](https://docs.astral.sh/uv/)
- Auth — either `ANTHROPIC_API_KEY`, **or** Amazon Bedrock (see below)

## Setup & run

```bash
cd pydantic-ai
uv sync
uv run seed                          # create data/sample.{db,xlsx,pptx}
export ANTHROPIC_API_KEY=sk-...
uv run agent "在庫切れの商品は？"
uv run agent                         # uses the built-in demo prompt
```

### Auth via Amazon Bedrock (no API key)

Set `AGENT_USE_BEDROCK=1` and use your normal AWS credentials. The default model
switches to a Bedrock model id, and Pydantic AI's Bedrock provider resolves
credentials through the standard boto3 chain (`AWS_PROFILE` / SSO / env vars /
instance role; region from `AWS_REGION` / `AWS_DEFAULT_REGION`).

```bash
export AGENT_USE_BEDROCK=1
export AWS_REGION=ap-northeast-1
export AWS_PROFILE=your-profile       # or AWS SSO / env keys / instance role
# Override if your account enables a different model / inference profile:
# export AGENT_MODEL=bedrock:us.anthropic.claude-sonnet-4-5-20250929-v1:0
uv run agent "在庫切れの商品は？"
```

> The default Bedrock model id (`bedrock:jp.anthropic.claude-sonnet-4-5-20250929-v1:0`,
> the Japan inference profile for `ap-northeast-1`) must be enabled in your
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
| `AGENT_MODEL` | `anthropic:claude-sonnet-4-5` (Bedrock: `bedrock:jp.anthropic.claude-sonnet-4-5-20250929-v1:0`) |

## Safety notes

- DB access is opened `mode=ro`; `db_query` accepts only a single `SELECT`/`WITH`
  statement and `db_search` allow-lists table/column names against the live
  schema, so neither can mutate data or be SQL-injected.
- Only the listed tools are exposed to the model; there is no `Bash`/file-write
  capability.
