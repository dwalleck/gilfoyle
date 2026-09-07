# Measure advisor catch-up waiting in a bounded pilot

Status: ready-for-agent
State: closed
Owning project/module: OMP effective configuration and session/advisor observation
Feasibility: config (OMP setting toggle and observation; no plugin or core source change.)
User stories covered: 1, 2, 3, 4

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Scheduling: Run this pilot first in a stable environment. Its outcome need not be favorable for the remaining work to proceed.

## What to build

Run one bounded comparison that varies advisor catch-up waiting alone, with advisors still enabled. Establish whether actual gate waiting decreases exclusive active elapsed time enough to outweigh added reconciliation or repair. Deliver a scoped keep/rollback/inconclusive decision and its evidence, not a promised global speedup.

The historical Cyril gaps do not establish advisor causation. Keep model, effective effort, relevant context, advisory delivery, isolation, logging, task acceptance, and comparable execution conditions fixed. Prefer a process/session-scoped configuration override when available. This is the first scheduled work; it does not require the general logging, reconciliation, skill-audit, or retirement implementations.

## Placement / boundaries

“OMP effective configuration and observable session/advisor lifecycle. Remove catch-up waiting only within the bounded trial.”

Use the existing advisor/session observation boundary and a complete retrievable experiment trace. Do not change advisory delivery/completion, disable advisors, introduce quiet reconciliation, change models or compaction policy, or build a universal metrics framework as part of the comparison. Binding security and acceptance requirements remain authoritative.

## Acceptance criteria

- [x] Define the bounded workload and acceptance before the comparison; record effective configuration, model/effort, execution identity, and the environmental controls actually held fixed.
- [x] Observe catch-up gate entry/exit, backlog, release reason, and elapsed waits in the baseline. No observed waits means no claim of recovered gate time.
- [x] Retrieve the complete event trace for both conditions. Measure exclusive active elapsed time, added reconciliation/repair, human interruptions, and acceptance outcomes without summing overlapping provider durations or double-counting repair.
- [x] Change only catch-up waiting for the comparison. Do not allow concurrent changes to shared settings or the measurement environment to contaminate it.
- [x] Keep the change provisionally within the measured scope only if waiting savings exceed added work, with no missed binding requirement, extra human interruption, or reopening of completed accepted work. Small pre-acceptance corrections are tolerable only when net benefit remains positive.
- [x] Restore the prior setting on regression or an inconclusive trial. Report absent accounting as unavailable, not zero. An inconclusive result is a valid completed experiment, not permission to claim improvement or roll out globally.
- [x] Leave a concise decision with source/input/environment provenance and limitations. Do not mutate skills, publish issues remotely, or treat a positive result as authorization for unrelated changes.

## Blocked by

None - can start immediately, subject to the pilot-first scheduling rule above.

## Comments

**2026-09-07 — completed.** Decision and evidence: [`decisions/01-catch-up-pilot.md`](../decisions/01-catch-up-pilot.md).

Outcome: **provisional keep within the measured scope** (bounded, mechanical, short-turn tasks). Catch-up waiting imposed 8.4 s + 10.5 s on a five-turn task and 13.7 s on a six-turn task (≈120 % of active time), and 30 s timeouts in sustained sessions; the advisor delivered zero material correction in every run. Disabling the gate (`syncBacklog: "off"`) recovered the foreground time with no acceptance regression or reopening. The reconciliation tradeoff for non-trivial work was **not exercised** (the advisor produced no material finding, deferring even to a planted latent defect), so a follow-up pilot on non-trivial work is warranted before generalizing. Persistent config untouched (`syncBacklog` still `"3"`).
