#!/usr/bin/env python3
"""Run a local replay and recovery benchmark for generated harnesses."""

from __future__ import annotations

import argparse
import json
import shutil
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_DIR = Path(__file__).resolve().parent
DEFAULT_TASKS = BENCHMARK_DIR / "tasks.json"
DEFAULT_SUMMARY = BENCHMARK_DIR / "expected_summary.json"
DEFAULT_RUNS = 3

RECOVERY_ARTIFACTS = [
    "goal_record",
    "current_status",
    "next_action",
    "ownership_record",
    "verification_record",
    "event_log",
    "machine_state",
    "portable_recovery_command",
    "status_report",
    "rule_update_path",
]

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

HARNESS_ARTIFACT_PATHS = {
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


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def count_events(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def slug(value: str) -> str:
    safe = "".join(ch if ch.isalnum() else "_" for ch in value.lower()).strip("_")
    return safe or "task"


def make_direct_fixture(root: Path, task: dict[str, str], run_index: int) -> Path:
    target = root / "direct_transcript" / task["id"] / f"run_{run_index:02d}"
    target.mkdir(parents=True, exist_ok=True)
    target.joinpath("transcript.md").write_text(
        "\n".join(
            [
                "# Direct Agent Session Transcript",
                "",
                f"Goal: {task['goal']}",
                "",
                "Assistant started a partial answer and wrote one draft artifact.",
                "The session was interrupted before explicit state, ownership, evaluator output, event log, or restart command were written.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    target.joinpath("artifact.md").write_text(
        "# Partial Artifact\n\nA useful draft may exist, but restart state is implicit in the chat transcript.\n",
        encoding="utf-8",
    )
    return target


def make_ad_hoc_fixture(root: Path, task: dict[str, str], run_index: int) -> Path:
    target = root / "ad_hoc_loop" / task["id"] / f"run_{run_index:02d}"
    target.mkdir(parents=True, exist_ok=True)
    write_json(
        target / "task.json",
        {
            "task_id": task["id"],
            "goal": task["goal"],
            "owner": "single-agent",
            "status": "interrupted",
        },
    )
    write_json(
        target / "state.json",
        {
            "current_feature": task.get("feature", "main_delivery"),
            "current_task": "resume from partial artifact",
            "next_action": task.get("next_action", "review the draft and continue"),
            "verification_status": "not_run",
        },
    )
    target.joinpath("run.log").write_text(
        "started\npartial artifact written\ninterrupted before evaluator report\n",
        encoding="utf-8",
    )
    target.joinpath("resume.sh").write_text("#!/usr/bin/env sh\npython3 loop.py --resume\n", encoding="utf-8")
    target.joinpath("artifact.md").write_text(
        "# Partial Artifact\n\nThe loop has state files, but no shared team registry, gate report, or canonical event stream.\n",
        encoding="utf-8",
    )
    return target


def make_harness_fixture(root: Path, task: dict[str, str], run_index: int) -> Path:
    target = root / "generated_harness" / task["id"] / f"run_{run_index:02d}"
    run(
        [
            sys.executable,
            "scripts/scaffold_harness.py",
            "--target",
            str(target),
            "--goal",
            task["goal"],
            "--project-name",
            f"Replay Recovery {task['id']}",
        ],
        ROOT,
    )
    run(["./init.sh"], target)
    return target


def summarize(
    mode: str,
    task: dict[str, str],
    run_index: int,
    artifact_hits: dict[str, bool],
    fact_hits: dict[str, bool],
    event_count: int,
) -> dict[str, Any]:
    artifact_present = sum(1 for value in artifact_hits.values() if value)
    fact_present = sum(1 for value in fact_hits.values() if value)
    artifact_total = len(artifact_hits)
    fact_total = len(fact_hits)
    artifact_coverage = artifact_present / artifact_total
    fact_coverage = fact_present / fact_total
    score = round(artifact_coverage * 0.6 + fact_coverage * 0.4, 3)
    return {
        "mode": mode,
        "task_id": task["id"],
        "run_index": run_index,
        "recovery_artifacts_present": artifact_present,
        "recovery_artifacts_total": artifact_total,
        "recovery_artifact_coverage": round(artifact_coverage, 3),
        "recoverable_facts_present": fact_present,
        "recoverable_facts_total": fact_total,
        "recoverable_fact_coverage": round(fact_coverage, 3),
        "event_count": event_count,
        "status_report_present": bool(artifact_hits.get("status_report")),
        "portable_recovery_command_present": bool(artifact_hits.get("portable_recovery_command")),
        "recovery_readiness_score": score,
        "missing_artifacts": [key for key, value in artifact_hits.items() if not value],
        "missing_facts": [key for key, value in fact_hits.items() if not value],
    }


def score_direct(path: Path, task: dict[str, str], run_index: int) -> dict[str, Any]:
    artifact_hits = {name: False for name in RECOVERY_ARTIFACTS}
    artifact_hits["goal_record"] = path.joinpath("transcript.md").exists()
    fact_hits = {name: False for name in RECOVERABLE_FACTS}
    fact_hits["project_goal"] = "Goal:" in path.joinpath("transcript.md").read_text(encoding="utf-8")
    return summarize("direct_transcript", task, run_index, artifact_hits, fact_hits, event_count=0)


def score_ad_hoc(path: Path, task: dict[str, str], run_index: int) -> dict[str, Any]:
    task_state = load_json(path / "task.json")
    run_state = load_json(path / "state.json")
    artifact_hits = {name: False for name in RECOVERY_ARTIFACTS}
    artifact_hits.update(
        {
            "goal_record": path.joinpath("task.json").exists(),
            "current_status": path.joinpath("state.json").exists(),
            "next_action": bool(run_state.get("next_action")),
            "machine_state": path.joinpath("state.json").exists(),
            "portable_recovery_command": path.joinpath("resume.sh").exists(),
        }
    )
    fact_hits = {name: False for name in RECOVERABLE_FACTS}
    fact_hits.update(
        {
            "project_goal": bool(task_state.get("goal")),
            "current_feature": bool(run_state.get("current_feature")),
            "current_task": bool(run_state.get("current_task")),
            "next_action": bool(run_state.get("next_action")),
        }
    )
    return summarize("ad_hoc_loop", task, run_index, artifact_hits, fact_hits, event_count=0)


def score_harness(path: Path, task: dict[str, str], run_index: int) -> dict[str, Any]:
    artifact_hits = {
        name: path.joinpath(rel).exists()
        for name, rel in HARNESS_ARTIFACT_PATHS.items()
    }
    feature_list = load_json(path / "feature_list.json")
    latest = load_json(path / "harness" / "evals" / "results" / "latest.json")
    events = count_events(path / "harness" / "events" / "events.jsonl")
    session_handoff = (path / "session-handoff.md").read_text(encoding="utf-8")
    fact_hits = {
        "project_goal": bool(feature_list.get("project_goal")),
        "current_feature": bool(feature_list.get("features")),
        "current_task": (path / "harness" / "shared" / "ACTIVE_SNAPSHOT.md").exists(),
        "next_action": "you are operator" in session_handoff,
        "verification_status": latest.get("verdict") == "PASS",
        "event_count": events > 0,
        "report_path": (path / "harness" / "reports" / "status.html").exists(),
        "canonical_memory_path": (path / "harness" / "shared" / "RECORDS_POLICY.md").exists(),
    }
    return summarize("generated_harness", task, run_index, artifact_hits, fact_hits, event_count=events)


def run_once(root: Path, task: dict[str, str], run_index: int) -> list[dict[str, Any]]:
    direct = make_direct_fixture(root, task, run_index)
    ad_hoc = make_ad_hoc_fixture(root, task, run_index)
    harness = make_harness_fixture(root, task, run_index)
    return [
        score_direct(direct, task, run_index),
        score_ad_hoc(ad_hoc, task, run_index),
        score_harness(harness, task, run_index),
    ]


def aggregate(results: list[dict[str, Any]], task_count: int, runs_per_task: int) -> dict[str, Any]:
    modes = sorted({result["mode"] for result in results})
    summary: dict[str, Any] = {
        "task_count": task_count,
        "runs_per_task": runs_per_task,
        "total_runs_per_mode": task_count * runs_per_task,
        "modes": {},
    }
    for mode in modes:
        subset = [result for result in results if result["mode"] == mode]
        summary["modes"][mode] = {
            "mean_recovery_artifact_coverage": round(statistics.mean(result["recovery_artifact_coverage"] for result in subset), 3),
            "mean_recoverable_fact_coverage": round(statistics.mean(result["recoverable_fact_coverage"] for result in subset), 3),
            "mean_recovery_readiness_score": round(statistics.mean(result["recovery_readiness_score"] for result in subset), 3),
            "mean_event_count": round(statistics.mean(result["event_count"] for result in subset), 3),
            "status_report_rate": round(statistics.mean(1 if result["status_report_present"] else 0 for result in subset), 3),
            "portable_recovery_command_rate": round(
                statistics.mean(1 if result["portable_recovery_command_present"] else 0 for result in subset),
                3,
            ),
        }
    return summary


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tasks", type=Path, default=DEFAULT_TASKS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--runs", type=int, default=DEFAULT_RUNS)
    parser.add_argument("--check-summary", action="store_true")
    parser.add_argument("--details", action="store_true")
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args(argv[1:])

    if args.runs < 1:
        raise SystemExit("--runs must be >= 1")

    tasks = load_json(args.tasks)
    if not isinstance(tasks, list) or not tasks:
        raise SystemExit("tasks file must contain a non-empty JSON array")

    temp = Path(tempfile.mkdtemp(prefix="replay_recovery_benchmark_"))
    try:
        results: list[dict[str, Any]] = []
        for task in tasks:
            task_id = slug(str(task.get("id", "")))
            if not task_id or not task.get("goal"):
                raise SystemExit("each task must contain id and goal")
            task = {**task, "id": task_id}
            for run_index in range(1, args.runs + 1):
                results.extend(run_once(temp, task, run_index))

        summary = aggregate(results, task_count=len(tasks), runs_per_task=args.runs)
        output: dict[str, Any] = {"summary": summary}
        if args.details:
            output["details"] = results
        print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))

        if args.check_summary:
            expected = load_json(args.summary)
            if summary != expected:
                print("replay recovery summary mismatch", file=sys.stderr)
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
