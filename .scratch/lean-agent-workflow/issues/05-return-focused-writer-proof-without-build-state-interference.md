# Return focused writer proof without build-state interference

Status: ready-for-agent
State: open
Owning project/module: OMP task-tool instructions and controlled writer execution policy
Feasibility: plugin (system-prompt/instructions override of the validation ban; controlled build state overlaps issue 02.)
User stories covered: 13, 14

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Scheduling: Schedule issue 01 first; do not alter its shared configuration or measurement environment while it runs. This is not an extra blocking edge or a requirement for a positive pilot result.

## What to build

Allow isolated writers to perform their focused slice proof and return its actual result before handoff. Replace the blanket concurrent-validation ban at its owning harness layer. Keep Main responsible for assembled cross-change, quality, and platform acceptance.

Source isolation alone is insufficient: commands must not interfere through shared mutable build/runtime state. Use separate state where supported and serialize operations that necessarily share it. A writer unable to run required proof returns unverified work, not PASS.

## Placement / boundaries

“OMP task-tool instructions and execution policy permit focused checks for isolated writers. Replace the blanket concurrent-validation prohibition; Main retains assembled-proof ownership.”

Do not add a Gilfoyle exception that contradicts a still-binding harness instruction. Use existing task execution controls and project-supported build/runtime isolation, not a new universal build framework. Preserve writer authority boundaries and do not require every worker to repeat the full assembled gate.

## Acceptance criteria

- [ ] The effective instructions in a fresh harness execution permit the intended focused checks for isolated writers; remove conflicting blanket-ban callers rather than only editing an unused prompt.
- [ ] A plausible fixture/type/API failure is detected and reported by the writer before integration, and the corrected slice supplies applicable focused proof against its baseline.
- [ ] Concurrent writers with independent state do not corrupt each other; commands sharing mutable build/runtime state are controlled rather than competing blindly.
- [ ] Missing execution capability, failed checks, and incomplete proof remain explicit. No consumer equates a worker result with assembled acceptance.
- [ ] Main exercises the applicable assembled quality/platform/cross-change requirements once the combined state is ready, retaining valid existing proof where appropriate.
- [ ] Demonstrate the actual task-to-proof handoff and record time-to-first-failure, repair rounds, and peak workspace/build resource use. Do not claim all historical Main repair work would have been avoided.

## Blocked by

None - can start immediately, subject to the pilot-first scheduling rule above.
