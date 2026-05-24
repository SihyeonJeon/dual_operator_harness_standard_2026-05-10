#!/usr/bin/env python3
"""Append safe tool-use metadata to the generated harness event log."""

from __future__ import annotations

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SECRET_KEYS = ("key", "secret", "token", "password", "credential")


def read_input() -> dict[str, Any]:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def project_root(data: dict[str, Any]) -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or ".").resolve()


def safe_text(value: Any, limit: int = 240) -> str:
    text = str(value)
    lowered = text.lower()
    if any(marker in lowered for marker in SECRET_KEYS):
        return "[redacted]"
    return text[:limit]


def main() -> int:
    data = read_input()
    root = project_root(data)
    event_log = root / "harness" / "events" / "events.jsonl"
    event_log.parent.mkdir(parents=True, exist_ok=True)

    tool_name = data.get("tool_name") or data.get("toolName") or "UNKNOWN"
    tool_input = data.get("tool_input") or data.get("toolInput") or {}
    if not isinstance(tool_input, dict):
        tool_input = {}
    evidence_path = ""
    for key in ("file_path", "path", "target_file", "notebook_path"):
        if isinstance(tool_input.get(key), str):
            evidence_path = safe_text(tool_input[key], 300)
            break

    event = {
        "event_id": f"evt_{uuid.uuid4().hex}",
        "trace_id": safe_text(data.get("trace_id") or data.get("session_id") or "trace_hook"),
        "task_id": safe_text(data.get("task_id") or "UNKNOWN"),
        "actor": "claude-code-hook",
        "actor_type": "hook",
        "event_type": "hook.post_tool_use",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "verdict": "NONE",
        "tool": safe_text(tool_name),
        "summary": f"PostToolUse indexed {safe_text(tool_name)}",
        "evidence_path": evidence_path,
        "part_id": "",
        "worker_id": "",
        "model": "",
        "effort": "",
    }
    with event_log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
