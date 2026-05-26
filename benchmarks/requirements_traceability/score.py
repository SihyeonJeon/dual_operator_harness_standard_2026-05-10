#!/usr/bin/env python3
"""Trace public kit surfaces against the agreed harness requirements.

This is a repo-state assay. It checks that a generated harness contains the
public-safe operating surfaces that were agreed for this kit, and that private
account-specific surfaces are absent from the generated public harness.
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
class TextCheck:
    path: str
    snippets: tuple[str, ...]


@dataclass(frozen=True)
class Category:
    id: str
    claim_level: str
    files: tuple[str, ...]
    text: tuple[TextCheck, ...] = ()
    absent_paths: tuple[str, ...] = ()


CATEGORIES: tuple[Category, ...] = (
    Category(
        id="implementer_bootstrap",
        claim_level="implemented",
        files=(
            "@kit/AGENTS.md",
            "@kit/IMPLEMENTER.md",
            "@kit/BOOTSTRAP.md",
            "@kit/POLICY_LINTER.md",
            "AGENTS.md",
            "CLAUDE.md",
            "scripts/validate_harness.py",
            "harness/IMPLEMENTER_HOOKS.md",
            "harness/SCAFFOLDING_CHECKLIST.md",
            "harness/SCAFFOLDING_REPORT.md",
        ),
        text=(
            TextCheck("@kit/AGENTS.md", ("IMPLEMENTER.md", "BOOTSTRAP.md", "POLICY_LINTER.md")),
            TextCheck("harness/IMPLEMENTER_HOOKS.md", ("PreScaffoldGoalIntake", "PostScaffoldValidation")),
        ),
    ),
    Category(
        id="dual_operator_and_council",
        claim_level="implemented",
        files=(
            "harness/operators/claude-code/AGENT.md",
            "harness/operators/codex/AGENT.md",
            "harness/shared/DUAL_OPERATOR_PROTOCOL.md",
            "harness/shared/OPERATOR_SESSION_REGISTRY.json",
            "harness/shared/MODEL_ROUTING.json",
            "harness/shared/COUNCIL_MCP.md",
        ),
        text=(
            TextCheck("harness/shared/MODEL_ROUTING.json", ("highest_verified_available", "part_owner_resume_when_safe")),
            TextCheck("harness/shared/DUAL_OPERATOR_PROTOCOL.md", ("Non-Coercion", "human")),
        ),
    ),
    Category(
        id="worker_team_and_part_ownership",
        claim_level="implemented",
        files=(
            "harness/shared/TEAM_TOPOLOGY.md",
            "harness/shared/WORKER_SESSION_REGISTRY.json",
            "harness/shared/PART_OWNERSHIP.md",
            "harness/teams/planning/TEAM_CONTEXT.md",
            "harness/teams/design/TEAM_CONTEXT.md",
            "harness/teams/coding/TEAM_CONTEXT.md",
            "harness/teams/evaluation/TEAM_CONTEXT.md",
            "harness/templates/WORKER_BRIEF.json",
        ),
        text=(
            TextCheck("harness/shared/PART_OWNERSHIP.md", ("same part", "no-touch")),
            TextCheck("harness/templates/WORKER_BRIEF.json", ("owned_paths", "no_touch_paths")),
        ),
    ),
    Category(
        id="context_memory_and_pressure",
        claim_level="implemented",
        files=(
            "feature_list.json",
            "progress.md",
            "session-handoff.md",
            "harness/shared/CONTEXT.md",
            "harness/shared/MEMORY.md",
            "harness/shared/CONTEXT_PRESSURE.md",
            "harness/shared/SESSION_CONTINUITY.md",
            "harness/shared/FAILURE_LEDGER.md",
            "harness/shared/RULE_CHANGE_LOG.md",
            "harness/shared/RECORDS_POLICY.md",
            "harness/shared/WORKSPACE_LAYOUT.md",
        ),
        text=(
            TextCheck("harness/shared/CONTEXT_PRESSURE.md", ("Context Pack Rule", "Part-Owner Isolation")),
            TextCheck("harness/shared/RECORDS_POLICY.md", ("Canonical Project Records", "Out Of Scope In Public Kit")),
        ),
    ),
    Category(
        id="hook_lifecycle",
        claim_level="implemented",
        files=(
            ".claude/settings.json",
            ".claude/hooks/session_start_context.py",
            ".claude/hooks/pre_tool_use_guard.py",
            ".claude/hooks/post_tool_use_index.py",
            ".claude/hooks/stop_clean_state.py",
            ".claude/hooks/task_completed_gate.py",
        ),
        text=(
            TextCheck(".claude/hooks/session_start_context.py", ("SessionStart", "additionalContext")),
            TextCheck(".claude/hooks/pre_tool_use_guard.py", ("PreToolUse", "permissionDecision")),
            TextCheck(".claude/hooks/post_tool_use_index.py", ("PostToolUse", "events.jsonl")),
        ),
    ),
    Category(
        id="spec_before_execution",
        claim_level="implemented_as_policy_and_templates",
        files=(
            "harness/spec/SPEC_AUTOMATION_POLICY.md",
            "harness/spec/PRD_DRAFT.md",
            "harness/spec/ANTI_PRD.md",
            "harness/tasks/F0-PLANNING-RUNWAY/BLUEPRINT.md",
            "harness/shared/SHARP_DEEP_EXECUTION.md",
            "harness/templates/TASK_BLUEPRINT.md",
        ),
        text=(
            TextCheck("harness/spec/SPEC_AUTOMATION_POLICY.md", ("PRD draft", "anti-PRD", "approved active slice")),
            TextCheck("harness/shared/SHARP_DEEP_EXECUTION.md", ("planning runway", "sharp/deep")),
        ),
    ),
    Category(
        id="evaluation_feedback_loop",
        claim_level="implemented",
        files=(
            "harness/evals/golden_suite.json",
            "harness/evals/public_release_suite.json",
            "harness/shared/QUALITY_GATES.md",
            "harness/templates/EVALUATION_REPORT.md",
            "scripts/harnessctl.py",
            "harness/evals/results/latest.json",
            "harness/evals/results/public_release.json",
        ),
        text=(
            TextCheck("harness/shared/QUALITY_GATES.md", ("evidence", "NOT-RUN")),
            TextCheck("harness/evals/results/latest.json", ("PASS",)),
        ),
    ),
    Category(
        id="visibility_and_static_reports",
        claim_level="implemented_local_only",
        files=(
            "harness/shared/OBSERVABILITY.md",
            "harness/events/events.jsonl",
            "harness/shared/VISUALIZATION_SPEC_POLICY.md",
            "harness/viz/VIZ_BACKENDS.json",
            "harness/viz/adapters/local_file.json",
            "harness/reports/status.html",
            "harness/reports/viz/summary.json",
        ),
        text=(
            TextCheck("harness/viz/VIZ_BACKENDS.json", ("local_file", "external_backend_requires_human_selection")),
            TextCheck("harness/reports/viz/summary.json", ("external_network_write", "false")),
        ),
    ),
    Category(
        id="remote_and_credential_boundary",
        claim_level="implemented_as_policy_and_descriptors",
        files=(
            ".gitignore",
            "harness/runtime/OFFLINE_OPERATION.md",
            "harness/runtime/REMOTE_OPERATION_POLICY.md",
            "harness/runtime/RUNNERS/local_runner.json",
            "harness/runtime/RUNNERS/codex_runner.json",
            "harness/runtime/RUNNERS/claude_code_runner.json",
            "harness/runtime/RUNNERS/remote_runner.json",
            "harness/runtime/RUNNERS/cloud_runner.example.json",
            "harness/shared/CREDENTIAL_LIFECYCLE.md",
            "harness/shared/PERMISSION_POLICY.json",
        ),
        text=(
            TextCheck(".gitignore", (".env", "harness_private/", "private_overlays/", "active_cloud_credentials.json")),
            TextCheck("harness/shared/PERMISSION_POLICY.json", ("fail_closed", "network_write", "explicit_human")),
            TextCheck("harness/runtime/REMOTE_OPERATION_POLICY.md", ("UNVERIFIED", "smoke evidence")),
        ),
    ),
    Category(
        id="readonly_mcp_export",
        claim_level="implemented_reference_export",
        files=(
            "harness/shared/MCP_TRUST.json",
            "harness/mcp_server/MANIFEST.json",
            "harness/mcp_server/README.md",
            "harness/mcp_server/server.py",
        ),
        text=(
            TextCheck("harness/mcp_server/MANIFEST.json", ("search_past_decisions", "read_only")),
            TextCheck("harness/mcp_server/server.py", ("get_capability_status", "list_open_questions")),
        ),
    ),
    Category(
        id="benchmark_evidence",
        claim_level="implemented_public_fixtures",
        files=(
            "benchmarks/replay_recovery/score.py",
            "benchmarks/agentic_governance/score.py",
            "benchmarks/operational_resilience/score.py",
            "benchmarks/runtime_persistence/score.py",
            "benchmarks/date_normalization/score.py",
            "benchmarks/bilingual_readme_parity/score.py",
            "benchmarks/cloud_runner_policy/score.py",
            "docs/BENCHMARK_REPORT_2026-05-26.md",
        ),
    ),
    Category(
        id="public_private_boundary",
        claim_level="explicitly_excluded_from_public_harness",
        files=(
            "harness/shared/RECORDS_POLICY.md",
            "harness/runtime/OFFLINE_OPERATION.md",
            "harness/shared/CREDENTIAL_LIFECYCLE.md",
        ),
        text=(
            TextCheck("harness/shared/RECORDS_POLICY.md", ("This public kit does not create", "private project overlay")),
            TextCheck("harness/runtime/OFFLINE_OPERATION.md", ("Requires Network", "Control Rule")),
        ),
        absent_paths=(
            ".env",
            "harness/account_connectors",
            "harness/private_channels",
            "harness/private_memory_store",
            "harness/runtime/RUNNERS/active_cloud_credentials.json",
        ),
    ),
)


KNOWN_NON_GOALS = (
    "No live provider outage benchmark in the public suite.",
    "No live human approval latency benchmark in the public suite.",
    "No live native-review bilingual quality benchmark in the public suite.",
    "No hosted dashboard or cloud runner enabled by default.",
    "No account-specific publishing workflow in the public kit.",
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


def scaffold(root: Path, target: Path, goal: str) -> None:
    run(
        [
            sys.executable,
            "scripts/scaffold_harness.py",
            "--target",
            str(target),
            "--goal",
            goal,
            "--project-name",
            "Traceability Smoke",
        ],
        root,
    )
    run(["./init.sh"], target)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def resolve_base_and_rel(root: Path, target: Path, rel: str) -> tuple[Path, str]:
    if rel.startswith("@kit/"):
        return root, rel.removeprefix("@kit/")
    if rel.startswith(("benchmarks/", "docs/")):
        return root, rel
    return target, rel


def check_category(category: Category, root: Path, target: Path) -> dict[str, Any]:
    missing_files: list[str] = []
    missing_text: list[str] = []
    unexpected_paths: list[str] = []

    for rel in category.files:
        base, normalized = resolve_base_and_rel(root, target, rel)
        if not base.joinpath(normalized).exists():
            missing_files.append(rel)

    for item in category.text:
        base, normalized = resolve_base_and_rel(root, target, item.path)
        text = read_text(base / normalized)
        for snippet in item.snippets:
            if snippet not in text:
                missing_text.append(f"{item.path}: {snippet}")

    for rel in category.absent_paths:
        if target.joinpath(rel).exists():
            unexpected_paths.append(rel)

    passed = not missing_files and not missing_text and not unexpected_paths
    total_checks = len(category.files) + sum(len(item.snippets) for item in category.text) + len(category.absent_paths)
    failed_checks = len(missing_files) + len(missing_text) + len(unexpected_paths)
    return {
        "id": category.id,
        "claim_level": category.claim_level,
        "passed": passed,
        "checks": total_checks,
        "failed_checks": failed_checks,
        "missing_files": missing_files,
        "missing_text": missing_text,
        "unexpected_paths": unexpected_paths,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="kit repository root")
    parser.add_argument("--target", default="", help="optional generated harness target")
    parser.add_argument("--keep", action="store_true", help="keep temporary generated harness")
    parser.add_argument("--check-summary", action="store_true", help="compare summary to expected_summary.json")
    args = parser.parse_args(argv[1:])

    root = Path(args.root).resolve()
    if args.target:
        target = Path(args.target).resolve()
        if target.exists():
            shutil.rmtree(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = False
    else:
        target = Path(tempfile.mkdtemp(prefix="eoh_traceability_"))
        temporary = True

    try:
        scaffold(root, target, "Create a restartable multi-workstream project harness")
        category_results = [check_category(category, root, target) for category in CATEGORIES]
        checks = sum(item["checks"] for item in category_results)
        failed_checks = sum(item["failed_checks"] for item in category_results)
        passed_categories = sum(1 for item in category_results if item["passed"])
        summary = {
            "categories": len(category_results),
            "passed_categories": passed_categories,
            "checks": checks,
            "failed_checks": failed_checks,
            "score": round((checks - failed_checks) / checks, 3) if checks else 0.0,
            "known_non_goals": list(KNOWN_NON_GOALS),
        }
        result = {
            "summary": summary,
            "categories": category_results,
            "generated_harness": str(target if args.keep or args.target else "temporary harness removed"),
        }

        if args.check_summary:
            expected_path = root / "benchmarks" / "requirements_traceability" / "expected_summary.json"
            expected = json.loads(expected_path.read_text(encoding="utf-8"))["summary"]
            comparable = {key: summary[key] for key in expected}
            if comparable != expected:
                print(json.dumps(result, ensure_ascii=False, indent=2))
                raise SystemExit(f"summary mismatch: expected {expected}, got {comparable}")

        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if failed_checks == 0 else 1
    finally:
        if temporary and not args.keep and target.exists():
            shutil.rmtree(target)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
