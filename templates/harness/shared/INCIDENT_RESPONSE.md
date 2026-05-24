# Incident Response

Use when an agent, tool, MCP server, cloud lane, credential, memory entry, or
generated artifact may have violated the harness contract.

## Immediate Actions

1. Pause active workers.
2. Disable suspected tool, MCP server, plugin, cloud lane, or hook.
3. Preserve evidence under the task `evidence/` directory.
4. Revoke or rotate affected credentials.
5. Mark affected memory/context entries as suspect.
6. Notify the human with a short incident packet.

## Recovery

1. Identify root cause.
2. Roll back affected artifacts when possible.
3. Add a failure ledger entry.
4. Add a prevention rule or linter/schema/eval when practical.
5. Require human approval before resuming the affected capability.
