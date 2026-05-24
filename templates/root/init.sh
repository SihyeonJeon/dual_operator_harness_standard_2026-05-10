#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "=== Harness bootstrap check ==="

python3 scripts/validate_harness.py .

python3 - <<'PY'
import json
from datetime import datetime, timezone
from pathlib import Path

required = [
    "AGENTS.md",
    "feature_list.json",
    "progress.md",
    "session-handoff.md",
    "harness/shared/ACTIVE_SNAPSHOT.md",
    "harness/shared/PROJECT_PROFILE.json",
    "harness/shared/WORKSTREAM_PROFILE.json",
]

missing = [path for path in required if not Path(path).exists()]
if missing:
    raise SystemExit("Missing bootstrap files: " + ", ".join(missing))

features = json.loads(Path("feature_list.json").read_text(encoding="utf-8"))
if not isinstance(features.get("features"), list) or not features["features"]:
    raise SystemExit("feature_list.json must contain at least one feature")

bad = []
for item in features["features"]:
    for key in ["id", "behavior", "verification", "state", "evidence"]:
        if key not in item:
            bad.append(f"{item.get('id', '<unknown>')} missing {key}")
    if item.get("state") == "passing" and not item.get("evidence"):
        bad.append(f"{item.get('id', '<unknown>')} passing without evidence")

if bad:
    raise SystemExit("Feature list errors: " + "; ".join(bad))

now = datetime.now(timezone.utc).isoformat()
mark_f0_active = False
for item in features["features"]:
    if item.get("id") == "H1":
        item["state"] = "passing"
        item["evidence"] = f"./init.sh passed at {now}"
        item["notes"] = "Bootstrap restart path verified by local init check."
        mark_f0_active = True

if mark_f0_active:
    for item in features["features"]:
        if item.get("id") == "F0-PLANNING-RUNWAY" and item.get("state") == "not_started":
            item["state"] = "active"
            item["notes"] = "Active after bootstrap. Fixed operators must run the planning runway and approve a slice before any production work."

Path("feature_list.json").write_text(json.dumps(features, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

progress = Path("progress.md")
if progress.exists():
    text = progress.read_text(encoding="utf-8")
    text = text.replace("- H1 bootstrap restart smoke is `active`.", "- H1 bootstrap restart smoke is `passing`.")
    text = text.replace("H1 - Bootstrap restart path", "F0 - Planning runway and slice gate")
    text = text.replace("- H1 bootstrap restart verification.", "- Planning runway and slice approval gate is pending.")
    text = text.replace("3. Resolve H1 or record the exact blocker.", "3. Run F0 planning runway or record the exact blocker.")
    marker = f"\n## Bootstrap Check {now}\n\n- `./init.sh` passed.\n"
    if "## Bootstrap Check" not in text:
        text += marker
    progress.write_text(text, encoding="utf-8")

handoff = Path("session-handoff.md")
if handoff.exists():
    text = handoff.read_text(encoding="utf-8")
    text = text.replace("- H1 bootstrap restart smoke is `active` and must be verified or blocked with evidence.", "- H1 bootstrap restart smoke is `passing`.")
    if "F0 planning runway and slice gate is `active`." not in text:
        text = text.replace(
            "- Planning runway is pending; first production slice remains a candidate until planning/design/evaluation gates approve it.",
            "- F0 planning runway and slice gate is `active`.\n- First production slice remains a candidate until planning/design/evaluation gates approve it.",
        )
    handoff.write_text(text, encoding="utf-8")

active = Path("harness/shared/ACTIVE_SNAPSHOT.md")
if active.exists():
    text = active.read_text(encoding="utf-8")
    text = text.replace("Current task id: H1-BOOTSTRAP-SMOKE", "Current task id: F0-PLANNING-RUNWAY")
    text = text.replace("- H1 bootstrap restart smoke: `active`", "- H1 bootstrap restart smoke: `passing`")
    if "- F0 planning runway and slice gate: `active`" not in text:
        text = text.replace(
            "- H1 bootstrap restart smoke: `passing`",
            "- H1 bootstrap restart smoke: `passing`\n- F0 planning runway and slice gate: `active`",
        )
    active.write_text(text, encoding="utf-8")

print("PASS: root bootstrap artifacts are present and parseable")
PY

python3 scripts/harnessctl.py event \
  --task-id H1-BOOTSTRAP-SMOKE \
  --trace-id trace_bootstrap \
  --actor init.sh \
  --actor-type hook \
  --event-type gate.pass \
  --verdict PASS \
  --summary "./init.sh bootstrap check passed" \
  --evidence-path "./init.sh"

python3 scripts/harnessctl.py eval-run \
  --task-id H1-BOOTSTRAP-SMOKE \
  --trace-id trace_bootstrap \
  --output harness/evals/results/latest.json

python3 scripts/harnessctl.py viz-export \
  --backend local_file \
  --task-id H1-BOOTSTRAP-SMOKE \
  --trace-id trace_bootstrap

python3 scripts/harnessctl.py eval-run \
  --task-id H1-BOOTSTRAP-SMOKE \
  --trace-id trace_bootstrap \
  --suite harness/evals/public_release_suite.json \
  --output harness/evals/results/public_release.json

python3 scripts/harnessctl.py report

echo "=== Bootstrap check complete ==="
echo "Next: say 'you are operator' to route the current agent through the fixed-operator harness."
