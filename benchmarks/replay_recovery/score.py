#!/usr/bin/env python3
"""Score a small replay and recovery readiness fixture."""

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
DEFAULT_SUMMARY = Path(__file__).resolve().parent / "expected_summary.json"

RECOVERY_ARTIFACTS = {
    "goal_record": "feature_list.json",
    "current_status": "progress.md",
    "next_action": "session-handoff.md",
    "ownership_record": "harness/shared/WORKER_SESSION_REGISTRY.json",
    "verification_record": "harness/evals/results/latest.json",
    "event_log": "harness/events/events.jsonl",
    "machine_state": "feature_list.json",
    "portable_recovery_command": "init.sh",
    "status_report": "harness/reports/status.html",
    "rule_update_path": "harness/shared/RULE_CHANGE_LOG.md",
}

RECOVERABLE_FACTS = [
    "project_goal",
    "current_feature",
    "current_task",
    "next_action",
    "verification_status",
    "event_count",
    "report_path",
    "canonical_memory_path",
]


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


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def count_events(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def make_direct_fixture(root: Path) -> Path:
    direct = root / "direct_session"
    direct.mkdir(parents=True, exist_ok=True)
    direct.joinpath("transcript.md").write_text(
        "\n".join(
            [
                "# Direct Agent Session Transcript",
                "",
                "User prompt: build a small agent project handoff plan",
                "",
                "The session was interrupted after a partial artifact.",
                "No separate task state, event log, evaluator verdict, or restart command was written.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    direct.joinpath("artifact.md").write_text(
        "# Partial Artifact\n\nA draft exists, but restart state is implicit in the transcript.\n",
        encoding="utf-8",
    )
    return direct


def make_harness_fixture(root: Path, goal: str) -> Path:
    target = root / "generated_harness"
    run(
        [
            sys.executable,
            "scripts/scaffold_harness.py",
            "--target",
            str(target),
            "--goal",
            goal,
            "--project-name",
            "Recovery Fixture",
        ],
        ROOT,
    )
    run(["./init.sh"], target)
    return target


def score_direct(path: Path) -> dict[str, Any]:
    artifact_hits = {
        "goal_record": path.joinpath("transcript.md").exists(),
        "current_status": False,
        "next_action": False,
        "ownership_record": False,
        "verification_record": False,
        "event_log": False,
        "machine_state": False,
        "portable_recovery_command": False,
        "status_report": False,
        "rule_update_path": False,
    }
    fact_hits = {
        "project_goal": True,
        "current_feature": False,
        "current_task": False,
        "next_action": False,
        "verification_status": False,
        "event_count": False,
        "report_path": False,
        "canonical_memory_path": False,
    }
    return summarize("direct_session", artifact_hits, fact_hits, event_count=0)


def score_harness(path: Path) -> dict[str, Any]:
    artifact_hits = {
        name: path.joinpath(rel).exists()
        for name, rel in RECOVERY_ARTIFACTS.items()
    }
    feature_list = read_json(path / "feature_list.json")
    latest = read_json(path / "harness" / "evals" / "results" / "latest.json")
    events = count_events(path / "harness" / "events" / "events.jsonl")
    fact_hits = {
        "project_goal": bool(feature_list.get("project_goal")),
        "current_feature": bool(feature_list.get("features")),
        "current_task": (path / "harness" / "shared" / "ACTIVE_SNAPSHOT.md").exists(),
        "next_action": "you are operator" in (path / "session-handoff.md").read_text(encoding="utf-8"),
        "verification_status": latest.get("verdict") == "PASS",
        "event_count": events > 0,
        "report_path": (path / "harness" / "reports" / "status.html").exists(),
        "canonical_memory_path": (path / "harness" / "shared" / "RECORDS_POLICY.md").exists(),
    }
    return summarize("generated_harness", artifact_hits, fact_hits, event_count=events)


def summarize(name: str, artifact_hits: dict[str, bool], fact_hits: dict[str, bool], event_count: int) -> dict[str, Any]:
    artifact_present = sum(1 for value in artifact_hits.values() if value)
    fact_present = sum(1 for value in fact_hits.values() if value)
    artifact_total = len(artifact_hits)
    fact_total = len(fact_hits)
    score = round((artifact_present / artifact_total) * 0.6 + (fact_present / fact_total) * 0.4, 3)
    return {
        "name": name,
        "recovery_artifacts_present": artifact_present,
        "recovery_artifacts_total": artifact_total,
        "recoverable_facts_present": fact_present,
        "recoverable_facts_total": fact_total,
        "event_count": event_count,
        "recovery_readiness_score": score,
        "missing_artifacts": [key for key, value in artifact_hits.items() if not value],
        "missing_facts": [key for key, value in fact_hits.items() if not value],
    }


def compact(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "recovery_artifacts": f"{result['recovery_artifacts_present']}/{result['recovery_artifacts_total']}",
        "recoverable_facts": f"{result['recoverable_facts_present']}/{result['recoverable_facts_total']}",
        "event_count": result["event_count"],
        "recovery_readiness_score": result["recovery_readiness_score"],
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--goal", default="Build a small agent project handoff plan")
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--check-summary", action="store_true")
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args(argv[1:])

    temp = Path(tempfile.mkdtemp(prefix="replay_recovery_fixture_"))
    try:
        direct = make_direct_fixture(temp)
        harness = make_harness_fixture(temp, args.goal)
        full = {
            "direct_session": score_direct(direct),
            "generated_harness": score_harness(harness),
        }
        result = {name: compact(value) for name, value in full.items()}
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        if args.check_summary:
            expected = json.loads(args.summary.read_text(encoding="utf-8"))
            if result != expected:
                print("replay recovery summary mismatch", file=sys.stderr)
                print("expected:", json.dumps(expected, ensure_ascii=False, sort_keys=True), file=sys.stderr)
                print("actual:", json.dumps(result, ensure_ascii=False, sort_keys=True), file=sys.stderr)
                return 1
        return 0
    finally:
        if args.keep:
            print(f"kept fixture at {temp}", file=sys.stderr)
        else:
            shutil.rmtree(temp)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
