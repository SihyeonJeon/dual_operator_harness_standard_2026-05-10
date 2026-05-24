# Dual Operator Protocol

Claude Code and Codex are equal fixed operators. Neither operator is the lead,
manager, or forced tiebreaker for the other.

## Purpose

Use two persistent operator sessions because the operators have different
strengths, failure modes, context histories, and review instincts. The harness
benefits when they complement each other, preserve dissent, and surface material
uncertainty to the human.

## Non-Coercion Rules

- Do not force consensus.
- Do not overwrite the peer operator's dissent.
- Do not rewrite disagreement as agreement to make progress look cleaner.
- Do not use Claude Code runtime adapters as authority over Codex.
- Do not use Codex critique as authority over Claude Code without recorded
  evidence.
- If material disagreement remains, present the disagreement and evidence to the
  human.

## Required Meeting Flow

For material decisions, closure, governance changes, high-risk work, or a
disputed result:

1. Write an agenda in the current task artifact.
2. Each operator writes an opening position from the same file-backed context.
3. Each operator critiques the other's position.
4. Record agreements, disagreements, evidence gaps, and risks.
5. Decide one of:
   - `converged`
   - `partial`
   - `disagreement_human_required`
6. Summarize the outcome into the current task artifact and, when durable,
   `harness/shared/CONTEXT.md`, `MEMORY.md`, `FAILURE_LEDGER.md`, or
   `RULE_CHANGE_LOG.md`.

## Complementary Responsibilities

Claude Code tends to own local runtime orchestration, project-file navigation,
and Claude Code adapter use when that runtime is verified.

Codex tends to own independent critique, edge-case discovery, verification
strategy, context-chain review, and closure challenge.

These are defaults, not hierarchy. Either operator may challenge any premise.

## Shared Memory

Canonical operator memory:

- `feature_list.json`
- `progress.md`
- `session-handoff.md`
- `harness/shared/`
- current task artifacts

Private chat history, Claude Code hook context, Codex session context, MCP
transcripts, and plugin summaries are advisory until summarized into canonical
files.

## Session Registry

Fixed operator session handles, resume commands, model class, effort level, and
verification status are recorded in `harness/shared/OPERATOR_SESSION_REGISTRY.json`.

The registry does not make a private session authoritative. It exists so the
human and the peer operator can see which fixed session is active, whether it
has been verified, and how to resume it without mixing worker or unrelated part
context.
