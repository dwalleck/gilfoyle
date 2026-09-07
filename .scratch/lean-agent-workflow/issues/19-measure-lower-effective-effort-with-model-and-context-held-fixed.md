# Measure lower effective effort with model and context held fixed

Status: ready-for-agent
State: open
Owning project/module: OMP effective role/effort configuration and bounded request/outcome observation
Feasibility: config (effort setting toggle and observation; no plugin or core source change.)
User stories covered: 1, 4, 21, 22

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Scheduling: Schedule issue 01 first; do not alter its shared configuration or measurement environment while it runs. This is not an extra blocking edge or a requirement for a positive pilot result.

## What to build

Run a separate bounded comparison of lower effective reasoning effort on self-contained work while holding the model, task, acceptance, and relevant context fixed. Establish the effort actually used by provider requests rather than trusting a role name or configured alias.

Prioritize exclusive active elapsed time and human interruptions over cost. Keep the accepted continue-first guidance for dependent work. This experiment does not prescribe mandatory context resets, smaller models, or permanent global compaction/effort changes.

## Placement / boundaries

“OMP effective role/effort selection varies effort for bounded self-contained work while keeping model and context fixed.”

Use existing effective-configuration/request observation and a trustworthy bounded trace. Do not change advisor catch-up or delivery, isolation, context policy, or the model in the same comparison. This is scheduled after the catch-up pilot but does not depend on its outcome; establish and hold the current configuration fixed for this experiment.

## Acceptance criteria

- [ ] Define the bounded comparable task, acceptance, model identity, relevant context, and effective effort baseline before changing the comparison variable.
- [ ] Confirm that the compared requests actually use the same model and different effective effort despite role/override precedence. Inability to establish that difference makes the result inconclusive.
- [ ] Hold other settings and environmental conditions fixed and measure exclusive active elapsed time, clarification, rework, and acceptance; do not add overlapping provider durations.
- [ ] Dependent reasoning remains available where needed. Do not create a handoff/reset requirement merely to make the experiment easier to run.
- [ ] Retain a lower-effort setting only provisionally within the tested scope when latency benefit is not erased by added work and no binding requirement is missed. Roll back on a missed invariant or a net regression.
- [ ] Report an inconclusive outcome without a speedup claim or global rollout. Treat unavailable cost accounting as unavailable, not zero; leave a concise source/input/environment-bound decision record.

## Blocked by

None - can start immediately, subject to the pilot-first scheduling rule above.
