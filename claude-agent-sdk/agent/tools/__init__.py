"""Custom SDK tools, grouped into in-process MCP servers.

Each module exposes a `create_sdk_mcp_server(...)` instance plus the list of
fully-qualified tool names (``mcp__<server>__<tool>``) so `agent.main` can wire
them into `ClaudeAgentOptions` without hard-coding strings.
"""

from agent.tools.database import DATABASE_SERVER, DATABASE_TOOL_NAMES
from agent.tools.documents import DOCUMENTS_SERVER, DOCUMENTS_TOOL_NAMES

__all__ = [
    "DATABASE_SERVER",
    "DATABASE_TOOL_NAMES",
    "DOCUMENTS_SERVER",
    "DOCUMENTS_TOOL_NAMES",
]
