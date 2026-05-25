#!/usr/bin/env python3
"""Read-only generated harness context export.

This is a small dependency-free reference surface, not a full runtime claim.
Use it for local smoke or wrap the functions in an approved MCP adapter.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


TOOL_NAMES = [
    "search_past_decisions",
    "get_capability_status",
    "get_current_task",
    "list_open_questions",
]


def project_root(root: Path) -> Path:
    root = root.resolve()
    if root.joinpath("harness", "shared").exists():
        return root
    if root.name == "harness" and root.joinpath("shared").exists():
        return root.parent
    for parent in root.parents:
        if parent.joinpath("harness", "shared").exists():
            return parent
    return root


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def canonical_search_paths(root: Path) -> list[Path]:
    harness = root / "harness"
    paths = [
        root / "feature_list.json",
        root / "progress.md",
        root / "session-handoff.md",
        harness / "shared" / "ACTIVE_SNAPSHOT.md",
        harness / "shared" / "MEMORY.md",
        harness / "shared" / "FAILURE_LEDGER.md",
        harness / "shared" / "RULE_CHANGE_LOG.md",
        harness / "shared" / "RECORDS_POLICY.md",
        harness / "events" / "events.jsonl",
    ]
    for task_path in sorted((harness / "tasks").glob("*/BLUEPRINT.md")):
        paths.append(task_path)
    return [path for path in paths if path.exists()]


def search_past_decisions(root: Path, args: dict[str, Any]) -> dict[str, Any]:
    query = str(args.get("query", "")).strip()
    limit = int(args.get("limit", 20) or 20)
    if not query:
        return {"query": query, "matches": [], "error": "query is required"}
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    matches: list[dict[str, Any]] = []
    for path in canonical_search_paths(root):
        for line_no, line in enumerate(read_text(path).splitlines(), 1):
            if pattern.search(line):
                matches.append(
                    {
                        "path": rel(path, root),
                        "line": line_no,
                        "text": line[:500],
                    }
                )
                if len(matches) >= limit:
                    return {"query": query, "matches": matches}
    return {"query": query, "matches": matches}


def get_capability_status(root: Path, args: dict[str, Any]) -> dict[str, Any]:
    registry = load_json(root / "harness" / "shared" / "CAPABILITY_REGISTRY.json", {})
    capability_id = str(args.get("id", "")).strip()
    caps = registry.get("capabilities", []) if isinstance(registry, dict) else []
    if capability_id:
        caps = [cap for cap in caps if isinstance(cap, dict) and cap.get("id") == capability_id]
    return {"capabilities": caps}


def get_current_task(root: Path, args: dict[str, Any]) -> dict[str, Any]:
    active_text = read_text(root / "harness" / "shared" / "ACTIVE_SNAPSHOT.md")
    current = "UNKNOWN"
    for line in active_text.splitlines():
        if line.lower().startswith("current task id:"):
            current = line.split(":", 1)[1].strip() or "UNKNOWN"
            break
    feature_list = load_json(root / "feature_list.json", {})
    active_features = []
    for feature in feature_list.get("features", []) if isinstance(feature_list, dict) else []:
        if isinstance(feature, dict) and feature.get("state") == "active":
            active_features.append(feature)
    return {"current_task_id": current, "active_features": active_features}


def collect_open_questions_from_text(text: str) -> list[str]:
    questions: list[str] = []
    in_section = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("## open questions"):
            in_section = True
            continue
        if in_section and stripped.startswith("## "):
            break
        if in_section and stripped.startswith("- "):
            questions.append(stripped[2:])
    return questions


def list_open_questions(root: Path, args: dict[str, Any]) -> dict[str, Any]:
    paths = [
        root / "harness" / "shared" / "ACTIVE_SNAPSHOT.md",
        root / "progress.md",
        root / "session-handoff.md",
    ]
    rows = []
    for path in paths:
        questions = collect_open_questions_from_text(read_text(path))
        if questions:
            rows.append({"path": rel(path, root), "questions": questions})
    return {"open_questions": rows}


def call_tool(root: Path, name: str, args: dict[str, Any]) -> dict[str, Any]:
    if name == "search_past_decisions":
        return search_past_decisions(root, args)
    if name == "get_capability_status":
        return get_capability_status(root, args)
    if name == "get_current_task":
        return get_current_task(root, args)
    if name == "list_open_questions":
        return list_open_questions(root, args)
    return {"error": f"unknown tool: {name}", "available_tools": TOOL_NAMES}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Generated project root")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list-tools")
    call = sub.add_parser("call-tool")
    call.add_argument("name")
    call.add_argument("--arguments", default="{}")
    args = parser.parse_args(argv[1:])

    root = project_root(Path(args.root))
    if args.command == "list-tools":
        print(json.dumps({"tools": TOOL_NAMES}, ensure_ascii=False, indent=2))
        return 0
    try:
        payload = json.loads(args.arguments)
    except json.JSONDecodeError as exc:
        print(json.dumps({"error": f"invalid JSON arguments: {exc}"}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(call_tool(root, args.name, payload), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
