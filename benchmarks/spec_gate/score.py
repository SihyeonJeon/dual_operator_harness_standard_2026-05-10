#!/usr/bin/env python3
"""Compare planning-gate surfaces before production work starts.

This deterministic assay checks whether a project surface preserves the
planning runway needed before sharp/deep execution: PRD draft, anti-PRD,
candidate slice, evaluator gate, worker brief, ownership, and closure evidence.
It does not measure model intelligence or final artifact quality.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class EvidenceOption:
    paths: tuple[str, ...]
    snippets: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class Criterion:
    id: str
    description: str
    options: tuple[EvidenceOption, ...]


CRITERIA: tuple[Criterion, ...] = (
    Criterion(
        "goal_intake",
        "project goal and unknown constraints are captured before planning",
        (
            EvidenceOption(
                ("feature_list.json", "harness/shared/PROJECT_PROFILE.json"),
                (
                    ("feature_list.json", "project_goal"),
                    ("harness/shared/PROJECT_PROFILE.json", "UNKNOWN"),
                ),
            ),
            EvidenceOption(("feature_list.json",), (("feature_list.json", "project_goal"),)),
            EvidenceOption(("brief.md",), (("brief.md", "Goal:"),)),
        ),
    ),
    Criterion(
        "workstream_profile",
        "workstream and risk assumptions are written into canonical state",
        (
            EvidenceOption(
                ("harness/shared/WORKSTREAM_PROFILE.json",),
                (
                    ("harness/shared/WORKSTREAM_PROFILE.json", "detected_workstreams"),
                    ("harness/shared/WORKSTREAM_PROFILE.json", "required_loop"),
                ),
            ),
            EvidenceOption(("brief.md",), (("brief.md", "Risks"),)),
        ),
    ),
    Criterion(
        "prd_template",
        "PRD draft exists before production",
        (
            EvidenceOption(
                ("harness/spec/PRD_DRAFT.md",),
                (
                    ("harness/spec/PRD_DRAFT.md", "Acceptance Criteria"),
                    ("harness/spec/PRD_DRAFT.md", "Required Evidence"),
                ),
            ),
            EvidenceOption(("brief.md",), (("brief.md", "Acceptance Criteria"),)),
        ),
    ),
    Criterion(
        "anti_prd_template",
        "failure-mode draft exists before production",
        (
            EvidenceOption(
                ("harness/spec/ANTI_PRD.md",),
                (
                    ("harness/spec/ANTI_PRD.md", "Likely Failure Modes"),
                    ("harness/spec/ANTI_PRD.md", "Verification Gaps"),
                ),
            ),
            EvidenceOption(("brief.md",), (("brief.md", "Risks"),)),
        ),
    ),
    Criterion(
        "spec_policy",
        "policy requires planning before sharp/deep production",
        (
            EvidenceOption(
                ("harness/spec/SPEC_AUTOMATION_POLICY.md", "harness/shared/SHARP_DEEP_EXECUTION.md"),
                (
                    ("harness/spec/SPEC_AUTOMATION_POLICY.md", "Production must not start from a vague goal alone"),
                    ("harness/shared/SHARP_DEEP_EXECUTION.md", "planning"),
                ),
            ),
        ),
    ),
    Criterion(
        "candidate_slice_gate",
        "candidate slice and approval gate are represented",
        (
            EvidenceOption(
                ("harness/tasks/F0-PLANNING-RUNWAY/BLUEPRINT.md", "harness/shared/ACTIVE_SNAPSHOT.md"),
                (
                    ("harness/tasks/F0-PLANNING-RUNWAY/BLUEPRINT.md", "slice"),
                    ("harness/shared/ACTIVE_SNAPSHOT.md", "F0"),
                ),
            ),
            EvidenceOption(("tasks.md",), (("tasks.md", "build homepage"), ("tasks.md", "review layout"))),
        ),
    ),
    Criterion(
        "worker_brief_contract",
        "worker brief contains owned paths, no-touch paths, evidence, and stop rules",
        (
            EvidenceOption(
                ("harness/templates/WORKER_BRIEF.json",),
                (
                    ("harness/templates/WORKER_BRIEF.json", "owned_paths"),
                    ("harness/templates/WORKER_BRIEF.json", "no_touch_paths"),
                    ("harness/templates/WORKER_BRIEF.json", "stop_conditions"),
                ),
            ),
        ),
    ),
    Criterion(
        "part_ownership",
        "part-owner worker reuse is explicit and bounded",
        (
            EvidenceOption(
                ("harness/shared/PART_OWNERSHIP.md", "harness/shared/WORKER_SESSION_REGISTRY.json"),
                (
                    ("harness/shared/PART_OWNERSHIP.md", "same part"),
                    ("harness/shared/WORKER_SESSION_REGISTRY.json", "part_id"),
                ),
            ),
        ),
    ),
    Criterion(
        "evaluator_gate",
        "evaluator checks PRD/anti-PRD and evidence before closure",
        (
            EvidenceOption(
                ("harness/teams/evaluation/AGENT.md", "harness/shared/QUALITY_GATES.md"),
                (
                    ("harness/teams/evaluation/AGENT.md", "evaluation"),
                    ("harness/shared/QUALITY_GATES.md", "NOT-RUN"),
                ),
            ),
            EvidenceOption(("tasks.md",), (("tasks.md", "review layout"),)),
        ),
    ),
    Criterion(
        "no_production_before_f0",
        "bootstrap leaves planning runway active before production",
        (
            EvidenceOption(
                ("feature_list.json", "progress.md", "session-handoff.md"),
                (
                    ("feature_list.json", "F0-PLANNING-RUNWAY"),
                    ("progress.md", "Planning"),
                    ("session-handoff.md", "planning"),
                ),
            ),
        ),
    ),
    Criterion(
        "visibility",
        "local status and event evidence are generated",
        (
            EvidenceOption(
                ("harness/events/events.jsonl", "harness/reports/status.html", "harness/reports/status.json"),
                (
                    ("harness/events/events.jsonl", "gate.pass"),
                    ("harness/reports/status.html", "Harness"),
                ),
            ),
            EvidenceOption(("progress.md",), (("progress.md", "Progress"),)),
        ),
    ),
    Criterion(
        "operator_closure",
        "operators remain responsible for review and closure",
        (
            EvidenceOption(
                (
                    "harness/operators/codex/AGENT.md",
                    "harness/operators/claude-code/AGENT.md",
                    "harness/shared/DUAL_OPERATOR_PROTOCOL.md",
                ),
                (
                    ("harness/shared/DUAL_OPERATOR_PROTOCOL.md", "Do not force consensus"),
                    ("harness/operators/codex/AGENT.md", "operator"),
                ),
            ),
        ),
    ),
)


BASELINES: dict[str, dict[str, dict[str, str]]] = {
    "direct_session": {
        "feature_list.json": {
            "text": '{"project_goal":"Build a sunglasses boutique website","features":[{"id":"site","state":"active"}]}'
        },
        "index.html": {"text": "<main>Sunglasses boutique</main>"},
        "notes.md": {"text": "# Notes\nStarted production from the prompt.\n"},
    },
    "ad_hoc_brief": {
        "feature_list.json": {
            "text": '{"project_goal":"Build a sunglasses boutique website","features":[{"id":"site","state":"active","evidence":"manual"}]}'
        },
        "brief.md": {
            "text": "# Brief\nGoal: Build a sunglasses boutique website\nAcceptance Criteria\n- Homepage exists\nRisks\n- Unknown assets\n"
        },
        "tasks.md": {"text": "# Tasks\n- build homepage\n- review layout\n"},
        "progress.md": {"text": "# Progress\nPlanning notes exist but no gate artifact.\n"},
    },
}


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


def write_baseline(target: Path, files: dict[str, dict[str, str]]) -> None:
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    for rel, meta in files.items():
        path = target / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(meta["text"], encoding="utf-8")


def scaffold_generated(root: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    run(
        [
            sys.executable,
            "scripts/scaffold_harness.py",
            "--target",
            str(target),
            "--goal",
            "Build a sunglasses boutique website",
            "--project-name",
            "Spec Gate Smoke",
        ],
        root,
    )
    run(["./init.sh"], target)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def score_surface(surface_root: Path) -> dict[str, Any]:
    results: dict[str, Any] = {}
    passed = 0
    for criterion in CRITERIA:
        option_failures: list[dict[str, Any]] = []
        ok = False
        for option in criterion.options:
            missing_paths = [rel for rel in option.paths if not surface_root.joinpath(rel).exists()]
            missing_snippets: list[str] = []
            for rel, snippet in option.snippets:
                if snippet not in read_text(surface_root / rel):
                    missing_snippets.append(f"{rel}: {snippet}")
            option_ok = not missing_paths and not missing_snippets
            if option_ok:
                ok = True
                break
            option_failures.append({"missing_paths": missing_paths, "missing_snippets": missing_snippets})
        if ok:
            passed += 1
        results[criterion.id] = {
            "passed": ok,
            "description": criterion.description,
            "failed_options": [] if ok else option_failures,
        }
    return {
        "score": round(passed / len(CRITERIA), 3),
        "passed": passed,
        "total": len(CRITERIA),
        "criteria": results,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="kit repository root")
    parser.add_argument("--target-dir", default="", help="optional directory for generated surfaces")
    parser.add_argument("--keep", action="store_true")
    parser.add_argument("--check-summary", action="store_true")
    args = parser.parse_args(argv[1:])

    root = Path(args.root).resolve()
    if args.target_dir:
        work = Path(args.target_dir).resolve()
        if work.exists():
            shutil.rmtree(work)
        temporary = False
    else:
        work = Path(tempfile.mkdtemp(prefix="eoh_spec_gate_"))
        temporary = True
    work.mkdir(parents=True, exist_ok=True)

    try:
        surfaces: dict[str, Path] = {}
        for name, files in BASELINES.items():
            target = work / name
            write_baseline(target, files)
            surfaces[name] = target

        generated = work / "generated_harness"
        scaffold_generated(root, generated)
        surfaces["generated_harness"] = generated

        scores = {name: score_surface(path) for name, path in surfaces.items()}
        generated_score = scores["generated_harness"]
        summary = {
            "criteria": len(CRITERIA),
            "generated_scaffold": {
                "passed": generated_score["passed"],
                "failed": generated_score["total"] - generated_score["passed"],
                "total": generated_score["total"],
                "conformance": generated_score["score"],
            },
            "authored_controls": {
                name: {
                    "score": item["score"],
                    "passed": item["passed"],
                    "total": item["total"],
                }
                for name, item in scores.items()
                if name != "generated_harness"
            },
        }
        result = {
            "summary": summary,
            "scores": scores,
            "claim_boundary": [
                "deterministic planning-gate surface regression guard",
                "not a neutral tool or framework comparison",
                "not a model intelligence benchmark",
                "not a final artifact quality benchmark",
                "control surfaces are authored fixtures",
            ],
        }

        if args.check_summary:
            expected_path = root / "benchmarks" / "spec_gate" / "expected_summary.json"
            expected = json.loads(expected_path.read_text(encoding="utf-8"))["summary"]
            if summary != expected:
                print(json.dumps(result, ensure_ascii=False, indent=2))
                raise SystemExit(f"summary mismatch: expected {expected}, got {summary}")

        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    finally:
        if temporary and not args.keep and work.exists():
            shutil.rmtree(work)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
