#!/usr/bin/env python3
"""Tiny generated harness control surface.

This is not an agent runtime. It validates the file-backed harness, appends
events, checks visualization specs, runs local eval suites, and compiles a
local static HTML report.

The report is a compiled view over canonical harness files, not canonical
memory.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ACTOR_TYPES = {
    "human",
    "operator",
    "worker",
    "evaluator",
    "hook",
    "mcp_server",
    "cloud_lane",
    "scaffolder",
}

VERDICTS = {"PASS", "WARN", "FAIL", "NOT-RUN", "NONE"}

VISUALIZATION_REQUIRED_SECTIONS = [
    "## Purpose",
    "## Audience",
    "## Source Artifacts",
    "## Data Contract",
    "## Views",
    "## Interaction",
    "## Redaction And Sharing",
    "## Acceptance Criteria",
    "## Approval",
]


def project_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if candidate.joinpath("AGENTS.md").exists() and candidate.joinpath("harness", "shared").exists():
            return candidate
    return current


def load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def read_text(path: Path, default: str = "") -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return default


SECRET_PATTERNS = [
    re.compile(r"(?i)\b([A-Z0-9_]*(?:KEY|SECRET|TOKEN|PASSWORD)[A-Z0-9_]*)\s*[:=]\s*['\"]?[^,\s'\"`]+"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"/Users/[^/\s]+"),
    re.compile(r"/home/[^/\s]+"),
    re.compile(r"/private/var/folders/[^,\s\"']+"),
    re.compile(r"/var/folders/[^,\s\"']+"),
    re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+"),
]

PRIVATE_MARKERS = [
    "broad" + "cast" + "-draft",
    "review" + "-packet",
    "channel" + "_records",
    "harness/" + "broad" + "cast",
    "harness/" + "reviewers",
    "published" + "_ledger",
    "th" + "reads",
    "x_" + "thread",
    "blog" + "_push",
    "github" + "_release",
    "anti" + "gravity",
    "lance" + "db",
    "ku" + "zu",
    "demo" + "_runs",
]


def scrub_text(value: Any) -> str:
    text = str(value)
    for pattern in SECRET_PATTERNS:
        text = pattern.sub("REDACTED", text)
    for marker in PRIVATE_MARKERS:
        text = re.sub(re.escape(marker), "REDACTED", text, flags=re.IGNORECASE)
    return text


def sha256_prefix(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    except Exception:
        return "UNREADABLE"


def source_metadata(path: Path, root: Path) -> dict[str, str]:
    exists = path.exists()
    try:
        mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat() if exists else "MISSING"
    except Exception:
        mtime = "UNREADABLE"
    return {
        "path": display_path(path, root),
        "status": "present" if exists else "missing",
        "sha256": sha256_prefix(path) if exists else "MISSING",
        "mtime": mtime,
    }


def display_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def run_validate(root: Path) -> int:
    validator = root / "scripts" / "validate_harness.py"
    if not validator.exists():
        print("ERROR: scripts/validate_harness.py is missing", file=sys.stderr)
        return 1
    result = subprocess.run(
        [sys.executable, str(validator), str(root)],
        cwd=str(root),
        text=True,
        check=False,
    )
    return result.returncode


def write_event(root: Path, event: dict[str, Any]) -> None:
    event_log = root / "harness" / "events" / "events.jsonl"
    event_log.parent.mkdir(parents=True, exist_ok=True)
    with event_log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def append_event(args: argparse.Namespace, root: Path) -> int:
    if args.actor_type not in ACTOR_TYPES:
        print(f"ERROR: invalid actor_type {args.actor_type}", file=sys.stderr)
        return 2
    if args.verdict and args.verdict not in VERDICTS:
        print(f"ERROR: invalid verdict {args.verdict}", file=sys.stderr)
        return 2

    event = {
        "event_id": args.event_id or f"evt_{uuid.uuid4().hex}",
        "trace_id": args.trace_id,
        "task_id": args.task_id,
        "slice_id": args.slice_id or "",
        "actor": args.actor,
        "actor_type": args.actor_type,
        "event_type": args.event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "verdict": args.verdict or "NONE",
        "summary": args.summary or "",
        "evidence_path": args.evidence_path or "",
        "part_id": args.part_id or "",
        "worker_id": args.worker_id or "",
        "model": args.model or "",
        "effort": args.effort or "",
    }
    for key in ["token_used", "time_elapsed_minutes", "cost_used_usd", "budget_percent"]:
        value = getattr(args, key, None)
        if value is not None:
            event[key] = value
    if getattr(args, "budget_status", ""):
        event["budget_status"] = args.budget_status
    write_event(root, event)
    print(f"event appended: {event['event_id']}")
    return 0


EVENT_ALLOWED_FIELDS = {
    "event_id",
    "trace_id",
    "task_id",
    "slice_id",
    "parent_event_id",
    "actor",
    "actor_type",
    "actor_session_id",
    "worker_id",
    "part_id",
    "event_type",
    "timestamp",
    "status",
    "verdict",
    "model",
    "effort",
    "tool",
    "evidence_path",
    "evidence_paths",
    "decision_id",
    "redaction",
    "summary",
    "token_used",
    "time_elapsed_minutes",
    "cost_used_usd",
    "budget_percent",
    "budget_status",
}


def sanitize_event(row: dict[str, Any]) -> dict[str, Any]:
    clean: dict[str, Any] = {}
    for key in EVENT_ALLOWED_FIELDS:
        if key not in row:
            continue
        value = row[key]
        if isinstance(value, list):
            clean[key] = [scrub_text(item) for item in value]
        elif isinstance(value, dict):
            clean[key] = scrub_text(value)
        else:
            clean[key] = scrub_text(value)
    return clean


def event_rows(root: Path, limit: int = 80) -> list[dict[str, Any]]:
    path = root / "harness" / "events" / "events.jsonl"
    rows: list[dict[str, Any]] = []
    for line in read_text(path).splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"event_type": "invalid_json", "summary": line[:200]})
    if limit <= 0:
        return rows
    return rows[-limit:]


def bounded_text(value: Any, max_chars: int = 1400) -> str:
    text = scrub_text(value)
    if max_chars <= 0 or len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "\n[truncated]"


def split_values(values: list[str] | None) -> list[str]:
    result: list[str] = []
    for value in values or []:
        for part in value.split(","):
            item = part.strip()
            if item:
                result.append(item)
    return result


def ensure_task_dir(root: Path, task_id: str) -> Path:
    task_dir = root / "harness" / "tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    return task_dir


def artifact_path(root: Path, output: str, task_id: str, filename: str) -> Path:
    path = Path(output) if output else ensure_task_dir(root, task_id) / filename
    if not path.is_absolute():
        path = root / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def project_goal(root: Path) -> str:
    feature_goal = load_json(root / "feature_list.json", {}).get("project_goal")
    if feature_goal:
        return scrub_text(feature_goal)
    profile_goal = load_json(root / "harness" / "shared" / "PROJECT_PROFILE.json", {}).get("primary_goal")
    return scrub_text(profile_goal or "UNKNOWN")


def json_artifact(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def status_badge(value: str) -> str:
    normalized = value or "UNKNOWN"
    safe = html.escape(normalized)
    css = "badge neutral"
    glyph = "-"
    if normalized in {"passing", "PASS", "DONE", "APPROVED", "VERIFIED"}:
        css = "badge pass"
        glyph = "✓"
    elif normalized in {"blocked", "FAIL", "BLOCKED", "DENIED"}:
        css = "badge fail"
        glyph = "!"
    elif normalized in {"active", "WARN", "PENDING_CROSS_CHECK", "PENDING", "DRAFT", "NOT-RUN", "NONE"}:
        css = "badge warn"
        glyph = "•"
    return f'<span class="{css}"><span>{glyph}</span>{safe}</span>'


def count_events(events: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(Counter(str(row.get(key, "UNKNOWN") or "UNKNOWN") for row in events))


def short_time(value: Any) -> str:
    text = str(value or "UNKNOWN")
    if "T" in text and len(text) >= 19:
        return text[:19].replace("T", " ")
    return text


def html_or_empty(value: str, empty: str) -> str:
    return value if value else f'<p class="empty">{html.escape(empty)}</p>'


def parse_cap(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)) and value >= 0:
        return float(value)
    if isinstance(value, str):
        try:
            parsed = float(value)
        except ValueError:
            return None
        return parsed if parsed >= 0 else None
    return None


def load_task_budget(root: Path, task_id: str) -> tuple[Path, dict[str, Any]]:
    candidates = [
        root / "harness" / "tasks" / task_id / "BUDGET.json",
        root / "harness" / "tasks" / "active" / task_id / "BUDGET.json",
        root / "harness" / "templates" / "BUDGET.json",
    ]
    for path in candidates:
        if path.exists():
            return path, load_json(path, {})
    return candidates[0], {}


def budget_check(args: argparse.Namespace, root: Path) -> int:
    budget_path, budget = load_task_budget(root, args.task_id)
    if not budget:
        write_event(
            root,
            {
                "event_id": f"evt_{uuid.uuid4().hex}",
                "trace_id": args.trace_id,
                "task_id": args.task_id,
                "actor": "harnessctl",
                "actor_type": "hook",
                "event_type": "budget.kill_required",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "verdict": "FAIL",
                "summary": "Task budget file is missing; dispatch must stop.",
                "evidence_path": display_path(budget_path, root),
                "budget_status": "missing_budget",
            },
        )
        return 3

    caps = {
        "token": parse_cap(budget.get("token_cap")),
        "time": parse_cap(budget.get("time_cap_minutes")),
        "cost": parse_cap(budget.get("cost_cap_usd")),
    }
    observed = {
        "token": args.token_used,
        "time": args.time_elapsed_minutes,
        "cost": args.cost_used_usd,
    }
    percents = [
        (observed[key] / cap) * 100
        for key, cap in caps.items()
        if cap and observed.get(key) is not None
    ]
    budget_percent = max(percents) if percents else 0.0
    warning_threshold = float(budget.get("warning_threshold_percent", 80) or 80)
    kill_threshold = float(budget.get("kill_threshold_percent", 100) or 100)
    generated_at = datetime.now(timezone.utc).isoformat()
    if budget_percent >= kill_threshold:
        event_type = "budget.kill_required"
        verdict = "FAIL"
        status = "kill_required"
    elif budget_percent >= warning_threshold:
        event_type = "budget.warning"
        verdict = "WARN"
        status = "warning"
    elif percents:
        event_type = "budget.ok"
        verdict = "PASS"
        status = "ok"
    else:
        event_type = "budget.warning"
        verdict = "WARN"
        status = "unmetered"

    summary = (
        f"Budget check for {args.task_id}: {status}, "
        f"max usage {budget_percent:.1f}%."
    )
    event = {
        "event_id": f"evt_{uuid.uuid4().hex}",
        "trace_id": args.trace_id,
        "task_id": args.task_id,
        "actor": "harnessctl",
        "actor_type": "hook",
        "event_type": event_type,
        "timestamp": generated_at,
        "verdict": verdict,
        "summary": summary,
        "evidence_path": display_path(budget_path, root),
        "budget_percent": round(budget_percent, 3),
        "budget_status": status,
    }
    if args.token_used is not None:
        event["token_used"] = args.token_used
    if args.time_elapsed_minutes is not None:
        event["time_elapsed_minutes"] = args.time_elapsed_minutes
    if args.cost_used_usd is not None:
        event["cost_used_usd"] = args.cost_used_usd
    write_event(root, event)

    if status == "kill_required":
        escalation = budget.get("escalation", {}) if isinstance(budget.get("escalation"), dict) else {}
        write_event(
            root,
            {
                "event_id": f"evt_{uuid.uuid4().hex}",
                "trace_id": args.trace_id,
                "task_id": args.task_id,
                "actor": "harnessctl",
                "actor_type": "hook",
                "event_type": escalation.get("event_type", "budget.escalation_required"),
                "timestamp": generated_at,
                "verdict": "FAIL",
                "summary": budget.get("kill_procedure", "Stop worker dispatch and escalate to operator."),
                "evidence_path": display_path(budget_path, root),
                "budget_percent": round(budget_percent, 3),
                "budget_status": "escalated",
            },
        )
        print(summary)
        print("budget kill required")
        return 3

    print(summary)
    return 0 if status == "ok" else 1


def build_report(args: argparse.Namespace, root: Path) -> int:
    out = Path(args.output) if args.output else root / "harness" / "reports" / "status.html"
    if not out.is_absolute():
        out = root / out
    out.parent.mkdir(parents=True, exist_ok=True)

    features = load_json(root / "feature_list.json", {}).get("features", [])
    project_goal = load_json(root / "feature_list.json", {}).get("project_goal", "UNKNOWN")
    worker_registry = load_json(root / "harness" / "shared" / "WORKER_SESSION_REGISTRY.json", {})
    active_snapshot = read_text(root / "harness" / "shared" / "ACTIVE_SNAPSHOT.md", "UNKNOWN")
    events = [sanitize_event(row) for row in event_rows(root, args.max_events)]
    generated_at = datetime.now(timezone.utc).isoformat()
    sources = [
        root / "feature_list.json",
        root / "progress.md",
        root / "session-handoff.md",
        root / "harness" / "shared" / "ACTIVE_SNAPSHOT.md",
        root / "harness" / "shared" / "WORKER_SESSION_REGISTRY.json",
        root / "harness" / "events" / "events.jsonl",
    ]
    source_rows = "\n".join(
        "<tr>"
        f"<td><code>{html.escape(item['path'])}</code></td>"
        f"<td>{status_badge(item['status'])}</td>"
        f"<td><code>{html.escape(item['sha256'])}</code></td>"
        f"<td>{html.escape(item['mtime'])}</td>"
        "</tr>"
        for item in [source_metadata(path, root) for path in sources]
    )
    verdict_counts = count_events(events, "verdict")
    actor_counts = count_events(events, "actor_type")
    pass_count = verdict_counts.get("PASS", 0)
    warn_count = verdict_counts.get("WARN", 0) + verdict_counts.get("NOT-RUN", 0)
    fail_count = verdict_counts.get("FAIL", 0)
    active_features = [item for item in features if isinstance(item, dict) and item.get("state") == "active"]
    gate_events = [
        row for row in events
        if "gate" in str(row.get("event_type", "")).lower()
        or str(row.get("verdict", "NONE")) in {"PASS", "WARN", "FAIL", "NOT-RUN"}
    ]

    feature_rows = "\n".join(
        "<tr>"
        f"<td><a href=\"#feature-{html.escape(str(item.get('id', 'UNKNOWN')))}\"><code>{html.escape(str(item.get('id', 'UNKNOWN')))}</code></a></td>"
        f"<td id=\"feature-{html.escape(str(item.get('id', 'UNKNOWN')))}\">{html.escape(scrub_text(item.get('name', 'UNKNOWN')))}</td>"
        f"<td>{status_badge(str(item.get('state', 'UNKNOWN')))}</td>"
        f"<td>{html.escape(scrub_text(item.get('owner', 'UNKNOWN')))}</td>"
        f"<td>{html.escape(scrub_text(item.get('evidence', 'UNKNOWN')))}</td>"
        "</tr>"
        for item in features
        if isinstance(item, dict)
    )
    feature_cards = "\n".join(
        "<article class=\"feature-card\">"
        f"<div class=\"event-head\"><code>{html.escape(str(item.get('id', 'UNKNOWN')))}</code>{status_badge(str(item.get('state', 'UNKNOWN')))}</div>"
        f"<h3>{html.escape(scrub_text(item.get('name', 'UNKNOWN')))}</h3>"
        f"<dl><dt>owner</dt><dd>{html.escape(scrub_text(item.get('owner', 'UNKNOWN')))}</dd>"
        f"<dt>evidence</dt><dd><code>{html.escape(scrub_text(item.get('evidence', 'UNKNOWN')))}</code></dd></dl>"
        "</article>"
        for item in features
        if isinstance(item, dict)
    )
    event_html = "\n".join(
        f"<article class=\"event-card\" id=\"event-{html.escape(str(row.get('event_id', 'UNKNOWN')))}\">"
        f"<div class=\"event-head\"><code>{html.escape(str(row.get('event_type', 'UNKNOWN')))}</code>{status_badge(str(row.get('verdict', 'NONE')))}</div>"
        f"<p>{html.escape(str(row.get('summary', row.get('evidence_path', ''))))}</p>"
        f"<dl><dt>time</dt><dd>{html.escape(short_time(row.get('timestamp', 'UNKNOWN')))}</dd>"
        f"<dt>task</dt><dd>{html.escape(str(row.get('task_id', 'UNKNOWN')))}</dd>"
        f"<dt>actor</dt><dd>{html.escape(str(row.get('actor_type', 'UNKNOWN')))} / {html.escape(str(row.get('actor', 'UNKNOWN')))}</dd>"
        f"<dt>evidence</dt><dd><code>{html.escape(str(row.get('evidence_path', '')))}</code></dd></dl>"
        "</article>"
        for row in events
    )
    workers = worker_registry.get("workers", [])
    worker_cards = "\n".join(
        "<article class=\"worker-card\">"
        f"<h3>{html.escape(scrub_text(item.get('worker_id', 'UNKNOWN')))}</h3>"
        f"<p><span>Part</span><code>{html.escape(scrub_text(item.get('part_id', 'UNKNOWN')))}</code></p>"
        f"<p><span>Resume</span>{status_badge(str(item.get('resume_status', 'UNKNOWN')))}</p>"
        f"<p><span>Checkpoint</span><code>{html.escape(scrub_text(item.get('last_checkpoint', 'UNKNOWN')))}</code></p>"
        "</article>"
        for item in workers
        if isinstance(item, dict)
    )
    lanes = ["human", "operator", "worker", "evaluator", "hook", "cloud_lane", "mcp_server", "scaffolder"]
    lane_html = "\n".join(
        "<section class=\"lane\">"
        f"<h3>{html.escape(lane)}</h3>"
        "<div class=\"lane-stack\">"
        + "\n".join(
            "<div class=\"lane-event\">"
            f"<time>{html.escape(short_time(row.get('timestamp', 'UNKNOWN')))}</time>"
            f"<strong>{html.escape(str(row.get('event_type', 'UNKNOWN')))}</strong>"
            f"{status_badge(str(row.get('verdict', 'NONE')))}"
            "</div>"
            for row in events
            if row.get("actor_type") == lane
        )
        + "</div></section>"
        for lane in lanes
        if any(row.get("actor_type") == lane for row in events)
    )
    gate_html = "\n".join(
        "<article class=\"gate-card\">"
        f"<h3>{html.escape(str(row.get('event_type', 'UNKNOWN')))}</h3>"
        f"{status_badge(str(row.get('verdict', 'NONE')))}"
        f"<p>{html.escape(str(row.get('summary', '')))}</p>"
        f"<code>{html.escape(str(row.get('evidence_path', '')))}</code>"
        "</article>"
        for row in gate_events[-24:]
    )
    metric_cards = "\n".join(
        f"<article class=\"metric\"><span>{label}</span><strong>{value}</strong></article>"
        for label, value in [
            ("Features", len(features) if isinstance(features, list) else 0),
            ("Active", len(active_features)),
            ("Workers", len(workers) if isinstance(workers, list) else 0),
            ("Events", len(events)),
            ("PASS", pass_count),
            ("WARN/NOT-RUN", warn_count),
            ("FAIL", fail_count),
        ]
    )
    status_payload = {
        "generated_at": generated_at,
        "authority": "compiled_view_not_canonical_memory",
        "canonical_sources": [
            "feature_list.json",
            "progress.md",
            "session-handoff.md",
            "harness/shared/",
            "harness/events/events.jsonl",
        ],
        "project_goal": scrub_text(project_goal),
        "counts": {
            "features": len(features) if isinstance(features, list) else 0,
            "active_features": len(active_features),
            "workers": len(workers) if isinstance(workers, list) else 0,
            "events": len(events),
            "verdicts": verdict_counts,
            "actors": actor_counts,
        },
        "sources": [source_metadata(path, root) for path in sources],
    }

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Harness Status</title>
<style>
:root {{ color-scheme: light; --ink: #172033; --muted: #5f6878; --line: #d9e0ea; --panel: #ffffff; --bg: #f3f6f8; --pass-bg: #dff5e6; --pass-ink: #14613b; --warn-bg: #fff0c6; --warn-ink: #7a4c00; --fail-bg: #ffe0df; --fail-ink: #8f1d1b; --neutral-bg: #e8edf2; --neutral-ink: #394252; --accent: #2457a6; --violet: #6750a4; }}
* {{ box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 0; color: var(--ink); background: var(--bg); }}
a {{ color: var(--accent); }}
.skip {{ position: absolute; left: 16px; top: -48px; background: var(--ink); color: white; padding: 8px 10px; border-radius: 6px; }}
.skip:focus {{ top: 12px; }}
header {{ border-bottom: 1px solid var(--line); background: var(--panel); }}
.wrap {{ max-width: 1240px; margin: 0 auto; padding: 20px; }}
.topline {{ display: grid; grid-template-columns: 1fr auto; gap: 16px; align-items: start; }}
h1 {{ font-size: 28px; margin: 0 0 8px; }}
h2 {{ font-size: 20px; margin: 0 0 14px; }}
h3 {{ font-size: 15px; margin: 0 0 8px; }}
p {{ line-height: 1.55; }}
nav {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; }}
nav a {{ border: 1px solid var(--line); border-radius: 6px; padding: 7px 10px; text-decoration: none; color: var(--ink); background: #f8fafc; }}
section.panel {{ margin: 18px 0; padding: 16px; background: var(--panel); border: 1px solid var(--line); border-radius: 8px; overflow-x: auto; }}
.authority {{ background: #fff; border-left: 5px solid var(--accent); padding: 10px 12px; margin-top: 14px; }}
.metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(132px, 1fr)); gap: 10px; margin: 18px 0; }}
.metric {{ border: 1px solid var(--line); border-radius: 8px; background: var(--panel); padding: 12px; min-height: 86px; }}
.metric span {{ display: block; color: var(--muted); font-size: 13px; }}
.metric strong {{ display: block; margin-top: 8px; font-size: 28px; }}
table {{ width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 14px; }}
th, td {{ text-align: left; padding: 9px; border-bottom: 1px solid #e7ebf0; vertical-align: top; overflow-wrap: anywhere; }}
th {{ color: var(--muted); font-size: 12px; text-transform: uppercase; }}
code {{ background: #eef2f6; padding: 2px 5px; border-radius: 4px; overflow-wrap: anywhere; }}
pre {{ white-space: pre-wrap; overflow-wrap: anywhere; background: #182234; color: #eef3f8; padding: 14px; border-radius: 8px; }}
.badge {{ display: inline-flex; align-items: center; gap: 5px; padding: 3px 8px; border-radius: 999px; font-size: 12px; font-weight: 700; white-space: nowrap; }}
.pass {{ background: var(--pass-bg); color: var(--pass-ink); }}
.warn {{ background: var(--warn-bg); color: var(--warn-ink); }}
.fail {{ background: var(--fail-bg); color: var(--fail-ink); }}
.neutral {{ background: var(--neutral-bg); color: var(--neutral-ink); }}
.worker-grid, .gate-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 12px; }}
.worker-card, .gate-card, .event-card, .feature-card {{ border: 1px solid var(--line); border-radius: 8px; background: #fbfcfe; padding: 12px; }}
.feature-card-list {{ display: none; gap: 10px; }}
.worker-card p {{ display: grid; grid-template-columns: 86px 1fr; gap: 8px; margin: 8px 0; }}
.worker-card span {{ color: var(--muted); }}
.lane-map {{ display: grid; gap: 10px; }}
.lane {{ display: grid; grid-template-columns: 140px 1fr; gap: 10px; align-items: start; border-left: 4px solid var(--violet); padding: 8px 0 8px 10px; }}
.lane h3 {{ color: var(--violet); }}
.lane-stack {{ display: grid; gap: 8px; }}
.lane-event {{ display: grid; grid-template-columns: minmax(180px, 1fr) minmax(170px, 2fr) auto; gap: 8px; align-items: center; padding: 7px 8px; border: 1px solid var(--line); border-radius: 6px; background: #fff; }}
.lane-event time {{ overflow-wrap: anywhere; }}
.lane-event time, .note, .empty {{ color: var(--muted); }}
.event-list {{ display: grid; gap: 10px; }}
.event-head {{ display: flex; justify-content: space-between; gap: 10px; align-items: start; }}
dl {{ display: grid; grid-template-columns: 72px 1fr; gap: 4px 10px; margin: 8px 0 0; }}
dt {{ color: var(--muted); }}
dd {{ margin: 0; overflow-wrap: anywhere; }}
details summary {{ cursor: pointer; font-weight: 700; }}
footer {{ color: var(--muted); padding-bottom: 30px; }}
@media (max-width: 720px) {{ .topline, .lane, .lane-event {{ grid-template-columns: 1fr; }} .wrap {{ padding: 14px; }} table {{ font-size: 12px; }} th, td {{ padding: 6px; }} .feature-table {{ display: none; }} .feature-card-list {{ display: grid; }} }}
@media print {{ nav {{ display: none; }} body {{ background: white; }} section.panel, .metric {{ break-inside: avoid; }} }}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to status</a>
<header>
<div class="wrap">
<div class="topline">
<div>
<h1>Harness Status</h1>
<p>{html.escape(scrub_text(project_goal))}</p>
</div>
<p class="note">Generated at<br>{html.escape(generated_at)}</p>
</div>
<p class="authority"><strong>Canonical sources:</strong> feature_list.json, progress.md, session-handoff.md, harness/shared/, and harness/events/events.jsonl. This report is a derived view. Edit source files, not this HTML.</p>
<nav aria-label="Report sections">
<a href="#features">Features</a>
<a href="#workers">Workers</a>
<a href="#timeline">Timeline</a>
<a href="#gates">Gates</a>
<a href="#events">Events</a>
<a href="#sources">Sources</a>
</nav>
</div>
</header>
<main id="main" class="wrap">
<div class="metrics">{metric_cards}</div>
<section class="panel" id="features">
<h2>Features</h2>
<table class="feature-table"><thead><tr><th>ID</th><th>Name</th><th>State</th><th>Owner</th><th>Evidence</th></tr></thead><tbody>{feature_rows}</tbody></table>
<div class="feature-card-list">{html_or_empty(feature_cards, "No features are available yet.")}</div>
</section>
<section class="panel" id="workers">
<h2>Workers</h2>
<div class="worker-grid">{html_or_empty(worker_cards, "No worker sessions are registered yet.")}</div>
</section>
<section class="panel" id="timeline">
<h2>Operator And Worker Timeline</h2>
<div class="lane-map">{html_or_empty(lane_html, "No timeline events are available yet.")}</div>
</section>
<section class="panel" id="gates">
<h2>Gate Board</h2>
<div class="gate-grid">{html_or_empty(gate_html, "No gate events are available yet.")}</div>
</section>
<section class="panel" id="events">
<h2>Recent Events</h2>
<div class="event-list">{html_or_empty(event_html, "No events are available yet.")}</div>
</section>
<section class="panel">
<h2>Active Snapshot</h2>
<pre>{html.escape(scrub_text(active_snapshot))}</pre>
</section>
<section class="panel" id="sources">
<h2>Source Files</h2>
<table><thead><tr><th>Path</th><th>Status</th><th>SHA-256</th><th>Modified</th></tr></thead><tbody>{source_rows}</tbody></table>
</section>
</main>
<footer class="wrap">Generated by scripts/harnessctl.py report. Static, dependency-free, and safe to open locally.</footer>
</body>
</html>
"""
    out.write_text(page, encoding="utf-8")
    status_path = out.with_suffix(".json")
    status_path.write_text(json.dumps(status_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"report written: {display_path(out, root)}")
    print(f"report json written: {display_path(status_path, root)}")
    return 0


def visualization_spec_path(args: argparse.Namespace, root: Path) -> Path:
    if args.path:
        path = Path(args.path)
        return path if path.is_absolute() else root / path
    if args.task_id:
        return root / "harness" / "tasks" / args.task_id / "VISUALIZATION_SPEC.md"
    return root / "harness" / "templates" / "VISUALIZATION_SPEC.md"


def check_visualization_spec(args: argparse.Namespace, root: Path) -> int:
    policy = root / "harness" / "shared" / "VISUALIZATION_SPEC_POLICY.md"
    if not policy.exists():
        print("ERROR: missing harness/shared/VISUALIZATION_SPEC_POLICY.md", file=sys.stderr)
        return 1
    path = visualization_spec_path(args, root)
    if not path.exists():
        print(f"ERROR: missing visualization spec: {path}", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8")
    missing = [section for section in VISUALIZATION_REQUIRED_SECTIONS if section not in text]
    if missing:
        print("ERROR: visualization spec missing sections: " + ", ".join(missing), file=sys.stderr)
        return 1
    if args.require_approved and "Status: APPROVED" not in text:
        print("ERROR: visualization spec is not approved", file=sys.stderr)
        return 1
    print(f"PASS: visualization spec gate satisfied for {display_path(path, root)}")
    return 0


def archive_task(args: argparse.Namespace, root: Path) -> int:
    layout = root / "harness" / "shared" / "WORKSPACE_LAYOUT.md"
    if not layout.exists():
        print("ERROR: missing harness/shared/WORKSPACE_LAYOUT.md", file=sys.stderr)
        return 1
    source = root / "harness" / "tasks" / args.task_id
    if not source.exists() or not source.is_dir():
        print(f"ERROR: missing task directory: {display_path(source, root)}", file=sys.stderr)
        return 1
    active_snapshot = read_text(root / "harness" / "shared" / "ACTIVE_SNAPSHOT.md")
    if f"Current task id: {args.task_id}" in active_snapshot and not args.force:
        print("ERROR: refusing to archive current active task without --force", file=sys.stderr)
        return 1
    target_dir = root / "harness" / "tasks" / "archive" / args.task_id
    if target_dir.exists():
        print(f"ERROR: archive target already exists: {display_path(target_dir, root)}", file=sys.stderr)
        return 1
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(target_dir))
    write_event(
        root,
        {
            "event_id": f"evt_{uuid.uuid4().hex}",
            "trace_id": args.trace_id,
            "task_id": args.task_id,
            "actor": "harnessctl",
            "actor_type": "operator",
            "event_type": "workspace.task_archived",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "verdict": "NONE",
            "summary": args.reason or "Task archived under WORKSPACE_LAYOUT.md",
            "evidence_path": display_path(target_dir, root),
            "part_id": "",
            "worker_id": "",
            "model": "",
            "effort": "",
        },
    )
    print(f"task archived: {display_path(target_dir, root)}")
    return 0


def load_viz_backend(root: Path, backend_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    config_path = root / "harness" / "viz" / "VIZ_BACKENDS.json"
    config = load_json(config_path, {})
    selected = backend_id or str(config.get("default_backend", "local_file"))
    for backend in config.get("backends", []):
        if isinstance(backend, dict) and backend.get("id") == selected:
            return config, backend
    return config, {}


def export_viz_events(args: argparse.Namespace, root: Path) -> int:
    policy = root / "harness" / "shared" / "VISUALIZATION_SPEC_POLICY.md"
    if not policy.exists():
        print("ERROR: missing harness/shared/VISUALIZATION_SPEC_POLICY.md", file=sys.stderr)
        return 1
    config, backend = load_viz_backend(root, args.backend)
    if not config:
        print("ERROR: missing or invalid harness/viz/VIZ_BACKENDS.json", file=sys.stderr)
        return 1
    if not backend:
        print(f"ERROR: unknown viz backend {args.backend or config.get('default_backend', 'local_file')}", file=sys.stderr)
        return 2
    mode = backend.get("mode", "UNKNOWN")
    status = backend.get("status", "UNVERIFIED")
    if mode != "local_file":
        print(
            "ERROR: non-local viz backend requires a worker-owned adapter, bounded policy, "
            "credential lifecycle entry, and smoke evidence before harnessctl can push events",
            file=sys.stderr,
        )
        return 2
    if status not in {"VERIFIED_LOCAL", "VERIFIED"}:
        print(f"ERROR: local viz backend is not verified: {status}", file=sys.stderr)
        return 2

    rows = [sanitize_event(row) for row in event_rows(root, args.max_events)]
    output_dir = Path(args.output_dir or backend.get("output_dir", "harness/reports/viz"))
    if not output_dir.is_absolute():
        output_dir = root / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    ndjson_path = output_dir / "events.ndjson"
    json_path = output_dir / "events.json"
    summary_path = output_dir / "summary.json"
    ndjson_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {
        "backend": backend.get("id", "local_file"),
        "status": status,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "event_count": len(rows),
        "counts": {
            "actor_type": count_events(rows, "actor_type"),
            "event_type": count_events(rows, "event_type"),
            "verdict": count_events(rows, "verdict"),
            "task_id": count_events(rows, "task_id"),
        },
        "source": source_metadata(root / "harness" / "events" / "events.jsonl", root),
        "outputs": [
            display_path(ndjson_path, root),
            display_path(json_path, root),
            display_path(summary_path, root),
        ],
        "external_network_write": False,
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_event(
        root,
        {
            "event_id": f"evt_{uuid.uuid4().hex}",
            "trace_id": args.trace_id,
            "task_id": args.task_id,
            "actor": "harnessctl",
            "actor_type": "hook",
            "event_type": "viz.export_created",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "verdict": "PASS",
            "summary": f"Viz event export created for backend {backend.get('id', 'local_file')}",
            "evidence_path": display_path(summary_path, root),
            "part_id": "",
            "worker_id": "",
            "model": "",
            "effort": "",
        },
    )
    print(f"viz events written: {display_path(summary_path, root)}")
    return 0


def json_lookup(data: Any, key_path: str) -> tuple[bool, Any]:
    if not key_path:
        return True, data
    current = data
    for part in key_path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit():
            index = int(part)
            if index >= len(current):
                return False, None
            current = current[index]
        else:
            return False, None
    return True, current


def check_events_schema(root: Path, case: dict[str, Any]) -> tuple[bool, str]:
    required = case.get("required_fields") or [
        "event_id",
        "trace_id",
        "task_id",
        "actor",
        "actor_type",
        "event_type",
        "timestamp",
        "verdict",
        "evidence_path",
    ]
    if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
        required = ["event_id", "trace_id", "task_id", "actor", "actor_type", "event_type", "timestamp"]
    rows = event_rows(root, 0)
    if not rows:
        return False, "event log has no rows"
    invalid: list[str] = []
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            invalid.append(f"line {index}: not an object")
            continue
        missing = [field for field in required if field not in row]
        if missing:
            invalid.append(f"line {index}: missing {', '.join(missing)}")
        if row.get("actor_type") not in ACTOR_TYPES:
            invalid.append(f"line {index}: invalid actor_type")
        if row.get("verdict", "NONE") not in VERDICTS:
            invalid.append(f"line {index}: invalid verdict")
    if invalid:
        return False, "; ".join(invalid[:5])
    return True, f"{len(rows)} event rows passed schema check"


def evidence_file_exists(root: Path, value: Any) -> bool:
    if not isinstance(value, str) or not value or value == "UNKNOWN":
        return False
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    return path.exists()


def check_verified_evidence(root: Path) -> tuple[bool, str]:
    failures: list[str] = []
    registry = load_json(root / "harness" / "shared" / "CAPABILITY_REGISTRY.json", {})
    for item in registry.get("capabilities", []) if isinstance(registry, dict) else []:
        if isinstance(item, dict) and item.get("status") == "VERIFIED":
            if not evidence_file_exists(root, item.get("evidence_path")):
                failures.append(f"capability {item.get('id', 'UNKNOWN')} lacks evidence")

    for path in sorted((root / "harness" / "runtime" / "RUNNERS").glob("*.json")):
        data = load_json(path, {})
        if isinstance(data, dict) and data.get("status") == "VERIFIED":
            if not evidence_file_exists(root, data.get("smoke_evidence_path")):
                failures.append(f"runner {path.name} lacks smoke evidence")

    viz = load_json(root / "harness" / "viz" / "VIZ_BACKENDS.json", {})
    for item in viz.get("backends", []) if isinstance(viz, dict) else []:
        if isinstance(item, dict) and item.get("status") in {"VERIFIED", "VERIFIED_LOCAL"}:
            if not evidence_file_exists(root, item.get("smoke_evidence_path")):
                failures.append(f"viz backend {item.get('id', 'UNKNOWN')} lacks smoke evidence")

    if failures:
        return False, "; ".join(failures[:5])
    return True, "all VERIFIED surfaces have evidence or remain honestly unverified"


def case_result(case: dict[str, Any], root: Path) -> dict[str, Any]:
    case_id = str(case.get("id", "UNKNOWN"))
    case_type = str(case.get("type", "UNKNOWN"))
    severity = str(case.get("severity", "required"))
    rel_path = str(case.get("path", ""))
    path = root / rel_path if rel_path else root
    notes = ""
    passed = False

    if case_type == "file_exists":
        passed = path.exists()
        notes = "path exists" if passed else "path is missing"
    elif case_type == "text_contains":
        terms = case.get("terms", [])
        if not isinstance(terms, list) or not all(isinstance(term, str) for term in terms):
            return {
                "id": case_id,
                "name": case.get("name", case_id),
                "type": case_type,
                "severity": severity,
                "result": "NOT-RUN",
                "evidence_path": display_path(path, root),
                "notes": "terms must be an array of strings",
            }
        text = read_text(path)
        if case.get("case_sensitive") is True:
            haystack = text
            needles = terms
        else:
            haystack = text.lower()
            needles = [term.lower() for term in terms]
        missing = [terms[index] for index, term in enumerate(needles) if term not in haystack]
        passed = path.exists() and not missing
        notes = "all terms present" if passed else "missing terms: " + ", ".join(missing)
    elif case_type == "json_has_key":
        data = load_json(path, None)
        ok, _value = json_lookup(data, str(case.get("key", "")))
        passed = path.exists() and ok
        notes = "key present" if passed else f"key missing: {case.get('key', '')}"
    elif case_type == "json_equals":
        data = load_json(path, None)
        ok, value = json_lookup(data, str(case.get("key", "")))
        expected = case.get("expected")
        passed = path.exists() and ok and value == expected
        notes = "expected value matched" if passed else f"expected {expected!r}, got {value!r}"
    elif case_type == "json_array_min_length":
        data = load_json(path, None)
        ok, value = json_lookup(data, str(case.get("key", "")))
        min_length = int(case.get("min_length", 1))
        passed = path.exists() and ok and isinstance(value, list) and len(value) >= min_length
        actual = len(value) if isinstance(value, list) else "not-array"
        notes = f"array length {actual}, minimum {min_length}"
    elif case_type == "event_count_min":
        min_count = int(case.get("min_count", 1))
        count = len(event_rows(root, 0))
        passed = count >= min_count
        notes = f"event count {count}, minimum {min_count}"
        rel_path = "harness/events/events.jsonl"
        path = root / rel_path
    elif case_type == "events_schema_valid":
        passed, notes = check_events_schema(root, case)
        rel_path = "harness/events/events.jsonl"
        path = root / rel_path
    elif case_type == "verified_evidence_integrity":
        passed, notes = check_verified_evidence(root)
        rel_path = "harness/shared/CAPABILITY_REGISTRY.json"
        path = root / rel_path
    else:
        return {
            "id": case_id,
            "name": case.get("name", case_id),
            "type": case_type,
            "severity": severity,
            "result": "NOT-RUN",
            "evidence_path": display_path(path, root),
            "notes": f"unsupported eval case type: {case_type}",
        }

    return {
        "id": case_id,
        "name": case.get("name", case_id),
        "type": case_type,
        "severity": severity,
        "result": "PASS" if passed else "FAIL",
        "evidence_path": display_path(path, root),
        "notes": notes,
    }


def eval_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Eval Run Result",
        "",
        f"Suite: {result['suite_id']}",
        f"Verdict: {result['verdict']}",
        f"Generated at: {result['generated_at']}",
        f"Source suite: `{result['source_suite']}`",
        "",
        "## Counts",
        "",
        f"- Cases: {result['case_count']}",
        f"- Passed: {result['passed']}",
        f"- Failed: {result['failed']}",
        f"- Not run: {result['not_run']}",
        "",
        "## Case Results",
        "",
        "| Case | Type | Severity | Result | Evidence | Notes |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in result["results"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    scrub_text(item.get("id", "UNKNOWN")).replace("|", "\\|"),
                    scrub_text(item.get("type", "UNKNOWN")).replace("|", "\\|"),
                    scrub_text(item.get("severity", "UNKNOWN")).replace("|", "\\|"),
                    scrub_text(item.get("result", "UNKNOWN")).replace("|", "\\|"),
                    "`" + scrub_text(item.get("evidence_path", "UNKNOWN")).replace("|", "\\|") + "`",
                    scrub_text(item.get("notes", "")).replace("|", "\\|"),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Safety",
            "",
            "- This eval runner performs no network writes.",
            "- This eval runner does not execute arbitrary shell commands.",
            "- This public harness helper performs no external publication, connector, or private review actions.",
            "",
        ]
    )
    return "\n".join(lines)


def run_eval_suite(args: argparse.Namespace, root: Path) -> int:
    suite_path = Path(args.suite or "harness/evals/golden_suite.json")
    if not suite_path.is_absolute():
        suite_path = root / suite_path
    suite = load_json(suite_path, None)
    if not isinstance(suite, dict):
        print(f"ERROR: invalid eval suite: {display_path(suite_path, root)}", file=sys.stderr)
        return 1
    cases = suite.get("cases", [])
    if not isinstance(cases, list) or not cases:
        print("ERROR: eval suite cases must be a non-empty array", file=sys.stderr)
        return 1

    results = [case_result(case, root) if isinstance(case, dict) else {
        "id": "UNKNOWN",
        "name": "Invalid case",
        "type": "UNKNOWN",
        "severity": "required",
        "result": "NOT-RUN",
        "evidence_path": "",
        "notes": "case is not an object",
    } for case in cases]
    required_failures = [
        item for item in results
        if item.get("severity", "required") == "required" and item.get("result") != "PASS"
    ]
    optional_failures = [
        item for item in results
        if item.get("severity", "required") != "required" and item.get("result") != "PASS"
    ]
    if required_failures:
        verdict = "FAIL"
    elif optional_failures:
        verdict = "WARN"
    else:
        verdict = "PASS"

    output = Path(args.output or "harness/evals/results/latest.json")
    if not output.is_absolute():
        output = root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).isoformat()
    result = {
        "suite_id": suite.get("suite_id", suite_path.stem),
        "generated_at": generated_at,
        "verdict": verdict,
        "case_count": len(results),
        "passed": sum(1 for item in results if item.get("result") == "PASS"),
        "failed": sum(1 for item in results if item.get("result") == "FAIL"),
        "not_run": sum(1 for item in results if item.get("result") == "NOT-RUN"),
        "source_suite": display_path(suite_path, root),
        "results": results,
        "external_network_write": False,
        "arbitrary_code_execution": False,
    }
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    markdown_output = Path(args.markdown_output) if args.markdown_output else output.with_suffix(".md")
    if not markdown_output.is_absolute():
        markdown_output = root / markdown_output
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(eval_markdown(result), encoding="utf-8")

    write_event(
        root,
        {
            "event_id": f"evt_{uuid.uuid4().hex}",
            "trace_id": args.trace_id,
            "task_id": args.task_id,
            "actor": "harnessctl",
            "actor_type": "evaluator",
            "event_type": "eval.suite_run",
            "timestamp": generated_at,
            "verdict": verdict,
            "summary": f"Eval suite {result['suite_id']} completed with {verdict}",
            "evidence_path": display_path(output, root),
            "part_id": "",
            "worker_id": "",
            "model": "",
            "effort": "",
        },
    )
    print(f"eval result written: {display_path(output, root)}")
    print(f"eval report written: {display_path(markdown_output, root)}")
    print(f"verdict: {verdict}")
    return 1 if verdict == "FAIL" else 0


