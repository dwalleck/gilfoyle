# Show compact progress without losing current ownership or blockers

Status: ready-for-agent
State: open
Owning project/module: OMP task/job progress presentation and its existing authoritative state
Feasibility: plugin (tool_result rewrite plus full-view custom tool; no core change.)
User stories covered: 32

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Scheduling: Schedule issue 01 first; do not alter its shared configuration or measurement environment while it runs. This is not an extra blocking edge or a requirement for a positive pilot result.

Related slices: [11 — Publish durable evidence references under one scoped authorization](11-publish-durable-evidence-references-under-one-scoped-authorization.md)

## What to build

Return compact progress updates that show changed ownership, blockers, and acceptance state without routinely replaying a large cross-phase task tree. Preserve a full view on demand, backed by the same authoritative state.

This is a complete state-transition-to-consumer-presentation path, not a reduction in the obligations themselves. A settled worker job must not silently turn an unverified or blocked issue into accepted work.

## Placement / boundaries

“Progress updates derive from existing owning task/job state and expose changed ownership, blocking conditions, and acceptance state without routinely replaying the full cross-phase tree. Keep a full view available on demand.”

Reuse existing task/job state and presentation ownership; do not create a second progress ledger or independently editable summary. The reference-based publication change belongs to issue 11 and is not required to make task updates coherent. Do not pin wording, exact transcript size, or internal field forwarding in tests.

## Acceptance criteria

- [ ] An ownership change, block/unblock transition, and acceptance-state change each produce a compact update reflecting the authoritative current state.
- [ ] The explicit full view agrees with those updates and still exposes all required outstanding work; compact output does not drop tasks or hide blockers.
- [ ] Worker settlement, missing proof, and actual integration acceptance remain distinguishable; display simplification does not invent completion.
- [ ] Exercise real task/job state transitions through the consumer-visible update and full-view interfaces, including a sufficiently large task tree to expose routine replay.
- [ ] Measure output volume and stale-view/correction occurrences without claiming that every prior tool call was unnecessary or that shorter text alone proves a speedup.

## Blocked by

None - can start immediately, subject to the pilot-first scheduling rule above.
