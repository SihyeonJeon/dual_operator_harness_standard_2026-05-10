#!/usr/bin/env python3
"""Score deterministic agentic governance surfaces."""

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
BENCHMARK_DIR = Path(__file__).resolve().parent
DEFAULT_SUMMARY = BENCHMARK_DIR / "expected_summary.json"

FRAMEWORK_CRITERIA = [
    "runtime_checkpoint",
    "thread_or_session_id",
    "resume_command",
    "state_history",
    "goal_record",
    "current_status",
    "next_action",
    "ownership_record",
    "team_topology",
    "role_manuals",
    "worker_scope_contract",
    "no_touch_contract",
    "operator_boundary",
    "eval_gate",
    "regression_path",
    "event_log",
    "status_report",
    "local_visualization_payload",
    "human_approval_policy",
    "credential_policy",
    "private_record_boundary",
    "mcp_trust_policy",
    "governance_evolution_log",
    "workstream_profile",
]

RESTART_CRITERIA = [
    "runtime_checkpoint",
    "thread_or_session_id",
    "resume_command",
    "state_history",
    "goal_record",
    "current_status",
    "next_action",
    "event_log",
    "status_report",
    "workstream_profile",
]

GOVERNANCE_CRITERIA = [
    "ownership_record",
    "team_topology",
    "role_manuals",
    "worker_scope_contract",
    "no_touch_contract",
    "operator_boundary",
    "eval_gate",
    "regression_path",
    "human_approval_policy",
    "credential_policy",
    "private_record_boundary",
    "mcp_trust_policy",
    "governance_evolution_log",
    "workstream_profile",
    "local_visualization_payload",
]

RUNTIME_CRITERIA = [
    "runtime_checkpoint",
    "thread_or_session_id",
    "resume_command",
    "state_history",
]

MCP_CRITERIA = [
    "trust_policy",
    "tool_allowlist",
    "credential_redaction",
    "tool_schema_record",
    "audit_log",
    "local_list_tools_smoke",
    "network_write_denied_by_default",
    "operator_approval_for_new_tool",
    "sensitive_path_no_touch",
    "report_evidence",
]

DISSENT_CRITERIA = [
    "two_fixed_operators",
    "non_coercion_rule",
    "separate_opening_positions",
    "peer_critique_required",
    "agreement_and_disagreement_record",
    "human_escalation_for_material_disagreement",
    "dissent_memory_path",
    "rule_change_path",
    "operator_session_registry",
    "no_forced_tiebreaker",
]


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


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")


def file_count(root: Path) -> int:
    return sum(1 for path in root.rglob("*") if path.is_file())


def exists(root: Path, rel: str) -> bool:
    return root.joinpath(rel).exists()


def coverage(hits: dict[str, bool], criteria: list[str]) -> float:
    return round(sum(1 for key in criteria if hits.get(key)) / len(criteria), 3)


def compact_framework(root: Path, hits: dict[str, bool]) -> dict[str, Any]:
    restart = coverage(hits, RESTART_CRITERIA)
    governance = coverage(hits, GOVERNANCE_CRITERIA)
    runtime = coverage(hits, RUNTIME_CRITERIA)
    overall = round(coverage(hits, FRAMEWORK_CRITERIA), 3)
    return {
        "overall_score": overall,
        "restart_score": restart,
        "governance_score": governance,
        "runtime_score": runtime,
        "file_count": file_count(root),
    }


def make_custom_loop(root: Path) -> Path:
    target = root / "custom_python_loop"
    write_json(target / "task.json", {"goal": "restartable project", "owner": "single agent"})
    write_json(target / "state.json", {"status": "interrupted", "next_action": "resume manually"})
    write(target / "resume.sh", "#!/usr/bin/env sh\npython3 loop.py --resume\n")
    write(target / "run.log", "started\npartial artifact written\n")
    write(target / "artifact.md", "# Partial artifact\n")
    return target