def default_context_files(root: Path, task_id: str, software: bool) -> list[str]:
    files = [
        "feature_list.json",
        "progress.md",
        "session-handoff.md",
        "harness/shared/ACTIVE_SNAPSHOT.md",
        "harness/shared/CONTEXT.md",
        "harness/shared/MEMORY.md",
        "harness/shared/PART_OWNERSHIP.md",
        "harness/shared/MODEL_ROUTING.json",
        "harness/shared/AGENT_COMMUNICATION.md",
        "harness/shared/CURRENT_MARKET_RESEARCH_POLICY.md",
        "harness/shared/CROSS_FEEDBACK_LOOP.md",
        "harness/shared/CONCEPT_TRANSLATION_POLICY.md",
        "harness/shared/QUALITY_GATES.md",
        "harness/shared/CONTEXT_PRESSURE.md",
        "harness/shared/SESSION_CONTINUITY.md",
    ]
    task_dir = root / "harness" / "tasks" / task_id
    for name in ["BLUEPRINT.md", "BUDGET.json", "WORKER_BRIEF.json", "TASK_PACKET.json"]:
        if task_dir.joinpath(name).exists():
            files.append(f"harness/tasks/{task_id}/{name}")
    if software:
        files.append("harness/shared/SOFTWARE_FEEDBACK_POLICY.md")
    return files


