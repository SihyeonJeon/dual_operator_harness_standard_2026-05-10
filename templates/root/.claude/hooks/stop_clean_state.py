#!/usr/bin/env python3
"""Block Claude Code stop when the generated harness is structurally invalid."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def read_input() -> dict[str, Any]:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def block(reason: str) -> int:
    print(json.dumps({"decision": "block", "reason": reason[:4000]}))
    return 0


def main() -> int:
    data = read_input()
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or ".").resolve()
    validator = root / "scripts" / "validate_harness.py"
    if not validator.exists():
        return 0
    result = subprocess.run(
        [sys.executable, str(validator), str(root)],
        cwd=str(root),
        text=True,
        capture_output=True,
        check=False,
        timeout=8,
    )
    if result.returncode != 0:
        output = "\n".join(part for part in [result.stdout.strip(), result.stderr.strip()] if part)
        return block("Local harness validator failed. Fix the scaffold or record an explicit blocker before stopping.\n" + output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

