# Consolidate stacked-merge guidance against verified protocol behavior

Status: ready-for-agent
State: open
Owning project/module: Managed async stacked-PR merge guides and their referencing callers
Feasibility: managed-skill (managed merge guides; not OMP.)
User stories covered: 26

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Scheduling: Schedule issue 01 first; do not alter its shared configuration or measurement environment while it runs. This is not an extra blocking edge or a requirement for a positive pilot result.

Related slices: [11 — Publish durable evidence references under one scoped authorization](11-publish-durable-evidence-references-under-one-scoped-authorization.md); [17 — Audit managed skills and repair unsupported workflow obligations](17-audit-managed-skills-and-repair-unsupported-workflow-obligations.md)

## What to build

Converge the two overlapping async stacked-PR merge guides on one maintained protocol adapter after verifying the authoritative direct and queued merge semantics. Preserve the richer safety coverage and migrate callers to the canonical guidance.

The inspected guides disagree on queue guidance; neither argument is accepted merely because it appears in a skill. Historical loading of both guides was not established. This issue is protocol verification plus a complete guidance cutover, not an assertion that both ran repeatedly in the audited session.

## Placement / boundaries

“Consolidate merge guidance only after verifying protocol equivalence and queue arguments against primary API evidence. Preserve exact-head checks, lower-stack targeting, dependent-branch safeguards, queue rules, and confirmation of the terminal merged state.”

Own the change in the managed skill library and actual referencing callers. Do not create another adapter, keep contradictory aliases, change branch protection to make a demonstration easier, or replace verified native protocol facts with remembered CLI behavior. Use managed-skill tooling for managed content.

## Acceptance criteria

- [ ] Gather primary API evidence for the supported asynchronous direct/queued operations and establish the correct arguments and result/terminal-state handling; unresolved semantics remain explicit rather than guessed.
- [ ] The canonical guide describes the complete authorized operation, including current-head checks, lower-stack target, dependent-branch preservation, queue handling, failure reporting, and terminal merge confirmation.
- [ ] Migrate affected references and retire the redundant managed guidance without leaving a competing active recipe or stale caller pointing to the retired name.
- [ ] Demonstrate the supported direct and queued paths through an authorized test surface or appropriate consumer-level protocol harness; reject stale-head/unsafe-stack inputs and do not equate request acceptance with terminal merge success.
- [ ] Preserve scoped shipping authorization and required CI/protection. Creating remote PRs, changing protection, or merging unrelated live work is not implicitly authorized by this ticket.
- [ ] Record verified semantics and cutover coverage concisely; do not claim historical cost savings from the mere existence of duplicate guides.

## Blocked by

None - can start immediately, subject to the pilot-first scheduling rule above.
