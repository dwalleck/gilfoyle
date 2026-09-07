# Run affected compatibility fences before broad repair qualification

Status: ready-for-agent
State: open
Owning project/module: Portable change-scoped verification guidance and Tethys compatibility qualification recipe
Feasibility: skill (portable change-scoped guidance plus Tethys recipe; not OMP core.)
User stories covered: 30

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Scheduling: Schedule issue 01 first; do not alter its shared configuration or measurement environment while it runs. This is not an extra blocking edge or a requirement for a positive pilot result.

Related slices: [14 — Reject missing CI baseline inputs before expensive qualification](14-reject-missing-ci-baseline-inputs-before-expensive-qualification.md); [16 — Collect the complete independent native diagnostic roster](16-collect-the-complete-independent-native-diagnostic-roster.md)

## What to build

For a cross-cutting repair, identify the existing behavior contracts it touches and run their cheapest established compatibility fences before broad repair qualification. Use the Tethys Rust logical/external-target versus C# physical-containment identity boundary as the concrete end-to-end path.

The historical global identity repair broke an existing passing Rust surface. This slice improves discovery order, not that already-recorded production fix. Reuse any current capability that already meets the contract; do not introduce a redundant framework or weaken established behavior to obtain a green result.

## Placement / boundaries

“Select early checks from the affected contracts and the next gate's required inputs: for example, existing language-specific identity behavior, fixture/API compatibility, pinned baseline availability in CI, active oracle stage, or target storage when relevant.”

Own generic selection guidance in the portable workflow and the concrete execution recipe with the project. Reuse the plan/evidence surface and existing fences; do not create a universal contract matrix or mandate a new worktree for every check. The missing-CI-baseline executable path belongs to issue 14.

## Acceptance criteria

- [ ] The chosen repair path identifies the existing language-specific contracts before applying a broad identity policy and selects the established fast fences that discriminate them.
- [ ] A controlled incompatible change on an isolated test state is rejected by the relevant compatibility fence before dependent broad qualification; restore the source without weakening the fence.
- [ ] Rust logical/external-target behavior and C# physical containment remain distinct where the approved design requires it. A generic hardening rule does not supersede the existing domain contract.
- [ ] Relevant existing checks and valid evidence are reused; unrelated checks and new mandatory planning fields are not added to every slice.
- [ ] Demonstrate the workflow ordering and actual compatibility outcome, then perform the required final acceptance on the stable repaired state. Do not substitute helper wiring or prompt-wording tests.
- [ ] Measure discovery/repair cycles and time to first actionable incompatibility; do not claim the historical test/build timing is the exact saving for all future work.

## Blocked by

None - can start immediately, subject to the pilot-first scheduling rule above.
