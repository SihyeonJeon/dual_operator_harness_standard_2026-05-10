#!/usr/bin/env python3
"""Score deterministic provider failover and approval-gate policies."""

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

FAILOVER_SCENARIOS = [
    {
        "id": "routine_primary_healthy",
        "difficulty": "routine",
        "primary_available": True,
        "requires_independent_check": False,
    },
    {
        "id": "routine_primary_down",
        "difficulty": "routine",
        "primary_available": False,
        "requires_independent_check": False,
    },
    {
        "id": "standard_primary_healthy",
        "difficulty": "standard",
        "primary_available": True,
        "requires_independent_check": False,
    },
    {
        "id": "standard_primary_down",
        "difficulty": "standard",
        "primary_available": False,
        "requires_independent_check": False,
    },
    {
        "id": "complex_independent_check",
        "difficulty": "complex",
        "primary_available": True,
        "requires_independent_check": True,
    },
    {
        "id": "complex_primary_down",
        "difficulty": "complex",
        "primary_available": False,
        "requires_independent_check": True,
    },
    {
        "id": "evaluation_vendor_split",
        "difficulty": "evaluation",
        "primary_available": True,
        "requires_independent_check": True,
    },
    {
        "id": "evaluation_primary_down",
        "difficulty": "evaluation",
        "primary_available": False,
        "requires_independent_check": True,
    },
]

APPROVAL_SCENARIOS = [
    {"id": "read_fs", "action_class": "read_fs", "expected": "allow"},
    {"id": "write_owned", "action_class": "write_fs", "expected": "scoped"},
    {"id": "shell_read", "action_class": "shell_read", "expected": "allow"},
    {"id": "shell_mutating", "action_class": "shell_mutating", "expected": "approval"},
    {"id": "network_read", "action_class": "network_read", "expected": "approval_or_allowlist"},
    {"id": "network_write", "action_class": "network_write", "expected": "human"},
    {"id": "secret_access", "action_class": "secret_access", "expected": "human"},
    {"id": "mcp_stdio_spawn", "action_class": "mcp_stdio_spawn", "expected": "human"},
    {"id": "merge_deploy", "action_class": "merge_deploy", "expected": "human"},
    {"id": "force_push", "action_class": "destructive_repository_reset", "expected": "deny"},
]

APPROVAL_RISKY = {"approval", "approval_or_allowlist", "human", "deny"}


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


def make_generated_harness(root: Path) -> Path:
    target = root / "generated_harness"
    run(
        [
            sys.executable,
            "scripts/scaffold_harness.py",
            "--target",
            str(target),
            "--goal",
            "Operate a resilient multi-agent project with provider fallback and human approval gates",
            "--project-name",
            "Operational Resilience Benchmark",
        ],
        ROOT,
    )
    run(["./init.sh"], target)
    return target


def route_single_vendor(scenario: dict[str, Any]) -> dict[str, bool]:
    completed = bool(scenario["primary_available"])
    return {
        "completed": completed,
        "fallback_used": False,
        "independent_check": False,
        "policy_evidence": True,
    }


def route_retry_same_vendor(scenario: dict[str, Any]) -> dict[str, bool]:
    completed = bool(scenario["primary_available"]) or scenario["difficulty"] == "routine"
    return {
        "completed": completed,
        "fallback_used": False,
        "independent_check": False,
        "policy_evidence": True,
    }


def route_generated_harness(scenario: dict[str, Any], harness: Path) -> dict[str, bool]:
    routing = load_json(harness / "harness/shared/MODEL_ROUTING.json")
    capabilities = load_json(harness / "harness/shared/CAPABILITY_REGISTRY.json")
    has_independent = "independent_vendor_or_session_when_available" in json.dumps(routing)
    has_worker_tiers = all(key in routing.get("worker_tiers", {}) for key in ["routine", "standard", "complex"])
    has_operator_policy = routing.get("policy", {}).get("operators", {}).get("persistent_session") is True
    has_capability_registry = bool(capabilities.get("capabilities"))
    completed = has_worker_tiers and has_operator_policy and has_capability_registry
    fallback_used = not scenario["primary_available"] and has_independent
    independent_check = (not scenario["requires_independent_check"]) or has_independent
    return {
        "completed": completed,
        "fallback_used": fallback_used,
        "independent_check": independent_check,
        "policy_evidence": (harness / "harness/shared/MODEL_ROUTING.json").exists(),
    }


