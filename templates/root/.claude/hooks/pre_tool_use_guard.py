#!/usr/bin/env python3
"""Fail-closed guard for obviously unsafe Claude Code tool calls."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any


SECRET_MARKERS = (
    ".env",
    ".pem",
    ".key",
    ".p12",
    ".pfx",
    "/.ssh/",
    "/.aws/",
    "secret",
    "credential",
    "private_key",
)

DANGEROUS_BASH_PATTERNS = [
    r"\brm\s+-rf\s+/",
    r"\brm\s+-rf\s+\.",
    r"\brm\s+-rf\s+\*",
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+clean\s+-[A-Za-z]*f",
    r"\bgit\s+checkout\s+--\s+\.",
    r"\bchmod\s+-R\s+777\b",
    r"\bsudo\b",
    r"(curl|wget)\b.*\|\s*(sh|bash)\b",
    r":\s*\(\)\s*\{",
]


def read_input() -> dict[str, Any]:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def deny(reason: str) -> int:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )
    return 0


def normalize_path(value: str, cwd: str) -> str:
    try:
        return str(Path(cwd, value).resolve()).lower()
    except Exception:
        return value.lower()


def extract_path(tool_input: dict[str, Any]) -> str:
    for key in ("file_path", "path", "target_file", "notebook_path"):
        value = tool_input.get(key)
        if isinstance(value, str):
            return value
    return ""


def main() -> int:
    data = read_input()
    tool_name = data.get("tool_name") or data.get("toolName") or ""
    tool_input = data.get("tool_input") or data.get("toolInput") or {}
    if not isinstance(tool_input, dict):
        tool_input = {}
    cwd = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or "."

    if tool_name == "Bash":
        command = str(tool_input.get("command", ""))
        for pattern in DANGEROUS_BASH_PATTERNS:
            if re.search(pattern, command, flags=re.IGNORECASE):
                return deny(
                    "Blocked by generated harness guard. Record explicit human approval and use a narrower safe command."
                )

    if tool_name in {"Read", "Write", "Edit", "MultiEdit"}:
        path = normalize_path(extract_path(tool_input), cwd)
        if any(marker in path for marker in SECRET_MARKERS):
            return deny(
                "Blocked secret/credential path. Use the approval packet and credential lifecycle policy before access."
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

