# Reconcile late advice quietly and surface only material live issues

Status: ready-for-agent
State: open
Owning project/module: OMP advisor delivery/completion and primary-session quiet reconciliation
Feasibility: core (quiet completion (no extra final answer) is core session/advisor lifecycle.)
User stories covered: 18, 19, 20

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Scheduling: Schedule issue 01 first; do not alter its shared configuration or measurement environment while it runs. This is not an extra blocking edge or a requirement for a positive pilot result.

## What to build

After Main has completed, assess late advisory findings through a bounded quiet reconciliation path. Coalesce available notes and reuse the dispositions from issue 06. Produce a new user-facing response only for a confirmed material live issue, not because a severity label triggered another primary turn.

A material live issue is an established binding security/acceptance violation or materially incorrect delivered result, not a repeated preference. Quiet assessment can consume model/check work, but assessment alone must not automatically emit another final response.

## Placement / boundaries

“Quiet reconciliation uses the advisor ADR. Coalesce available notes, preserve decisions, and reassess a resolved finding only when new relevant evidence warrants it.”

Extend issue 06's finding identity, reviewed-state applicability, disposition, new-evidence and conversation-epoch contract in the existing session delivery/completion lifecycle. Do not solve this by simply disabling catch-up waits, ignoring all old notes, or preserving every late note until the next user turn. User-stop and reset boundaries remain binding.

## Acceptance criteria

- [ ] A late resolved or refuted finding is assessed without reopening accepted work or creating an unrelated final response; its disposition remains retrievable.
- [ ] A confirmed material live finding can produce a bounded proactive correction. Repeated delivery without new relevant evidence does not repeatedly recheck or re-notify.
- [ ] New relevant evidence can reopen the applicability decision; text deduplication or a fixed age cutoff is not the resolution policy.
- [ ] Observe actual primary evaluation, persisted dispositions, and user-visible output for resolved, refuted, live, repeated, and genuinely changed-evidence cases. A primary-call count alone is insufficient.
- [ ] User-stopped work is not autonomously resumed to assess advice; preserve applicable notes according to that boundary. Reset prevents old-conversation notes/dispositions from leaking into a new conversation.
- [ ] Reconciliation remains bounded and records its cost/work separately from saved catch-up waiting. A failure to reconcile a binding requirement cannot be silently reported as success.

## Blocked by

- [06 — Reconcile current advice and required reviews before acceptance](06-reconcile-current-advice-and-required-reviews-before-acceptance.md)
