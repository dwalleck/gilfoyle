# Integrate retained worker results through an explicit owner handoff

Status: ready-for-agent
State: open
Owning project/module: OMP task result lifecycle, retained artifacts, and Main integration handoff
Feasibility: core (retained artifact lifecycle lives in dispatch/isolation/job-manager; no hook/event exposes it.)
User stories covered: 11, 12

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Scheduling: Schedule issue 01 first; do not alter its shared configuration or measurement environment while it runs. This is not an extra blocking edge or a requirement for a positive pilot result.

Related slices: [04 — Dispatch writers from an owner-selected baseline including WIP](04-dispatch-writers-from-an-owner-selected-baseline-including-wip.md); [18 — Retire owned temporary workspaces without losing retained work](18-retire-owned-temporary-workspaces-without-losing-retained-work.md)

## What to build

Deliver a retained worker result that the integration owner can inspect and explicitly apply to its declared target after the worker workspace is gone. Remove normal reliance on temporary patch paths and implicit automatic application. Worker success is not integration acceptance.

The shared handoff contract must identify the retained output, actual baseline, owned delta, intended integration target, and integration outcome. This slice can use the existing dispatch baseline, but must make its identity explicit. Owner selection of a different baseline or selected WIP is the subsequent baseline-selection issue. Manual-worktree retirement will consume this same retained-output contract.

## Placement / boundaries

“OMP dispatch/source selection and result lifecycle identify the intended integration baseline and retained delta. Main applies it to the declared target.”

Own this in the existing task/result/artifact and Main integration interfaces. Do not create a second patch-transfer protocol or leave an implicit-apply path as the normal workflow. Source selection is extended separately; this slice must not claim to have implemented deliberate WIP selection. Retained output and disposable workspace lifetimes remain distinct.

## Acceptance criteria

- [ ] A completed writer returns an authoritative retained result whose output and baseline/target identity remain retrievable after actual child cleanup and workspace teardown.
- [ ] Main explicitly applies the owned delta to the declared target. A successful worker does not silently apply its work or mark the assembled result accepted.
- [ ] Both ordinary and background result delivery lead to the same retained handoff; the consumer does not need a path inside the destroyed workspace.
- [ ] Applying a fresh delta preserves unrelated target work; an already-applied delta is handled accurately; a conflict preserves target contents/index and the retained result for resolution.
- [ ] An unavailable, incomplete, or wrong-target handoff produces an explicit unverified/conflict result rather than fallback application or success. Do not erase recoverable output merely because integration failed.
- [ ] Update all affected producers and consumers to the single handoff contract. Prove dispatch/result delivery through real teardown and integration using temporary repositories, not only a mocked cleanup promise.
- [ ] Document the retained-result contract for the dependent baseline-selection and workspace-retirement issues, including who owns integration acceptance.

## Blocked by

None - can start immediately, subject to the pilot-first scheduling rule above.