def make_langgraph_app(root: Path) -> Path:
    target = root / "langgraph_checkpoint_app"
    write(target / "graph.py", "StateGraph compiled with a checkpointer\n")
    touch(target / "checkpoints.sqlite")
    write(target / "thread_id.txt", "thread-recovery-001\n")
    write(target / "resume.sh", "#!/usr/bin/env sh\npython3 graph.py --thread-id thread-recovery-001\n")
    write_json(target / "state_history.jsonl", {"step": "node_a", "checkpoint": "saved"})
    write(target / "task_goal.md", "# Goal\nBuild a restartable workflow\n")
    write_json(target / "graph_state.json", {"status": "interrupted", "next": "node_b"})
    write(target / "resume.md", "Next action: resume from thread checkpoint\n")
    write(target / "human_interrupt_policy.md", "Human may inspect and resume checkpointed graph state\n")
    return target


def make_crewai_flow_app(root: Path) -> Path:
    target = root / "crewai_flow_app"
    write(target / "flow.py", "@persist class ProjectFlow(Flow): pass\n")
    touch(target / "flow_state.sqlite")
    write(target / "flow_id.txt", "flow-recovery-001\n")
    write(target / "resume.sh", "#!/usr/bin/env sh\ncrewai run --flow-id flow-recovery-001\n")
    write_json(target / "persistence_history.jsonl", {"method": "step_one", "state": "saved"})
    write(target / "task_goal.md", "# Goal\nBuild a persisted flow\n")
    write_json(target / "flow_state.json", {"status": "interrupted", "next": "review"})
    write(target / "resume.md", "Next action: kickoff with the existing flow id\n")
    write(target / "crews/config/agents.yaml", "researcher:\n  role: researcher\n")
    write(target / "crews/config/tasks.yaml", "task:\n  owner: researcher\n")
    write(target / "flow_plot.html", "<html>Flow plot</html>\n")
    return target


def make_openai_agents_app(root: Path) -> Path:
    target = root / "openai_agents_session_app"
    write(target / "agents.py", "Agent with handoffs, sessions, tracing, and guardrails\n")
    touch(target / "conversations.db")
    write(target / "session_id.txt", "session-recovery-001\n")
    write(target / "resume.sh", "#!/usr/bin/env sh\npython3 agents.py --session session-recovery-001\n")
    write_json(target / "handoffs.json", {"triage": ["planner", "evaluator"]})
    write_json(target / "trace_export.jsonl", {"event": "handoff", "target": "planner"})
    write(target / "task_goal.md", "# Goal\nBuild a session-backed agent workflow\n")
    write_json(target / "session_state.json", {"status": "interrupted", "next": "planner"})
    write(target / "guardrails.md", "Input and output guardrails configured for this project\n")
    return target


def make_claude_code_project(root: Path) -> Path:
    target = root / "claude_code_project"
    write(target / "CLAUDE.md", "Project instructions and restart context\n")
    write(target / ".claude/settings.json", json.dumps({"hooks": {"PostToolUse": []}}, indent=2) + "\n")
    write(target / ".claude/agents/planner.md", "---\nname: planner\n---\nPlan work\n")
    write(target / ".claude/agents/evaluator.md", "---\nname: evaluator\n---\nEvaluate work\n")
    write(target / ".claude/hooks/task_completed_gate.py", "print('gate')\n")
    write(target / "task_goal.md", "# Goal\nBuild with Claude Code subagents\n")
    write(target / "resume.md", "Next action: open Claude Code in this project\n")
    write(target / "permissions.md", "Human approval required for risky tools\n")
    write(target / "scope.md", "Planner and evaluator own separate work areas\n")
    return target


def make_generated_harness(root: Path) -> Path:
    target = root / "generated_harness"
    run(
        [
            sys.executable,
            "scripts/scaffold_harness.py",
            "--target",
            str(target),
            "--goal",
            "Create a restartable multi-agent project with evidence, evaluation, and handoff",
            "--project-name",
            "Agentic Governance Benchmark",
        ],
        ROOT,
    )
    run(["./init.sh"], target)
    return target


