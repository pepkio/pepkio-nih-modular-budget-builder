"""Test configuration and environment loading."""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

# Load workspace level .env if present
workspace_env = Path(__file__).resolve().parents[3] / ".env"
if workspace_env.exists():
    load_dotenv(workspace_env)
else:
    load_dotenv()
