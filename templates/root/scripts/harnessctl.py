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

    report = sub.add_parser("report", help="Compile local static HTML status report")
    report.add_argument("--output", default="")
    report.add_argument("--max-events", type=int, default=80)

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

    args = parser.parse_args(argv[1:])
    root = project_root()
    if args.command == "validate":
        return run_validate(root)
    if args.command == "event":
        return append_event(args, root)
    if args.command == "report":
        return build_report(args, root)
    if args.command == "viz-spec-check":
        return check_visualization_spec(args, root)
    if args.command == "viz-export":
        return export_viz_events(args, root)
    if args.command == "eval-run":
        return run_eval_suite(args, root)
    if args.command == "archive":
        return archive_task(args, root)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
