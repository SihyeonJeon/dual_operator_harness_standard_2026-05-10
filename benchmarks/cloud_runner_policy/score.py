#!/usr/bin/env python3
"""Score deterministic cloud runner policy and dry-run surfaces."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_DIR = Path(__file__).resolve().parent
DEFAULT_SUMMARY = BENCHMARK_DIR / "expected_summary.json"


DESCRIPTOR_CRITERIA = {
    "status_unverified": lambda d: d.get("status") == "UNVERIFIED",
    "allowed_tools_empty": lambda d: d.get("allowed_tools") == [],
    "network_denied": lambda d: d.get("network_default") == "DENIED",
    "budget_unknown": lambda d: d.get("budget") == "UNKNOWN",
    "audit_path_events": lambda d: d.get("audit_path") == "harness/events/events.jsonl",
    "smoke_evidence_unknown": lambda d: d.get("smoke_evidence_path") == "UNKNOWN",
    "kill_procedure_unknown": lambda d: d.get("kill_procedure") == "UNKNOWN",
    "private_overlay_location": lambda d: d.get("implementation_location") == "project_private_overlay",
    "bounded_policy_note": lambda d: "require bounded policy" in d.get("notes", ""),
    "credential_and_approval_note": lambda d: "scoped credentials" in d.get("notes", "")
    and "explicit approval" in d.get("notes", ""),
}

POLICY_TEXT_CRITERIA = {
    "remote_disabled_until_approved": (
        "harness/runtime/REMOTE_OPERATION_POLICY.md",
        ("disabled until explicitly approved and smoked",),
    ),
    "bounded_connector_shape": (
        "harness/runtime/REMOTE_OPERATION_POLICY.md",
        ("bounded connector", "file-backed harness state"),
    ),
    "required_runner_fields": (
        "harness/runtime/REMOTE_OPERATION_POLICY.md",
        ("allowed command/tool list", "budget and timeout", "stop/kill procedure", "smoke evidence"),
    ),
    "network_write_denied": (
        "harness/runtime/REMOTE_OPERATION_POLICY.md",
        ("network writes", "explicit human approval"),
    ),
    "external_viz_backend_gated": (
        "harness/runtime/REMOTE_OPERATION_POLICY.md",
        ("External visualization backends", "credential", "lifecycle records", "rollback or disable path"),
    ),
    "offline_cloud_requires_approval": (
        "harness/runtime/OFFLINE_OPERATION.md",
        ("Cloud deployment or always-on worker execution", "denied until explicitly approved"),
    ),
    "credential_lifecycle_default_denied": (
        "harness/shared/CREDENTIAL_LIFECYCLE.md",
        ("Default: no secret access", "Credentials are human-owned"),
    ),
    "credential_required_fields": (
        "harness/shared/CREDENTIAL_LIFECYCLE.md",
        ("scope:", "expires at:", "revocation trigger:", "audit event:"),
    ),
    "private_overlay_gitignore": (
        ".gitignore",
        (".env", "harness_private/", "private_overlays/", "active_cloud_credentials.json"),
    ),
}


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise SystemExit(
            "command failed: "
            + " ".join(cmd)
            + "\nstdout:\n"
            + result.stdout
            + "\nstderr:\n"
            + result.stderr
        )
    return result


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def make_generated_harness(root: Path) -> Path:
    target = root / "generated_harness"
    run(
        [
            sys.executable,
            "scripts/scaffold_harness.py",
            "--target",
            str(target),
            "--goal",
            "Prepare a bounded cloud runner policy without enabling remote execution or credentials",
            "--project-name",
            "Cloud Runner Policy Smoke",
        ],
        ROOT,
    )
    run(["./init.sh"], target)
    return target


def unsafe_descriptor() -> dict[str, Any]:
    return {
        "id": "unsafe_active_cloud_runner",
        "status": "VERIFIED",
        "surface": "remote_or_cloud",
        "allowed_tools": ["shell", "network_write"],
        "network_default": "ALLOWED",
        "budget": "unbounded",
        "audit_path": "UNKNOWN",
        "smoke_evidence_path": "UNKNOWN",
        "kill_procedure": "UNKNOWN",
        "implementation_location": "project_root",
        "notes": "unsafe active runner",
    }


def partial_descriptor() -> dict[str, Any]:
    return {
        "id": "partial_cloud_runner",
        "status": "UNVERIFIED",
        "surface": "remote_or_cloud",
        "allowed_tools": [],
        "network_default": "DENIED",
        "budget": "UNKNOWN",
        "audit_path": "harness/events/events.jsonl",
        "smoke_evidence_path": "UNKNOWN",
        "kill_procedure": "UNKNOWN",
        "implementation_location": "project_private_overlay",
        "notes": "placeholder without bounded policy or approval language",
    }


def score_descriptor(name: str, descriptor: dict[str, Any]) -> dict[str, Any]:
    checks = {
        criterion: bool(check(descriptor))
        for criterion, check in DESCRIPTOR_CRITERIA.items()
    }
    passed = sum(1 for value in checks.values() if value)
    total = len(checks)
    return {
        "name": name,
        "passed": passed,
        "failed": total - passed,
        "total": total,
        "score": round(passed / total, 3),
        "checks": checks,
    }


def score_policy_docs(harness: Path) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    for criterion, (rel, snippets) in POLICY_TEXT_CRITERIA.items():
        text = read_text(harness / rel)
        checks[criterion] = all(snippet in text for snippet in snippets)
    active_credential = harness / "harness/runtime/RUNNERS/active_cloud_credentials.json"
    checks["no_active_cloud_credentials"] = not active_credential.exists()
    passed = sum(1 for value in checks.values() if value)
    total = len(checks)
    return {
        "passed": passed,
        "failed": total - passed,
        "total": total,
        "score": round(passed / total, 3),
        "checks": checks,
    }


def compact(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "passed": result["passed"],
        "failed": result["failed"],
        "total": result["total"],
        "score": result["score"],
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--check-summary", action="store_true")
    parser.add_argument("--details", action="store_true")
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args(argv[1:])

    temp = Path(tempfile.mkdtemp(prefix="cloud_runner_policy_benchmark_"))
    try:
        harness = make_generated_harness(temp)
        generated_descriptor = load_json(harness / "harness/runtime/RUNNERS/cloud_runner.example.json")
        details = {
            "descriptor_controls": {
                "unsafe_active": score_descriptor("unsafe_active", unsafe_descriptor()),
                "partial_placeholder": score_descriptor("partial_placeholder", partial_descriptor()),
                "generated_cloud_example": score_descriptor("generated_cloud_example", generated_descriptor),
            },
            "generated_policy_docs": score_policy_docs(harness),
        }
        summary = {
            "descriptor_controls": {
                name: compact(result)
                for name, result in details["descriptor_controls"].items()
            },
            "generated_policy_docs": compact(details["generated_policy_docs"]),
        }
        output: dict[str, Any] = {
            "summary": summary,
            "claim_boundary": [
                "deterministic cloud runner policy smoke",
                "no cloud execution",
                "no credentials",
                "no remote terminal control",
                "authored controls are illustrative fixtures",
            ],
        }
        if args.details:
            output["details"] = details
        print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
        if args.check_summary:
            expected = json.loads(args.summary.read_text(encoding="utf-8"))
            if summary != expected:
                print("cloud runner policy summary mismatch", file=sys.stderr)
                print("expected:", json.dumps(expected, ensure_ascii=False, sort_keys=True), file=sys.stderr)
                print("actual:", json.dumps(summary, ensure_ascii=False, sort_keys=True), file=sys.stderr)
                return 1
        return 0
    finally:
        if args.keep:
            print(f"kept benchmark workspace at {temp}", file=sys.stderr)
        else:
            shutil.rmtree(temp)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
