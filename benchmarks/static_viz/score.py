#!/usr/bin/env python3
"""Validate the default local visualization evidence path.

This regression guard scaffolds a harness, runs the bootstrap, exports sanitized
events through the default `local_file` backend, and verifies that the generated
status/viz files are local compiled views rather than external memory or network
publication.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ALLOWED_EVENT_FIELDS = {
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

LEAK_PATTERNS = (
    re.compile(r"/Users/[^/\s]+"),
    re.compile(r"/home/[^/\s]+"),
    re.compile(r"/private/var/folders/[^,\s\"']+"),
    re.compile(r"/var/folders/[^,\s\"']+"),
    re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+"),
    re.compile(r"(?i)\b[A-Z0-9_]*(?:KEY|SECRET|TOKEN|PASSWORD)[A-Z0-9_]*\s*[:=]"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
)

FORBIDDEN_PAYLOAD_MARKERS = (
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
)


@dataclass(frozen=True)
class Check:
    id: str
    description: str


CHECKS = (
    Check("local_backend_verified", "default backend is verified local_file"),
    Check("policy_boundary_present", "visualization policy keeps canonical memory in files"),
    Check("status_report_exists", "status HTML and JSON reports exist"),
    Check("viz_payload_exists", "viz summary, JSON, and NDJSON outputs exist"),
    Check("no_network_write", "default export reports no external network write"),
    Check("count_consistency", "summary count matches JSON and NDJSON rows"),
    Check("schema_allowlist", "exported event fields stay within the allowlist"),
    Check("redaction_smoke", "exported payload does not contain common secret or local path patterns"),
    Check("public_marker_scan", "exported payload does not contain private public-source markers"),
    Check("source_metadata", "summary records source metadata for events.jsonl"),
    Check("compiled_view_authority", "status JSON states reports are compiled views, not canonical memory"),
    Check("event_audit_trail", "source event log records the viz export event"),
)


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            "command failed: "
            + " ".join(cmd)
            + "\nSTDOUT:\n"
            + result.stdout
            + "\nSTDERR:\n"
            + result.stderr
        )
    return result


def load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def scaffold(root: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    run(
        [
            sys.executable,
            "scripts/scaffold_harness.py",
            "--target",
            str(target),
            "--goal",
            "Create a restartable project with local worker visibility",
            "--project-name",
            "Static Viz Smoke",
        ],
        root,
    )
    run(["./init.sh"], target)
    run(
        [
            sys.executable,
            "scripts/harnessctl.py",
            "viz-export",
            "--backend",
            "local_file",
            "--task-id",
            "VIZ-STATIC-SMOKE",
            "--trace-id",
            "trace_static_viz",
        ],
        target,
    )
    run([sys.executable, "scripts/harnessctl.py", "report"], target)


def ndjson_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in read_text(path).splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def source_events(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in read_text(path).splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"event_type": "invalid_json"})
    return rows


def has_leak(text: str) -> bool:
    return any(pattern.search(text) for pattern in LEAK_PATTERNS)


def has_forbidden_marker(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in FORBIDDEN_PAYLOAD_MARKERS)


def evaluate(target: Path) -> dict[str, Any]:
    summary_path = target / "harness" / "reports" / "viz" / "summary.json"
    events_json_path = target / "harness" / "reports" / "viz" / "events.json"
    events_ndjson_path = target / "harness" / "reports" / "viz" / "events.ndjson"
    status_html_path = target / "harness" / "reports" / "status.html"
    status_json_path = target / "harness" / "reports" / "status.json"
    source_log_path = target / "harness" / "events" / "events.jsonl"
    backend_config = load_json(target / "harness" / "viz" / "VIZ_BACKENDS.json", {})
    policy_text = read_text(target / "harness" / "shared" / "VISUALIZATION_SPEC_POLICY.md")
    summary = load_json(summary_path, {})
    status_json = load_json(status_json_path, {})
    events_json = load_json(events_json_path, [])
    events_ndjson = ndjson_rows(events_ndjson_path) if events_ndjson_path.exists() else []
    source_rows = source_events(source_log_path)
    exported_text = "\n".join(
        [
            read_text(summary_path),
            read_text(events_json_path),
            read_text(events_ndjson_path),
            read_text(status_html_path),
            read_text(status_json_path),
        ]
    )

    local_backend = {}
    for item in backend_config.get("backends", []) if isinstance(backend_config, dict) else []:
        if isinstance(item, dict) and item.get("id") == "local_file":
            local_backend = item
            break

    check_results = {
        "local_backend_verified": bool(
            backend_config.get("default_backend") == "local_file"
            and local_backend.get("status") == "VERIFIED_LOCAL"
            and local_backend.get("network_write_default") == "DENIED"
        ),
        "policy_boundary_present": "Canonical sources remain the file-backed harness artifacts" in policy_text
        and "must not become competing memory" in policy_text,
        "status_report_exists": status_html_path.exists() and status_json_path.exists(),
        "viz_payload_exists": summary_path.exists() and events_json_path.exists() and events_ndjson_path.exists(),
        "no_network_write": summary.get("external_network_write") is False,
        "count_consistency": summary.get("event_count") == len(events_json) == len(events_ndjson),
        "schema_allowlist": all(set(row).issubset(ALLOWED_EVENT_FIELDS) for row in events_json)
        and all(set(row).issubset(ALLOWED_EVENT_FIELDS) for row in events_ndjson),
        "redaction_smoke": not has_leak(exported_text),
        "public_marker_scan": not has_forbidden_marker(exported_text),
        "source_metadata": summary.get("source", {}).get("path") == "harness/events/events.jsonl"
        and summary.get("source", {}).get("status") == "present",
        "compiled_view_authority": status_json.get("authority") == "compiled_view_not_canonical_memory",
        "event_audit_trail": any(row.get("event_type") == "viz.export_created" for row in source_rows),
    }
    passed = sum(1 for value in check_results.values() if value)
    return {
        "passed": passed,
        "failed": len(CHECKS) - passed,
        "total": len(CHECKS),
        "conformance": round(passed / len(CHECKS), 3),
        "event_count": summary.get("event_count", 0),
        "source_event_count": len(source_rows),
        "checks": {
            check.id: {
                "passed": bool(check_results[check.id]),
                "description": check.description,
            }
            for check in CHECKS
        },
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="kit repository root")
    parser.add_argument("--target", default="", help="optional generated harness target")
    parser.add_argument("--keep", action="store_true")
    parser.add_argument("--check-summary", action="store_true")
    args = parser.parse_args(argv[1:])

    root = Path(args.root).resolve()
    if args.target:
        target = Path(args.target).resolve()
        temporary = False
    else:
        target = Path(tempfile.mkdtemp(prefix="eoh_static_viz_"))
        temporary = True

    try:
        scaffold(root, target)
        result = {
            "summary": evaluate(target),
            "claim_boundary": [
                "local static visualization regression guard",
                "not a hosted dashboard benchmark",
                "not a UX quality benchmark",
                "no network writes or external publishing",
            ],
        }
        if args.check_summary:
            expected = json.loads((root / "benchmarks" / "static_viz" / "expected_summary.json").read_text(encoding="utf-8"))["summary"]
            comparable = {
                key: result["summary"][key]
                for key in ["passed", "failed", "total", "conformance"]
            }
            if comparable != expected:
                print(json.dumps(result, ensure_ascii=False, indent=2))
                raise SystemExit(f"summary mismatch: expected {expected}, got {comparable}")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["summary"]["failed"] == 0 else 1
    finally:
        if temporary and not args.keep and target.exists():
            shutil.rmtree(target)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
