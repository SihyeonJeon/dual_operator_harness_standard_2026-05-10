#!/usr/bin/env python3
"""Create a project-local harness from this kit and a project goal."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
import re


def contains_any(text: str, terms: list[str]) -> bool:
    for term in terms:
        normalized = term.lower()
        if re.search(r"[^\x00-\x7f]", normalized) or " " in normalized or "-" in normalized:
            if normalized in text:
                return True
        elif re.search(rf"\b{re.escape(normalized)}\b", text):
            return True
    return False


def classify_project_type(goal: str, constraints: str) -> str:
    text = f"{goal} {constraints}".lower()
    checks = [
        ("software", ["app", "code", "software", "web", "api", "ios", "android", "server", "앱", "웹", "소프트웨어"]),
        ("game", ["game", "unity", "unreal", "visual novel", "게임"]),
        ("video", ["video", "film", "edit", "youtube", "render", "영상", "비디오"]),
        ("research", ["research", "paper", "analysis", "market", "study", "연구", "논문", "분석"]),
        ("writing", ["book", "essay", "script", "story", "copywriting", "글쓰기", "책", "스토리"]),
        ("design", ["design", "brand", "ui", "ux", "figma", "디자인", "브랜드"]),
    ]
    hits = [kind for kind, words in checks if contains_any(text, words)]
    if len(set(hits)) > 1:
        return "mixed"
    return hits[0] if hits else "unknown"


def assess_risk(goal: str, constraints: str) -> tuple[int, list[str], str]:
    text = f"{goal} {constraints}".lower()
    categories = {
        "medical_or_health": [
            "medical",
            "health",
            "healthcare",
            "clinical",
            "diagnosis",
            "diagnostic",
            "triage",
            "patient",
            "의료",
            "건강",
            "진단",
            "환자",
            "트리아지",
        ],
        "legal_or_public_sector": ["legal", "law", "lawyer", "contract", "public-sector", "government", "법률", "계약", "공공"],
        "financial": ["finance", "financial", "investment", "tax", "loan", "payment", "금융", "투자", "세금", "결제"],
        "hr_or_employment": ["hr", "hiring", "employment", "recruiting", "채용", "인사"],
        "safety_or_child_related": ["safety", "child", "minor", "emergency", "안전", "아동", "미성년", "응급"],
        "private_data_or_secrets": ["secret", "credential", "private data", "pii", "personal data", "개인정보", "비밀", "자격증명"],
        "production_external_action": [
            "production",
            "deploy",
            "customer",
            "publish",
            "outreach",
            "cloud",
            "server",
            "배포",
            "고객",
            "게시",
            "클라우드",
            "서버",
        ],
    }
    flags = [name for name, words in categories.items() if contains_any(text, words)]
    if any(flag in flags for flag in ["medical_or_health", "legal_or_public_sector", "financial", "hr_or_employment", "safety_or_child_related"]):
        return 3, flags, "regulated_candidate_requires_human_review"
    if any(flag in flags for flag in ["private_data_or_secrets", "production_external_action"]):
        return 2, flags, "sensitive_or_external_action_candidate"
    return 1, ["UNKNOWN"], "not_selected"


def detect_workstreams(goal: str, constraints: str) -> tuple[str, list[str]]:
    text = f"{goal} {constraints}".lower()
    checks = [
        ("software", ["app", "web", "api", "code", "software", "ios", "android", "saas", "앱", "웹", "소프트웨어"]),
        ("research", ["research", "analysis", "study", "paper", "survey", "market", "조사", "연구", "분석", "논문"]),
        ("writing", ["write", "book", "essay", "article", "script", "story", "copy", "작성", "글", "책", "스토리"]),
        ("design", ["design", "brand", "ui", "ux", "figma", "visual", "디자인", "브랜드"]),
        ("media", ["video", "film", "audio", "youtube", "render", "podcast", "영상", "비디오", "오디오"]),
        ("data", ["data", "dataset", "etl", "dashboard", "analytics", "데이터", "대시보드"]),
        ("operations", ["operation", "workflow", "process", "sop", "support", "ops", "운영", "프로세스"]),
        ("business", ["business", "sales", "marketing", "proposal", "startup", "사업", "영업", "마케팅", "제안"]),
        ("education", ["course", "curriculum", "lesson", "training", "교육", "강의", "커리큘럼"]),
        ("game", ["game", "unity", "unreal", "play", "게임"]),
    ]
    hits = [name for name, words in checks if contains_any(text, words)]
    if not hits:
        hits = ["general"]
    primary = hits[0] if len(hits) == 1 else "mixed"
    return primary, hits


def build_workstream_profile(goal: str, primary: str, streams: list[str], risk_tier: int, risk_flags: list[str]) -> dict:
    needs_design = any(stream in streams for stream in ["software", "design", "media", "writing", "education", "game"])
    needs_council = risk_tier >= 2 or primary == "mixed"
    required_loop = [
        "current_state_research_before_overall_plan",
        "planning_runway",
        "workstream_and_risk_confirmation",
        "candidate_slice_generation",
        "design_when_needed" if needs_design else "design_not_required_by_default",
        "pre_visualization_spec_gate_when_needed",
        "slice_approval_gate",
        "production",
        "debugging_or_revision",
        "evaluation",
        "cross_feedback_loop",
        "cross_evaluation_when_required" if needs_council else "cross_evaluation_optional",
        "completed_work_packet",
        "operator_review",
        "human_review_when_material",
        "context_update",
        "regulation_review",
    ]
    activation_notes = {
        "planning": "Always active. Runs current-state market/comparable research when external reality matters, builds the planning runway, confirms workstream/risk assumptions, proposes candidate slices, then approves one sharp/deep slice before production.",
        "design": "Activate when output quality depends on interaction, visual form, information architecture, narrative structure, media continuity, curriculum shape, or subjective taste. Visualization production requires a task-local VISUALIZATION_SPEC.md first.",
        "production": "Use coding/production team files for any artifact production: code, research notes, writing, media plans, data artifacts, business operations, or documentation.",
        "evaluation": "Always active. Converts acceptance criteria into evidence, records cross-feedback for material artifacts, and returns failures to the correct phase.",
    }
    if "research" in streams:
        activation_notes["planning"] += " For research, it must define sources, claim hygiene, and provenance gates."
    if "business" in streams or "operations" in streams:
        activation_notes["production"] += " For business/operations, production outputs are proposals, SOPs, process artifacts, or operating packets, not necessarily code."
    if "medical_or_health" in risk_flags or risk_tier >= 3:
        activation_notes["evaluation"] += " Regulated or high-risk work requires independent evaluation and human review before external use."
    return {
        "version": "1.0",
        "project_goal": goal,
        "primary_workstream": primary,
        "detected_workstreams": streams,
        "risk_tier": risk_tier,
        "risk_flags": risk_flags,
        "team_topology": {
            "selection_policy": "project_goal_and_task_shape",
            "fixed_operators": ["claude-code", "codex"],
            "always_present_teams": ["planning", "production", "evaluation"],
            "conditional_teams": ["design", "cross_evaluation", "council"],
            "team_activation_notes": activation_notes,
            "recommended_initial_topology": {
                "planning": "active",
                "design": "active" if needs_design else "on_demand",
                "production": "after_planning",
                "evaluation": "active",
                "cross_evaluation": "required" if needs_council else "on_demand",
                "council": "advisory_after_smoke" if needs_council else "optional_after_smoke",
            },
        },
        "current_market_research": {
            "policy_path": "harness/shared/CURRENT_MARKET_RESEARCH_POLICY.md",
            "required_before_overall_plan": True,
            "as_of": "command_time",
            "not_run_requires_reason_and_risk": True,
            "artifact": "harness/tasks/{task_id}/CURRENT_RESEARCH.json",
        },
        "cross_feedback_loop": {
            "policy_path": "harness/shared/CROSS_FEEDBACK_LOOP.md",
            "required_for_material_artifacts": True,
            "preserve_dissent": True,
            "artifact": "harness/tasks/{task_id}/CROSS_FEEDBACK.json",
        },
        "operator_boundary": {
            "operators_do": [
                "orchestrate",
                "critique",
                "convene council",
                "review completed work packets",
                "communicate with human",
                "evolve governance from evidence",
            ],
            "operators_do_not": [
                "directly perform production work",
                "debug inside the team loop",
                "self-approve completion",
                "bypass team evaluation",
            ],
        },
        "required_loop": required_loop,
        "initial_feature_seeds": ["H0", "H1", "F0-PLANNING-RUNWAY"],
        "open_questions": [
            "Confirm planning runway inputs and slice-approval criteria.",
            "Confirm project-specific verification commands.",
            "Confirm whether detected workstreams are correct.",
        ],
    }


def choose_mode(goal: str, constraints: str, risk_tier: int) -> str:
    text = f"{goal} {constraints}".lower()
    if risk_tier >= 3:
        return "full"
    if risk_tier >= 2 or contains_any(text, ["team", "cloud", "server", "multi-agent", "long-running", "팀", "클라우드", "서버"]):
        return "standard"
    if contains_any(text, ["toy", "demo", "scratch", "experiment", "장난감", "데모", "실험"]):
        return "lite"
    return "standard"


def update_json(path: Path, updater) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    updater(data)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_template(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def copy_rendered_tree(source: Path, target: Path, values: dict[str, str]) -> None:
    for path in source.rglob("*"):
        if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
            continue
        rel = path.relative_to(source)
        destination = target / rel
        if path.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(render_template(path.read_text(encoding="utf-8"), values), encoding="utf-8")


def run_validator(target: Path, validator: Path) -> tuple[str, str]:
    result = subprocess.run(
        [sys.executable, str(validator), str(target)],
        check=False,
        text=True,
        capture_output=True,
    )
    output = "\n".join(part for part in [result.stdout.strip(), result.stderr.strip()] if part)
    return ("PASS" if result.returncode == 0 else "FAIL"), output


def run_implementer_hook(script: Path, command: str, args: list[str]) -> tuple[str, str]:
    result = subprocess.run(
        [sys.executable, str(script), command, *args],
        check=False,
        text=True,
        capture_output=True,
    )
    output = "\n".join(part for part in [result.stdout.strip(), result.stderr.strip()] if part)
    return ("PASS" if result.returncode == 0 else "FAIL"), output


def write_implementer_hook_run(harness: Path, pre_hook_result: str, pre_hook_output: str) -> None:
    path = harness / "IMPLEMENTER_HOOKS_RUN.json"
    data = {
        "version": "1.0",
        "pre_scaffold": {
            "status": pre_hook_result,
            "hook": "PreScaffoldGoalIntake",
            "output": pre_hook_output,
        },
        "intake_validate": {
            "status": "UNKNOWN",
            "hook": "IntakeValidate",
            "timestamp": "UNKNOWN",
        },
        "profile_derive_audit": {
            "status": "UNKNOWN",
            "hook": "ProfileDeriveAudit",
            "timestamp": "UNKNOWN",
        },
        "adoption_mode_select": {
            "status": "UNKNOWN",
            "hook": "AdoptionModeSelect",
            "timestamp": "UNKNOWN",
        },
        "domain_pack_select": {
            "status": "UNKNOWN",
            "hook": "DomainPackSelect",
            "timestamp": "UNKNOWN",
        },
        "post_scaffold": {
            "status": "UNKNOWN",
            "hook": "PostScaffoldValidation",
            "timestamp": "UNKNOWN",
        },
        "handoff_complete": {
            "status": "UNKNOWN",
            "hook": "HandoffComplete",
            "timestamp": "UNKNOWN",
        },
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def update_feature_state_from_doctor(target: Path, doctor_result: str, doctor_output: str) -> None:
    path = target / "feature_list.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for feature in data.get("features", []):
        if feature.get("id") == "H0":
            if doctor_result == "PASS":
                feature["state"] = "passing"
                feature["evidence"] = "harness/SCAFFOLDING_REPORT.md#validation-result"
                feature["notes"] = "Local harness doctor passed during scaffold generation."
            else:
                feature["state"] = "blocked"
                feature["evidence"] = doctor_output[:500] if doctor_output else "validator failed"
                feature["notes"] = "Local harness doctor failed during scaffold generation."
        elif feature.get("id") == "H1" and doctor_result == "PASS":
            feature["state"] = "active"
            feature["notes"] = "Run ./init.sh from a fresh session, then route through operator startup."
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_root_handoff_from_doctor(target: Path, values: dict[str, str], doctor_result: str) -> None:
    h0_state = "passing" if doctor_result == "PASS" else "blocked"
    h1_state = "active" if doctor_result == "PASS" else "not_started"
    current_task = "H1-BOOTSTRAP-SMOKE" if doctor_result == "PASS" else "H0-LOCAL-SMOKE"
    target.joinpath("harness", "shared", "ACTIVE_SNAPSHOT.md").write_text(
        "\n".join(
            [
                "# Active Snapshot",
                "",
                f"Date: {values['DATE']}",
                f"Current task id: {current_task}",
                f"Adoption mode: {values['MODE']}",
                f"Risk tier: {values['RISK_TIER']}",
                f"Risk flags: {values['RISK_FLAGS']}",
                f"Compliance profile: {values['COMPLIANCE_PROFILE']}",
                f"Primary workstream: {values['PRIMARY_WORKSTREAM']}",
                f"Detected workstreams: {values['DETECTED_WORKSTREAMS']}",
                "",
                "## Current State",
                "",
                "Harness scaffold created. Root agent entrypoint files exist. Production work has not started.",
                f"- H0 local smoke: `{h0_state}`",
                f"- H1 bootstrap restart smoke: `{h1_state}`",
                "",
                "## Active Blockers",
                "",
                "- Project-specific runtime commands are `UNKNOWN`.",
                "- Planning runway and slice approval criteria are `UNKNOWN`.",
                "- Workstream profile is an initial scaffold inference and must be confirmed by operators/human when material.",
                "- Dual-operator protocol must preserve Codex/Claude parity and dissent.",
                "- Fixed operator session handles are `UNKNOWN` until recorded in `OPERATOR_SESSION_REGISTRY.json`.",
                "- Part-owner worker sessions must not be reused for unrelated parts.",
                "- Context-saving plugin stack is capped at four and starts `UNVERIFIED`.",
                "- Visualization or dashboard work is blocked until the pre-visualization spec gate passes.",
                "- External viz backend work is blocked until backend selection, bounded policy, credential lifecycle, and smoke evidence exist.",
                "- Claude Code hooks, subagents, skills, and agent teams are generated but `UNVERIFIED` until target-runtime smoke.",
                "- Runtime capabilities are `UNVERIFIED`.",
                "- MCP export is scaffolded but `UNVERIFIED`; non-local interfaces remain disabled until approved.",
                "- Canonical records and compiled local report views must remain separated.",
                "- Runner descriptors are `UNVERIFIED`; remote/cloud runners deny network by default.",
                "- Remote terminal, cloud, mobile, chat, and always-on operation are denied until `harness/runtime/REMOTE_OPERATION_POLICY.md` is satisfied.",
                "",
                "## Open Questions",
                "",
                "- Confirm quality bar.",
                "- Confirm planning runway inputs before approving a sharp/deep production slice.",
                "- Confirm visualization purpose, source artifacts, redaction, and acceptance criteria before any dashboard/HTML/UI visualization production.",
                "- Confirm visualization backend and whether `events.jsonl` should stay local or flow to an external adapter.",
                "- Confirm whether MCP context export or private overlay adapters are required before activating them.",
                "- Confirm detected workstreams and team topology.",
                "- Confirm project-specific start, test, build, and evaluation commands.",
                "- Confirm any private-data, secret, budget, cloud, or compliance constraints not included in the two inputs.",
                "- Confirm whether remote terminal, mobile approval, chat connector, or cloud runner operation is required and who approves it.",
                "- If risk flags are not `UNKNOWN`, confirm whether regulated-domain controls are required before production work.",
                "",
                "## Human Decisions",
                "",
                f"- Project goal: {values['PROJECT_GOAL']}",
                f"- Prior information and constraints: {values['PRIOR_INFO_AND_CONSTRAINTS']}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    target.joinpath("progress.md").write_text(
        "\n".join(
            [
                "# Session Progress Log",
                "",
                f"Last updated: {values['DATE']}",
                f"Project goal: {values['PROJECT_GOAL']}",
                f"Adoption mode: {values['MODE']}",
                f"Risk tier: {values['RISK_TIER']}",
                "",
                "## Current State",
                "",
                "- Harness scaffold created.",
                "- Production work has not started.",
                f"- H0 local smoke is `{h0_state}`.",
                f"- H1 bootstrap restart smoke is `{h1_state}`.",
                "",
                "## Active Feature",
                "",
                "H1 - Bootstrap restart path" if doctor_result == "PASS" else "H0 - Harness scaffold doctor",
                "",
                "## Done",
                "",
                "- Project-local `harness/` directory created.",
                "- Root agent entry files created.",
                "- Claude Code `.claude/` adapter files created.",
                "- Dual-operator parity protocol created.",
                "- Part ownership, plugin routing, and quality gates created.",
                "- Records policy and context-pressure controls created.",
                "- MCP export and spec automation scaffolds created.",
                "- Shared context and operator role files created.",
                "- Local validator and schemas copied into the target project.",
                "- Dependency-free golden eval suite copied into the target project.",
                "",
                "## In Progress",
                "",
                "- H1 bootstrap restart verification." if doctor_result == "PASS" else "- H0 local smoke remediation.",
                "",
                "## Blockers And Risks",
                "",
                "- Project-specific runtime commands are UNKNOWN.",
                "- Planning runway and slice approval criteria are UNKNOWN.",
                "- Material human decisions remain in `harness/shared/ACTIVE_SNAPSHOT.md`.",
                "- Local report views remain separate from canonical project records.",
                "",
                "## Decisions",
                "",
                f"- Project goal from input: {values['PROJECT_GOAL']}",
                f"- Prior information and constraints: {values['PRIOR_INFO_AND_CONSTRAINTS']}",
                f"- Initial risk flags: {values['RISK_FLAGS']}",
                f"- Initial detected workstreams: {values['DETECTED_WORKSTREAMS']}",
                "- Codex and Claude Code are equal fixed operators; no forced consensus.",
                "",
                "## Evidence",
                "",
                "- `harness/SCAFFOLDING_REPORT.md`",
                "- `harness/IMPLEMENTER_HANDOFF.md`",
                "- `harness/shared/ACTIVE_SNAPSHOT.md`",
                "",
                "## Next Session",
                "",
                "1. Run `./init.sh`.",
                "2. Say \"you are operator\" to the selected fixed operator agent.",
                "3. Resolve H1, then enter F0 planning runway or record the exact blocker.",
                "4. Ask the human only for material decisions that change scope, risk, cost, private data, irreversible action, or production authority.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    target.joinpath("session-handoff.md").write_text(
        "\n".join(
            [
                "# Session Handoff",
                "",
                f"Date: {values['DATE']}",
                "Status: IMPLEMENTER_HANDOFF_COMPLETE",
                "",
                "## Restart Path",
                "",
                "1. Open the project root.",
                "2. Run `./init.sh`.",
                "3. Read `AGENTS.md`.",
                "4. Read `feature_list.json` and `progress.md`.",
                "5. If acting as an operator, load the matching role from `harness/operators/`.",
                "",
                "## Canonical Memory",
                "",
                "- Root scope state: `feature_list.json`",
                "- Current progress: `progress.md`",
                "- Shared harness memory: `harness/shared/`",
                "- Current task artifacts: `harness/tasks/`",
                "- Records policy boundary: `harness/shared/RECORDS_POLICY.md`",
                "- Context pressure controls: `harness/shared/CONTEXT_PRESSURE.md`",
                "",
                "## Open Work",
                "",
                f"- H0 local smoke is `{h0_state}`.",
                f"- H1 bootstrap restart smoke is `{h1_state}` and must be verified or blocked with evidence.",
                "- Planning runway is pending; first production slice remains a candidate until planning/design/evaluation gates approve it.",
                "- Workstream profile is available at `harness/shared/WORKSTREAM_PROFILE.json`.",
                "",
                "## Do Not Carry Forward As Authority",
                "",
                "- Hidden chat context from the implementer.",
                "- Unrecorded assumptions about domain strategy, budget, tools, deployment, audience, or compliance.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, help="Target project directory")
    parser.add_argument("--constraints", default="UNKNOWN", help="Optional prior information and constraints")
    parser.add_argument("--goal", required=True, help="Project goal")
    parser.add_argument("--project-name", default="UNKNOWN")
    parser.add_argument("--mode", choices=["lite", "standard", "full"], default=None)
    args = parser.parse_args()

    standard_root = Path(__file__).resolve().parents[1]
    implementer_hook_script = standard_root / "scripts" / "implementer_hooks.py"
    template_harness = standard_root / "templates" / "harness"
    template_root = standard_root / "templates" / "root"
    input_packet_template = standard_root / "templates" / "input" / "INPUT_PACKET.md"
    target = Path(args.target).resolve()
    pre_hook_result, pre_hook_output = run_implementer_hook(
        implementer_hook_script,
        "pre-scaffold",
        [
            "--target",
            str(target),
            "--goal",
            args.goal,
            "--constraints",
            args.constraints,
            "--kit-root",
            str(standard_root),
        ],
    )
    if pre_hook_result != "PASS":
        print("Implementer pre-scaffold hook failed.")
        if pre_hook_output:
            print(pre_hook_output)
        return 1
    harness = target / "harness"
    harness.mkdir(parents=True, exist_ok=True)
    shutil.copytree(template_harness, harness, dirs_exist_ok=True)
    target_scripts = target / "scripts"
    target_scripts.mkdir(parents=True, exist_ok=True)
    shutil.copy2(standard_root / "scripts" / "validate_harness.py", target_scripts / "validate_harness.py")
    shutil.copy2(implementer_hook_script, target_scripts / "implementer_hooks.py")
    target_schemas = target / "schemas"
    target_schemas.mkdir(parents=True, exist_ok=True)
    shutil.copytree(standard_root / "schemas", target_schemas, dirs_exist_ok=True)

    project_type = classify_project_type(args.goal, args.constraints)
    risk_tier, risk_flags, compliance_profile = assess_risk(args.goal, args.constraints)
    primary_workstream, detected_workstreams = detect_workstreams(args.goal, args.constraints)
    workstream_profile = build_workstream_profile(args.goal, primary_workstream, detected_workstreams, risk_tier, risk_flags)
    mode = args.mode or choose_mode(args.goal, args.constraints, risk_tier)
    today = date.today().isoformat()
    render_values = {
        "DATE": today,
        "PROJECT_GOAL": args.goal,
        "PROJECT_NAME": args.project_name,
        "PROJECT_TYPE": project_type,
        "MODE": mode,
        "RISK_TIER": str(risk_tier),
        "RISK_FLAGS": ", ".join(risk_flags),
        "COMPLIANCE_PROFILE": compliance_profile,
        "PRIMARY_WORKSTREAM": primary_workstream,
        "DETECTED_WORKSTREAMS": ", ".join(detected_workstreams),
        "PRIOR_INFO_AND_CONSTRAINTS": args.constraints,
    }
    copy_rendered_tree(template_root, target, render_values)
    harness.joinpath("spec", "INPUT_PACKET.md").write_text(
        render_template(input_packet_template.read_text(encoding="utf-8"), render_values),
        encoding="utf-8",
    )
    target.joinpath("init.sh").chmod(0o755)
    harnessctl = target.joinpath("scripts", "harnessctl.py")
    if harnessctl.exists():
        harnessctl.chmod(0o755)

    def profile_updater(data: dict) -> None:
        data["project_name"] = args.project_name
        data["project_type"] = project_type
        data["primary_goal"] = args.goal
        data["domain_risks"] = risk_flags
        data["compliance_profile"] = compliance_profile
        data["initial_risk_tier"] = risk_tier
        data["workstream_profile_path"] = "harness/shared/WORKSTREAM_PROFILE.json"
        data["initial_team_topology_path"] = "harness/shared/TEAM_TOPOLOGY.md"
        data["initial_feature_state_path"] = "feature_list.json"
        data["known_constraints"] = [args.constraints]
        data["created_from_inputs"] = {
            "prior_information_and_constraints": args.constraints,
            "project_goal": args.goal,
        }

    def config_updater(data: dict) -> None:
        data["harness"]["mode"] = mode

    update_json(harness / "shared" / "PROJECT_PROFILE.json", profile_updater)
    update_json(harness / "shared" / "HARNESS_CONFIG.json", config_updater)
    write_implementer_hook_run(harness, pre_hook_result, pre_hook_output)
    extra_hook_runs = [
        (
            "intake-validate",
            [
                "--target",
                str(target),
                "--goal",
                args.goal,
                "--constraints",
                args.constraints,
            ],
        ),
        ("profile-derive-audit", ["--target", str(target)]),
        ("adoption-mode-select", ["--target", str(target)]),
        ("domain-pack-select", ["--target", str(target)]),
    ]
    for hook_command, hook_args in extra_hook_runs:
        hook_result, hook_output = run_implementer_hook(
            target_scripts / "implementer_hooks.py",
            hook_command,
            hook_args,
        )
        if hook_result != "PASS":
            print(f"Implementer hook failed: {hook_command}")
            if hook_output:
                print(hook_output)
            return 1
    (harness / "shared" / "WORKSTREAM_PROFILE.json").write_text(
        json.dumps(workstream_profile, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    active = harness / "shared" / "ACTIVE_SNAPSHOT.md"
    active.write_text(
        "\n".join(
            [
                "# Active Snapshot",
                "",
                f"Date: {today}",
                "Current task id: H0-LOCAL-SMOKE",
                f"Adoption mode: {mode}",
                f"Risk tier: {risk_tier}",
                f"Risk flags: {', '.join(risk_flags)}",
                f"Compliance profile: {compliance_profile}",
                f"Primary workstream: {primary_workstream}",
                f"Detected workstreams: {', '.join(detected_workstreams)}",
                "",
                "## Current State",
                "",
                "Harness scaffold created. Root agent entrypoint files exist. Production work has not started.",
                "",
                "## Active Blockers",
                "",
                "- H0 local smoke has not run.",
                "- H1 bootstrap restart smoke has not run.",
                "- Claude Code runtime adapters have not been smoked.",
                "- Runtime capabilities are `UNVERIFIED`.",
                "",
                "## Open Questions",
                "",
                "- Confirm quality bar.",
                "- Confirm planning runway inputs before approving a sharp/deep production slice.",
                "- Confirm project-specific start, test, build, and evaluation commands.",
                "- Confirm any private-data, secret, budget, cloud, or compliance constraints not included in the two inputs.",
                "- If risk flags are not `UNKNOWN`, confirm whether regulated-domain controls are required before production work.",
                "",
                "## Human Decisions",
                "",
                f"- Project goal: {args.goal}",
                f"- Prior information and constraints: {args.constraints}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    report = harness / "SCAFFOLDING_REPORT.md"

    def write_report(doctor_result: str, doctor_output: str) -> None:
        report.write_text(
            "\n".join(
                [
                    "# Scaffolding Report",
                    "",
                    "Created by: harness implementer",
                    f"Date: {today}",
                    "",
                    "## Inputs",
                    "",
                    "Project goal:",
                    "",
                    "```text",
                    args.goal,
                    "```",
                    "",
                    "Prior information and constraints:",
                    "",
                    "```text",
                    args.constraints,
                    "```",
                    "",
                    "## Derived Initial Settings",
                    "",
                    f"Project type: {project_type}",
                    f"Adoption mode: {mode}",
                    f"Risk tier: {risk_tier}",
                    f"Risk flags: {', '.join(risk_flags)}",
                    f"Compliance profile: {compliance_profile}",
                    f"Primary workstream: {primary_workstream}",
                    f"Detected workstreams: {', '.join(detected_workstreams)}",
                    "Domain packs selected: UNKNOWN",
                    "",
                    "## Root Harness Entry",
                    "",
                    "- `AGENTS.md`: operator routing and startup workflow",
                    "- `CLAUDE.md`: Claude Code adapter entry",
                    "- `.claude/`: Claude Code hooks, project agents, skills, and agent-team adapter",
                    "- `README.md`: Korean/English project README",
                    "- `init.sh`: local bootstrap check",
                    "- `feature_list.json`: feature state source of truth",
                    "- `progress.md` and `session-handoff.md`: session continuity",
                    "- `scripts/harnessctl.py`: thin local validation, event, report, visualization-spec, eval-run, viz-export, archive, context-pack, worker-brief, model-route, task-packet, concept-check, and software-feedback command surface",
                    "- `harness/shared/WORKSTREAM_PROFILE.json`: inferred workstream and team topology",
                    "- `harness/shared/OPERATOR_SESSION_REGISTRY.json`: fixed operator session handles and verification status",
                    "- `harness/shared/DUAL_OPERATOR_PROTOCOL.md`: Codex/Claude parity and non-forced meetings",
                    "- `harness/shared/PART_OWNERSHIP.md`: part-owner worker session reuse rules",
                    "- `harness/shared/PLUGIN_ROUTING.json`: four-plugin context-saving policy with caveman slot",
                    "- `harness/shared/QUALITY_GATES.md`: artifact, context, runtime, UI/UX, and feedback gates",
                    "- `harness/shared/VISUALIZATION_SPEC_POLICY.md`: pre-visualization spec gate",
                    "- `harness/shared/RECORDS_POLICY.md`: canonical project records vs compiled local report views",
                    "- `harness/shared/CONTEXT_PRESSURE.md`: context budget, compaction, and context pack rules",
                    "- `harness/mcp_server/`: read-only harness context export scaffold",
                    "- `harness/spec/INPUT_PACKET.md`: rendered two-input intake packet for operator handoff",
                    "- `harness/spec/`: PRD/anti-PRD/spec automation policy",
                    "- `harness/runtime/RUNNERS/`: unverified runner descriptors",
                    "- `harness/shared/WORKSPACE_LAYOUT.md` and `MEMORY_BACKEND.json`: active/archive and retrieval controls",
                    "- `harness/IMPLEMENTER_HOOKS.md`: implementer scaffold hook contract",
                    "- `harness/IMPLEMENTER_HOOKS_RUN.json`: implementer hook run evidence",
                    "",
                    "## Capabilities",
                    "",
                    "All runtime, model, MCP, cloud, browser/computer-use, hook, deploy, merge, and secret-access capabilities start as `UNVERIFIED`.",
                    "",
                    "## Open Questions Left For Operators",
                    "",
                    "- Confirm quality bar.",
                    "- Confirm planning runway inputs before approving a sharp/deep production slice.",
                    "- Confirm detected workstreams and team topology.",
                    "- Confirm fixed Codex and Claude operator session handles.",
                    "- Confirm any local context-saving plugins beyond caveman.",
                    "- Confirm project-specific start/test/build/evaluation commands.",
                    "- Confirm visualization spec before creating dashboards, timelines, graphs, live status UI, or status views.",
                    "- Confirm MCP export or private overlay activation before using non-local interfaces.",
                    "- Smoke Claude Code hooks, project agents, skills, and agent teams before relying on them as enforcement.",
                    "- Confirm any private-data, secret, budget, cloud, or compliance constraints not included in the inputs.",
                    "",
                    "## Validation Result",
                    "",
                    f"Doctor result: {doctor_result}",
                    "",
                    "```text",
                    doctor_output or "NOT-RUN",
                    "```",
                    "",
                    "## Implementer Hooks",
                    "",
                    "- Scaffold lifecycle hooks are recorded in `harness/IMPLEMENTER_HOOKS_RUN.json`.",
                    "- Hook events are appended to `harness/events/events.jsonl` when post-scaffold validation runs.",
                    "",
                    "## Handoff",
                    "",
                    "Production work has not started. Fixed operators take over after reading the root entrypoint, shared context, feature state, and H0/H1 smoke tasks.",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    write_report("NOT-RUN", "Initial report written before validator execution.")

    handoff = harness / "IMPLEMENTER_HANDOFF.md"
    handoff.write_text(
        "\n".join(
            [
                "# Implementer Handoff",
                "",
                f"Date: {today}",
                "Status: IMPLEMENTER_HANDOFF_COMPLETE",
                "",
                "## Role Boundary",
                "",
                "This file is written by the harness implementer.",
                "",
                "The implementer is not a fixed operator and must not continue into the project's operational objective.",
                "Future project work belongs to fixed operators and approved workers after explicit human instruction.",
                "",
                "## Completed By Implementer",
                "",
                "- Harness scaffold: complete",
                "- H0 local smoke blueprint: created",
                "- H1 bootstrap restart smoke blueprint: created",
                "- Root agent entry files: created",
                "- Project README: created",
                "- Claude Code `.claude/` adapters: created",
                "- Dual-operator protocol: created",
                "- Part ownership, plugin routing, and quality gates: created",
                "- Feature state and session handoff files: created",
                "- Workstream profile and initial team topology inference: created",
                "- Human guide: created",
                "- Offline/local-continuity note: created",
                "- Remote/mobile/cloud operation policy: created",
                "- Records policy and context-pressure controls: created",
                "- MCP export and spec automation scaffolds: created",
                "- Operator session registry, workspace layout, memory backend, and runner descriptors: created",
                "- Visualization backend policy and local event export adapter: created",
                "- Dependency-free golden eval suite: created",
                "- Cloud/viz human decision guide: created",
                "- Local validator: `scripts/validate_harness.py`",
                "- Local harness control surface: `scripts/harnessctl.py`",
                "- Implementer hook script: `scripts/implementer_hooks.py`",
                "- Local schemas: `schemas/`",
                "",
                "## Fixed Operator Sessions",
                "",
                "- Claude Code: UNKNOWN",
                "- Codex: UNKNOWN",
                "",
                "## Next Non-Implementer Work",
                "",
                "Fixed operators should run `./init.sh`, load the shared context, resolve H0/H1 smoke, and ask the human for material decisions.",
                "Codex and Claude Code remain equal fixed operators; disagreement should be preserved, not forced into consensus.",
                "Claude Code operators should also treat `.claude/` features as unverified until runtime smoke records evidence.",
                "The implementer should not execute project operations.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    guide = target / "guide_for_human.md"
    guide.write_text(
        "\n".join(
            [
                "# Guide For Human",
                "",
                f"Date: {today}",
                "",
                "## Current Status",
                "",
                "Harness scaffold is complete. The implementer role is complete and should not continue as an operator.",
                "",
                "To start operation with a capable agent, open this project and say: `you are operator`.",
                "",
                "Fixed operator session names are not bootstrapped yet:",
                "",
                "- Claude Code: UNKNOWN",
                "- Codex: UNKNOWN",
                "",
                "## What You Need To Decide",
                "",
                "- Confirm quality bar and planning runway inputs.",
                "- Confirm detected workstreams and whether the initial team topology is right.",
                "- Confirm the fixed Codex and Claude Code operator sessions.",
                "- Confirm which four context-saving plugins to use; caveman is the preferred compression slot when verified.",
                "- Confirm visualization spec before creating dashboards, timelines, graphs, live status UI, or status views.",
                "- Confirm visualization backend before connecting `events.jsonl` to external or live viz systems.",
                "- Confirm MCP export and private overlay needs before activating non-local interfaces.",
                "- Confirm project-specific start, test, build, and evaluation commands.",
                "- Confirm private data, secret, budget, cloud, and compliance constraints.",
                "- Confirm cloud lane, bounded policy, credentials lifecycle, smoke evidence, and adapter ownership before remote operation.",
                "- Confirm remote terminal, mobile approval, chat connector, or cloud runner needs before enabling any of them.",
                "- Confirm whether fixed operator sessions should be created now.",
                "- Confirm whether Claude Code hooks, project agents, skills, and agent teams should be smoked now.",
                "- Confirm whether any offline, cloud, or mobile approval channel is required.",
                "",
                "## Current Safe Commands",
                "",
                "```sh",
                "./init.sh",
                "python3 scripts/validate_harness.py .",
                "python3 scripts/harnessctl.py validate",
                "python3 scripts/harnessctl.py report",
                "python3 scripts/harnessctl.py eval-run",
                "python3 scripts/harnessctl.py context-pack --task-id TASK",
                "python3 scripts/harnessctl.py worker-brief --task-id TASK --owned-path PATH",
                "python3 scripts/harnessctl.py model-route --role worker --task-difficulty routine --simple",
                "python3 scripts/harnessctl.py task-packet --task-id TASK --sender A --receiver B --intent handoff --summary 'summary'",
                "python3 scripts/harnessctl.py concept-check --task-id TASK --artifact-path PATH --forbidden-phrase 'prompt phrase'",
                "python3 scripts/harnessctl.py software-feedback --task-id TASK --lint-command '...' --smoke-command '...'",
                "python3 scripts/harnessctl.py viz-export --backend local_file",
                "python3 scripts/harnessctl.py viz-spec-check",
                "python3 scripts/harnessctl.py archive --task-id TASK --reason 'closed or superseded'",
                "```",
                "",
                "## What Not To Do Yet",
                "",
                "- Do not perform customer outreach.",
                "- Do not submit proposals, bids, listings, or public posts.",
                "- Do not create external posts, outreach, or reviewer ledgers from the public kit scaffold.",
                "- Do not log in to accounts or use credentials.",
                "- Do not spend money or execute contracts.",
                "- Do not deploy cloud or always-on workers.",
                "- Do not enable remote terminal control, mobile approval connectors, or chat connectors before policy, smoke evidence, and approval are recorded.",
                "- Do not connect external visualization backends before `VISUALIZATION_SPEC.md`, bounded policy, credential lifecycle, and smoke evidence are recorded.",
                "",
                "## Evidence To Review",
                "",
                "- `harness/SCAFFOLDING_REPORT.md`",
                "- `harness/IMPLEMENTER_HANDOFF.md`",
                "- `harness/runtime/OFFLINE_OPERATION.md`",
                "- `harness/runtime/REMOTE_OPERATION_POLICY.md`",
                "- `harness/runtime/CLOUD_VIZ_OPERATOR_GUIDE.md`",
                "- `harness/shared/RECORDS_POLICY.md`",
                "- `harness/shared/CONTEXT_PRESSURE.md`",
                "- `harness/viz/VIZ_BACKENDS.json`",
                "- `harness/mcp_server/README.md`",
                "- `harness/evals/README.md`",
                "- `harness/evals/golden_suite.json`",
                "- `harness/IMPLEMENTER_HOOKS_RUN.json`",
                "- `harness/shared/ACTIVE_SNAPSHOT.md`",
                "- `feature_list.json`",
                "- `progress.md`",
                "- `harness/shared/WORKSTREAM_PROFILE.json`",
                "- `.claude/settings.json`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    doctor_result, doctor_output = run_validator(target, target_scripts / "validate_harness.py")
    update_feature_state_from_doctor(target, doctor_result, doctor_output)
    update_root_handoff_from_doctor(target, render_values, doctor_result)
    write_report(doctor_result, doctor_output)
    post_hook_result, post_hook_output = run_implementer_hook(
        target_scripts / "implementer_hooks.py",
        "post-scaffold",
        ["--target", str(target), "--doctor-result", doctor_result],
    )
    if post_hook_result != "PASS":
        doctor_result = "FAIL"
        doctor_output = "\n".join(part for part in [doctor_output, post_hook_output] if part)
        write_report(doctor_result, doctor_output)
        print(f"Created harness at {harness}")
        print(f"Doctor result: {doctor_result}")
        if doctor_output:
            print(doctor_output)
        return 1
    handoff_hook_result, handoff_hook_output = run_implementer_hook(
        target_scripts / "implementer_hooks.py",
        "handoff-complete",
        ["--target", str(target)],
    )
    if handoff_hook_result != "PASS":
        doctor_result = "FAIL"
        doctor_output = "\n".join(part for part in [doctor_output, handoff_hook_output] if part)
        write_report(doctor_result, doctor_output)
        print(f"Created harness at {harness}")
        print(f"Doctor result: {doctor_result}")
        if doctor_output:
            print(doctor_output)
        return 1
    doctor_result, doctor_output = run_validator(target, target_scripts / "validate_harness.py")
    write_report(doctor_result, doctor_output)

    print(f"Created harness at {harness}")
    print(f"Doctor result: {doctor_result}")
    if doctor_output:
        print(doctor_output)
    print("Next: run ./init.sh in the target project, then invoke an agent with: you are operator")
    return 0 if doctor_result == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
