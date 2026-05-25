#!/usr/bin/env python3
"""Score the public date-normalization benchmark predictions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_CASES = ROOT / "cases.jsonl"
DEFAULT_PREDICTIONS = ROOT / "predictions"
DEFAULT_SUMMARY = ROOT / "expected_summary.json"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{line_no}: invalid JSONL row: {exc}") from exc
        if not isinstance(row, dict):
            raise SystemExit(f"{path}:{line_no}: row is not an object")
        rows.append(row)
    return rows


def rows_by_id(path: Path, key: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for row in read_jsonl(path):
        row_id = row.get("id")
        value = row.get(key)
        if not isinstance(row_id, str) or not row_id:
            raise SystemExit(f"{path}: row missing string id")
        if not isinstance(value, str) or not value:
            raise SystemExit(f"{path}: row {row_id} missing string {key}")
        if row_id in result:
            raise SystemExit(f"{path}: duplicate id {row_id}")
        result[row_id] = value
    return result


def score(cases_path: Path, predictions_path: Path) -> dict[str, Any]:
    expected = rows_by_id(cases_path, "date")
    predicted = rows_by_id(predictions_path, "date")
    missing = sorted(set(expected) - set(predicted))
    extra = sorted(set(predicted) - set(expected))
    if missing or extra:
        raise SystemExit(
            f"{predictions_path}: id mismatch missing={missing or 'none'} extra={extra or 'none'}"
        )

    errors = []
    correct = 0
    case_text = {row["id"]: row["text"] for row in read_jsonl(cases_path)}
    for row_id in sorted(expected):
        if predicted[row_id] == expected[row_id]:
            correct += 1
            continue
        errors.append(
            {
                "id": row_id,
                "expected": expected[row_id],
                "predicted": predicted[row_id],
                "text": case_text.get(row_id, ""),
            }
        )
    total = len(expected)
    return {
        "correct": correct,
        "total": total,
        "accuracy": correct / total if total else 0.0,
        "errors": errors,
    }


def compact_summary(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "correct": result["correct"],
        "total": result["total"],
        "accuracy": result["accuracy"],
        "errors": len(result["errors"]),
    }


def all_prediction_paths(predictions_dir: Path) -> dict[str, Path]:
    return {
        "codex_goal": predictions_dir / "codex_goal.jsonl",
        "harness_first_pass": predictions_dir / "harness_first_pass.jsonl",
        "harness_feedback_loop": predictions_dir / "harness_feedback_loop.jsonl",
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--predictions", type=Path)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--check-summary", action="store_true")
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    args = parser.parse_args(argv[1:])

    if args.all == bool(args.predictions):
        parser.error("use exactly one of --all or --predictions")

    if args.all:
        results = {
            name: compact_summary(score(args.cases, path))
            for name, path in all_prediction_paths(DEFAULT_PREDICTIONS).items()
        }
        print(json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True))
        if args.check_summary:
            expected = json.loads(args.summary.read_text(encoding="utf-8"))
            if results != expected:
                print("benchmark summary mismatch", file=sys.stderr)
                print("expected:", json.dumps(expected, ensure_ascii=False, sort_keys=True), file=sys.stderr)
                print("actual:", json.dumps(results, ensure_ascii=False, sort_keys=True), file=sys.stderr)
                return 1
        return 0

    result = score(args.cases, args.predictions)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
