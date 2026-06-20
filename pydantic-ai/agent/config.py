"""Shared paths and settings.

Everything is resolved relative to the project root so the agent and the seed
script agree on where the sample data lives, regardless of the current working
directory. Override any path with the matching environment variable.
"""

from __future__ import annotations

import os
from pathlib import Path

# pydantic-ai/agent/config.py -> pydantic-ai/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("AGENT_DATA_DIR", PROJECT_ROOT / "data"))

DB_PATH = Path(os.environ.get("AGENT_DB_PATH", DATA_DIR / "sample.db"))
XLSX_PATH = Path(os.environ.get("AGENT_XLSX_PATH", DATA_DIR / "sample.xlsx"))
PPTX_PATH = Path(os.environ.get("AGENT_PPTX_PATH", DATA_DIR / "sample.pptx"))


def _env_bool(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


# Auth backend: by default Pydantic AI uses the Anthropic API (ANTHROPIC_API_KEY).
# Set AGENT_USE_BEDROCK=1 to route through Amazon Bedrock instead (no API key).
USE_BEDROCK = _env_bool("AGENT_USE_BEDROCK")

# Pydantic AI infers the provider from the model string prefix. Bedrock needs a
# Bedrock model id / inference profile (region-prefixed: jp.* for ap-northeast-1,
# us.* for us-* regions); the Anthropic API uses an alias. AWS credentials/region
# for the Bedrock path come from the standard boto3 chain (AWS_PROFILE / SSO /
# env vars / instance role; region from AWS_REGION / AWS_DEFAULT_REGION).
_DEFAULT_MODEL = (
    "bedrock:jp.anthropic.claude-sonnet-4-5-20250929-v1:0"
    if USE_BEDROCK
    else "anthropic:claude-sonnet-4-5"
)
MODEL = os.environ.get("AGENT_MODEL", _DEFAULT_MODEL)
