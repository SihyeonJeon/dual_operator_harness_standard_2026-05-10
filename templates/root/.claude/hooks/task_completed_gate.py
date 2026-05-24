#!/usr/bin/env python3
"""Validate harness structure when a Claude Code teammate completes a task."""

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
        return block("Task completion blocked because local harness validation failed.\n" + output)
    harnessctl = root / "scripts" / "harnessctl.py"
    suite = root / "harness" / "evals" / "golden_suite.json"
    if harnessctl.exists() and suite.exists():
        eval_result = subprocess.run(
            [
                sys.executable,
                str(harnessctl),
                "eval-run",
                "--suite",
                "harness/evals/golden_suite.json",
                "--output",
                "harness/evals/results/latest.json",
            ],
            cwd=str(root),
            text=True,
            capture_output=True,
            check=False,
            timeout=10,
        )
        if eval_result.returncode != 0:
            output = "\n".join(part for part in [eval_result.stdout.strip(), eval_result.stderr.strip()] if part)
            return block("Task completion blocked because local golden eval failed.\n" + output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