def build_context_pack(args: argparse.Namespace, root: Path) -> int:
    include_files = default_context_files(root, args.task_id, args.software)
    include_files.extend(split_values(args.include_file))
    seen: set[str] = set()
    sources: list[dict[str, Any]] = []
    for rel in include_files:
        if rel in seen:
            continue
        seen.add(rel)
        path = root / rel
        meta = source_metadata(path, root)
        source = {
            **meta,
            "excerpt": bounded_text(read_text(path), args.max_chars_per_file) if path.exists() else "",
        }
        sources.append(source)

    events = [sanitize_event(row) for row in event_rows(root, args.include_events)]
    payload = {
        "artifact": "context_pack",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task_id": args.task_id,
        "part_id": args.part_id or "UNKNOWN",
        "worker_id": args.worker_id or "UNKNOWN",
        "project_goal": project_goal(root),
        "token_saving_rules": [
            "Use this bounded context pack before loading full files.",
            "Open source paths only when the excerpt is insufficient.",
            "Do not forward full transcripts to routine workers.",
            "Keep durable lessons in TEAM_CONTEXT.md and cross-team decisions in harness/shared/CONTEXT.md.",
        ],
        "source_count": len(sources),
        "sources": sources,
        "recent_events": events,
        "do_not_load_by_default": [
            "private logs",
            "full archives",
            "generated reports unless the task needs a compiled view",
            "unrelated part-owner session history",
        ],
    }
    output = artifact_path(root, args.output, args.task_id, "CONTEXT_PACK.json")
    json_artifact(output, payload)

    markdown = output.with_suffix(".md")
    lines = [
        "# Context Pack",
        "",
        f"Task: `{args.task_id}`",
        f"Part: `{args.part_id or 'UNKNOWN'}`",
        f"Generated: {payload['generated_at']}",
        "",
        "## Token Rules",
        "",
        *[f"- {item}" for item in payload["token_saving_rules"]],
        "",
        "## Source Paths",
        "",
        "| path | status | sha256 |",
        "| --- | --- | --- |",
    ]
    for source in sources:
        lines.append(f"| `{source['path']}` | {source['status']} | `{source['sha256']}` |")
    lines.extend(["", "## Recent Events", ""])
    for row in events:
        lines.append(
            f"- `{row.get('event_type', 'UNKNOWN')}` {row.get('verdict', 'NONE')} "
            f"`{row.get('evidence_path', '')}`"
        )
    markdown.write_text("\n".join(lines) + "\n", encoding="utf-8")

    write_event(
        root,
        {
            "event_id": f"evt_{uuid.uuid4().hex}",
            "trace_id": args.trace_id,
            "task_id": args.task_id,
            "actor": "harnessctl",
            "actor_type": "hook",
            "event_type": "context_pack.created",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "verdict": "PASS",
            "summary": f"Context pack created with {len(sources)} bounded sources.",
            "evidence_path": display_path(output, root),
            "part_id": args.part_id or "",
            "worker_id": args.worker_id or "",
            "model": "",
            "effort": "",
        },
    )
    print(f"context pack written: {display_path(output, root)}")
    print(f"context pack markdown written: {display_path(markdown, root)}")
    return 0