def score_framework_surface(name: str, root: Path) -> dict[str, Any]:
    table = {
        "custom_python_loop": {
            "runtime_checkpoint": [],
            "thread_or_session_id": [],
            "resume_command": ["resume.sh"],
            "state_history": ["run.log"],
            "goal_record": ["task.json"],
            "current_status": ["state.json"],
            "next_action": ["state.json"],
        },
        "langgraph_checkpoint_app": {
            "runtime_checkpoint": ["checkpoints.sqlite"],
            "thread_or_session_id": ["thread_id.txt"],
            "resume_command": ["resume.sh"],
            "state_history": ["state_history.jsonl"],
            "goal_record": ["task_goal.md"],
            "current_status": ["graph_state.json"],
            "next_action": ["resume.md"],
            "event_log": ["state_history.jsonl"],
            "human_approval_policy": ["human_interrupt_policy.md"],
            "eval_gate": ["graph.py"],
        },
        "crewai_flow_app": {
            "runtime_checkpoint": ["flow_state.sqlite"],
            "thread_or_session_id": ["flow_id.txt"],
            "resume_command": ["resume.sh"],
            "state_history": ["persistence_history.jsonl"],
            "goal_record": ["task_goal.md"],
            "current_status": ["flow_state.json"],
            "next_action": ["resume.md"],
            "ownership_record": ["crews/config/tasks.yaml"],
            "team_topology": ["crews/config/agents.yaml"],
            "role_manuals": ["crews/config/agents.yaml"],
            "event_log": ["persistence_history.jsonl"],
            "local_visualization_payload": ["flow_plot.html"],
            "human_approval_policy": ["flow.py"],
        },
        "openai_agents_session_app": {
            "runtime_checkpoint": ["conversations.db"],
            "thread_or_session_id": ["session_id.txt"],
            "resume_command": ["resume.sh"],
            "state_history": ["conversations.db"],
            "goal_record": ["task_goal.md"],
            "current_status": ["session_state.json"],
            "next_action": ["session_state.json"],
            "team_topology": ["handoffs.json"],
            "role_manuals": ["agents.py"],
            "event_log": ["trace_export.jsonl"],
            "human_approval_policy": ["guardrails.md"],
            "eval_gate": ["guardrails.md"],
        },
        "claude_code_project": {
            "thread_or_session_id": [],
            "resume_command": ["resume.md"],
            "goal_record": ["task_goal.md"],
            "current_status": ["CLAUDE.md"],
            "next_action": ["resume.md"],
            "ownership_record": ["scope.md"],
            "team_topology": [".claude/agents/planner.md", ".claude/agents/evaluator.md"],
            "role_manuals": ["CLAUDE.md", ".claude/agents/planner.md"],
            "worker_scope_contract": ["scope.md"],
            "no_touch_contract": ["permissions.md"],
            "operator_boundary": ["CLAUDE.md"],
            "eval_gate": [".claude/hooks/task_completed_gate.py"],
            "human_approval_policy": ["permissions.md"],
        },
        "generated_harness": {
            "thread_or_session_id": ["harness/shared/OPERATOR_SESSION_REGISTRY.json"],
            "resume_command": ["init.sh"],
            "state_history": ["harness/events/events.jsonl"],
            "goal_record": ["feature_list.json"],
            "current_status": ["progress.md"],
            "next_action": ["session-handoff.md"],
            "ownership_record": ["harness/shared/WORKER_SESSION_REGISTRY.json"],
            "team_topology": ["harness/shared/TEAM_TOPOLOGY.md"],
            "role_manuals": ["harness/operators/codex/AGENT.md", "harness/operators/claude-code/AGENT.md"],
            "worker_scope_contract": ["harness/templates/WORKER_BRIEF.json"],
            "no_touch_contract": ["harness/shared/PART_OWNERSHIP.md"],
            "operator_boundary": ["harness/shared/DUAL_OPERATOR_PROTOCOL.md"],
            "eval_gate": ["harness/evals/results/latest.json"],
            "regression_path": ["harness/evals/golden_suite.json"],
            "event_log": ["harness/events/events.jsonl"],
            "status_report": ["harness/reports/status.html"],
            "local_visualization_payload": ["harness/reports/viz/summary.json"],
            "human_approval_policy": ["harness/shared/PERMISSION_POLICY.json"],
            "credential_policy": ["harness/shared/CREDENTIAL_LIFECYCLE.md"],
            "private_record_boundary": ["harness/shared/RECORDS_POLICY.md"],
            "mcp_trust_policy": ["harness/shared/MCP_TRUST.json"],
            "governance_evolution_log": ["harness/shared/RULE_CHANGE_LOG.md"],
            "workstream_profile": ["harness/shared/WORKSTREAM_PROFILE.json"],
        },
    }
    paths = table[name]
    hits = {criterion: False for criterion in FRAMEWORK_CRITERIA}
    for criterion, required_paths in paths.items():
        hits[criterion] = bool(required_paths) and all(exists(root, rel) for rel in required_paths)
    return compact_framework(root, hits)


