---
name: gilfoyle-workflow
description: Root-only Pi orchestration for the local Gilfoyle workflow. Use for non-trivial feature work requiring signed specification, probe, falsifiable design, budgeted plan, checkpointed implementation, bounded review, and human escalation on falsification.
---

# gilfoyle-workflow

The root Pi session owns this workflow. Never delegate orchestration to a child.

## Invariants

- Run data is versioned JSON under `.gilfoyle/runs/<feature-slug>/`; Markdown is not authoritative.
- Refuse autonomous launch unless Git is on an attached branch and tracked/untracked state is clean except ignored run data.
- Validate every result against its `.pi/schemas/` contract, current run ID, signed-spec digest, acceptance evidence, and lifecycle IDs.
- Launch every leaf with `async: true`, its declared timeout, and fresh artifact-driven context; use `wait()`, never sleep or status polling.
- Leaf agents never receive `subagent`; `gilfoyle-implementer` is the sole production writer.

## State machine

1. Run `interrogated-spec` interactively and record confirmation text, UTC timestamp, and SHA-256 before autonomous work.
2. Launch `gilfoyle-prober` with a 30-minute timeout. `CONTINUE` advances; any other decision routes below.
3. Launch `gilfoyle-designer` with a 30-minute timeout after accepted probe evidence.
4. Run saved chain `gilfoyle-plan-audit` with a 30-minute planning timeout; fanout is at most 12, concurrency 4.
5. Launch one `gilfoyle-implementer` with a 90-minute timeout; it commits one fully gated slice at a time.
6. Launch a fresh `gilfoyle-gatekeeper` with a 45-minute timeout.
7. `ALL_GREEN` completes. Eligible Class-A `NEEDS_WORK` increments the root-owned counter and repeats build then gate, at most five times.
8. Class B, out-of-slice work, oracle/check contradiction, stale evidence, timeout, failed acceptance, or ambiguity stops downstream launch as `HALT_FALSIFIED` or `NEEDS_DECISION`.
9. On retry exhaustion, initialize Rivets when needed, update a matching ticket or create one, persist its ID, and halt for non-convergence.
10. When PR feedback arrives, run `gilfoyle-review-feedback`: verify findings read-only, collect accept/modify decisions, use one writer, then one fresh gate.

## Evidence and completion

After each child, reconcile pi-subagents `status.json` and `events.jsonl` with the structured result before changing state. Persist artifact hashes, commands, exit codes, expected/actual outputs, commit SHA, acceptance provenance, and terminal reason. A child completion message alone never advances the workflow.