def compute_model_route(
    root: Path,
    role: str,
    task_difficulty: str,
    simple: bool,
    verified_alias: str = "",
) -> dict[str, Any]:
    routing = load_json(root / "harness" / "shared" / "MODEL_ROUTING.json", {})
    policy = routing.get("policy", {}) if isinstance(routing, dict) else {}
    tiers = routing.get("worker_tiers", {}) if isinstance(routing, dict) else {}
    if role == "operator":
        operator = policy.get("operators", {}) if isinstance(policy, dict) else {}
        return {
            "role": role,
            "task_difficulty": task_difficulty,
            "selected_model_class": operator.get("model_class", "highest_verified_available"),
            "selected_reasoning_effort": operator.get("reasoning_effort", "highest_verified_available"),
            "candidate_aliases": [],
            "verification_status": "operator_uses_highest_verified_available",
            "policy_path": "harness/shared/MODEL_ROUTING.json",
        }

    workers = policy.get("workers", {}) if isinstance(policy, dict) else {}
    tier_key = "routine" if simple else task_difficulty
    tier = tiers.get(tier_key, {}) if isinstance(tiers, dict) else {}
    aliases = workers.get("routine_task_aliases", []) if isinstance(workers, dict) else []
    if not isinstance(aliases, list):
        aliases = []
    selected_alias = verified_alias if verified_alias in aliases else ""
    use_routine = simple or task_difficulty == "routine"
    selected_model = selected_alias or workers.get("default_model_class", "lowest_verified_that_satisfies_gate")
    verification = "verified_alias_selected" if selected_alias else "requires_local_alias_verification"
    if not use_routine:
        selected_model = tier.get("example_model_classes", ["strong_verified"])[0]
        verification = "tier_policy_selected_requires_local_verification"
    return {
        "role": role,
        "task_difficulty": task_difficulty,
        "simple_task": use_routine,
        "selected_model_class": selected_model,
        "selected_reasoning_effort": tier.get(
            "reasoning_effort",
            workers.get("default_reasoning_effort", "lowest_verified_that_satisfies_gate"),
        ),
        "candidate_aliases": aliases if use_routine else tier.get("example_model_classes", []),
        "verified_alias": selected_alias,
        "verification_status": verification,
        "part_owner_session_policy": workers.get("session_policy", "part_owner_resume_when_safe"),
        "policy_path": "harness/shared/MODEL_ROUTING.json",
    }