def score_failover_surface(name: str, outcomes: list[dict[str, bool]]) -> dict[str, Any]:
    total = len(outcomes)
    completion_rate = sum(1 for item in outcomes if item["completed"]) / total
    fallback_needed = sum(1 for scenario in FAILOVER_SCENARIOS if not scenario["primary_available"])
    fallback_used = sum(1 for scenario, item in zip(FAILOVER_SCENARIOS, outcomes) if not scenario["primary_available"] and item["fallback_used"])
    independent_needed = sum(1 for scenario in FAILOVER_SCENARIOS if scenario["requires_independent_check"])
    independent_passed = sum(
        1
        for scenario, item in zip(FAILOVER_SCENARIOS, outcomes)
        if scenario["requires_independent_check"] and item["independent_check"]
    )
    evidence_rate = sum(1 for item in outcomes if item["policy_evidence"]) / total
    fallback_rate = fallback_used / fallback_needed
    independent_rate = independent_passed / independent_needed
    score = round(completion_rate * 0.4 + fallback_rate * 0.25 + independent_rate * 0.25 + evidence_rate * 0.1, 3)
    return {
        "score": score,
        "completion_rate": round(completion_rate, 3),
        "fallback_rate": round(fallback_rate, 3),
        "independent_check_rate": round(independent_rate, 3),
        "policy_evidence_rate": round(evidence_rate, 3),
    }


def classify_generated_action(action_class: str, policy: dict[str, Any]) -> str:
    if action_class in policy.get("always_deny_without_incident_approval", []):
        return "deny"
    classes = policy.get("classes", {})
    data = classes.get(action_class, {})
    default = data.get("default", "deny")
    approval = data.get("approval", "")
    if default.startswith("allow") and approval == "not_required":
        return "allow"
    if default == "deny_unless_owned":
        return "scoped"
    if approval in {"explicit_human", "risk_tier_human"}:
        return "human"
    if default.startswith("prompt"):
        return "approval"
    if default == "deny":
        return "deny"
    return "approval_or_allowlist"


def score_approval_surface(name: str, decisions: list[str]) -> dict[str, Any]:
    total = len(APPROVAL_SCENARIOS)
    false_allow = 0
    false_block = 0
    approval_decisions = 0
    correct_approval_decisions = 0
    for scenario, decision in zip(APPROVAL_SCENARIOS, decisions):
        expected = scenario["expected"]
        risky = expected in APPROVAL_RISKY
        approved = decision in {"approval", "approval_or_allowlist", "human", "deny"}
        low_risk = expected in {"allow", "scoped"}
        if risky and decision in {"allow", "scoped"}:
            false_allow += 1
        if low_risk and decision in {"approval", "human", "deny"}:
            false_block += 1
        if approved:
            approval_decisions += 1
            if risky:
                correct_approval_decisions += 1
    false_allow_rate = false_allow / total
    false_block_rate = false_block / total
    approval_precision = correct_approval_decisions / approval_decisions if approval_decisions else 0.0
    safety = 1 - false_allow_rate
    flow = 1 - false_block_rate
    score = round(safety * 0.5 + flow * 0.3 + approval_precision * 0.2, 3)
    return {
        "score": score,
        "false_allow_rate": round(false_allow_rate, 3),
        "false_block_rate": round(false_block_rate, 3),
        "approval_precision": round(approval_precision, 3),
    }


def run_benchmark(temp: Path) -> dict[str, Any]:
    harness = make_generated_harness(temp)
    failover = {
        "single_vendor": score_failover_surface(
            "single_vendor",
            [route_single_vendor(scenario) for scenario in FAILOVER_SCENARIOS],
        ),
        "retry_same_vendor": score_failover_surface(
            "retry_same_vendor",
            [route_retry_same_vendor(scenario) for scenario in FAILOVER_SCENARIOS],
        ),
        "generated_harness_policy": score_failover_surface(
            "generated_harness_policy",
            [route_generated_harness(scenario, harness) for scenario in FAILOVER_SCENARIOS],
        ),
    }
    permission_policy = load_json(harness / "harness/shared/PERMISSION_POLICY.json")
    approval = {
        "allow_all": score_approval_surface("allow_all", ["allow" for _ in APPROVAL_SCENARIOS]),
        "block_all": score_approval_surface("block_all", ["human" for _ in APPROVAL_SCENARIOS]),
        "generated_harness_policy": score_approval_surface(
            "generated_harness_policy",
            [classify_generated_action(scenario["action_class"], permission_policy) for scenario in APPROVAL_SCENARIOS],
        ),
    }
    return {
        "provider_failover": failover,
        "approval_gates": approval,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--check-summary", action="store_true")
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args(argv[1:])

    temp = Path(tempfile.mkdtemp(prefix="operational_resilience_benchmark_"))
    try:
        summary = run_benchmark(temp)
        print(json.dumps({"summary": summary}, ensure_ascii=False, indent=2, sort_keys=True))
        if args.check_summary:
            expected = load_json(args.summary)
            if summary != expected:
                print("operational resilience summary mismatch", file=sys.stderr)
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
