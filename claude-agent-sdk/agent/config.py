"""Shared paths and settings.

Everything is resolved relative to the project root so the agent and the seed
script agree on where the sample data lives, regardless of the current working
directory. Override any path with the matching environment variable.
"""

from __future__ import annotations

import os
from pathlib import Path

# claude-agent-sdk/agent/config.py -> claude-agent-sdk/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("AGENT_DATA_DIR", PROJECT_ROOT / "data"))

DB_PATH = Path(os.environ.get("AGENT_DB_PATH", DATA_DIR / "sample.db"))
XLSX_PATH = Path(os.environ.get("AGENT_XLSX_PATH", DATA_DIR / "sample.xlsx"))
PPTX_PATH = Path(os.environ.get("AGENT_PPTX_PATH", DATA_DIR / "sample.pptx"))

def _env_bool(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


# Auth backend: by default the SDK uses ANTHROPIC_API_KEY. Set AGENT_USE_BEDROCK=1
# to route through Amazon Bedrock instead (no API key needed).
USE_BEDROCK = _env_bool("AGENT_USE_BEDROCK")

# The agent SDK talks to Claude through the Claude Code runtime; pick the model
# here so it is easy to swap. Bedrock needs a Bedrock model id / inference
# profile (region-prefixed: apac.* for ap-northeast-1, us.* for us-* regions);
# the direct API uses an Anthropic alias.
_DEFAULT_MODEL = (
    "jp.anthropic.claude-sonnet-4-5-20250929-v1:0"
    if USE_BEDROCK
    else "claude-sonnet-4-5"
)
MODEL = os.environ.get("AGENT_MODEL", _DEFAULT_MODEL)


def bedrock_env() -> dict[str, str]:
    """Env overrides for the SDK's CLI process when using Bedrock.

    Only ``CLAUDE_CODE_USE_BEDROCK`` is forced. AWS credentials are left to the
    standard resolution chain (env vars, ``AWS_PROFILE``, SSO, instance role) via
    the inherited environment, so this works with whatever AWS auth you already
    use. Region/profile are echoed through only when set, to make intent explicit.
    """
    if not USE_BEDROCK:
        return {}
    env = {"CLAUDE_CODE_USE_BEDROCK": "1"}
    for key in ("AWS_REGION", "AWS_PROFILE"):
        value = os.environ.get(key)
        if value:
            env[key] = value
    return env