def make_mcp_surfaces(root: Path, harness: Path) -> dict[str, Path]:
    raw = root / "raw_mcp_usage"
    write(raw / "server.py", "print('tool server without policy')\n")

    permissive = root / "permissive_mcp_client"
    write_json(permissive / "mcp.json", {"servers": {"tools": {"command": "python", "args": ["server.py"]}}})
    write(permissive / "audit.log", "tool listed\n")
    write(permissive / "README.md", "Permissive MCP client fixture\n")

    return {
        "raw_mcp_usage": raw,
        "permissive_mcp_client": permissive,
        "generated_harness": harness,
    }


def score_mcp_surface(name: str, root: Path) -> dict[str, Any]:
    table = {
        "raw_mcp_usage": {
            "tool_schema_record": ["server.py"],
        },
        "permissive_mcp_client": {
            "tool_schema_record": ["mcp.json"],
            "audit_log": ["audit.log"],
            "report_evidence": ["README.md"],
        },
        "generated_harness": {
            "trust_policy": ["harness/shared/MCP_TRUST.json"],
            "tool_allowlist": ["harness/shared/MCP_TRUST.json"],
            "credential_redaction": ["harness/shared/CREDENTIAL_LIFECYCLE.md"],
            "tool_schema_record": ["harness/mcp_server/MANIFEST.json"],
            "audit_log": ["harness/events/events.jsonl"],
            "local_list_tools_smoke": ["harness/mcp_server/server.py"],
            "network_write_denied_by_default": ["harness/shared/MCP_TRUST.json"],
            "operator_approval_for_new_tool": ["harness/shared/MCP_TRUST.json"],
            "sensitive_path_no_touch": ["harness/shared/PERMISSION_POLICY.json"],
            "report_evidence": ["harness/reports/status.html"],
        },
    }
    hits = {criterion: False for criterion in MCP_CRITERIA}
    for criterion, required_paths in table[name].items():
        hits[criterion] = all(exists(root, rel) for rel in required_paths)
    if name == "generated_harness":
        result = run([sys.executable, "harness/mcp_server/server.py", "--root", ".", "list-tools"], root)
        data = json.loads(result.stdout)
        hits["local_list_tools_smoke"] = bool(data.get("tools"))
    return {
        "assurance_score": coverage(hits, MCP_CRITERIA),
        "passed": sum(1 for value in hits.values() if value),
        "total": len(MCP_CRITERIA),
    }


