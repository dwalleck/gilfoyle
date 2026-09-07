# Reject missing CI baseline inputs before expensive qualification

Status: ready-for-agent
State: open
Owning project/module: ResourceFS CI checkout setup and gate prerequisite entrypoint; applicable portable workflow guidance
Feasibility: project (ResourceFS checkout/gate plus portable guidance; not OMP.)
User stories covered: 30

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Scheduling: Schedule issue 01 first; do not alter its shared configuration or measurement environment while it runs. This is not an extra blocking edge or a requirement for a positive pilot result.

Related slices: [15 — Run affected compatibility fences before broad repair qualification](15-run-affected-compatibility-fences-before-broad-repair-qualification.md)

## What to build

Establish the pinned baseline required by the ResourceFS module-placement fence before launching dependent expensive qualification. Make the normal hosted checkout supply the required input, and make the gate report a missing baseline early if the environment is incomplete.

The historical failure was a deterministic missing input discovered after a 20m48s hosted job, not established test flakiness. Deliver this concrete checkout-to-prerequisite-to-gate path without weakening the fence or requiring an unrelated checklist on every slice.

## Placement / boundaries

“Portable workflow guidance and owning project gate entrypoints select cheap existing compatibility and prerequisite checks from the actual change.”

Own executable behavior in ResourceFS CI checkout and the existing gate entrypoint. Portable guidance should express the scoped ordering rule, not reimplement the project checker or require all projects to fetch all history. Preserve the oracle and explicit source identity. Compatibility selection is separately covered by issue 15.

## Acceptance criteria

- [ ] A shallow test checkout missing the pinned baseline reports that specific prerequisite failure before dependent expensive build/test/scale qualification starts.
- [ ] The normal CI checkout supplies the baseline the active fence actually requires, without assuming a commit mentioned in prose is present.
- [ ] With the input present, the unchanged fence and intended dependent gates execute normally. No missing input is converted to a skip, N/A, or passing fence.
- [ ] Exercise the real checkout/gate boundary using temporary Git repositories and command outcomes, not source-string assertions or a mock that only echoes the expected ordering.
- [ ] The early check is relevant to this gate and does not impose the entire historical preflight recommendation on every task.
- [ ] Record time to actionable failure and avoided dependent launches; retain the historical duration as context rather than an exact savings claim.

## Blocked by

None - can start immediately, subject to the pilot-first scheduling rule above.