def route_model(args: argparse.Namespace, root: Path) -> int:
    payload = {
        "artifact": "model_route",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task_id": args.task_id,
        **compute_model_route(root, args.role, args.task_difficulty, args.simple, args.verified_alias),
    }
    output = Path(args.output) if args.output else None
    if output:
        if not output.is_absolute():
            output = root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        json_artifact(output, payload)
        evidence_path = display_path(output, root)
        print(f"model route written: {evidence_path}")
    else:
        evidence_path = ""
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    if args.task_id:
        write_event(
            root,
            {
                "event_id": f"evt_{uuid.uuid4().hex}",
                "trace_id": args.trace_id,
                "task_id": args.task_id,
                "actor": "harnessctl",
                "actor_type": "hook",
                "event_type": "model_route.selected",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "verdict": "PASS",
                "summary": f"Model route selected for {args.role}/{args.task_difficulty}.",
                "evidence_path": evidence_path,
                "part_id": "",
                "worker_id": "",
                "model": str(payload.get("selected_model_class", "")),
                "effort": str(payload.get("selected_reasoning_effort", "")),
            },
        )
    return 0


def generate_worker_brief(args: argparse.Namespace, root: Path) -> int:
    template = load_json(root / "harness" / "templates" / "WORKER_BRIEF.json", {})
    if not isinstance(template, dict):
        print("ERROR: invalid harness/templates/WORKER_BRIEF.json", file=sys.stderr)
        return 1
    brief = dict(template)
    owned_paths = split_values(args.owned_path) or ["UNKNOWN"]
    no_touch_paths = split_values(args.no_touch_path) or ["UNKNOWN"]
    success_criteria = split_values(args.success_criterion) or ["UNKNOWN"]
    evidence_required = split_values(args.evidence_command) or ["UNKNOWN"]
    part_id = args.part_id or args.task_id
    route = compute_model_route(root, "worker", args.task_difficulty, args.simple, args.verified_alias)

    brief.update(
        {
            "task_id": args.task_id,
            "feature_id": args.feature_id or "UNKNOWN",
            "slice_id": args.slice_id or "UNKNOWN",
            "part_id": part_id,
            "part_scope": args.part_scope or "UNKNOWN",
            "goal": args.goal or project_goal(root),
            "owned_paths": owned_paths,
            "no_touch_paths": no_touch_paths,
            "context_pack_path": args.context_pack or f"harness/tasks/{args.task_id}/CONTEXT_PACK.json",
            "success_criteria": success_criteria,
            "commands_or_evidence_required": evidence_required,
            "checkpoint_eta": args.checkpoint_eta or "UNKNOWN",
        }
    )
    model_routing = dict(brief.get("model_routing", {}))
    model_routing.update(
        {
            "model_class": route["selected_model_class"],
            "reasoning_effort": route["selected_reasoning_effort"],
            "task_difficulty": args.task_difficulty,
            "candidate_aliases": route.get("candidate_aliases", []),
            "verification_status": route.get("verification_status", "UNKNOWN"),
        }
    )
    brief["model_routing"] = model_routing

    output = artifact_path(root, args.output, args.task_id, "WORKER_BRIEF.json")
    json_artifact(output, brief)
    write_event(
        root,
        {
            "event_id": f"evt_{uuid.uuid4().hex}",
            "trace_id": args.trace_id,
            "task_id": args.task_id,
            "actor": "harnessctl",
            "actor_type": "operator",
            "event_type": "worker_brief.created",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "verdict": "PASS",
            "summary": f"Worker brief created for part {part_id}.",
            "evidence_path": display_path(output, root),
            "part_id": part_id,
            "worker_id": args.worker_id or "",
            "model": str(route.get("selected_model_class", "")),
            "effort": str(route.get("selected_reasoning_effort", "")),
        },
    )
    print(f"worker brief written: {display_path(output, root)}")
    return 0