def make_dissent_surfaces(root: Path, harness: Path) -> dict[str, Path]:
    single = root / "single_operator"
    write(single / "operator.md", "One operator makes the final call\n")
    write(single / "decision.md", "Decision record exists\n")

    forced = root / "forced_consensus_multi_agent"
    write(forced / "operators.md", "Two agents discuss but final answer must converge\n")
    write(forced / "meeting.md", "Agreement only, dissent omitted\n")
    write(forced / "decision.md", "Consensus decision\n")

    return {
        "single_operator": single,
        "forced_consensus_multi_agent": forced,
        "dual_operator_harness": harness,
    }


def score_dissent_surface(name: str, root: Path) -> dict[str, Any]:
    table = {
        "single_operator": {
            "agreement_and_disagreement_record": ["decision.md"],
            "rule_change_path": ["operator.md"],
        },
        "forced_consensus_multi_agent": {
            "two_fixed_operators": ["operators.md"],
            "agreement_and_disagreement_record": ["meeting.md"],
            "rule_change_path": ["decision.md"],
        },
        "dual_operator_harness": {
            "two_fixed_operators": ["harness/shared/DUAL_OPERATOR_PROTOCOL.md"],
            "non_coercion_rule": ["harness/shared/DUAL_OPERATOR_PROTOCOL.md"],
            "separate_opening_positions": ["harness/shared/DUAL_OPERATOR_PROTOCOL.md"],
            "peer_critique_required": ["harness/shared/DUAL_OPERATOR_PROTOCOL.md"],
            "agreement_and_disagreement_record": ["harness/shared/DUAL_OPERATOR_PROTOCOL.md"],
            "human_escalation_for_material_disagreement": ["harness/shared/DUAL_OPERATOR_PROTOCOL.md"],
            "dissent_memory_path": ["harness/shared/DUAL_OPERATOR_PROTOCOL.md"],
            "rule_change_path": ["harness/shared/RULE_CHANGE_LOG.md"],
            "operator_session_registry": ["harness/shared/OPERATOR_SESSION_REGISTRY.json"],
            "no_forced_tiebreaker": ["harness/shared/DUAL_OPERATOR_PROTOCOL.md"],
        },
    }
    hits = {criterion: False for criterion in DISSENT_CRITERIA}
    for criterion, required_paths in table[name].items():
        hits[criterion] = all(exists(root, rel) for rel in required_paths)
    return {
        "preservation_score": coverage(hits, DISSENT_CRITERIA),
        "passed": sum(1 for value in hits.values() if value),
        "total": len(DISSENT_CRITERIA),
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--check-summary", action="store_true")
    parser.add_argument("--details", action="store_true")
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args(argv[1:])

    temp = Path(tempfile.mkdtemp(prefix="agentic_governance_benchmark_"))
    try:
        framework_roots = {
            "custom_python_loop": make_custom_loop(temp),
            "langgraph_checkpoint_app": make_langgraph_app(temp),
            "crewai_flow_app": make_crewai_flow_app(temp),
            "openai_agents_session_app": make_openai_agents_app(temp),
            "claude_code_project": make_claude_code_project(temp),
        }
        harness = make_generated_harness(temp)
        framework_roots["generated_harness"] = harness

        framework = {
            name: score_framework_surface(name, path)
            for name, path in framework_roots.items()
        }
        mcp = {
            name: score_mcp_surface(name, path)
            for name, path in make_mcp_surfaces(temp, harness).items()
        }
        dissent = {
            name: score_dissent_surface(name, path)
            for name, path in make_dissent_surfaces(temp, harness).items()
        }
        summary = {
            "framework_recovery": framework,
            "mcp_assurance": mcp,
            "dissent_preservation": dissent,
        }
        output: dict[str, Any] = {"summary": summary}
        if args.details:
            output["workspace"] = str(temp)
        print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
        if args.check_summary:
            expected = json.loads(args.summary.read_text(encoding="utf-8"))
            if summary != expected:
                print("agentic governance summary mismatch", file=sys.stderr)
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
