#!/usr/bin/env python3
"""Fail-closed guard for unsafe or unbounded Claude Code tool calls."""

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

CODE_SUFFIXES = {
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".css",
    ".go",
    ".html",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".mjs",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".scss",
    ".sh",
    ".sql",
    ".swift",
    ".ts",
    ".tsx",
    ".vue",
}

HARNESS_REL_PREFIXES = (
    ".claude/",
    ".github/",
    "docs/",
    "harness/",
    "schemas/",
)

LOCK_OR_GENERATED_FILES = (
    "cargo.lock",
    "go.sum",
    "package-lock.json",
    "pnpm-lock.yaml",
    "poetry.lock",
    "yarn.lock",
)

OUTPUT_CAP_PATTERNS = (
    r"\|\s*head\b",
    r"\|\s*tail\b",
    r"\|\s*sed\s+-n\b",
    r"\|\s*wc\b",
    r"\|\s*jq\b",
    r">\s*\S+",
    r"--max-count\b",
    r"\s-m\s*\d+",
    r"--count\b",
    r"--files-with-matches\b",
)


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


def command_has_output_cap(command: str) -> bool:
    return any(re.search(pattern, command, flags=re.IGNORECASE) for pattern in OUTPUT_CAP_PATTERNS)


def command_is_uncapped_broad_read(command: str) -> bool:
    lowered = command.lower()
    if command_has_output_cap(command):
        return False
    if re.search(r"\brg\s+--files\b", lowered):
        return True
    if re.search(r"\bfind\s+(\.|\$pwd|/|\S+)", lowered) and "-maxdepth" not in lowered:
        return True
    if re.search(r"\brg\b", lowered) and re.search(r"(-g|--glob)\s*['\"]?\*\*?/", lowered):
        return True
    if re.search(r"\b(grep|rg)\b", lowered) and any(marker in lowered for marker in ("node_modules", "vendor/", "dist/", "build/")):
        return True
    if re.search(r"\bcat\s+\S+", lowered) and any(name in lowered for name in LOCK_OR_GENERATED_FILES):
        return True
    return False


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


def project_root(cwd: str) -> Path:
    current = Path(cwd).resolve()
    for candidate in [current, *current.parents]:
        if candidate.joinpath("harness", "tasks").exists():
            return candidate
    return current


def relative_path(value: str, cwd: str, root: Path) -> str:
    try:
        input_path = Path(value)
        path = input_path if input_path.is_absolute() else Path(cwd, value)
        return path.resolve().relative_to(root.resolve()).as_posix()
    except Exception:
        return value.replace("\\", "/").lstrip("./")


def is_code_path(rel_path: str) -> bool:
    suffix = Path(rel_path).suffix.lower()
    if suffix not in CODE_SUFFIXES:
        return False
    if rel_path.startswith(HARNESS_REL_PREFIXES):
        return False
    return True


def path_matches_evidence(rel_path: str, value: str) -> bool:
    normalized = value.replace("\\", "/").strip().lstrip("./")
    if not normalized or normalized == "UNKNOWN":
        return False
    return rel_path == normalized or rel_path.startswith(normalized.rstrip("/") + "/")


def integration_evidence_allows(root: Path, rel_path: str) -> bool:
    task_root = root / "harness" / "tasks"
    if not task_root.exists():
        return False
    for path in task_root.glob("**/INTEGRATION_EVIDENCE.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if data.get("status") not in {"RECORDED", "APPROVED"}:
            continue
        files = data.get("files_to_edit") or []
        if not isinstance(files, list):
            continue
        if any(path_matches_evidence(rel_path, str(item)) for item in files):
            return True
    return False


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
        if command_is_uncapped_broad_read(command):
            return deny(
                "Blocked unbounded read/search command. Add an output cap such as `| head`, `| sed -n`, `--max-count`, or write bounded evidence through harnessctl."
            )

    if tool_name in {"Read", "Write", "Edit", "MultiEdit"}:
        path = normalize_path(extract_path(tool_input), cwd)
        if any(marker in path for marker in SECRET_MARKERS):
            return deny(
                "Blocked secret/credential path. Use the approval packet and credential lifecycle policy before access."
            )
        root = project_root(cwd)
        rel_path = relative_path(extract_path(tool_input), cwd, root)
        if tool_name in {"Write", "Edit", "MultiEdit"} and is_code_path(rel_path):
            if not integration_evidence_allows(root, rel_path):
                return deny(
                    "Blocked code edit without integration evidence. Run `python3 scripts/harnessctl.py integration-evidence --task-id TASK --integration-point FILE:LINE --file-to-edit PATH --planned-check COMMAND` before editing."
                )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