def create_task_packet(args: argparse.Namespace, root: Path) -> int:
    evidence_paths = split_values(args.evidence_path)
    missing = []
    for value in evidence_paths:
        if value == "UNKNOWN":
            continue
        path = Path(value)
        candidate = path if path.is_absolute() else root / path
        if not candidate.exists():
            missing.append(value)
    payload = {
        "artifact": "task_packet",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task_id": args.task_id,
        "part_id": args.part_id or "UNKNOWN",
        "sender": args.sender,
        "receiver": args.receiver,
        "intent": args.intent,
        "summary": bounded_text(args.summary, args.max_summary_chars),
        "evidence_paths": evidence_paths,
        "requested_action": args.requested_action or "UNKNOWN",
        "stop_if_unanswered": args.stop_if_unanswered,
        "missing_evidence_paths": missing,
        "communication_policy": "harness/shared/AGENT_COMMUNICATION.md",
    }
    output = artifact_path(root, args.output, args.task_id, "TASK_PACKET.json")
    json_artifact(output, payload)
    verdict = "WARN" if missing else "PASS"
    write_event(
        root,
        {
            "event_id": f"evt_{uuid.uuid4().hex}",
            "trace_id": args.trace_id,
            "task_id": args.task_id,
            "actor": "harnessctl",
            "actor_type": "hook",
            "event_type": "task_packet.created",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "verdict": verdict,
            "summary": f"Task packet created for {args.receiver}.",
            "evidence_path": display_path(output, root),
            "part_id": args.part_id or "",
            "worker_id": "",
            "model": "",
            "effort": "",
        },
    )
    print(f"task packet written: {display_path(output, root)}")
    if missing and not args.allow_missing_evidence:
        print("ERROR: task packet has missing evidence paths: " + ", ".join(missing), file=sys.stderr)
        return 1
    return 0


def record_current_research(args: argparse.Namespace, root: Path) -> int:
    queries = split_values(args.query)
    sources = split_values(args.source)
    findings = split_values(args.finding)
    alternatives = split_values(args.alternative)
    impacts = split_values(args.decision_impact)
    not_run_reason = args.not_run_reason.strip()
    if not_run_reason:
        verdict = "NOT-RUN"
    elif sources and findings:
        verdict = "PASS"
    else:
        verdict = "WARN"

    output = artifact_path(root, args.output, args.task_id, "CURRENT_RESEARCH.json")
    payload = {
        "artifact": "current_research",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task_id": args.task_id,
        "trace_id": args.trace_id,
        "policy": "harness/shared/CURRENT_MARKET_RESEARCH_POLICY.md",
        "as_of": args.as_of or datetime.now(timezone.utc).date().isoformat(),
        "scope": args.scope or "current_market_and_comparable_state",
        "must_precede": "overall_plan",
        "verdict": verdict,
        "queries": queries,
        "sources": sources,
        "alternatives_or_comparables": alternatives,
        "findings": findings,
        "decision_impact": impacts,
        "not_run_reason": not_run_reason,
        "external_network_write": False,
        "claim_boundary": [
            "records current-state research evidence",
            "does not browse or buy data",
            "does not replace source quality judgment",
        ],
    }
    json_artifact(output, payload)
    markdown = output.with_suffix(".md")
    lines = [
        "# Current Research",
        "",
        f"Task: `{args.task_id}`",
        f"Verdict: {verdict}",
        f"As-of: {payload['as_of']}",
        "",
        "## Queries",
        "",
        *[f"- {scrub_text(item)}" for item in queries],
        "",
        "## Sources",
        "",
        *[f"- {scrub_text(item)}" for item in sources],
        "",
        "## Alternatives Or Comparables",
        "",
        *[f"- {scrub_text(item)}" for item in alternatives],
        "",
        "## Findings",
        "",
        *[f"- {scrub_text(item)}" for item in findings],
        "",
        "## Decision Impact",
        "",
        *[f"- {scrub_text(item)}" for item in impacts],
    ]
    if not_run_reason:
        lines.extend(["", "## NOT-RUN Reason", "", scrub_text(not_run_reason)])
    markdown.write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_event(
        root,
        {
            "event_id": f"evt_{uuid.uuid4().hex}",
            "trace_id": args.trace_id,
            "task_id": args.task_id,
            "actor": "harnessctl",
            "actor_type": "hook",
            "event_type": "current_research.completed",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "verdict": verdict,
            "summary": f"Current research recorded with {verdict}.",
            "evidence_path": display_path(output, root),
            "part_id": "",
            "worker_id": "",
            "model": "",
            "effort": "",
        },
    )
    print(f"current research written: {display_path(output, root)}")
    print(f"current research markdown written: {display_path(markdown, root)}")
    print(f"verdict: {verdict}")
    if verdict == "PASS" or (verdict == "NOT-RUN" and args.allow_not_run):
        return 0
    return 1


def record_cross_feedback(args: argparse.Namespace, root: Path) -> int:
    evidence_paths = split_values(args.evidence_path)
    missing = []
    for value in evidence_paths:
        path = Path(value)
        candidate = path if path.is_absolute() else root / path
        if value != "UNKNOWN" and not candidate.exists():
            missing.append(value)
    verdict = args.verdict
    if missing and verdict == "PASS":
        verdict = "WARN"
    output = artifact_path(root, args.output, args.task_id, "CROSS_FEEDBACK.json")
    payload = {
        "artifact": "cross_feedback",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task_id": args.task_id,
        "trace_id": args.trace_id,
        "policy": "harness/shared/CROSS_FEEDBACK_LOOP.md",
        "round": args.round,
        "producer": args.producer,
        "reviewer": args.reviewer,
        "verdict": verdict,
        "feedback": bounded_text(args.feedback, args.max_feedback_chars),
        "requested_action": args.requested_action or "UNKNOWN",
        "route_to": args.route_to or "UNKNOWN",
        "evidence_paths": evidence_paths,
        "missing_evidence_paths": missing,
        "dissent_preserved": args.dissent_preserved,
        "force_consensus": False,
    }
    json_artifact(output, payload)
    markdown = output.with_suffix(".md")
    lines = [
        "# Cross Feedback",
        "",
        f"Task: `{args.task_id}`",
        f"Round: {args.round}",
        f"Producer: `{args.producer}`",
        f"Reviewer: `{args.reviewer}`",
        f"Verdict: {verdict}",
        "",
        "## Feedback",
        "",
        scrub_text(args.feedback),
        "",
        "## Requested Action",
        "",
        scrub_text(args.requested_action or "UNKNOWN"),
        "",
        "## Evidence Paths",
        "",
        *[f"- `{scrub_text(item)}`" for item in evidence_paths],
    ]
    markdown.write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_event(
        root,
        {
            "event_id": f"evt_{uuid.uuid4().hex}",
            "trace_id": args.trace_id,
            "task_id": args.task_id,
            "actor": "harnessctl",
            "actor_type": "evaluator",
            "event_type": "cross_feedback.recorded",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "verdict": verdict,
            "summary": f"Cross feedback recorded by {args.reviewer} for {args.producer}.",
            "evidence_path": display_path(output, root),
            "part_id": "",
            "worker_id": args.reviewer,
            "model": "",
            "effort": "",
        },
    )
    print(f"cross feedback written: {display_path(output, root)}")
    print(f"cross feedback markdown written: {display_path(markdown, root)}")
    print(f"verdict: {verdict}")
    if missing and not args.allow_missing_evidence:
        print("ERROR: cross feedback has missing evidence paths: " + ", ".join(missing), file=sys.stderr)
        return 1
    if verdict == "FAIL" and not args.allow_fail:
        return 1
    return 0


DEFAULT_CONCEPT_META_PHRASES = [
    "as requested",
    "as you requested",
    "this is a website for",
    "this website was created",
    "this page was created",
    "created for your request",
    "requested by the user",
    "the user asked for",
    "요청하신",
    "요청에 따라",
    "사용자가 요청한",
    "사용자의 요청",
    "요청한 것을",
    "라는 요청",
    "만들어줘",
]

CONCEPT_ANNOUNCEMENT_PHRASES = [
    "here is",
    "this is",
    "this is a",
    "이것은",
    "인 것입니다",
    "만든 것입니다",
]

TASK_ARTIFACT_NOUNS = [
    "app",
    "application",
    "dashboard",
    "document",
    "page",
    "portfolio",
    "report",
    "service",
    "site",
    "tool",
    "web app",
    "web page",
    "web site",
    "website",
    "도구",
    "문서",
    "보고서",
    "사이트",
    "서비스",
    "앱",
    "어플",
    "웹사이트",
    "페이지",
    "포트폴리오",
]

ASSIGNMENT_STYLE_TERMS = [
    "about",
    "for",
    "that",
    "to",
    "with",
    "만드는",
    "위한",
    "용",
    "파는",
    "판매",
    "하는",
]


def normalized_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.casefold()).strip()


def derived_goal_phrases(goal: str) -> list[str]:
    normalized = normalized_text(goal)
    if not normalized or normalized == "unknown":
        return []
    phrases = {normalized}
    replacements = [
        (r"^(please\s+)?(make|create|build|generate|design)\s+(me\s+)?(a|an|the)?\s*", ""),
        (r"\s+(for me|please)$", ""),
        (r"(를|을)?\s*(만들어\s*줘|만들어줘|만들어\s*주세요|제작해\s*줘|제작해줘|생성해\s*줘|생성해줘|구현해\s*줘|구현해줘)$", ""),
        (r"^\s*(나는|제가|나에게)\s*", ""),
        (r"\s*(원한다|하고\s*싶다|싶어)$", ""),
    ]
    candidate = normalized
    changed = True
    while changed:
        changed = False
        for pattern, replacement in replacements:
            updated = re.sub(pattern, replacement, candidate).strip()
            if updated and updated != candidate:
                phrases.add(updated)
                candidate = updated
                changed = True
    compact = re.sub(r"\b(a|an|the)\b", "", normalized).strip()
    compact = re.sub(r"\s+", " ", compact)
    if compact and compact != normalized:
        phrases.add(compact)
    return sorted(phrases, key=len, reverse=True)


def assignment_style_phrase(phrase: str) -> bool:
    normalized = normalized_text(phrase)
    if len(normalized) < 10:
        return False
    has_artifact_noun = any(noun in normalized for noun in TASK_ARTIFACT_NOUNS)
    has_assignment_term = any(term in normalized for term in ASSIGNMENT_STYLE_TERMS)
    return has_artifact_noun and has_assignment_term


def prominent_phrase_line(text: str, phrase: str) -> bool:
    normalized_phrase = normalized_text(phrase)
    if not normalized_phrase:
        return False
    for index, line in enumerate(text.splitlines()):
        stripped = line.strip()
        normalized_line = normalized_text(stripped.lstrip("#").strip())
        if normalized_phrase not in normalized_line:
            continue
        is_heading = stripped.startswith("#") or stripped.lower().startswith(("<h1", "<h2", "<title"))
        is_early = index < 8
        is_standalone = len(normalized_line) <= len(normalized_phrase) + 18
        if is_heading or (is_early and is_standalone):
            return True
    return False


def phrase_near_marker(text: str, phrase: str, markers: list[str], window: int = 96) -> bool:
    normalized = normalized_text(text)
    normalized_phrase = normalized_text(phrase)
    if not normalized_phrase:
        return False
    start = 0
    while True:
        index = normalized.find(normalized_phrase, start)
        if index < 0:
            return False
        context = normalized[max(0, index - window): index + len(normalized_phrase) + window]
        if any(normalized_text(marker) in context for marker in markers):
            return True
        start = index + len(normalized_phrase)


