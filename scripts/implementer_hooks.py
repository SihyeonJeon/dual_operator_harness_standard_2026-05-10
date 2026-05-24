#!/usr/bin/env python3
"""Dependency-free hooks for the harness implementer scaffold lifecycle."""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def emit(data: dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def fail(message: str, **extra: Any) -> int:
    payload = {
        "status": "FAIL",
        "hook": extra.pop("hook", "UNKNOWN"),
        "timestamp": now(),
        "message": message,
        **extra,
    }
    emit(payload)
    return 1


def read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_event(target: Path, event: dict[str, Any]) -> None:
    path = target / "harness" / "events" / "events.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def run_path(target: Path) -> Path:
    return target / "harness" / "IMPLEMENTER_HOOKS_RUN.json"


def update_run(target: Path, key: str, payload: dict[str, Any]) -> None:
    data = read_json(run_path(target), {"version": "1.0"})
    data[key] = payload
    write_json(run_path(target), data)


def pass_payload(hook: str, **extra: Any) -> dict[str, Any]:
    return {
        "status": "PASS",
        "hook": hook,
        "timestamp": now(),
        **extra,
    }


def pre_scaffold(args: argparse.Namespace) -> int:
    hook = "PreScaffoldGoalIntake"
    target = Path(args.target).resolve()
    kit_root = Path(args.kit_root).resolve() if args.kit_root else None
    goal = args.goal.strip()

    if not goal or goal.upper() == "UNKNOWN":
        return fail("Project goal is required before scaffolding.", hook=hook, target=str(target))
    if kit_root and target == kit_root:
        return fail("Refusing to scaffold into the standard kit root.", hook=hook, target=str(target))
    if target == Path("/"):
        return fail("Refusing to scaffold into filesystem root.", hook=hook, target=str(target))

    payload = {
        "status": "PASS",
        "hook": hook,
        "timestamp": now(),
        "target": str(target),
        "goal_present": True,
        "constraints_present": bool(args.constraints and args.constraints != "UNKNOWN"),
        "production_started": False,
        "notes": [
            "Scaffolding may create harness files only.",
            "Missing material facts must be recorded as UNKNOWN.",
            "Project production strategy remains for fixed operators after handoff.",
        ],
    }
    emit(payload)
    return 0


def intake_validate(args: argparse.Namespace) -> int:
    hook = "IntakeValidate"
    target = Path(args.target).resolve()
    goal = args.goal.strip()
    if not goal or goal.upper() == "UNKNOWN":
        return fail("Project goal is required.", hook=hook, target=str(target))
    payload = pass_payload(
        hook,
        target=str(target),
        goal_present=True,
        constraints_present=bool(args.constraints and args.constraints != "UNKNOWN"),
        missing_values_policy="UNKNOWN",
    )
    if (target / "harness").exists():
        update_run(target, "intake_validate", payload)
    emit(payload)
    return 0


def profile_derive_audit(args: argparse.Namespace) -> int:
    hook = "ProfileDeriveAudit"
    target = Path(args.target).resolve()
    profile_path = target / "harness" / "shared" / "PROJECT_PROFILE.json"
    profile = read_json(profile_path, {})
    if not isinstance(profile, dict) or not profile:
        return fail("PROJECT_PROFILE.json missing or invalid.", hook=hook, target=str(target))
    blanks: list[str] = []

    def walk(value: Any, prefix: str) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                walk(item, f"{prefix}.{key}" if prefix else key)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                walk(item, f"{prefix}[{index}]")
        elif value == "":
            blanks.append(prefix)

    walk(profile, "PROJECT_PROFILE.json")
    if blanks:
        return fail("PROJECT_PROFILE.json contains blank values.", hook=hook, blanks=blanks)
    if profile.get("primary_goal") in {"", "UNKNOWN", None}:
        return fail("PROJECT_PROFILE.json primary_goal was not derived from input.", hook=hook)
    payload = pass_payload(
        hook,
        profile_path="harness/shared/PROJECT_PROFILE.json",
        primary_goal_present=True,
        blank_values=[],
        invented_values_policy="UNKNOWN_FOR_MISSING_FACTS",
    )
    update_run(target, "profile_derive_audit", payload)
    emit(payload)
    return 0


def adoption_mode_select(args: argparse.Namespace) -> int:
    hook = "AdoptionModeSelect"
    target = Path(args.target).resolve()
    config = read_json(target / "harness" / "shared" / "HARNESS_CONFIG.json", {})
    mode = config.get("harness", {}).get("mode") if isinstance(config, dict) else None
    if mode not in {"lite", "standard", "full"}:
        return fail("HARNESS_CONFIG.json has invalid adoption mode.", hook=hook, mode=mode)
    payload = pass_payload(
        hook,
        mode=mode,
        rationale="selected by scaffold risk/workstream heuristic; operators may revise with evidence",
    )
    update_run(target, "adoption_mode_select", payload)
    emit(payload)
    return 0


def domain_pack_select(args: argparse.Namespace) -> int:
    hook = "DomainPackSelect"
    target = Path(args.target).resolve()
    payload = pass_payload(
        hook,
        selected_domain_packs=[],
        status_detail="No domain pack is selected during scaffold unless explicitly justified by inputs.",
        production_strategy_started=False,
    )
    update_run(target, "domain_pack_select", payload)
    emit(payload)
    return 0


def post_scaffold(args: argparse.Namespace) -> int:
    hook = "PostScaffoldValidation"
    target = Path(args.target).resolve()
    harness = target / "harness"
    if not harness.exists():
        return fail("Harness directory missing after scaffold.", hook=hook, target=str(target))

    required = [
        target / "README.md",
        target / "AGENTS.md",
        target / "feature_list.json",
        target / "scripts" / "validate_harness.py",
        target / "scripts" / "harnessctl.py",
        harness / "SCAFFOLDING_REPORT.md",
        harness / "IMPLEMENTER_HANDOFF.md",
        harness / "IMPLEMENTER_HOOKS.md",
        harness / "shared" / "PROJECT_PROFILE.json",
        harness / "shared" / "WORKSTREAM_PROFILE.json",
    ]
    missing = [str(path.relative_to(target)) for path in required if not path.exists()]
    status = "PASS" if args.doctor_result == "PASS" and not missing else "FAIL"
    payload = read_json(run_path(target), {"version": "1.0"})
    payload["post_scaffold"] = {
        "status": status,
        "hook": hook,
        "timestamp": now(),
        "doctor_result": args.doctor_result,
        "missing_required_outputs": missing,
        "production_started": False,
        "handoff_required": True,
    }
    write_json(run_path(target), payload)
    append_event(
        target,
        {
            "event_id": f"evt_{uuid.uuid4().hex}",
            "trace_id": "trace_scaffold",
            "task_id": "H0-LOCAL-SMOKE",
            "actor": "implementer_hooks.py",
            "actor_type": "hook",
            "event_type": "implementer.post_scaffold",
            "timestamp": now(),
            "verdict": "PASS" if status == "PASS" else "FAIL",
            "summary": f"Post-scaffold hook {status}",
            "evidence_path": "harness/IMPLEMENTER_HOOKS_RUN.json",
        },
    )
    emit(payload["post_scaffold"])
    return 0 if status == "PASS" else 1


def handoff_complete(args: argparse.Namespace) -> int:
    hook = "HandoffComplete"
    target = Path(args.target).resolve()
    required = [
        target / "guide_for_human.md",
        target / "harness" / "IMPLEMENTER_HANDOFF.md",
        target / "harness" / "tasks" / "H0-LOCAL-SMOKE" / "BLUEPRINT.md",
        target / "harness" / "tasks" / "H1-BOOTSTRAP-SMOKE" / "BLUEPRINT.md",
        target / "harness" / "tasks" / "F0-PLANNING-RUNWAY" / "BLUEPRINT.md",
        target / "harness" / "shared" / "OPERATOR_SESSION_REGISTRY.json",
        target / "harness" / "shared" / "CHANNEL_RECORDS.md",
        target / "harness" / "shared" / "CONTEXT_PRESSURE.md",
    ]
    missing = [str(path.relative_to(target)) for path in required if not path.exists()]
    status = "PASS" if not missing else "FAIL"
    payload = {
        "status": status,
        "hook": hook,
        "timestamp": now(),
        "missing_required_handoff_files": missing,
        "implementer_role_complete": status == "PASS",
        "production_started": False,
    }
    update_run(target, "handoff_complete", payload)
    append_event(
        target,
        {
            "event_id": f"evt_{uuid.uuid4().hex}",
            "trace_id": "trace_scaffold",
            "task_id": "H0-LOCAL-SMOKE",
            "actor": "implementer_hooks.py",
            "actor_type": "hook",
            "event_type": "implementer.handoff_complete",
            "timestamp": now(),
            "verdict": status,
            "summary": f"Handoff-complete hook {status}",
            "evidence_path": "harness/IMPLEMENTER_HOOKS_RUN.json",
        },
    )
    emit(payload)
    return 0 if status == "PASS" else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    pre = sub.add_parser("pre-scaffold")
    pre.add_argument("--target", required=True)
    pre.add_argument("--goal", required=True)
    pre.add_argument("--constraints", default="UNKNOWN")
    pre.add_argument("--kit-root", default="")

    post = sub.add_parser("post-scaffold")
    post.add_argument("--target", required=True)
    post.add_argument("--doctor-result", required=True)

    intake = sub.add_parser("intake-validate")
    intake.add_argument("--target", required=True)
    intake.add_argument("--goal", required=True)
    intake.add_argument("--constraints", default="UNKNOWN")

    profile = sub.add_parser("profile-derive-audit")
    profile.add_argument("--target", required=True)

    adoption = sub.add_parser("adoption-mode-select")
    adoption.add_argument("--target", required=True)

    domain = sub.add_parser("domain-pack-select")
    domain.add_argument("--target", required=True)

    handoff = sub.add_parser("handoff-complete")
    handoff.add_argument("--target", required=True)

    args = parser.parse_args(argv[1:])
    if args.command == "pre-scaffold":
        return pre_scaffold(args)
    if args.command == "intake-validate":
        return intake_validate(args)
    if args.command == "profile-derive-audit":
        return profile_derive_audit(args)
    if args.command == "adoption-mode-select":
        return adoption_mode_select(args)
    if args.command == "domain-pack-select":
        return domain_pack_select(args)
    if args.command == "post-scaffold":
        return post_scaffold(args)
    if args.command == "handoff-complete":
        return handoff_complete(args)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
