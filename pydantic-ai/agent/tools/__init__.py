"""Plain tool functions, grouped by capability.

Pydantic AI builds each tool's schema from the function signature + docstring,
so the tools are just ordinary functions returning ``str``. `agent.main`
collects the lists below and passes them to ``Agent(tools=...)``.
"""

from agent.tools.database import DATABASE_TOOLS
from agent.tools.documents import DOCUMENT_TOOLS
from agent.tools.web import WEB_TOOLS

__all__ = ["DATABASE_TOOLS", "DOCUMENT_TOOLS", "WEB_TOOLS"]