def add_concept_finding(
    findings: list[dict[str, Any]],
    path: Path,
    root: Path,
    phrase: str,
    reason: str,
    mode: str,
) -> None:
    findings.append(
        {
            "artifact_path": display_path(path, root),
            "phrase": scrub_text(phrase),
            "reason": reason,
            "mode": mode,
        }
    )


def concept_check(args: argparse.Namespace, root: Path) -> int:
    policy = root / "harness" / "shared" / "CONCEPT_TRANSLATION_POLICY.md"
    if not policy.exists():
        print("ERROR: missing harness/shared/CONCEPT_TRANSLATION_POLICY.md", file=sys.stderr)
        return 1
    artifacts = split_values(args.artifact_path)
    if not artifacts:
        print("ERROR: concept-check requires at least one --artifact-path", file=sys.stderr)
        return 2

    explicit_forbidden = split_values(args.forbidden_phrase)
    raw_goal_phrases: list[str] = []
    derived_phrases: list[str] = []
    if not args.allow_project_goal:
        goal = project_goal(root)
        if goal and goal != "UNKNOWN":
            raw_goal_phrases.append(goal)
            derived_phrases = [
                phrase for phrase in derived_goal_phrases(goal)
                if normalized_text(phrase) != normalized_text(goal)
            ]
    hard_forbidden = [*explicit_forbidden, *raw_goal_phrases]
    if not args.disable_meta_phrases:
        hard_forbidden.extend(DEFAULT_CONCEPT_META_PHRASES)

    min_length = max(1, args.min_phrase_length)
    findings: list[dict[str, Any]] = []
    checked: list[dict[str, str]] = []
    for artifact in artifacts:
        path = Path(artifact)
        if not path.is_absolute():
            path = root / path
        checked.append(source_metadata(path, root))
        text = read_text(path)
        normalized = normalized_text(text)
        for phrase in hard_forbidden:
            normalized_phrase = normalized_text(phrase)
            if len(normalized_phrase) < min_length:
                continue
            if normalized_phrase and normalized_phrase in normalized:
                add_concept_finding(
                    findings,
                    path,
                    root,
                    phrase,
                    "literal prompt or self-descriptive meta-copy leakage",
                    "hard_literal",
                )
        if args.disable_derived_goal:
            continue
        contextual_markers = [] if args.disable_meta_phrases else [
            *DEFAULT_CONCEPT_META_PHRASES,
            *CONCEPT_ANNOUNCEMENT_PHRASES,
        ]
        for phrase in derived_phrases:
            normalized_phrase = normalized_text(phrase)
            if len(normalized_phrase) < min_length or normalized_phrase not in normalized:
                continue
            if args.strict_derived_goal:
                add_concept_finding(
                    findings,
                    path,
                    root,
                    phrase,
                    "derived goal phrase used as artifact copy under strict mode",
                    "strict_derived_goal",
                )
                continue
            if contextual_markers and phrase_near_marker(text, phrase, contextual_markers):
                add_concept_finding(
                    findings,
                    path,
                    root,
                    phrase,
                    "concept phrase used in a self-descriptive announcement",
                    "contextual_announcement",
                )
                continue
            if assignment_style_phrase(phrase) and prominent_phrase_line(text, phrase):
                add_concept_finding(
                    findings,
                    path,
                    root,
                    phrase,
                    "assignment-style concept phrase used as prominent artifact copy",
                    "prominent_assignment_phrase",
                )

    verdict = "FAIL" if findings else "PASS"
    output = artifact_path(root, args.output, args.task_id, "CONCEPT_CHECK.json")
    payload = {
        "artifact": "concept_check",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task_id": args.task_id,
        "trace_id": args.trace_id,
        "policy": "harness/shared/CONCEPT_TRANSLATION_POLICY.md",
        "verdict": verdict,
        "checked": checked,
        "finding_count": len(findings),
        "derived_goal_phrase_count": len(derived_phrases) if not args.allow_project_goal else 0,
        "derived_goal_policy": "disabled" if args.disable_derived_goal else ("strict" if args.strict_derived_goal else "contextual"),
        "findings": findings,
        "claim_boundary": [
            "literal leakage guard",
            "derived goal phrases are contextual signals by default, not universal bans",
            "not a complete writing or design quality judge",
            "not semantic proof that the concept was translated well",
        ],
    }
    json_artifact(output, payload)
    write_event(
        root,
        {
            "event_id": f"evt_{uuid.uuid4().hex}",
            "trace_id": args.trace_id,
            "task_id": args.task_id,
            "actor": "harnessctl",
            "actor_type": "evaluator",
            "event_type": "concept_check.completed",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "verdict": verdict,
            "summary": f"Concept translation literal leakage check completed with {verdict}.",
            "evidence_path": display_path(output, root),
            "part_id": "",
            "worker_id": "",
            "model": "",
            "effort": "",
        },
    )
    print(f"concept check written: {display_path(output, root)}")
    print(f"verdict: {verdict}")
    if findings:
        for finding in findings[:10]:
            print(
                f"finding: {finding['artifact_path']} contains {finding['phrase']}",
                file=sys.stderr,
            )
    return 1 if verdict == "FAIL" and not args.allow_findings else 0


