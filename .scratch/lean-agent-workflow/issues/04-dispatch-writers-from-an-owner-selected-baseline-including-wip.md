# Dispatch writers from an owner-selected baseline including WIP

Status: ready-for-agent
State: open
Owning project/module: OMP dispatch/source selection and retained-result integration contract
Feasibility: core (worker baseline is derived in dispatch from the launch checkout; no field or event exposes selection.)
User stories covered: 9, 10

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Scheduling: Schedule issue 01 first; do not alter its shared configuration or measurement environment while it runs. This is not an extra blocking edge or a requirement for a positive pilot result.

## What to build

Let the integration owner select the identified baseline a worker must receive, including deliberately selected uncommitted work while excluding unrelated WIP. Carry that selection through materialization, worker execution, retained delta capture, and application to the intended target.

A baseline mentioned only in task prose is not an execution contract. Consume the retained handoff established by issue 03; the worker result must remain attributable to the state actually selected, even if the launching checkout subsequently changes.

## Placement / boundaries

“OMP dispatch/source selection and result lifecycle identify the intended integration baseline and retained delta. Main applies it to the declared target.”

Replace implicit launch-checkout selection at the owning source-selection boundary, not with nested clean worktrees constructed by each caller. Extend the existing retained-result identity rather than inventing another transfer format. Main selects and integrates; workers do not edit another owner's target. An unprovable or conflicting baseline must not silently proceed.

## Acceptance criteria

- [ ] The owner can select an identified committed baseline and an intended snapshot containing selected tracked/untracked WIP; the selection is consumed by execution, not merely included in a prompt.
- [ ] The child receives required prerequisites and does not inherit unrelated WIP. The retained delta contains only worker-owned changes relative to that selected baseline.
- [ ] Materialization either establishes the selected state consistently or reports a mismatch before worker mutation. Changes to the launching checkout cannot silently alter an already-selected baseline.
- [ ] The selected identity survives background delivery and teardown and remains associated with the declared integration target through the issue 03 handoff.
- [ ] Exercise dispatch with selected versus unrelated WIP, a parent-change case, and wrong-target/conflict handling in real temporary repositories; preserve unrelated contents and index state.
- [ ] Migrate affected callers and remove normal nested-checkout repair or prose-only selection conventions. Do not add unrelated retry policy or imply that workspace separation itself enforces every security restriction.

## Blocked by

- [03 — Integrate retained worker results through an explicit owner handoff](03-integrate-retained-worker-results-through-an-explicit-owner-handoff.md)
