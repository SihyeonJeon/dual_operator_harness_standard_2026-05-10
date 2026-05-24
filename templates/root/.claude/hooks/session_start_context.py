#!/usr/bin/env python3
"""Inject compact file-backed harness context at Claude Code session start."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


def read_input() -> dict[str, Any]:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def project_root(data: dict[str, Any]) -> Path:
    candidate = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or "."
    return Path(candidate).resolve()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def first_matching_line(path: Path, prefixes: tuple[str, ...]) -> str:
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith(prefixes):
                return line.strip()
    except Exception:
        pass
    return "UNKNOWN"


def main() -> int:
    data = read_input()
    root = project_root(data)
    feature_list = load_json(root / "feature_list.json") or {}
    workstream = load_json(root / "harness" / "shared" / "WORKSTREAM_PROFILE.json") or {}

    active = []
    for feature in feature_list.get("features", []):
        if isinstance(feature, dict) and feature.get("state") == "active":
            active.append(feature.get("id", "UNKNOWN"))

    lines = [
        "Dual-operator harness context:",
        f"- active feature(s): {', '.join(active) if active else 'UNKNOWN'}",
        f"- project goal: {feature_list.get('project_goal', 'UNKNOWN')}",
        f"- workstream: {workstream.get('primary_workstream', 'UNKNOWN')}",
        f"- detected streams: {', '.join(workstream.get('detected_workstreams', [])) or 'UNKNOWN'}",
        f"- current task: {first_matching_line(root / 'harness' / 'shared' / 'ACTIVE_SNAPSHOT.md', ('Current task id:',))}",
        "- canonical memory: feature_list.json, progress.md, session-handoff.md, harness/shared/, harness/tasks/",
        "- team shared memory: harness/teams/*/TEAM_CONTEXT.md plus task artifacts",
        "- internal/external boundary: load harness/shared/CHANNEL_RECORDS.md before using broadcast, reviewer, chat, mobile, or connector records",
        "- context pressure: load harness/shared/CONTEXT_PRESSURE.md before delegation, compaction, or part-owner worker resume",
        "- local visibility: python3 scripts/harnessctl.py report",
        "- local viz export: python3 scripts/harnessctl.py viz-export --backend local_file",
        "- external drafts: python3 scripts/harnessctl.py broadcast-draft creates drafts only; no automatic publication",
        "- external review: python3 scripts/harnessctl.py review-packet creates evidence packets; reviewer output is not authority",
        "- visualization gate: Claude owns visualization/diagram IA; load harness/shared/VISUALIZATION_SPEC_POLICY.md before dashboard/timeline/graph/report UI work",
    ]
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "\n".join(lines),
        }
    }
    print(json.dumps(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