def run_feedback_command(root: Path, task_dir: Path, axis: str, command: str, required: bool, timeout: int) -> dict[str, Any]:
    if not command:
        return {
            "axis": axis,
            "required": required,
            "result": "NOT-RUN",
            "command": "",
            "returncode": None,
            "notes": "No command supplied.",
            "log_path": "",
        }
    log_path = task_dir / "software_feedback" / f"{axis}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    started_at = datetime.now(timezone.utc).isoformat()
    try:
        result = subprocess.run(
            command,
            cwd=str(root),
            shell=True,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        output = [
            f"$ {command}",
            f"started_at: {started_at}",
            f"returncode: {result.returncode}",
            "",
            "## stdout",
            result.stdout,
            "",
            "## stderr",
            result.stderr,
        ]
        log_path.write_text("\n".join(output), encoding="utf-8")
        return {
            "axis": axis,
            "required": required,
            "result": "PASS" if result.returncode == 0 else "FAIL",
            "command": command,
            "returncode": result.returncode,
            "notes": "command completed",
            "log_path": display_path(log_path, root),
            "stdout_tail": bounded_text(result.stdout[-1200:], 1200),
            "stderr_tail": bounded_text(result.stderr[-1200:], 1200),
        }
    except subprocess.TimeoutExpired as exc:
        log_path.write_text(f"$ {command}\nTIMEOUT after {timeout}s\n{exc}\n", encoding="utf-8")
        return {
            "axis": axis,
            "required": required,
            "result": "FAIL",
            "command": command,
            "returncode": None,
            "notes": f"timeout after {timeout}s",
            "log_path": display_path(log_path, root),
        }


def run_software_feedback(args: argparse.Namespace, root: Path) -> int:
    task_dir = ensure_task_dir(root, args.task_id)
    axes = [
        run_feedback_command(root, task_dir, "lint_static", args.lint_command, True, args.timeout_seconds),
        run_feedback_command(root, task_dir, "runtime_smoke", args.smoke_command, True, args.timeout_seconds),
        run_feedback_command(root, task_dir, "tests", args.test_command, args.require_tests, args.timeout_seconds),
        run_feedback_command(
            root,
            task_dir,
            "browser_playwright",
            args.playwright_command,
            args.require_playwright,
            args.timeout_seconds,
        ),
    ]
    context_files = [
        root / "harness" / "spec" / "PRD_DRAFT.md",
        root / "harness" / "spec" / "ANTI_PRD.md",
        task_dir / "WORKER_BRIEF.json",
    ]
    if not context_files[-1].exists():
        context_files[-1] = root / "harness" / "templates" / "WORKER_BRIEF.json"
    missing_context = [display_path(path, root) for path in context_files if not path.exists()]
    axes.append(
        {
            "axis": "context_chain",
            "required": True,
            "result": "PASS" if not missing_context else "FAIL",
            "command": "file existence check",
            "returncode": 0 if not missing_context else 1,
            "notes": "PRD, anti-PRD, and worker brief references exist." if not missing_context else "missing: " + ", ".join(missing_context),
            "log_path": "",
        }
    )
    ui_required = args.require_ui_review
    ui_result = "PASS" if args.ui_review_note else ("NOT-RUN" if ui_required else "NOT-RUN")
    axes.append(
        {
            "axis": "ui_ux_layout_review",
            "required": ui_required,
            "result": ui_result,
            "command": "",
            "returncode": None,
            "notes": bounded_text(args.ui_review_note or "No UI/UX/layout review note supplied.", 1600),
            "log_path": "",
        }
    )

    required_axes = [axis for axis in axes if axis.get("required") is True]
    if any(axis.get("result") == "FAIL" for axis in required_axes):
        verdict = "FAIL"
    elif any(axis.get("result") == "NOT-RUN" for axis in required_axes):
        verdict = "WARN"
    else:
        verdict = "PASS"

    output = artifact_path(root, args.output, args.task_id, "SOFTWARE_FEEDBACK.json")
    payload = {
        "artifact": "software_feedback",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task_id": args.task_id,
        "trace_id": args.trace_id,
        "policy": "harness/shared/SOFTWARE_FEEDBACK_POLICY.md",
        "verdict": verdict,
        "allow_not_run": args.allow_not_run,
        "axes": axes,
        "external_network_write": "not_requested_by_harnessctl",
    }
    json_artifact(output, payload)
    markdown = output.with_suffix(".md")
    lines = [
        "# Software Feedback",
        "",
        f"Task: `{args.task_id}`",
        f"Verdict: {verdict}",
        f"Generated: {payload['generated_at']}",
        "",
        "| axis | required | result | command | evidence | notes |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for axis in axes:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(axis.get("axis", "UNKNOWN")).replace("|", "\\|"),
                    str(axis.get("required", False)).replace("|", "\\|"),
                    str(axis.get("result", "UNKNOWN")).replace("|", "\\|"),
                    "`" + scrub_text(axis.get("command", "")).replace("|", "\\|") + "`",
                    "`" + scrub_text(axis.get("log_path", "")).replace("|", "\\|") + "`",
                    scrub_text(axis.get("notes", "")).replace("|", "\\|").replace("\n", " "),
                ]
            )
            + " |"
        )
    markdown.write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_event(
        root,
        {
            "event_id": f"evt_{uuid.uuid4().hex}",
            "trace_id": args.trace_id,
            "task_id": args.task_id,
            "actor": "harnessctl",
            "actor_type": "evaluator",
            "event_type": "software_feedback.completed",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "verdict": verdict,
            "summary": f"Software feedback completed with {verdict}.",
            "evidence_path": display_path(output, root),
            "part_id": "",
            "worker_id": "",
            "model": "",
            "effort": "",
        },
    )
    print(f"software feedback written: {display_path(output, root)}")
    print(f"software feedback markdown written: {display_path(markdown, root)}")
    if verdict == "PASS" or (args.allow_not_run and verdict == "WARN"):
        return 0
    return 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("validate", help="Run local harness validator")

    event = sub.add_parser("event", help="Append one observability event")
    event.add_argument("--task-id", required=True)
    event.add_argument("--slice-id", default="")
    event.add_argument("--trace-id", default="trace_UNKNOWN")
    event.add_argument("--actor", required=True)
    event.add_argument("--actor-type", required=True)
    event.add_argument("--event-type", required=True)
    event.add_argument("--event-id", default="")
    event.add_argument("--verdict", default="NONE")
    event.add_argument("--summary", default="")
    event.add_argument("--evidence-path", default="")
    event.add_argument("--part-id", default="")
    event.add_argument("--worker-id", default="")
    event.add_argument("--model", default="")
    event.add_argument("--effort", default="")
    event.add_argument("--token-used", type=float, default=None)
    event.add_argument("--time-elapsed-minutes", type=float, default=None)
    event.add_argument("--cost-used-usd", type=float, default=None)
    event.add_argument("--budget-percent", type=float, default=None)
    event.add_argument("--budget-status", default="")

    report = sub.add_parser("report", help="Compile local static HTML status report")
    report.add_argument("--output", default="")
    report.add_argument("--max-events", type=int, default=80)

    budget = sub.add_parser("budget-check", help="Check task budget thresholds and write budget events")
    budget.add_argument("--task-id", required=True)
    budget.add_argument("--trace-id", default="trace_budget")
    budget.add_argument("--token-used", type=float, default=None)
    budget.add_argument("--time-elapsed-minutes", type=float, default=None)
    budget.add_argument("--cost-used-usd", type=float, default=None)

    viz = sub.add_parser("viz-spec-check", help="Check the pre-visualization spec gate")
    viz.add_argument("--task-id", default="")
    viz.add_argument("--path", default="")
    viz.add_argument("--require-approved", action="store_true")

    viz_export = sub.add_parser("viz-export", help="Export events.jsonl to an approved local viz backend payload")
    viz_export.add_argument("--backend", default="")
    viz_export.add_argument("--output-dir", default="")
    viz_export.add_argument("--task-id", default="VIZ-EXPORT")
    viz_export.add_argument("--trace-id", default="trace_viz_export")
    viz_export.add_argument("--max-events", type=int, default=500)

    eval_run = sub.add_parser("eval-run", help="Run a dependency-free local eval suite")
    eval_run.add_argument("--suite", default="harness/evals/golden_suite.json")
    eval_run.add_argument("--output", default="harness/evals/results/latest.json")
    eval_run.add_argument("--markdown-output", default="")
    eval_run.add_argument("--task-id", default="EVAL-RUN")
    eval_run.add_argument("--trace-id", default="trace_eval_run")

    archive = sub.add_parser("archive", help="Move a non-active task directory into harness/tasks/archive")
    archive.add_argument("--task-id", required=True)
    archive.add_argument("--trace-id", default="trace_UNKNOWN")
    archive.add_argument("--reason", default="")
    archive.add_argument("--force", action="store_true")

    context_pack = sub.add_parser("context-pack", help="Compile a bounded context pack for a task")
    context_pack.add_argument("--task-id", required=True)
    context_pack.add_argument("--part-id", default="")
    context_pack.add_argument("--worker-id", default="")
    context_pack.add_argument("--include-file", action="append", default=[])
    context_pack.add_argument("--include-events", type=int, default=12)
    context_pack.add_argument("--max-chars-per-file", type=int, default=1400)
    context_pack.add_argument("--software", action="store_true")
    context_pack.add_argument("--output", default="")
    context_pack.add_argument("--trace-id", default="trace_context_pack")

    model_route = sub.add_parser("model-route", help="Select a model route from MODEL_ROUTING.json")
    model_route.add_argument("--role", choices=["operator", "worker", "evaluator"], default="worker")
    model_route.add_argument("--task-difficulty", choices=["routine", "standard", "complex", "independent_evaluation"], default="routine")
    model_route.add_argument("--simple", action="store_true")
    model_route.add_argument("--verified-alias", default="")
    model_route.add_argument("--task-id", default="")
    model_route.add_argument("--trace-id", default="trace_model_route")
    model_route.add_argument("--output", default="")

    worker_brief = sub.add_parser("worker-brief", help="Generate a task-local worker brief from the canonical template")
    worker_brief.add_argument("--task-id", required=True)
    worker_brief.add_argument("--feature-id", default="")
    worker_brief.add_argument("--slice-id", default="")
    worker_brief.add_argument("--part-id", default="")
    worker_brief.add_argument("--part-scope", default="")
    worker_brief.add_argument("--goal", default="")
    worker_brief.add_argument("--owned-path", action="append", default=[])
    worker_brief.add_argument("--no-touch-path", action="append", default=[])
    worker_brief.add_argument("--success-criterion", action="append", default=[])
    worker_brief.add_argument("--evidence-command", action="append", default=[])
    worker_brief.add_argument("--context-pack", default="")
    worker_brief.add_argument("--task-difficulty", choices=["routine", "standard", "complex", "independent_evaluation"], default="routine")
    worker_brief.add_argument("--simple", action="store_true")
    worker_brief.add_argument("--verified-alias", default="")
    worker_brief.add_argument("--worker-id", default="")
    worker_brief.add_argument("--checkpoint-eta", default="")
    worker_brief.add_argument("--trace-id", default="trace_worker_brief")
    worker_brief.add_argument("--output", default="")

    task_packet = sub.add_parser("task-packet", help="Write a bounded agent-to-agent task packet")
    task_packet.add_argument("--task-id", required=True)
    task_packet.add_argument("--part-id", default="")
    task_packet.add_argument("--sender", required=True)
    task_packet.add_argument("--receiver", required=True)
    task_packet.add_argument("--intent", choices=["status", "question", "feedback", "handoff", "decision"], required=True)
    task_packet.add_argument("--summary", required=True)
    task_packet.add_argument("--evidence-path", action="append", default=[])
    task_packet.add_argument("--requested-action", default="")
    task_packet.add_argument("--stop-if-unanswered", action="store_true")
    task_packet.add_argument("--allow-missing-evidence", action="store_true")
    task_packet.add_argument("--max-summary-chars", type=int, default=900)
    task_packet.add_argument("--trace-id", default="trace_task_packet")
    task_packet.add_argument("--output", default="")

    current_research = sub.add_parser("current-research", help="Record current-state research before overall planning")
    current_research.add_argument("--task-id", required=True)
    current_research.add_argument("--trace-id", default="trace_current_research")
    current_research.add_argument("--query", action="append", default=[])
    current_research.add_argument("--source", action="append", default=[])
    current_research.add_argument("--alternative", action="append", default=[])
    current_research.add_argument("--finding", action="append", default=[])
    current_research.add_argument("--decision-impact", action="append", default=[])
    current_research.add_argument("--not-run-reason", default="")
    current_research.add_argument("--allow-not-run", action="store_true")
    current_research.add_argument("--as-of", default="")
    current_research.add_argument("--scope", default="")
    current_research.add_argument("--output", default="")

    cross_feedback = sub.add_parser("cross-feedback", help="Record independent cross-feedback for a task artifact")
    cross_feedback.add_argument("--task-id", required=True)
    cross_feedback.add_argument("--trace-id", default="trace_cross_feedback")
    cross_feedback.add_argument("--round", default="1")
    cross_feedback.add_argument("--producer", required=True)
    cross_feedback.add_argument("--reviewer", required=True)
    cross_feedback.add_argument("--verdict", choices=["PASS", "WARN", "FAIL", "NOT-RUN"], required=True)
    cross_feedback.add_argument("--feedback", required=True)
    cross_feedback.add_argument("--requested-action", default="")
    cross_feedback.add_argument("--route-to", choices=["planning", "design", "production", "evaluation", "context_update", "governance_update", "human_decision", "none"], default="none")
    cross_feedback.add_argument("--evidence-path", action="append", default=[])
    cross_feedback.add_argument("--dissent-preserved", action="store_true")
    cross_feedback.add_argument("--allow-missing-evidence", action="store_true")
    cross_feedback.add_argument("--allow-fail", action="store_true")
    cross_feedback.add_argument("--max-feedback-chars", type=int, default=1600)
    cross_feedback.add_argument("--output", default="")

    concept = sub.add_parser("concept-check", help="Check user-facing artifacts for literal prompt or task-label leakage")
    concept.add_argument("--task-id", required=True)
    concept.add_argument("--trace-id", default="trace_concept_check")
    concept.add_argument("--artifact-path", action="append", default=[])
    concept.add_argument("--forbidden-phrase", action="append", default=[])
    concept.add_argument("--allow-project-goal", action="store_true")
    concept.add_argument("--disable-meta-phrases", action="store_true")
    concept.add_argument("--disable-derived-goal", action="store_true")
    concept.add_argument("--strict-derived-goal", action="store_true")
    concept.add_argument("--allow-findings", action="store_true")
    concept.add_argument("--min-phrase-length", type=int, default=3)
    concept.add_argument("--output", default="")

    software_feedback = sub.add_parser("software-feedback", help="Run and record software feedback evidence")
    software_feedback.add_argument("--task-id", required=True)
    software_feedback.add_argument("--trace-id", default="trace_software_feedback")
    software_feedback.add_argument("--lint-command", default="")
    software_feedback.add_argument("--test-command", default="")
    software_feedback.add_argument("--smoke-command", default="")
    software_feedback.add_argument("--playwright-command", default="")
    software_feedback.add_argument("--require-tests", action="store_true")
    software_feedback.add_argument("--require-playwright", action="store_true")
    software_feedback.add_argument("--require-ui-review", action="store_true")
    software_feedback.add_argument("--ui-review-note", default="")
    software_feedback.add_argument("--timeout-seconds", type=int, default=120)
    software_feedback.add_argument("--allow-not-run", action="store_true")
    software_feedback.add_argument("--output", default="")

    args = parser.parse_args(argv[1:])
    root = project_root()
    if args.command == "validate":
        return run_validate(root)
    if args.command == "event":
        return append_event(args, root)
    if args.command == "report":
        return build_report(args, root)
    if args.command == "budget-check":
        return budget_check(args, root)
    if args.command == "viz-spec-check":
        return check_visualization_spec(args, root)
    if args.command == "viz-export":
        return export_viz_events(args, root)
    if args.command == "eval-run":
        return run_eval_suite(args, root)
    if args.command == "archive":
        return archive_task(args, root)
    if args.command == "context-pack":
        return build_context_pack(args, root)
    if args.command == "model-route":
        return route_model(args, root)
    if args.command == "worker-brief":
        return generate_worker_brief(args, root)
    if args.command == "task-packet":
        return create_task_packet(args, root)
    if args.command == "current-research":
        return record_current_research(args, root)
    if args.command == "cross-feedback":
        return record_cross_feedback(args, root)
    if args.command == "concept-check":
        return concept_check(args, root)
    if args.command == "software-feedback":
        return run_software_feedback(args, root)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
