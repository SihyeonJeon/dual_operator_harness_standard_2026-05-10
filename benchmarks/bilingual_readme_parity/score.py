#!/usr/bin/env python3
"""Score deterministic bilingual README parity for generated harnesses."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_DIR = Path(__file__).resolve().parent
DEFAULT_SUMMARY = BENCHMARK_DIR / "expected_summary.json"
PROJECT_GOAL = "Create a procurement decision matrix with evidence, tradeoffs, and operator handoff"


@dataclass(frozen=True)
class Criterion:
    id: str
    description: str
    check: Callable[[dict[str, str]], bool]


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


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def has_all(text: str, snippets: tuple[str, ...]) -> bool:
    return all(snippet in text for snippet in snippets)


def split_sections(text: str) -> dict[str, str]:
    korean = ""
    english = ""
    if "## 한국어" in text:
        after_ko = text.split("## 한국어", 1)[1]
        korean = after_ko.split("## English", 1)[0] if "## English" in after_ko else after_ko
    if "## English" in text:
        english = text.split("## English", 1)[1]
    return {"all": text, "ko": korean, "en": english}


def both(sections: dict[str, str], snippets: tuple[str, ...]) -> bool:
    return has_all(sections["ko"], snippets) and has_all(sections["en"], snippets)


PRIVATE_MARKERS = (
    "thr" + "eads",
    "draft" + "_queue",
    "private" + "_memory_store",
    "active" + "_cloud_credentials",
    "lance" + "db",
    "ku" + "zu",
)


CRITERIA: tuple[Criterion, ...] = (
    Criterion("korean_section", "Korean section exists", lambda s: bool(s["ko"].strip())),
    Criterion("english_section", "English section exists", lambda s: bool(s["en"].strip())),
    Criterion("goal_echo", "project goal is present in both sections", lambda s: both(s, (PROJECT_GOAL,))),
    Criterion(
        "start_commands",
        "bootstrap, validator, report, and eval commands are present in both sections",
        lambda s: both(s, ("./init.sh", "validate_harness.py", "harnessctl.py report", "harnessctl.py eval-run")),
    ),
    Criterion("operator_entry", "operator entry phrase is present in both sections", lambda s: both(s, ("you are operator",))),
    Criterion(
        "operator_worker_roles",
        "operator and worker role vocabulary is present in both sections",
        lambda s: both(s, ("Codex", "Claude Code", "operator", "worker")),
    ),
    Criterion(
        "planning_and_slice",
        "planning runway and sharp deep slice policy are present in both sections",
        lambda s: both(s, ("planning runway", "sharp deep slice")),
    ),
    Criterion(
        "part_owner_reuse",
        "same-part worker session reuse is present in both sections",
        lambda s: both(s, ("part owner session same part reuse",)),
    ),
    Criterion(
        "records_policy",
        "canonical shared context and records policy are present in both sections",
        lambda s: both(s, ("shared context", "team context", "RECORDS_POLICY.md")),
    ),
    Criterion(
        "visualization_boundary",
        "visualization spec, local events, and status HTML are present in both sections",
        lambda s: both(s, ("VISUALIZATION_SPEC.md", "events jsonl", "status html")),
    ),
    Criterion(
        "mcp_remote_boundary",
        "MCP read-only and remote denial policy are present in both sections",
        lambda s: both(s, ("MCP read only", "remote mobile cloud denied by default")),
    ),
    Criterion(
        "file_inventory",
        "core generated files are listed in both sections",
        lambda s: both(s, ("AGENTS.md", "feature_list.json", "harness/evals", "harness/mcp_server")),
    ),
    Criterion(
        "public_private_boundary",
        "public README states no external posting scaffold in both sections",
        lambda s: both(s, ("public kit no external posting scaffold",)),
    ),
    Criterion(
        "private_marker_absence",
        "private account-specific markers are absent",
        lambda s: not any(marker in s["all"].lower() for marker in PRIVATE_MARKERS),
    ),
)


def make_korean_only(root: Path) -> Path:
    target = root / "korean_only"
    target.mkdir(parents=True, exist_ok=True)
    target.joinpath("README.md").write_text(
        "\n".join(
            [
                "# Korean Only",
                "",
                "## 한국어",
                "",
                "목표",
                "",
                f"```text\n{PROJECT_GOAL}\n```",
                "",
                "시작",
                "",
                "```sh\n./init.sh\n```",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return target / "README.md"


def make_bilingual_summary(root: Path) -> Path:
    target = root / "bilingual_summary"
    target.mkdir(parents=True, exist_ok=True)
    target.joinpath("README.md").write_text(
        "\n".join(
            [
                "# Bilingual Summary",
                "",
                "## 한국어",
                "",
                f"목표 {PROJECT_GOAL}",
                "",
                "시작 ./init.sh",
                "",
                "operator 진입 you are operator",
                "",
                "shared context 기록",
                "",
                "## English",
                "",
                f"Goal {PROJECT_GOAL}",
                "",
                "Start ./init.sh",
                "",
                "Operator entry you are operator",
                "",
                "shared context records",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return target / "README.md"


def make_generated_harness(root: Path) -> Path:
    target = root / "generated_harness"
    run(
        [
            sys.executable,
            "scripts/scaffold_harness.py",
            "--target",
            str(target),
            "--goal",
            PROJECT_GOAL,
            "--project-name",
            "Bilingual Parity Smoke",
        ],
        ROOT,
    )
    run(["./init.sh"], target)
    return target / "README.md"


def score_readme(name: str, path: Path) -> dict[str, Any]:
    sections = split_sections(path.read_text(encoding="utf-8"))
    checks: dict[str, dict[str, Any]] = {}
    passed = 0
    for criterion in CRITERIA:
        ok = criterion.check(sections)
        if ok:
            passed += 1
        checks[criterion.id] = {"passed": ok, "description": criterion.description}
    total = len(CRITERIA)
    return {
        "name": name,
        "passed": passed,
        "failed": total - passed,
        "total": total,
        "parity_score": round(passed / total, 3),
        "checks": checks,
    }


def compact(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "passed": result["passed"],
        "failed": result["failed"],
        "total": result["total"],
        "parity_score": result["parity_score"],
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--check-summary", action="store_true")
    parser.add_argument("--details", action="store_true")
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args(argv[1:])

    temp = Path(tempfile.mkdtemp(prefix="bilingual_readme_parity_benchmark_"))
    try:
        results = {
            "korean_only": score_readme("korean_only", make_korean_only(temp)),
            "bilingual_summary": score_readme("bilingual_summary", make_bilingual_summary(temp)),
            "generated_harness": score_readme("generated_harness", make_generated_harness(temp)),
        }
        summary = {name: compact(result) for name, result in results.items()}
        output: dict[str, Any] = {
            "summary": summary,
            "claim_boundary": [
                "deterministic bilingual README parity guard",
                "not a native fluency benchmark",
                "not a translation quality benchmark",
                "authored controls are illustrative fixtures",
            ],
        }
        if args.details:
            output["details"] = results
        print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
        if args.check_summary:
            expected = json.loads(args.summary.read_text(encoding="utf-8"))
            if summary != expected:
                print("bilingual quality summary mismatch", file=sys.stderr)
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
