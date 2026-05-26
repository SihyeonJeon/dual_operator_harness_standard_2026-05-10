#!/usr/bin/env python3
"""Validate this public kit and a generated smoke harness."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT_REQUIRED = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "AGENTS.md",
    "manifest.json",
    "IMPLEMENTER.md",
    "BOOTSTRAP.md",
    "SPEC.md",
    "POLICY_LINTER.md",
    "scripts/scaffold_harness.py",
    "scripts/validate_harness.py",
    "scripts/implementer_hooks.py",
    ".github/workflows/ci.yml",
    "benchmarks/date_normalization/README.md",
    "benchmarks/date_normalization/cases.jsonl",
    "benchmarks/date_normalization/score.py",
    "benchmarks/date_normalization/expected_summary.json",
    "benchmarks/date_normalization/predictions/codex_goal.jsonl",
    "benchmarks/date_normalization/predictions/harness_first_pass.jsonl",
    "benchmarks/date_normalization/predictions/harness_feedback_loop.jsonl",
    "benchmarks/agentic_governance/README.md",
    "benchmarks/agentic_governance/score.py",
    "benchmarks/agentic_governance/sources.json",
    "benchmarks/agentic_governance/expected_summary.json",
    "benchmarks/operational_resilience/README.md",
    "benchmarks/operational_resilience/score.py",
    "benchmarks/operational_resilience/expected_summary.json",
    "benchmarks/replay_recovery/README.md",
    "benchmarks/replay_recovery/score.py",
    "benchmarks/replay_recovery/tasks.json",
    "benchmarks/replay_recovery/expected_summary.json",
    "benchmarks/bilingual_readme_parity/README.md",
    "benchmarks/bilingual_readme_parity/score.py",
    "benchmarks/bilingual_readme_parity/expected_summary.json",
    "benchmarks/cloud_runner_policy/README.md",
    "benchmarks/cloud_runner_policy/score.py",
    "benchmarks/cloud_runner_policy/expected_summary.json",
    "benchmarks/runtime_persistence/README.md",
    "benchmarks/runtime_persistence/score.py",
    "benchmarks/runtime_persistence/expected_summary.json",
    "benchmarks/spec_gate/README.md",
    "benchmarks/spec_gate/score.py",
    "benchmarks/spec_gate/expected_summary.json",
    "benchmarks/static_viz/README.md",
    "benchmarks/static_viz/score.py",
    "benchmarks/static_viz/expected_summary.json",
    "benchmarks/requirements_traceability/README.md",
    "benchmarks/requirements_traceability/score.py",
    "benchmarks/requirements_traceability/expected_summary.json",
    "schemas/feature-list.schema.json",
    "schemas/eval-suite.schema.json",
    "schemas/budget.schema.json",
    "schemas/connector-config.schema.json",
    "schemas/observability-event.schema.json",
    "docs/BENCHMARK_REPORT_2026-05-26.md",
    "docs/BENCHMARKS.md",
    "docs/PHASE2_BENCHMARK_ROADMAP.md",
    "docs/README.md",
    "docs/REQUIREMENT_TRACEABILITY_2026-05-26.md",
    "templates/root/init.sh",
    "templates/root/.gitignore",
    "templates/root/scripts/harnessctl.py",
    "templates/root/.claude/settings.json",
    "templates/root/.claude/hooks/post_tool_use_index.py",
    "templates/harness/evals/golden_suite.json",
    "templates/harness/evals/public_release_suite.json",
    "templates/harness/shared/DUAL_OPERATOR_PROTOCOL.md",
    "templates/harness/shared/SESSION_CONTINUITY.md",
    "templates/harness/shared/REGULATION_EVOLUTION.md",
    "templates/harness/shared/AGENT_COMMUNICATION.md",
    "templates/harness/shared/CONCEPT_TRANSLATION_POLICY.md",
    "templates/harness/shared/SOFTWARE_FEEDBACK_POLICY.md",
    "templates/harness/shared/BUDGET_GOVERNANCE.md",
    "templates/harness/shared/RECORDS_POLICY.md",
    "templates/harness/shared/MCP_TRUST.json",
    "templates/harness/runtime/CONNECTORS/README.md",
    "templates/harness/runtime/CONNECTORS/discord_approval.example.json",
    "templates/harness/templates/BUDGET.json",
]

FORBIDDEN_PUBLIC_MARKERS = [
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
    "sections" + "/",
    "split" + "_harness",
    "demo" + "_runs",
]

TEXT_SUFFIXES = {
    ".md",
    ".json",
    ".jsonl",
    ".py",
    ".sh",
    ".html",
    ".txt",
    ".yml",
    ".yaml",
}


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    printable = " ".join(cmd)
    print(f"$ {printable}")
    result = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True, check=False)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode != 0:
        raise SystemExit(f"command failed: {printable}")
    return result


def parse_json_files(root: Path) -> int:
    count = 0
    for path in sorted([root / "manifest.json", *root.glob("schemas/*.json"), *root.glob("templates/**/*.json"), *root.glob("templates/**/*.jsonl")]):
        if path.suffix == ".jsonl":
            for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if line.strip():
                    json.loads(line)
                    count += 1
            continue
        json.loads(path.read_text(encoding="utf-8"))
        count += 1
    return count


def scan_public_markers(root: Path) -> list[str]:
    findings: list[str] = []
    ignored_parts = {".git", "__pycache__", "node_modules"}
    ignored_files = {"harness_evaluation_checklist.md", "check.md", "conv_log.md", "convlog.md", "conversation_log.md"}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name in ignored_files or any(part in ignored_parts for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for marker in FORBIDDEN_PUBLIC_MARKERS:
            if marker in text:
                findings.append(f"{path.relative_to(root)} contains {marker}")
    return findings


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_smoke(root: Path, args: argparse.Namespace) -> dict[str, object]:
    target = Path(args.target) if args.target else Path(tempfile.mkdtemp(prefix="easy_orchestration_harness_smoke_"))
    if target.exists() and args.target:
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)

    run(
        [
            sys.executable,
            "scripts/scaffold_harness.py",
            "--target",
            str(target),
            "--goal",
            args.goal,
            "--project-name",
            "Public Kit Smoke",
        ],
        root,
    )
    run(["./init.sh"], target)
    run([sys.executable, "harness/mcp_server/server.py", "--root", ".", "list-tools"], target)
    budget_result = subprocess.run(
        [
            sys.executable,
            "scripts/harnessctl.py",
            "budget-check",
            "--task-id",
            "F0-PLANNING-RUNWAY",
            "--time-elapsed-minutes",
            "181",
        ],
        cwd=str(target),
        text=True,
        capture_output=True,
        check=False,
    )
    if budget_result.returncode != 3:
        print(budget_result.stdout, end="")
        print(budget_result.stderr, end="", file=sys.stderr)
        raise SystemExit("budget-check smoke did not return kill-required exit code")

    run(
        [
            sys.executable,
            "scripts/harnessctl.py",
            "context-pack",
            "--task-id",
            "H0-LOCAL-SMOKE",
            "--software",
        ],
        target,
    )
    run(
        [
            sys.executable,
            "scripts/harnessctl.py",
            "model-route",
            "--task-id",
            "H0-LOCAL-SMOKE",
            "--role",
            "worker",
            "--task-difficulty",
            "routine",
            "--simple",
            "--output",
            "harness/tasks/H0-LOCAL-SMOKE/MODEL_ROUTE.json",
        ],
        target,
    )
    run(
        [
            sys.executable,
            "scripts/harnessctl.py",
            "worker-brief",
            "--task-id",
            "H0-LOCAL-SMOKE",
            "--part-id",
            "local-control-surface",
            "--owned-path",
            "scripts/harnessctl.py",
            "--no-touch-path",
            ".env",
            "--success-criterion",
            "local control surface smoke passes",
            "--evidence-command",
            "python3 scripts/harnessctl.py validate",
            "--simple",
        ],
        target,
    )
    run(
        [
            sys.executable,
            "scripts/harnessctl.py",
            "task-packet",
            "--task-id",
            "H0-LOCAL-SMOKE",
            "--part-id",
            "local-control-surface",
            "--sender",
            "harnessctl",
            "--receiver",
            "operator",
            "--intent",
            "handoff",
            "--summary",
            "Executable governance smoke artifacts are ready.",
            "--evidence-path",
            "harness/tasks/H0-LOCAL-SMOKE/CONTEXT_PACK.json",
            "--evidence-path",
            "harness/tasks/H0-LOCAL-SMOKE/WORKER_BRIEF.json",
        ],
        target,
    )
    concept_sample = target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "USER_FACING_SAMPLE.txt"
    concept_sample.write_text(
        "Noon Archive\nPolarized frames for clear streets, long drives, and bright weekends.\n",
        encoding="utf-8",
    )
    run(
        [
            sys.executable,
            "scripts/harnessctl.py",
            "concept-check",
            "--task-id",
            "H0-LOCAL-SMOKE",
            "--artifact-path",
            "harness/tasks/H0-LOCAL-SMOKE/USER_FACING_SAMPLE.txt",
            "--forbidden-phrase",
            "선글라스 파는 웹사이트",
        ],
        target,
    )
    concept_bad_sample = target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "USER_FACING_BAD_SAMPLE.txt"
    concept_bad_sample.write_text(
        "이것은 선글라스 파는 웹사이트입니다.\n",
        encoding="utf-8",
    )
    run(
        [
            sys.executable,
            "scripts/harnessctl.py",
            "concept-check",
            "--task-id",
            "H0-LOCAL-SMOKE",
            "--artifact-path",
            "harness/tasks/H0-LOCAL-SMOKE/USER_FACING_BAD_SAMPLE.txt",
            "--allow-findings",
            "--output",
            "harness/tasks/H0-LOCAL-SMOKE/CONCEPT_CHECK_BAD.json",
        ],
        target,
    )
    run(
        [
            sys.executable,
            "scripts/harnessctl.py",
            "software-feedback",
            "--task-id",
            "H0-LOCAL-SMOKE",
            "--lint-command",
            "python3 -m py_compile scripts/harnessctl.py",
            "--smoke-command",
            "python3 scripts/harnessctl.py validate",
        ],
        target,
    )
    events_text = (target / "harness" / "events" / "events.jsonl").read_text(encoding="utf-8")
    if "budget.kill_required" not in events_text or "budget.escalation_required" not in events_text:
        raise SystemExit("budget-check smoke did not write kill and escalation events")
    for event_name in [
        "context_pack.created",
        "model_route.selected",
        "worker_brief.created",
        "task_packet.created",
        "concept_check.completed",
        "software_feedback.completed",
    ]:
        if event_name not in events_text:
            raise SystemExit(f"{event_name} smoke event was not written")

    latest = load_json(target / "harness" / "evals" / "results" / "latest.json")
    public = load_json(target / "harness" / "evals" / "results" / "public_release.json")
    viz = load_json(target / "harness" / "reports" / "viz" / "summary.json")
    context_pack = load_json(target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "CONTEXT_PACK.json")
    concept_check = load_json(target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "CONCEPT_CHECK.json")
    concept_check_bad = load_json(target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "CONCEPT_CHECK_BAD.json")
    software_feedback = load_json(target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "SOFTWARE_FEEDBACK.json")
    file_count = sum(1 for path in target.rglob("*") if path.is_file())
    if latest.get("verdict") != "PASS":
        raise SystemExit("golden suite did not pass")
    if public.get("verdict") != "PASS":
        raise SystemExit("public release suite did not pass")
    if viz.get("external_network_write") is not False:
        raise SystemExit("viz smoke performed or reported an external network write")
    if context_pack.get("artifact") != "context_pack":
        raise SystemExit("context-pack smoke did not write the expected artifact")
    if concept_check.get("verdict") != "PASS":
        raise SystemExit("concept-check smoke did not pass")
    if concept_check_bad.get("verdict") != "FAIL" or concept_check_bad.get("finding_count", 0) < 1:
        raise SystemExit("concept-check negative smoke did not catch prompt wording leakage")
    if software_feedback.get("verdict") != "PASS":
        raise SystemExit("software-feedback smoke did not pass")

    summary = {
        "target": str(target),
        "file_count": file_count,
        "golden": {
            "case_count": latest.get("case_count"),
            "passed": latest.get("passed"),
            "failed": latest.get("failed"),
            "not_run": latest.get("not_run"),
        },
        "public_release": {
            "case_count": public.get("case_count"),
            "passed": public.get("passed"),
            "failed": public.get("failed"),
            "not_run": public.get("not_run"),
        },
        "viz": {
            "backend": viz.get("backend"),
            "status": viz.get("status"),
            "event_count": viz.get("event_count"),
            "external_network_write": viz.get("external_network_write"),
        },
        "budget": {
            "kill_exit_code": budget_result.returncode,
            "kill_event": "budget.kill_required",
            "escalation_event": "budget.escalation_required",
        },
        "executable_governance": {
            "context_pack_sources": context_pack.get("source_count"),
            "concept_check_verdict": concept_check.get("verdict"),
            "concept_check_negative_verdict": concept_check_bad.get("verdict"),
            "software_feedback_verdict": software_feedback.get("verdict"),
            "task_packet": "harness/tasks/H0-LOCAL-SMOKE/TASK_PACKET.json",
            "worker_brief": "harness/tasks/H0-LOCAL-SMOKE/WORKER_BRIEF.json",
        },
    }
    if not args.keep and not args.target:
        shutil.rmtree(target)
        summary["target"] = "removed temporary smoke directory"
    return summary


def validate_benchmark(root: Path) -> dict[str, object]:
    result = run(
        [
            sys.executable,
            "benchmarks/date_normalization/score.py",
            "--all",
            "--check-summary",
        ],
        root,
    )
    return json.loads(result.stdout)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="public kit root")
    parser.add_argument("--goal", default="선글라스 파는 웹사이트 만들어 줘")
    parser.add_argument("--target", default="", help="optional smoke target path")
    parser.add_argument("--skip-smoke", action="store_true")
    parser.add_argument("--keep", action="store_true", help="keep temporary smoke target")
    args = parser.parse_args(argv[1:])

    root = Path(args.root).resolve()
    missing = [rel for rel in ROOT_REQUIRED if not root.joinpath(rel).exists()]
    if missing:
        for rel in missing:
            print(f"ERROR missing required kit file: {rel}", file=sys.stderr)
        return 1

    json_count = parse_json_files(root)
    findings = scan_public_markers(root)
    if findings:
        for finding in findings:
            print(f"ERROR public marker finding: {finding}", file=sys.stderr)
        return 1

    run(
        [
            sys.executable,
            "-m",
            "py_compile",
            "scripts/scaffold_harness.py",
            "scripts/validate_harness.py",
            "scripts/implementer_hooks.py",
            "benchmarks/date_normalization/score.py",
            "benchmarks/agentic_governance/score.py",
            "benchmarks/operational_resilience/score.py",
            "benchmarks/replay_recovery/score.py",
            "benchmarks/bilingual_readme_parity/score.py",
            "benchmarks/cloud_runner_policy/score.py",
            "benchmarks/runtime_persistence/score.py",
            "benchmarks/spec_gate/score.py",
            "benchmarks/static_viz/score.py",
            "benchmarks/requirements_traceability/score.py",
            "templates/root/scripts/harnessctl.py",
            "templates/root/.claude/hooks/post_tool_use_index.py",
        ],
        root,
    )

    summary: dict[str, object] = {
        "kit_root": str(root),
        "required_files": len(ROOT_REQUIRED),
        "json_artifacts_checked": json_count,
        "public_marker_scan": "PASS",
    }
    summary["date_normalization_benchmark"] = validate_benchmark(root)
    governance = run(
        [
            sys.executable,
            "benchmarks/agentic_governance/score.py",
            "--check-summary",
        ],
        root,
    )
    summary["agentic_governance_benchmark"] = json.loads(governance.stdout)["summary"]
    resilience = run(
        [
            sys.executable,
            "benchmarks/operational_resilience/score.py",
            "--check-summary",
        ],
        root,
    )
    summary["operational_resilience_benchmark"] = json.loads(resilience.stdout)["summary"]
    recovery = run(
        [
            sys.executable,
            "benchmarks/replay_recovery/score.py",
            "--check-summary",
        ],
        root,
    )
    summary["replay_recovery_benchmark"] = json.loads(recovery.stdout)["summary"]
    bilingual = run(
        [
            sys.executable,
            "benchmarks/bilingual_readme_parity/score.py",
            "--check-summary",
        ],
        root,
    )
    summary["bilingual_readme_parity_guard"] = json.loads(bilingual.stdout)["summary"]
    cloud_runner = run(
        [
            sys.executable,
            "benchmarks/cloud_runner_policy/score.py",
            "--check-summary",
        ],
        root,
    )
    summary["cloud_runner_policy_smoke"] = json.loads(cloud_runner.stdout)["summary"]
    traceability = run(
        [
            sys.executable,
            "benchmarks/requirements_traceability/score.py",
            "--check-summary",
        ],
        root,
    )
    summary["requirements_traceability_assay"] = json.loads(traceability.stdout)["summary"]
    spec_gate = run(
        [
            sys.executable,
            "benchmarks/spec_gate/score.py",
            "--check-summary",
        ],
        root,
    )
    summary["spec_gate_assay"] = json.loads(spec_gate.stdout)["summary"]
    static_viz = run(
        [
            sys.executable,
            "benchmarks/static_viz/score.py",
            "--check-summary",
        ],
        root,
    )
    summary["static_viz_guard"] = json.loads(static_viz.stdout)["summary"]
    if not args.skip_smoke:
        summary["smoke"] = validate_smoke(root, args)

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("PASS: public kit validation complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
