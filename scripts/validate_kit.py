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
    "benchmarks/replay_recovery/README.md",
    "benchmarks/replay_recovery/score.py",
    "benchmarks/replay_recovery/tasks.json",
    "benchmarks/replay_recovery/expected_summary.json",
    "benchmarks/runtime_persistence/README.md",
    "benchmarks/runtime_persistence/score.py",
    "benchmarks/runtime_persistence/expected_summary.json",
    "schemas/feature-list.schema.json",
    "schemas/eval-suite.schema.json",
    "schemas/observability-event.schema.json",
    "docs/BENCHMARK_REPORT_2026-05-26.md",
    "templates/root/init.sh",
    "templates/root/scripts/harnessctl.py",
    "templates/root/.claude/settings.json",
    "templates/root/.claude/hooks/post_tool_use_index.py",
    "templates/harness/evals/golden_suite.json",
    "templates/harness/evals/public_release_suite.json",
    "templates/harness/shared/DUAL_OPERATOR_PROTOCOL.md",
    "templates/harness/shared/SESSION_CONTINUITY.md",
    "templates/harness/shared/REGULATION_EVOLUTION.md",
    "templates/harness/shared/RECORDS_POLICY.md",
    "templates/harness/shared/MCP_TRUST.json",
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
    ignored_files = {"harness_evaluation_checklist.md", "check.md", "conv_log.md", "conversation_log.md"}
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

    latest = load_json(target / "harness" / "evals" / "results" / "latest.json")
    public = load_json(target / "harness" / "evals" / "results" / "public_release.json")
    viz = load_json(target / "harness" / "reports" / "viz" / "summary.json")
    file_count = sum(1 for path in target.rglob("*") if path.is_file())
    if latest.get("verdict") != "PASS":
        raise SystemExit("golden suite did not pass")
    if public.get("verdict") != "PASS":
        raise SystemExit("public release suite did not pass")
    if viz.get("external_network_write") is not False:
        raise SystemExit("viz smoke performed or reported an external network write")

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
            "benchmarks/replay_recovery/score.py",
            "benchmarks/runtime_persistence/score.py",
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
    recovery = run(
        [
            sys.executable,
            "benchmarks/replay_recovery/score.py",
            "--check-summary",
        ],
        root,
    )
    summary["replay_recovery_benchmark"] = json.loads(recovery.stdout)["summary"]
    if not args.skip_smoke:
        summary["smoke"] = validate_smoke(root, args)

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("PASS: public kit validation complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
