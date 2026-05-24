#!/usr/bin/env python3
"""Dependency-free doctor for generated dual-operator harnesses."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


P0_REQUIRED = [
    "SCAFFOLDING_REPORT.md",
    "SCAFFOLDING_CHECKLIST.md",
    "IMPLEMENTER_HANDOFF.md",
    "IMPLEMENTER_HOOKS.md",
    "IMPLEMENTER_HOOKS_RUN.json",
    "shared/PROJECT_PROFILE.json",
    "shared/HARNESS_CONFIG.json",
    "shared/CAPABILITY_REGISTRY.json",
    "shared/TOOL_REGISTRY.json",
    "shared/PERMISSION_POLICY.json",
    "shared/MCP_TRUST.json",
    "shared/COUNCIL_MCP.md",
    "shared/ACTIVE_SNAPSHOT.md",
    "shared/CONTEXT.md",
    "shared/MEMORY.md",
    "shared/FAILURE_LEDGER.md",
    "shared/RULE_CHANGE_LOG.md",
    "shared/REGULATION_EVOLUTION.md",
    "shared/SESSION_CONTINUITY.md",
    "shared/IDENTITY.md",
    "shared/CREDENTIAL_LIFECYCLE.md",
    "shared/INCIDENT_RESPONSE.md",
    "shared/OPERATOR_SESSION_REGISTRY.json",
    "shared/WORKER_SESSION_REGISTRY.json",
    "shared/CONTEXT_LOADING.md",
    "shared/WORKSPACE_LAYOUT.md",
    "shared/MEMORY_BACKEND.json",
    "shared/MODEL_ROUTING.json",
    "shared/DUAL_OPERATOR_PROTOCOL.md",
    "shared/PART_OWNERSHIP.md",
    "shared/PLUGIN_ROUTING.json",
    "shared/QUALITY_GATES.md",
    "shared/VISUALIZATION_SPEC_POLICY.md",
    "shared/CHANNEL_RECORDS.md",
    "shared/CONTEXT_PRESSURE.md",
    "shared/TEAM_TOPOLOGY.md",
    "shared/WORKSTREAM_PROFILE.json",
    "shared/OBSERVABILITY.md",
    "shared/CLEAN_STATE.md",
    "operators/claude-code/AGENT.md",
    "operators/claude-code/SKILLS.md",
    "operators/codex/AGENT.md",
    "operators/codex/SKILLS.md",
    "teams/planning/AGENT.md",
    "teams/planning/TEAM_CONTEXT.md",
    "teams/planning/SKILLS.md",
    "teams/design/AGENT.md",
    "teams/design/TEAM_CONTEXT.md",
    "teams/design/SKILLS.md",
    "teams/coding/AGENT.md",
    "teams/coding/TEAM_CONTEXT.md",
    "teams/coding/SKILLS.md",
    "teams/evaluation/AGENT.md",
    "teams/evaluation/TEAM_CONTEXT.md",
    "teams/evaluation/SKILLS.md",
    "templates/TASK_BLUEPRINT.md",
    "templates/WORKER_BRIEF.json",
    "templates/EVALUATION_REPORT.md",
    "templates/HUMAN_REVIEW_PACKET.md",
    "templates/VISUALIZATION_SPEC.md",
    "templates/BROADCAST_DRAFT.md",
    "templates/EXTERNAL_REVIEW_PACKET.md",
    "templates/BUDGET.json",
    "spec/INPUT_PACKET.md",
    "spec/SPEC_AUTOMATION_POLICY.md",
    "spec/PRD_DRAFT.md",
    "spec/ANTI_PRD.md",
    "broadcast/BROADCAST_POLICY.md",
    "broadcast/DRAFT_QUEUE.md",
    "broadcast/PUBLISHED_LEDGER.jsonl",
    "broadcast/connectors/generic_publication.example.json",
    "broadcast/connectors/manual_export.example.json",
    "reviewers/REVIEWER_POLICY.md",
    "reviewers/REVIEW_LEDGER.jsonl",
    "reviewers/adapters/ai_reviewer.example.json",
    "reviewers/adapters/human_reviewer.json",
    "mcp_server/README.md",
    "mcp_server/MANIFEST.json",
    "mcp_server/server.py",
    "viz/README.md",
    "viz/VIZ_BACKENDS.json",
    "viz/adapters/local_file.json",
    "viz/adapters/WORKER_ADAPTER_BRIEF.md",
    "reports/README.md",
    "evals/README.md",
    "evals/golden_suite.json",
    "evals/public_release_suite.json",
    "evals/results/.gitkeep",
    "tasks/H0-LOCAL-SMOKE/BLUEPRINT.md",
    "tasks/H0-LOCAL-SMOKE/BUDGET.json",
    "tasks/H1-BOOTSTRAP-SMOKE/BLUEPRINT.md",
    "tasks/H1-BOOTSTRAP-SMOKE/BUDGET.json",
    "tasks/F0-PLANNING-RUNWAY/BLUEPRINT.md",
    "tasks/F0-PLANNING-RUNWAY/BUDGET.json",
    "events/events.jsonl",
    "runtime/OFFLINE_OPERATION.md",
    "runtime/REMOTE_OPERATION_POLICY.md",
    "runtime/CLOUD_VIZ_OPERATOR_GUIDE.md",
    "runtime/RUNNERS/local_runner.json",
    "runtime/RUNNERS/claude_code_runner.json",
    "runtime/RUNNERS/codex_runner.json",
    "runtime/RUNNERS/remote_runner.json",
    "runtime/RUNNERS/cloud_runner.example.json",
    "tasks/active/.gitkeep",
    "tasks/archive/.gitkeep",
]

ROOT_REQUIRED = [
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "init.sh",
    "feature_list.json",
    "progress.md",
    "session-handoff.md",
    "guide_for_human.md",
    "scripts/implementer_hooks.py",
    "scripts/validate_harness.py",
    "scripts/harnessctl.py",
    "schemas/feature-list.schema.json",
    "schemas/broadcast-connector.schema.json",
    "schemas/capability-registry.schema.json",
    "schemas/eval-suite.schema.json",
    "schemas/harness-config.schema.json",
    "schemas/implementer-hooks-run.schema.json",
    "schemas/mcp-trust.schema.json",
    "schemas/memory-backend.schema.json",
    "schemas/model-routing.schema.json",
    "schemas/observability-event.schema.json",
    "schemas/operator-session-registry.schema.json",
    "schemas/permission-policy.schema.json",
    "schemas/plugin-routing.schema.json",
    "schemas/project-profile.schema.json",
    "schemas/reviewer-adapter.schema.json",
    "schemas/runner-config.schema.json",
    "schemas/task-state.schema.json",
    "schemas/tool-registry.schema.json",
    "schemas/viz-backends.schema.json",
    "schemas/worker-brief.schema.json",
    "schemas/worker-session-registry.schema.json",
    "schemas/workstream-profile.schema.json",
    ".claude/README.md",
    ".claude/settings.json",
    ".claude/hooks/session_start_context.py",
    ".claude/hooks/pre_tool_use_guard.py",
    ".claude/hooks/post_tool_use_index.py",
    ".claude/hooks/stop_clean_state.py",
    ".claude/hooks/task_completed_gate.py",
    ".claude/agents/harness-planner.md",
    ".claude/agents/harness-production-worker.md",
    ".claude/agents/harness-evaluator.md",
    ".claude/agents/harness-operator-reviewer.md",
    ".claude/skills/harness-operator/SKILL.md",
    ".claude/skills/harness-task-close/SKILL.md",
]

PROJECT_PROFILE_REQUIRED = [
    "project_name",
    "project_type",
    "primary_goal",
    "target_user_or_audience",
    "primary_deliverables",
    "non_goals",
    "quality_bar",
    "default_quality_mode",
    "first_sharp_deep_slice",
    "domain_risks",
    "required_surfaces",
    "forbidden_shortcuts",
    "known_constraints",
    "budget_or_plan_availability",
    "human_taste_decisions",
    "compliance_profile",
    "workstream_profile_path",
    "initial_team_topology_path",
    "initial_feature_state_path",
    "created_from_inputs",
]


def find_harness_root(root: Path) -> Path:
    if root.name == "harness" and root.joinpath("shared").exists():
        return root
    if root.joinpath("harness", "shared").exists():
        return root / "harness"
    if root.joinpath("shared").exists():
        return root
    raise SystemExit(f"Could not find harness root under {root}")


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"Invalid JSON: {path}: {exc}")
        return {}


def require_keys(obj: dict[str, Any], keys: list[str], label: str, errors: list[str]) -> None:
    for key in keys:
        if key not in obj:
            errors.append(f"{label} missing required key: {key}")


def blank_unknown_check(obj: Any, path: str, errors: list[str]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            blank_unknown_check(value, f"{path}.{key}", errors)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            blank_unknown_check(value, f"{path}[{index}]", errors)
    elif obj == "":
        errors.append(f"{path} is blank; use UNKNOWN or an explicit value")


def check_capabilities(registry: dict[str, Any], errors: list[str]) -> None:
    caps = registry.get("capabilities")
    if not isinstance(caps, list):
        errors.append("CAPABILITY_REGISTRY.json capabilities must be an array")
        return
    cap_ids = {cap.get("id") for cap in caps if isinstance(cap, dict)}
    for required_id in {
        "codex_operator_session",
        "codex_image_generation",
        "harnessctl_local_report",
        "broadcast_draft_queue",
        "external_reviewer_adapters",
        "harness_mcp_server",
    }:
        if required_id not in cap_ids:
            errors.append(f"CAPABILITY_REGISTRY.json missing capability {required_id}")
    for cap in caps:
        if not isinstance(cap, dict):
            errors.append("Capability entry is not an object")
            continue
        require_keys(
            cap,
            ["id", "name", "class", "status", "evidence_path", "verified_at", "reviewer", "notes"],
            f"capability {cap.get('id', '<unknown>')}",
            errors,
        )
        if cap.get("status") == "VERIFIED":
            for key in ["evidence_path", "verified_at", "reviewer"]:
                if not cap.get(key):
                    errors.append(f"VERIFIED capability {cap.get('id')} lacks {key}")


def check_tools(registry: dict[str, Any], errors: list[str]) -> None:
    tools = registry.get("tools")
    if not isinstance(tools, list):
        errors.append("TOOL_REGISTRY.json tools must be an array")
        return
    required = [
        "id",
        "owner",
        "description",
        "input_schema",
        "output_schema",
        "side_effect_class",
        "approval",
        "timeout_seconds",
        "retry_policy",
        "idempotency",
        "auth_scopes",
        "output_trust_level",
        "audit_event",
    ]
    side_effecting = {
        "write_fs",
        "shell_mutating",
        "network_write",
        "secret_access",
        "merge_deploy",
        "external_action",
    }
    no_approval = {"", "not_required", "not_required_scoped", None}
    for tool in tools:
        if not isinstance(tool, dict):
            errors.append("Tool entry is not an object")
            continue
        require_keys(tool, required, f"tool {tool.get('id', '<unknown>')}", errors)
        if tool.get("side_effect_class") in side_effecting and tool.get("approval") in no_approval:
            errors.append(f"Side-effecting tool {tool.get('id')} lacks approval policy")
        if not isinstance(tool.get("timeout_seconds"), int) or tool.get("timeout_seconds", 0) <= 0:
            errors.append(f"Tool {tool.get('id')} timeout_seconds must be positive integer")


def check_feature_list(feature_list: dict[str, Any], errors: list[str]) -> None:
    require_keys(feature_list, ["version", "project_goal", "state_machine", "features"], "feature_list.json", errors)
    state_machine = feature_list.get("state_machine", {})
    if isinstance(state_machine, dict):
        require_keys(state_machine, ["states", "passing_requires", "single_active_feature"], "feature_list.json state_machine", errors)
    features = feature_list.get("features")
    if not isinstance(features, list) or not features:
        errors.append("feature_list.json features must be a non-empty array")
        return
    active_count = 0
    ids = {feature.get("id") for feature in features if isinstance(feature, dict)}
    for required_id in ["H0", "H1", "F0-PLANNING-RUNWAY"]:
        if required_id not in ids:
            errors.append(f"feature_list.json missing required feature seed {required_id}")
    required = ["id", "name", "behavior", "dependencies", "state", "verification", "evidence", "owner", "notes"]
    valid_states = {"not_started", "active", "blocked", "passing"}
    for feature in features:
        if not isinstance(feature, dict):
            errors.append("feature_list.json feature entry is not an object")
            continue
        label = f"feature {feature.get('id', '<unknown>')}"
        require_keys(feature, required, label, errors)
        if feature.get("state") not in valid_states:
            errors.append(f"{label} has invalid state")
        if feature.get("state") == "active":
            active_count += 1
        if feature.get("state") == "passing" and not feature.get("evidence"):
            errors.append(f"{label} is passing without evidence")
        verification = feature.get("verification")
        if not isinstance(verification, dict):
            errors.append(f"{label} verification must be an object")
        else:
            require_keys(verification, ["command", "required"], f"{label} verification", errors)
            if verification.get("required") is True and not verification.get("command"):
                errors.append(f"{label} required verification lacks command")
    if state_machine.get("single_active_feature") is True and active_count > 1:
        errors.append("feature_list.json allows only one active feature")


def check_workstream_profile(profile: dict[str, Any], errors: list[str]) -> None:
    require_keys(
        profile,
        [
            "version",
            "project_goal",
            "primary_workstream",
            "detected_workstreams",
            "risk_tier",
            "team_topology",
            "operator_boundary",
            "required_loop",
            "initial_feature_seeds",
            "open_questions",
        ],
        "WORKSTREAM_PROFILE.json",
        errors,
    )
    detected = profile.get("detected_workstreams")
    if not isinstance(detected, list) or not detected:
        errors.append("WORKSTREAM_PROFILE.json detected_workstreams must be non-empty array")
    topology = profile.get("team_topology", {})
    if isinstance(topology, dict):
        require_keys(
            topology,
            [
                "selection_policy",
                "fixed_operators",
                "always_present_teams",
                "conditional_teams",
                "team_activation_notes",
                "recommended_initial_topology",
            ],
            "WORKSTREAM_PROFILE.json team_topology",
            errors,
        )
        always = topology.get("always_present_teams", [])
        for required_team in ["planning", "production", "evaluation"]:
            if required_team not in always:
                errors.append(f"WORKSTREAM_PROFILE.json must keep {required_team} in always_present_teams")
        recommended = topology.get("recommended_initial_topology", {})
        if isinstance(recommended, dict):
            for required_team in ["planning", "production", "evaluation"]:
                if required_team not in recommended:
                    errors.append(
                        f"WORKSTREAM_PROFILE.json recommended_initial_topology lacks {required_team}"
                    )
    boundary = profile.get("operator_boundary", {})
    if isinstance(boundary, dict):
        do_not = " ".join(boundary.get("operators_do_not", []))
        if "production" not in do_not:
            errors.append("WORKSTREAM_PROFILE.json operator boundary must forbid direct production work")
    required_loop = profile.get("required_loop", [])
    if isinstance(required_loop, list):
        for required_step in [
            "planning_runway",
            "pre_visualization_spec_gate_when_needed",
            "slice_approval_gate",
            "production",
        ]:
            if required_step not in required_loop:
                errors.append(f"WORKSTREAM_PROFILE.json required_loop lacks {required_step}")


def check_dual_operator_protocol(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8").lower()
    for phrase in ["equal fixed operators", "do not force consensus", "do not overwrite", "disagreement_human_required"]:
        if phrase not in text:
            errors.append(f"DUAL_OPERATOR_PROTOCOL.md lacks required phrase: {phrase}")


def check_plugin_routing(profile: dict[str, Any], errors: list[str]) -> None:
    policy = profile.get("policy", {})
    if not isinstance(policy, dict):
        errors.append("PLUGIN_ROUTING.json policy must be an object")
        return
    if policy.get("max_active_context_plugins") != 4:
        errors.append("PLUGIN_ROUTING.json must cap active context plugins at 4")
    if policy.get("no_private_memory_authority") is not True:
        errors.append("PLUGIN_ROUTING.json must forbid private plugin memory authority")
    slots = profile.get("preferred_plugin_slots", [])
    if not isinstance(slots, list) or len(slots) != 4:
        errors.append("PLUGIN_ROUTING.json must define exactly 4 preferred plugin slots")
        return
    plugins = {slot.get("preferred_plugin") for slot in slots if isinstance(slot, dict)}
    if "caveman" not in plugins:
        errors.append("PLUGIN_ROUTING.json must include caveman as preferred context compression plugin")
    for slot in slots:
        if isinstance(slot, dict) and slot.get("status") == "VERIFIED":
            errors.append("PLUGIN_ROUTING.json plugin slots must start UNVERIFIED in generated scaffolds")


def check_model_routing(model_routing: dict[str, Any], errors: list[str]) -> None:
    op_policy = model_routing.get("policy", {}).get("operators", {})
    if op_policy.get("model_class") != "highest_verified_available":
        errors.append("MODEL_ROUTING.json operators.model_class must be highest_verified_available")
    if op_policy.get("reasoning_effort") != "highest_verified_available":
        errors.append("MODEL_ROUTING.json operators.reasoning_effort must be highest_verified_available")
    worker_policy = model_routing.get("policy", {}).get("workers", {})
    if worker_policy.get("session_policy") != "part_owner_resume_when_safe":
        errors.append("MODEL_ROUTING.json workers.session_policy must be part_owner_resume_when_safe")
    if worker_policy.get("do_not_use_part_owner_for_unrelated_parts") is not True:
        errors.append("MODEL_ROUTING.json must isolate part-owner worker sessions")
    tiers = model_routing.get("worker_tiers", {})
    for tier in ["routine", "standard", "complex", "independent_evaluation"]:
        if tier not in tiers:
            errors.append(f"MODEL_ROUTING.json missing worker tier {tier}")
    routine = tiers.get("routine", {}) if isinstance(tiers, dict) else {}
    examples = routine.get("example_model_classes", []) if isinstance(routine, dict) else []
    preferred = routine.get("preferred_session_for_simple_tasks") if isinstance(routine, dict) else None
    if not isinstance(examples, list) or not examples:
        errors.append("MODEL_ROUTING.json routine tier must include example model classes")
    if not isinstance(preferred, str) or preferred in {"", "UNKNOWN"}:
        errors.append("MODEL_ROUTING.json routine tier must define preferred_session_for_simple_tasks")


def check_operator_sessions(registry: dict[str, Any], errors: list[str]) -> None:
    policy = registry.get("policy", {})
    if not isinstance(policy, dict):
        errors.append("OPERATOR_SESSION_REGISTRY.json policy must be an object")
    else:
        if policy.get("fixed_operator_sessions_required") is not True:
            errors.append("OPERATOR_SESSION_REGISTRY.json must require fixed operator sessions")
        if policy.get("private_session_memory_is_advisory") is not True:
            errors.append("OPERATOR_SESSION_REGISTRY.json must mark private session memory advisory")
    operators = registry.get("operators")
    if not isinstance(operators, list):
        errors.append("OPERATOR_SESSION_REGISTRY.json operators must be an array")
        return
    ids = {operator.get("operator_id") for operator in operators if isinstance(operator, dict)}
    for required_id in ["claude_code", "codex"]:
        if required_id not in ids:
            errors.append(f"OPERATOR_SESSION_REGISTRY.json missing {required_id}")
    for operator in operators:
        if not isinstance(operator, dict):
            errors.append("Operator session entry is not an object")
            continue
        require_keys(
            operator,
            [
                "operator_id",
                "surface",
                "session_handle",
                "resume_command",
                "model_class",
                "reasoning_effort",
                "status",
                "evidence_path",
                "verified_at",
                "reviewer",
            ],
            f"operator session {operator.get('operator_id', '<unknown>')}",
            errors,
        )
        if operator.get("model_class") != "highest_verified_available":
            errors.append(f"operator session {operator.get('operator_id')} must use highest_verified_available model_class")
        if operator.get("reasoning_effort") != "highest_verified_available":
            errors.append(f"operator session {operator.get('operator_id')} must use highest_verified_available reasoning_effort")
        if operator.get("status") == "VERIFIED":
            for key in ["evidence_path", "verified_at", "reviewer"]:
                if not operator.get(key):
                    errors.append(f"VERIFIED operator session {operator.get('operator_id')} lacks {key}")


def check_runner_configs(harness: Path, errors: list[str]) -> None:
    runner_dir = harness / "runtime" / "RUNNERS"
    required = ["id", "status", "surface", "allowed_tools", "network_default", "audit_path", "smoke_evidence_path"]
    for name in ["local_runner", "claude_code_runner", "codex_runner", "remote_runner", "cloud_runner.example"]:
        path = runner_dir / f"{name}.json"
        runner = load_json(path, errors)
        if isinstance(runner, dict):
            require_keys(runner, required, f"runner {name}", errors)
            if runner.get("status") != "UNVERIFIED":
                errors.append(f"runner {name} must start UNVERIFIED")
            if runner.get("network_default") != "DENIED":
                errors.append(f"runner {name} must deny network by default")
            if runner.get("audit_path") != "harness/events/events.jsonl":
                errors.append(f"runner {name} must audit to harness/events/events.jsonl")


def check_viz_backend_configs(harness: Path, errors: list[str]) -> None:
    config = load_json(harness / "viz" / "VIZ_BACKENDS.json", errors)
    if not isinstance(config, dict):
        return
    policy = config.get("selection_policy", {})
    if isinstance(policy, dict):
        if policy.get("task_local_visualization_spec_required") is not True:
            errors.append("VIZ_BACKENDS.json must require task-local visualization spec")
        if policy.get("claude_owns_visual_information_architecture") is not True:
            errors.append("VIZ_BACKENDS.json must make Claude owner for visual information architecture")
        if policy.get("codex_owns_bitmap_image_generation") is not True:
            errors.append("VIZ_BACKENDS.json must make Codex owner for bitmap image generation")
        if policy.get("canonical_memory_remains_files") is not True:
            errors.append("VIZ_BACKENDS.json must keep canonical memory in files")
    backends = config.get("backends")
    if not isinstance(backends, list) or not backends:
        errors.append("VIZ_BACKENDS.json backends must be a non-empty array")
        return
    ids = {backend.get("id") for backend in backends if isinstance(backend, dict)}
    if "local_file" not in ids:
        errors.append("VIZ_BACKENDS.json must define local_file backend")
    for backend in backends:
        if not isinstance(backend, dict):
            errors.append("VIZ_BACKENDS.json backend entry is not an object")
            continue
        for key in [
            "id",
            "status",
            "mode",
            "description",
            "network_write_default",
            "requires_human_approval",
            "requires_credentials",
            "adapter_descriptor",
            "smoke_evidence_path",
        ]:
            if key not in backend:
                errors.append(f"VIZ_BACKENDS.json backend {backend.get('id', '<unknown>')} lacks {key}")
        if backend.get("id") != "local_file" and backend.get("status") != "UNVERIFIED":
            errors.append(f"external viz backend {backend.get('id')} must start UNVERIFIED")
        if backend.get("network_write_default") != "DENIED":
            errors.append(f"viz backend {backend.get('id')} must deny network writes by default")


def check_visualization_policy(harness: Path, errors: list[str]) -> None:
    policy = harness / "shared" / "VISUALIZATION_SPEC_POLICY.md"
    text = policy.read_text(encoding="utf-8")
    for phrase in [
        "pre-visualization specification gate",
        "VISUALIZATION_SPEC.md",
        "compiled views",
        "SPEC_BLOCKED",
        "Claude owns visualization",
        "Codex image generation",
        "viz-export",
    ]:
        if phrase not in text:
            errors.append(f"VISUALIZATION_SPEC_POLICY.md lacks required phrase: {phrase}")
    template = harness / "templates" / "VISUALIZATION_SPEC.md"
    template_text = template.read_text(encoding="utf-8")
    for section in [
        "## Purpose",
        "## Audience",
        "## Source Artifacts",
        "## Data Contract",
        "## Views",
        "## Interaction",
        "## Redaction And Sharing",
        "## Acceptance Criteria",
        "## Approval",
        "Visualization backend",
        "Claude Visualization / Design",
    ]:
        if section not in template_text:
            errors.append(f"VISUALIZATION_SPEC.md lacks {section}")


def check_external_interfaces(harness: Path, errors: list[str]) -> None:
    broadcast = harness / "broadcast" / "BROADCAST_POLICY.md"
    broadcast_text = broadcast.read_text(encoding="utf-8")
    for phrase in [
        "Draft Queue",
        "human approval",
        "Automatic external publish is denied",
        "not canonical",
    ]:
        if phrase not in broadcast_text:
            errors.append(f"BROADCAST_POLICY.md lacks required phrase: {phrase}")

    channel_text = (harness / "shared" / "CHANNEL_RECORDS.md").read_text(encoding="utf-8")
    for phrase in [
        "Internal Canonical Records",
        "External Channel Records",
        "not canonical memory until",
        "Reviewer findings remain evidence",
    ]:
        if phrase not in channel_text:
            errors.append(f"CHANNEL_RECORDS.md lacks required phrase: {phrase}")

    pressure_text = (harness / "shared" / "CONTEXT_PRESSURE.md").read_text(encoding="utf-8")
    for phrase in [
        "Context Budget",
        "Compaction Triggers",
        "Context Pack Rule",
        "At most four active context-saving plugins",
        "Part-Owner Isolation",
    ]:
        if phrase not in pressure_text:
            errors.append(f"CONTEXT_PRESSURE.md lacks required phrase: {phrase}")

    workspace_text = (harness / "shared" / "WORKSPACE_LAYOUT.md").read_text(encoding="utf-8")
    for phrase in ["Active Workspace", "Archive Workspace", "Seven-Day Rule", "bounded context pack"]:
        if phrase not in workspace_text:
            errors.append(f"WORKSPACE_LAYOUT.md lacks required phrase: {phrase}")

    memory_backend = load_json(harness / "shared" / "MEMORY_BACKEND.json", errors)
    if isinstance(memory_backend, dict):
        if memory_backend.get("status") != "UNVERIFIED":
            errors.append("MEMORY_BACKEND.json must start UNVERIFIED")
        rules = memory_backend.get("rules", {})
        if isinstance(rules, dict) and rules.get("retrieval_must_return_source_paths") is not True:
            errors.append("MEMORY_BACKEND.json must require source paths for retrieval")

    reviewer_text = (harness / "reviewers" / "REVIEWER_POLICY.md").read_text(encoding="utf-8")
    for phrase in [
        "evidence, not authority",
        "No forced consensus",
        "Review Packet",
        "Ledger",
    ]:
        if phrase not in reviewer_text:
            errors.append(f"REVIEWER_POLICY.md lacks required phrase: {phrase}")

    spec_text = (harness / "spec" / "SPEC_AUTOMATION_POLICY.md").read_text(encoding="utf-8")
    for phrase in [
        "PRD draft",
        "anti-PRD",
        "candidate slices",
        "worker brief",
        "Production must not start from a vague goal alone",
    ]:
        if phrase not in spec_text:
            errors.append(f"SPEC_AUTOMATION_POLICY.md lacks required phrase: {phrase}")

    mcp_manifest = load_json(harness / "mcp_server" / "MANIFEST.json", errors)
    if isinstance(mcp_manifest, dict):
        names = {
            tool.get("name")
            for tool in mcp_manifest.get("tools", [])
            if isinstance(tool, dict)
        }
        for name in [
            "search_past_decisions",
            "get_capability_status",
            "get_current_task",
            "list_open_questions",
        ]:
            if name not in names:
                errors.append(f"mcp_server/MANIFEST.json missing tool {name}")

    mcp_trust_text = (harness / "shared" / "MCP_TRUST.json").read_text(encoding="utf-8")
    for phrase in ["read_only_context", "prompt_injection", "tool_poisoning"]:
        if phrase not in mcp_trust_text:
            errors.append(f"MCP_TRUST.json lacks required trust-boundary phrase: {phrase}")

    connector_paths = [
        "broadcast/connectors/generic_publication.example.json",
        "broadcast/connectors/manual_export.example.json",
    ]
    for rel in connector_paths:
        connector = load_json(harness / rel, errors)
        if isinstance(connector, dict):
            if connector.get("status") not in {"UNVERIFIED", "AVAILABLE_LOCAL"}:
                errors.append(f"{rel} must start UNVERIFIED or AVAILABLE_LOCAL")
            if connector.get("requires_human_approval") is not True:
                errors.append(f"{rel} must require human approval")
            if connector.get("network_write_default") != "DENIED":
                errors.append(f"{rel} must deny network writes by default")

    adapter_paths = [
        "reviewers/adapters/ai_reviewer.example.json",
        "reviewers/adapters/human_reviewer.json",
    ]
    for rel in adapter_paths:
        adapter = load_json(harness / rel, errors)
        if isinstance(adapter, dict):
            if adapter.get("status") != "UNVERIFIED":
                errors.append(f"{rel} must start UNVERIFIED")
            if "evidence" not in str(adapter.get("authority", "")):
                errors.append(f"{rel} must mark reviewer authority as evidence-oriented")


def check_harnessctl(project_root: Path, errors: list[str]) -> None:
    path = project_root / "scripts" / "harnessctl.py"
    text = path.read_text(encoding="utf-8")
    for phrase in ["event", "report", "viz-export", "viz-spec-check", "eval-run", "broadcast-draft", "review-packet", "archive", "compiled view"]:
        if phrase not in text:
            errors.append(f"scripts/harnessctl.py lacks {phrase}")


def check_one_eval_suite(path: Path, errors: list[str]) -> set[str]:
    suite = load_json(path, errors)
    if not isinstance(suite, dict):
        return set()
    label = path.name
    require_keys(suite, ["suite_id", "version", "cases"], label, errors)
    cases = suite.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append(f"{label} cases must be a non-empty array")
        return set()
    supported = {
        "file_exists",
        "text_contains",
        "json_has_key",
        "json_equals",
        "json_array_min_length",
        "event_count_min",
        "events_schema_valid",
        "verified_evidence_integrity",
    }
    ids: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            errors.append(f"{label} case entry is not an object")
            continue
        require_keys(case, ["id", "name", "type", "severity"], f"eval case {case.get('id', '<unknown>')}", errors)
        case_id = case.get("id")
        if case_id in ids:
            errors.append(f"{label} duplicate case id: {case_id}")
        ids.add(case_id)
        if case.get("type") not in supported:
            errors.append(f"{label} unsupported case type: {case.get('type')}")
        if case.get("severity") not in {"required", "optional"}:
            errors.append(f"{label} invalid severity for {case_id}")
    return ids


def check_eval_suite(harness: Path, errors: list[str]) -> None:
    ids = check_one_eval_suite(harness / "evals" / "golden_suite.json", errors)
    required_ids = {
        "root_agents_entry_exists",
        "feature_list_has_features",
        "workstream_profile_detected",
        "dual_operator_parity",
        "visualization_spec_gate",
        "broadcast_publish_denied",
        "regulation_change_process",
        "held_out_challenge_eval_gate",
    }
    for required_id in required_ids:
        if required_id not in ids:
            errors.append(f"golden_suite.json missing required eval case: {required_id}")
    public_ids = check_one_eval_suite(harness / "evals" / "public_release_suite.json", errors)
    if len(public_ids) < 22:
        errors.append("public_release_suite.json must include at least 22 checklist-derived cases")
    for required_id in {
        "topology_dual_operator_dissent",
        "planning_before_production",
        "events_schema_valid",
        "verified_evidence_integrity",
        "budget_caps_defined",
    }:
        if required_id not in public_ids:
            errors.append(f"public_release_suite.json missing required eval case: {required_id}")


def check_operator_manual(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    lower = text.lower()
    if "ambiguity protocol" not in lower:
        errors.append(f"{path} lacks Ambiguity protocol")
    if "ask the user" not in lower:
        errors.append(f"{path} must instruct operator to ask the user on material ambiguity")
    if "do not" not in lower:
        errors.append(f"{path} lacks explicit negative boundaries")


def check_claude_adapter(project_root: Path, settings: dict[str, Any], errors: list[str]) -> None:
    hooks = settings.get("hooks", {}) if isinstance(settings, dict) else {}
    for hook_name in ["SessionStart", "PreToolUse", "PostToolUse", "Stop", "TaskCompleted"]:
        if hook_name not in hooks:
            errors.append(f".claude/settings.json lacks {hook_name} hook")
    settings_text = (project_root / ".claude" / "settings.json").read_text(encoding="utf-8")
    for script_name in [
        "session_start_context.py",
        "pre_tool_use_guard.py",
        "post_tool_use_index.py",
        "stop_clean_state.py",
        "task_completed_gate.py",
    ]:
        if script_name not in settings_text:
            errors.append(f".claude/settings.json does not reference {script_name}")
    env = settings.get("env", {}) if isinstance(settings, dict) else {}
    if env.get("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS") != "1":
        errors.append(".claude/settings.json must enable Claude Code agent teams for generated team adapters")

    agents = {
        "harness-planner.md": True,
        "harness-production-worker.md": True,
        "harness-evaluator.md": True,
        "harness-operator-reviewer.md": False,
    }
    for filename, must_have_team_context in agents.items():
        path = project_root / ".claude" / "agents" / filename
        text = path.read_text(encoding="utf-8")
        if "harness/shared" not in text:
            errors.append(f".claude/agents/{filename} must point to harness/shared")
        if must_have_team_context and "TEAM_CONTEXT.md" not in text:
            errors.append(f".claude/agents/{filename} must preserve team TEAM_CONTEXT.md")
        if "\nmemory:" in text:
            errors.append(f".claude/agents/{filename} must not create separate Claude memory authority")

    for rel in [
        ".claude/skills/harness-operator/SKILL.md",
        ".claude/skills/harness-task-close/SKILL.md",
    ]:
        text = project_root.joinpath(rel).read_text(encoding="utf-8")
        if "harness/shared" not in text:
            errors.append(f"{rel} must point to harness/shared canonical memory")


def check_portability(project_root: Path, errors: list[str]) -> None:
    portable_paths = [
        project_root / "AGENTS.md",
        project_root / "CLAUDE.md",
        project_root / "feature_list.json",
        project_root / "harness" / "shared" / "MCP_TRUST.json",
        project_root / "harness" / "shared" / "COUNCIL_MCP.md",
    ]
    forbidden = ["/Users/", "/home/", "C:\\Users\\", ".npm/_npx", "NODE_PATH="]
    for path in portable_paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for marker in forbidden:
            if marker in text:
                errors.append(f"{path} contains non-portable absolute path marker {marker}")


def check_text_files(harness: Path, project_root: Path, errors: list[str]) -> None:
    readme = project_root / "README.md"
    readme_text = readme.read_text(encoding="utf-8")
    for phrase in ["## 한국어", "## English", "you are operator", "VISUALIZATION_SPEC.md", "BROADCAST_POLICY.md"]:
        if phrase not in readme_text:
            errors.append(f"README.md lacks required bilingual/operation phrase: {phrase}")
    report = harness / "SCAFFOLDING_REPORT.md"
    report_text = report.read_text(encoding="utf-8")
    if "Project goal" not in report_text:
        errors.append("SCAFFOLDING_REPORT.md lacks Project goal")
    if "Production work has not started" not in report_text:
        errors.append("SCAFFOLDING_REPORT.md must state production work has not started")
    input_packet = harness / "spec" / "INPUT_PACKET.md"
    input_packet_text = input_packet.read_text(encoding="utf-8")
    for phrase in ["Harness Intake Packet", "Project Goal", "Prior Information And Constraints"]:
        if phrase not in input_packet_text:
            errors.append(f"INPUT_PACKET.md lacks {phrase}")
    checklist = harness / "SCAFFOLDING_CHECKLIST.md"
    if "No production work has started" not in checklist.read_text(encoding="utf-8"):
        errors.append("SCAFFOLDING_CHECKLIST.md lacks no-production-work check")
    active = harness / "shared" / "ACTIVE_SNAPSHOT.md"
    if "Open Questions" not in active.read_text(encoding="utf-8"):
        errors.append("ACTIVE_SNAPSHOT.md lacks Open Questions section")
    agents = project_root / "AGENTS.md"
    agents_text = agents.read_text(encoding="utf-8")
    if "you are operator" not in agents_text:
        errors.append("AGENTS.md must route the phrase 'you are operator'")
    if "feature_list.json" not in agents_text:
        errors.append("AGENTS.md must reference feature_list.json")
    eval_template = harness / "templates" / "EVALUATION_REPORT.md"
    eval_text = eval_template.read_text(encoding="utf-8")
    for verdict in ["PASS", "WARN", "FAIL", "NOT-RUN"]:
        if verdict not in eval_text:
            errors.append(f"EVALUATION_REPORT.md lacks verdict {verdict}")
    if "pre-visualization spec gate" not in eval_text:
        errors.append("EVALUATION_REPORT.md lacks pre-visualization spec gate")
    task_text = (harness / "templates" / "TASK_BLUEPRINT.md").read_text(encoding="utf-8")
    if "Visualization Pre-Spec Gate" not in task_text:
        errors.append("TASK_BLUEPRINT.md lacks Visualization Pre-Spec Gate")
    if "Held-Out / Challenge Eval Gate" not in task_text:
        errors.append("TASK_BLUEPRINT.md lacks Held-Out / Challenge Eval Gate")
    quality_text = (harness / "shared" / "QUALITY_GATES.md").read_text(encoding="utf-8")
    for phrase in [
        "Held-Out And Challenge Eval Gate",
        "A local golden set proves regression coverage, not generalization",
        "feedback slice",
        "future regression fixtures",
    ]:
        if phrase not in quality_text:
            errors.append(f"QUALITY_GATES.md lacks required held-out eval phrase: {phrase}")
    hooks_text = (harness / "IMPLEMENTER_HOOKS.md").read_text(encoding="utf-8")
    for phrase in [
        "PreScaffoldGoalIntake",
        "IntakeValidate",
        "ProfileDeriveAudit",
        "AdoptionModeSelect",
        "DomainPackSelect",
        "PostScaffoldValidation",
        "HandoffComplete",
        "production work has not started",
    ]:
        if phrase not in hooks_text:
            errors.append(f"IMPLEMENTER_HOOKS.md lacks {phrase}")
    hooks_run = load_json(harness / "IMPLEMENTER_HOOKS_RUN.json", errors)
    if isinstance(hooks_run, dict):
        for key in [
            "pre_scaffold",
            "intake_validate",
            "profile_derive_audit",
            "adoption_mode_select",
            "domain_pack_select",
            "post_scaffold",
            "handoff_complete",
        ]:
            if key not in hooks_run:
                errors.append(f"IMPLEMENTER_HOOKS_RUN.json lacks {key}")
    remote_text = (harness / "runtime" / "REMOTE_OPERATION_POLICY.md").read_text(encoding="utf-8")
    for phrase in ["bounded connector", "unrestricted shell", "Mobile Approval Rule"]:
        if phrase not in remote_text:
            errors.append(f"REMOTE_OPERATION_POLICY.md lacks {phrase}")
    task_close_skill = (project_root / ".claude" / "skills" / "harness-task-close" / "SKILL.md").read_text(encoding="utf-8")
    for phrase in ["broadcast", "external reviewer", "canonical"]:
        if phrase not in task_close_skill.lower():
            errors.append(f"harness-task-close skill lacks {phrase}")


def main(argv: list[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else ".").resolve()
    harness = find_harness_root(root)
    project_root = harness.parent
    errors: list[str] = []
    warnings: list[str] = []

    for rel in P0_REQUIRED:
        if not harness.joinpath(rel).exists():
            errors.append(f"Missing required file: {rel}")
    for rel in ROOT_REQUIRED:
        if not project_root.joinpath(rel).exists():
            errors.append(f"Missing required file: {rel}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    project = load_json(harness / "shared" / "PROJECT_PROFILE.json", errors)
    config = load_json(harness / "shared" / "HARNESS_CONFIG.json", errors)
    capabilities = load_json(harness / "shared" / "CAPABILITY_REGISTRY.json", errors)
    tools = load_json(harness / "shared" / "TOOL_REGISTRY.json", errors)
    permissions = load_json(harness / "shared" / "PERMISSION_POLICY.json", errors)
    mcp = load_json(harness / "shared" / "MCP_TRUST.json", errors)
    worker_sessions = load_json(harness / "shared" / "WORKER_SESSION_REGISTRY.json", errors)
    operator_sessions = load_json(harness / "shared" / "OPERATOR_SESSION_REGISTRY.json", errors)
    model_routing = load_json(harness / "shared" / "MODEL_ROUTING.json", errors)
    worker_brief = load_json(harness / "templates" / "WORKER_BRIEF.json", errors)
    feature_list = load_json(project_root / "feature_list.json", errors)
    workstream_profile = load_json(harness / "shared" / "WORKSTREAM_PROFILE.json", errors)
    plugin_routing = load_json(harness / "shared" / "PLUGIN_ROUTING.json", errors)
    claude_settings = load_json(project_root / ".claude" / "settings.json", errors)

    if isinstance(project, dict):
        require_keys(project, PROJECT_PROFILE_REQUIRED, "PROJECT_PROFILE.json", errors)
        blank_unknown_check(project, "PROJECT_PROFILE.json", errors)
        if project.get("project_type") not in {
            "software",
            "game",
            "video",
            "research",
            "writing",
            "design",
            "mixed",
            "other",
            "unknown",
        }:
            errors.append("PROJECT_PROFILE.json project_type has invalid value")

    mode = config.get("harness", {}).get("mode") if isinstance(config, dict) else None
    if mode not in {"lite", "standard", "full"}:
        errors.append("HARNESS_CONFIG.json harness.mode must be lite, standard, or full")
    if isinstance(config, dict):
        for operator_id in ["claude_code", "codex"]:
            operator = config.get("operators", {}).get(operator_id, {})
            if not operator.get("persistent"):
                errors.append(f"HARNESS_CONFIG.json operator {operator_id} must be persistent")
            if operator.get("session_policy") != "fixed_persistent":
                errors.append(f"HARNESS_CONFIG.json operator {operator_id} must use fixed_persistent session_policy")
            if operator.get("model_class") != "highest_verified_available":
                errors.append(f"HARNESS_CONFIG.json operator {operator_id} must use highest_verified_available model_class")
            if operator.get("reasoning_effort") != "highest_verified_available":
                errors.append(f"HARNESS_CONFIG.json operator {operator_id} must use highest_verified_available reasoning_effort")

    if isinstance(capabilities, dict):
        check_capabilities(capabilities, errors)
    if isinstance(tools, dict):
        check_tools(tools, errors)
    if isinstance(permissions, dict) and permissions.get("default") != "fail_closed":
        errors.append("PERMISSION_POLICY.json default must be fail_closed")
    if isinstance(mcp, dict) and "mcp_servers" not in mcp:
        errors.append("MCP_TRUST.json lacks mcp_servers")
    if isinstance(worker_sessions, dict):
        policy = worker_sessions.get("policy", {})
        if policy.get("fixed_operator_sessions") is not True:
            errors.append("WORKER_SESSION_REGISTRY.json must assert fixed_operator_sessions true")
        if policy.get("resume_prior_worker_when_safe") is not True:
            errors.append("WORKER_SESSION_REGISTRY.json must require resume_prior_worker_when_safe")
        if policy.get("part_owner_session_isolation") is not True:
            errors.append("WORKER_SESSION_REGISTRY.json must isolate part-owner worker sessions")
        if policy.get("do_not_reuse_part_owner_for_unrelated_parts") is not True:
            errors.append("WORKER_SESSION_REGISTRY.json must forbid unrelated reuse of part-owner sessions")
        if policy.get("part_reopen_prefers_prior_owner") is not True:
            errors.append("WORKER_SESSION_REGISTRY.json must prefer prior part owner on reopen")
    if isinstance(operator_sessions, dict):
        check_operator_sessions(operator_sessions, errors)
    if isinstance(model_routing, dict):
        check_model_routing(model_routing, errors)
    if isinstance(worker_brief, dict):
        require_keys(
            worker_brief,
            [
                "owned_paths",
                "no_touch_paths",
                "ownership_contract",
                "success_criteria",
                "stop_conditions",
                "worker_session",
                "runner_config",
                "model_routing",
                "plugin_routing",
                "context_pressure",
                "external_channel_gate",
                "visualization_spec_gate",
                "independent_verification",
            ],
            "WORKER_BRIEF.json",
            errors,
        )
    if isinstance(feature_list, dict):
        check_feature_list(feature_list, errors)
    if isinstance(workstream_profile, dict):
        check_workstream_profile(workstream_profile, errors)
    if isinstance(plugin_routing, dict):
        check_plugin_routing(plugin_routing, errors)
    if isinstance(claude_settings, dict):
        check_claude_adapter(project_root, claude_settings, errors)
    check_dual_operator_protocol(harness / "shared" / "DUAL_OPERATOR_PROTOCOL.md", errors)
    check_runner_configs(harness, errors)
    check_viz_backend_configs(harness, errors)
    check_visualization_policy(harness, errors)
    check_external_interfaces(harness, errors)
    check_eval_suite(harness, errors)
    check_harnessctl(project_root, errors)

    check_operator_manual(harness / "operators" / "claude-code" / "AGENT.md", errors)
    check_operator_manual(harness / "operators" / "codex" / "AGENT.md", errors)
    check_text_files(harness, project_root, errors)
    check_portability(project_root, errors)

    if mode in {"standard", "full"}:
        for rel in ["templates/HUMAN_REVIEW_PACKET.md", "shared/IDENTITY.md", "shared/CREDENTIAL_LIFECYCLE.md"]:
            if not harness.joinpath(rel).exists():
                warnings.append(f"Recommended for {mode}: {rel}")

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(f"PASS: harness doctor checks passed for {harness}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
