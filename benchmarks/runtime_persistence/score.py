#!/usr/bin/env python3
"""Run optional live dependency smoke tests for runtime persistence APIs."""

from __future__ import annotations

import argparse
import asyncio
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SUMMARY = Path(__file__).resolve().parent / "expected_summary.json"

CRITERIA = [
    "dependency_imported",
    "no_llm_api_call",
    "state_id_or_thread_id",
    "state_after_first_run",
    "resume_or_reload",
    "history_or_items_available",
    "durable_file_or_checkpointer",
    "no_network_required",
    "native_runtime_api",
    "observable_output",
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


def missing_dependency(name: str, exc: BaseException) -> None:
    raise SystemExit(
        f"missing optional dependency for {name}: {exc}\n"
        "Run with:\n"
        "uv run --python 3.12 --with langgraph --with crewai --with openai-agents "
        "python benchmarks/runtime_persistence/score.py --check-summary"
    )


def compact(hits: dict[str, bool]) -> dict[str, Any]:
    passed = sum(1 for criterion in CRITERIA if hits.get(criterion))
    total = len(CRITERIA)
    return {
        "score": round(passed / total, 3),
        "passed": passed,
        "total": total,
    }


def langgraph_smoke() -> dict[str, Any]:
    try:
        from typing_extensions import TypedDict
        from langgraph.checkpoint.memory import InMemorySaver
        from langgraph.graph import END, START, StateGraph
    except Exception as exc:  # pragma: no cover - dependency boundary
        missing_dependency("langgraph", exc)

    class State(TypedDict):
        step: int
        log: list[str]

    def node_a(state: State) -> State:
        return {"step": state["step"] + 1, "log": state["log"] + ["a"]}

    def node_b(state: State) -> State:
        return {"step": state["step"] + 1, "log": state["log"] + ["b"]}

    builder = StateGraph(State)
    builder.add_node("a", node_a)
    builder.add_node("b", node_b)
    builder.add_edge(START, "a")
    builder.add_edge("a", "b")
    builder.add_edge("b", END)
    graph = builder.compile(checkpointer=InMemorySaver())
    config = {"configurable": {"thread_id": "runtime-smoke"}}
    result = graph.invoke({"step": 0, "log": []}, config)
    history = list(graph.get_state_history(config))
    hits = {
        "dependency_imported": True,
        "no_llm_api_call": True,
        "state_id_or_thread_id": True,
        "state_after_first_run": result.get("step") == 2,
        "resume_or_reload": len(history) >= 2,
        "history_or_items_available": len(history) >= 2,
        "durable_file_or_checkpointer": True,
        "no_network_required": True,
        "native_runtime_api": True,
        "observable_output": result.get("log") == ["a", "b"],
    }
    return compact(hits)


def crewai_smoke() -> dict[str, Any]:
    try:
        from crewai.flow.flow import Flow, listen, start
        from crewai.flow.persistence import persist
    except Exception as exc:  # pragma: no cover - dependency boundary
        missing_dependency("crewai", exc)

    os.environ.setdefault("CREWAI_TRACING_ENABLED", "false")

    @persist()
    class CounterFlow(Flow[dict]):
        @start()
        def first(self) -> int:
            self.state["counter"] = self.state.get("counter", 0) + 1
            return self.state["counter"]

        @listen(first)
        def second(self, value: int) -> int:
            self.state["counter"] = value + 1
            return self.state["counter"]

    captured = io.StringIO()
    with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
        flow = CounterFlow()
        first_result = flow.kickoff()
        state_id = flow.state["id"]
        resumed = CounterFlow()
        second_result = resumed.kickoff(inputs={"id": state_id})

    hits = {
        "dependency_imported": True,
        "no_llm_api_call": True,
        "state_id_or_thread_id": bool(state_id),
        "state_after_first_run": first_result == 2,
        "resume_or_reload": second_result == 4 and resumed.state.get("id") == state_id,
        "history_or_items_available": False,
        "durable_file_or_checkpointer": True,
        "no_network_required": True,
        "native_runtime_api": True,
        "observable_output": "Flow" in captured.getvalue(),
    }
    return compact(hits)


async def openai_agents_async(temp: Path) -> dict[str, Any]:
    try:
        from agents import SQLiteSession
    except Exception as exc:  # pragma: no cover - dependency boundary
        missing_dependency("openai-agents", exc)

    db_path = temp / "agents-session.db"
    session = SQLiteSession("runtime-smoke", str(db_path))
    await session.add_items(
        [
            {"role": "user", "content": "record state"},
            {"role": "assistant", "content": "state recorded"},
        ]
    )
    first_items = await session.get_items()
    reloaded = SQLiteSession("runtime-smoke", str(db_path))
    second_items = await reloaded.get_items()
    hits = {
        "dependency_imported": True,
        "no_llm_api_call": True,
        "state_id_or_thread_id": True,
        "state_after_first_run": len(first_items) == 2,
        "resume_or_reload": second_items == first_items,
        "history_or_items_available": len(second_items) == 2,
        "durable_file_or_checkpointer": db_path.exists(),
        "no_network_required": True,
        "native_runtime_api": True,
        "observable_output": second_items[-1]["content"] == "state recorded",
    }
    return compact(hits)


def openai_agents_smoke(temp: Path) -> dict[str, Any]:
    return asyncio.run(openai_agents_async(temp))


def generated_harness_smoke(temp: Path) -> dict[str, Any]:
    target = temp / "generated_harness"
    run(
        [
            sys.executable,
            "scripts/scaffold_harness.py",
            "--target",
            str(target),
            "--goal",
            "Create a runtime persistence smoke project with restart evidence",
            "--project-name",
            "Runtime Persistence Smoke",
        ],
        ROOT,
    )
    run(["./init.sh"], target)
    hits = {
        "dependency_imported": True,
        "no_llm_api_call": True,
        "state_id_or_thread_id": (target / "harness/shared/OPERATOR_SESSION_REGISTRY.json").exists(),
        "state_after_first_run": (target / "feature_list.json").exists(),
        "resume_or_reload": (target / "session-handoff.md").exists(),
        "history_or_items_available": (target / "harness/events/events.jsonl").exists(),
        "durable_file_or_checkpointer": (target / "feature_list.json").exists(),
        "no_network_required": True,
        "native_runtime_api": False,
        "observable_output": (target / "harness/reports/status.html").exists(),
    }
    return compact(hits)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--check-summary", action="store_true")
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args(argv[1:])

    temp = Path(tempfile.mkdtemp(prefix="runtime_persistence_smoke_"))
    try:
        summary = {
            "langgraph_memory_checkpointer": langgraph_smoke(),
            "crewai_persist_flow": crewai_smoke(),
            "openai_agents_sqlite_session": openai_agents_smoke(temp),
            "generated_harness": generated_harness_smoke(temp),
        }
        output = {"summary": summary}
        print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
        if args.check_summary:
            expected = json.loads(args.summary.read_text(encoding="utf-8"))
            if summary != expected:
                print("runtime persistence summary mismatch", file=sys.stderr)
                print("expected:", json.dumps(expected, ensure_ascii=False, sort_keys=True), file=sys.stderr)
                print("actual:", json.dumps(summary, ensure_ascii=False, sort_keys=True), file=sys.stderr)
                return 1
        return 0
    finally:
        if args.keep:
            print(f"kept smoke workspace at {temp}", file=sys.stderr)
        else:
            shutil.rmtree(temp)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
