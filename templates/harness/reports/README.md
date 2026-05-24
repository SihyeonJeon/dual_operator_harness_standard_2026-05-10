# Reports

Generated reports and external evidence views live here.

Default local report:

```sh
python3 scripts/harnessctl.py report
```

Default local event export for a viz backend worker:

```sh
python3 scripts/harnessctl.py viz-export --backend local_file
```

Reports are compiled views over canonical harness files. They are not canonical
memory and must not override `feature_list.json`, `progress.md`,
`session-handoff.md`, `harness/shared/`, `harness/tasks/`, or
`harness/events/events.jsonl`.

The report UI and any diagram/timeline/information architecture are
Claude-owned design surfaces. Worker implementation should follow an approved
task-local `VISUALIZATION_SPEC.md`.

External evidence drafts belong in `harness/broadcast/`, not directly in
reports. Publication requires `harness/broadcast/BROADCAST_POLICY.md`.
