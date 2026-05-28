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
    "templates/harness/shared/CURRENT_MARKET_RESEARCH_POLICY.md",
    "templates/harness/shared/CROSS_FEEDBACK_LOOP.md",
    "templates/harness/shared/CONCEPT_TRANSLATION_POLICY.md",
    "templates/harness/shared/SOFTWARE_FEEDBACK_POLICY.md",
    "templates/harness/shared/BUDGET_GOVERNANCE.md",
    "templates/harness/shared/AGENT_PROVIDER_OVERRIDES.json",
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
    ignored_parts = {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".tmp",
        ".venv",
        "__pycache__",
        "node_modules",
        "venv",
    }
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


def run_claude_hook(target: Path, payload: dict) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, ".claude/hooks/pre_tool_use_guard.py"],
        cwd=str(target),
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=False,
    )


def hook_denied(result: subprocess.CompletedProcess[str]) -> bool:
    return "permissionDecision" in result.stdout and "deny" in result.stdout


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
            "--extra-agent-surface",
            "gemini-cli",
        ],
        root,
    )
    run(["./init.sh"], target)
    run([sys.executable, "harness/mcp_server/server.py", "--root", ".", "list-tools"], target)
    overrides = load_json(target / "harness" / "shared" / "AGENT_PROVIDER_OVERRIDES.json")
    requested_surfaces = [
        entry.get("surface")
        for entry in overrides.get("requested_extra_surfaces", [])
        if isinstance(entry, dict)
    ]
    if requested_surfaces != ["gemini-cli"]:
        raise SystemExit("extra agent surface smoke did not record gemini-cli")
    if overrides.get("policy", {}).get("extra_surfaces_do_not_change_operator_parity_by_default") is not True:
        raise SystemExit("extra agent surface smoke did not preserve default operator parity")
    broad_search_guard = run_claude_hook(
        target,
        {
            "tool_name": "Bash",
            "tool_input": {"command": "rg --files"},
            "cwd": str(target),
        },
    )
    if not hook_denied(broad_search_guard):
        print(broad_search_guard.stdout, end="")
        print(broad_search_guard.stderr, end="", file=sys.stderr)
        raise SystemExit("pre_tool_use_guard did not deny uncapped rg --files")
    capped_search_guard = run_claude_hook(
        target,
        {
            "tool_name": "Bash",
            "tool_input": {"command": "rg --files | head -50"},
            "cwd": str(target),
        },
    )
    if hook_denied(capped_search_guard) or capped_search_guard.returncode != 0:
        print(capped_search_guard.stdout, end="")
        print(capped_search_guard.stderr, end="", file=sys.stderr)
        raise SystemExit("pre_tool_use_guard denied capped rg --files")
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
    edit_without_evidence_guard = run_claude_hook(
        target,
        {
            "tool_name": "Edit",
            "tool_input": {"file_path": "src/example.py"},
            "cwd": str(target),
        },
    )
    if not hook_denied(edit_without_evidence_guard):
        print(edit_without_evidence_guard.stdout, end="")
        print(edit_without_evidence_guard.stderr, end="", file=sys.stderr)
        raise SystemExit("pre_tool_use_guard did not deny code edit without integration evidence")
    run(
        [
            sys.executable,
            "scripts/harnessctl.py",
            "integration-evidence",
            "--task-id",
            "H0-LOCAL-SMOKE",
            "--integration-point",
            "src/example.py: demo_function",
            "--file-to-edit",
            "src/example.py",
            "--planned-check",
            "python3 -m py_compile src/example.py",
            "--search-summary",
            "Focused callsite smoke evidence.",
            "--rationale",
            "Exercise executable pre-edit evidence gate.",
        ],
        target,
    )
    target.joinpath("src").mkdir(exist_ok=True)
    edit_with_evidence_guard = run_claude_hook(
        target,
        {
            "tool_name": "Edit",
            "tool_input": {"file_path": "src/example.py"},
            "cwd": str(target),
        },
    )
    if hook_denied(edit_with_evidence_guard) or edit_with_evidence_guard.returncode != 0:
        print(edit_with_evidence_guard.stdout, end="")
        print(edit_with_evidence_guard.stderr, end="", file=sys.stderr)
        raise SystemExit("pre_tool_use_guard denied code edit with integration evidence")
    edit_from_subdir_guard = run_claude_hook(
        target,
        {
            "tool_name": "Edit",
            "tool_input": {"file_path": "example.py"},
            "cwd": str(target / "src"),
        },
    )
    if hook_denied(edit_from_subdir_guard) or edit_from_subdir_guard.returncode != 0:
        print(edit_from_subdir_guard.stdout, end="")
        print(edit_from_subdir_guard.stderr, end="", file=sys.stderr)
        raise SystemExit("pre_tool_use_guard did not resolve integration evidence from a subdirectory cwd")

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
    run(
        [
            sys.executable,
            "scripts/harnessctl.py",
            "current-research",
            "--task-id",
            "H0-LOCAL-SMOKE",
            "--query",
            "current comparable harness control surfaces",
            "--source",
            "local smoke fixture",
            "--alternative",
            "direct transcript",
            "--finding",
            "Current-state research artifact records planning evidence before overall plan approval.",
            "--decision-impact",
            "Keep file-backed planning evidence before production.",
        ],
        target,
    )
    run(
        [
            sys.executable,
            "scripts/harnessctl.py",
            "cross-feedback",
            "--task-id",
            "H0-LOCAL-SMOKE",
            "--producer",
            "harnessctl",
            "--reviewer",
            "evaluator",
            "--verdict",
            "PASS",
            "--feedback",
            "Executable governance smoke artifacts are independently reviewable.",
            "--evidence-path",
            "harness/tasks/H0-LOCAL-SMOKE/TASK_PACKET.json",
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
    concept_context_sample = target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "USER_FACING_CONTEXT_SAMPLE.txt"
    concept_context_sample.write_text(
        "이것은 편광 렌즈의 반사 억제 성능을 설명하는 문장입니다.\n",
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
            "harness/tasks/H0-LOCAL-SMOKE/USER_FACING_CONTEXT_SAMPLE.txt",
            "--output",
            "harness/tasks/H0-LOCAL-SMOKE/CONCEPT_CHECK_CONTEXT.json",
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
    benchmark_input = target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "BENCHMARK_OUTPUT_SAMPLE.txt"
    benchmark_input.write_text("model: Claude\nCodex and Gemini reviewed this output.\n", encoding="utf-8")
    run(
        [
            sys.executable,
            "scripts/harnessctl.py",
            "preregister-benchmark",
            "--task-id",
            "H0-LOCAL-SMOKE",
            "--benchmark-id",
            "smoke-pilot",
            "--seed",
            "20260528",
            "--task",
            "task-a",
            "--arm",
            "standalone",
            "--arm",
            "harness",
            "--metric",
            "pass_at_1",
            "--metric",
            "score_per_minute",
            "--claim-boundary",
            "smoke only",
        ],
        target,
    )
    run(
        [
            sys.executable,
            "scripts/harnessctl.py",
            "blind-redact",
            "--task-id",
            "H0-LOCAL-SMOKE",
            "--input",
            "harness/tasks/H0-LOCAL-SMOKE/BENCHMARK_OUTPUT_SAMPLE.txt",
        ],
        target,
    )
    run(
        [
            sys.executable,
            "scripts/harnessctl.py",
            "council-decision",
            "--task-id",
            "H0-LOCAL-SMOKE",
            "--decision-id",
            "smoke-decision",
            "--question",
            "Which route should the smoke use?",
            "--position",
            "codex=Use the bounded local route.",
            "--position",
            "claude=Use the bounded local route with dissent field checked.",
            "--no-material-dissent",
            "--selected-option",
            "bounded local route",
            "--evidence-path",
            "harness/tasks/H0-LOCAL-SMOKE/BENCHMARK_OUTPUT_SAMPLE.txt",
        ],
        target,
    )
    run(
        [
            sys.executable,
            "scripts/harnessctl.py",
            "recovery-evidence",
            "--task-id",
            "H0-LOCAL-SMOKE",
            "--run-log",
            "harness/tasks/H0-LOCAL-SMOKE/BENCHMARK_OUTPUT_SAMPLE.txt",
            "--exception-type",
            "SmokeOnly",
            "--runtime-seconds",
            "1",
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
        "integration_evidence.recorded",
        "current_research.completed",
        "cross_feedback.recorded",
        "concept_check.completed",
        "software_feedback.completed",
        "benchmark.preregistered",
        "benchmark.blind_redaction",
        "council_decision.recorded",
        "benchmark.recovery_evidence_packet",
    ]:
        if event_name not in events_text:
            raise SystemExit(f"{event_name} smoke event was not written")

    latest = load_json(target / "harness" / "evals" / "results" / "latest.json")
    public = load_json(target / "harness" / "evals" / "results" / "public_release.json")
    viz = load_json(target / "harness" / "reports" / "viz" / "summary.json")
    context_pack = load_json(target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "CONTEXT_PACK.json")
    integration_evidence = load_json(target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "INTEGRATION_EVIDENCE.json")
    current_research = load_json(target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "CURRENT_RESEARCH.json")
    cross_feedback = load_json(target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "CROSS_FEEDBACK.json")
    concept_check = load_json(target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "CONCEPT_CHECK.json")
    concept_check_context = load_json(target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "CONCEPT_CHECK_CONTEXT.json")
    concept_check_bad = load_json(target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "CONCEPT_CHECK_BAD.json")
    software_feedback = load_json(target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "SOFTWARE_FEEDBACK.json")
    preregistration = load_json(target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "BENCHMARK_PREREGISTRATION.json")
    blind_redaction = load_json(target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "BLIND_REDACTION.json")
    council_decision = load_json(target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "COUNCIL_DECISION_PACKET.json")
    recovery_evidence = load_json(target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "RECOVERY_EVIDENCE_PACKET.json")
    file_count = sum(1 for path in target.rglob("*") if path.is_file())
    if latest.get("verdict") != "PASS":
        raise SystemExit("golden suite did not pass")
    if public.get("verdict") != "PASS":
        raise SystemExit("public release suite did not pass")
    if viz.get("external_network_write") is not False:
        raise SystemExit("viz smoke performed or reported an external network write")
    if context_pack.get("artifact") != "context_pack":
        raise SystemExit("context-pack smoke did not write the expected artifact")
    if integration_evidence.get("artifact") != "integration_evidence" or integration_evidence.get("status") != "RECORDED":
        raise SystemExit("integration-evidence smoke did not write the expected artifact")
    if current_research.get("verdict") != "PASS":
        raise SystemExit("current-research smoke did not pass")
    if cross_feedback.get("verdict") != "PASS":
        raise SystemExit("cross-feedback smoke did not pass")
    if concept_check.get("verdict") != "PASS":
        raise SystemExit("concept-check smoke did not pass")
    if concept_check_context.get("verdict") != "PASS":
        raise SystemExit("concept-check contextual smoke over-constrained ordinary language")
    if concept_check_bad.get("verdict") != "FAIL" or concept_check_bad.get("finding_count", 0) < 1:
        raise SystemExit("concept-check negative smoke did not catch prompt wording leakage")
    if software_feedback.get("verdict") != "PASS":
        raise SystemExit("software-feedback smoke did not pass")
    if preregistration.get("artifact") != "benchmark_preregistration" or "pass_at_1" not in preregistration.get("metrics", []):
        raise SystemExit("benchmark preregistration smoke did not write expected metrics")
    if blind_redaction.get("artifact") != "blind_redaction" or not blind_redaction.get("records"):
        raise SystemExit("blind-redact smoke did not write expected records")
    redacted_path = target / blind_redaction["records"][0]["redacted_path"]
    redacted_text = redacted_path.read_text(encoding="utf-8")
    if "Claude" in redacted_text or "Codex" in redacted_text or "Gemini" in redacted_text:
        raise SystemExit("blind-redact smoke did not strip system identity")
    if council_decision.get("artifact") != "council_decision_packet" or council_decision.get("dissent_preserved") is not True:
        raise SystemExit("council-decision smoke did not preserve dissent field")
    if recovery_evidence.get("artifact") != "recovery_evidence_packet" or recovery_evidence.get("same_packet_required_for_all_recovery_arms") is not True:
        raise SystemExit("recovery-evidence smoke did not write matched packet rule")

    default_target_summary: dict[str, object] = {"status": "SKIPPED"}
    default_name = "eoh-default-path-smoke"
    default_project = root.parent / default_name
    if default_project.exists():
        shutil.rmtree(default_project)
    try:
        run(
            [
                sys.executable,
                str(root / "scripts" / "scaffold_harness.py"),
                "--project-name",
                default_name,
                "--goal",
                "default target smoke",
            ],
            root,
        )
        if not default_project.joinpath("harness", "shared", "AGENT_PROVIDER_OVERRIDES.json").exists():
            raise SystemExit("default target smoke did not create generated project at ../<project-name>")
        default_target_summary = {
            "status": "PASS",
            "target_name": default_name,
            "created_at": str(default_project),
        }
    finally:
        if default_project.exists():
            shutil.rmtree(default_project)

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
        "agent_provider_overrides": {
            "requested_extra_surfaces": requested_surfaces,
            "default_operator_parity_preserved": True,
        },
        "default_target": default_target_summary,
        "executable_governance": {
            "context_pack_sources": context_pack.get("source_count"),
            "current_research_verdict": current_research.get("verdict"),
            "cross_feedback_verdict": cross_feedback.get("verdict"),
            "concept_check_verdict": concept_check.get("verdict"),
            "concept_check_contextual_verdict": concept_check_context.get("verdict"),
            "concept_check_negative_verdict": concept_check_bad.get("verdict"),
            "software_feedback_verdict": software_feedback.get("verdict"),
            "benchmark_preregistration": preregistration.get("status"),
            "blind_redaction_records": len(blind_redaction.get("records", [])),
            "council_decision": council_decision.get("decision_id"),
            "recovery_evidence": recovery_evidence.get("status"),
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
