# Close the remaining portable-skill gaps found by the PR #1–#14 review survey

Status: ready-for-agent
State: open
Owning project/module: Portable Gilfoyle skill (`skills/gilfoyle/references/`)
Feasibility: skill (portable guidance only; no runner or harness change.)
User stories covered: 6, 14, 24, 30

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Evidence base: `resourcefs/docs/research/pr1-code-review-2026-09-06.md`, `pr10-code-review-2026-09-08.md`, `pr12-code-review-2026-09-10.md`, `pr13-code-review-2026-09-11.md`, `pr13-rereview-2026-09-11.md`, `pr14-code-review-2026-09-11.md`, `ci-platform-failures-2026-09-06.md`.

Related slices: [14 — Reject missing CI baseline inputs before expensive qualification](14-reject-missing-ci-baseline-inputs-before-expensive-qualification.md); [15 — Run affected compatibility fences before broad repair qualification](15-run-affected-compatibility-fences-before-broad-repair-qualification.md); [16 — Collect the complete independent native diagnostic roster](16-collect-the-complete-independent-native-diagnostic-roster.md).

## What to build

A survey of those six review documents against the portable skill produced seven defect classes the workflow did not force; the classes with recurrence evidence across increments were amended, and the four below were deferred as single-document or lower-recurrence. Close them the same way: one clause or enumeration inside an existing field, no new mandatory per-slice field, and no weakening of the obligations already added.

### 1. Loop exit paths and per-failure-site verdicts

PR #10 F4/F9: a loop's `break`/termination paths and the loop-carried state they leave the caller (continuation, partial result) were never enumerated, so two local-ceiling exits could not name a continuation and two retryable exits stranded the page. PR #10 F7/F8: one loop gave different degrade-or-reject verdicts at different failure sites, and a downstream acceptance validator re-rejected a partial the producer had decided to keep.

Draft (`falsifiable-design` step 2 decision cells): *Enumerate every exit path of a new or changed loop and the caller-visible state each leaves — continuation, partial result, or error — and record one degrade-or-reject verdict per failure site in that loop, including whether the downstream validator re-accepts the partial.*

### 2. Detector mis-fires repaired, not worked around

PR #12 F15: a `wiring_calls` allowlist compensated for the gate's own `CALL` pattern matching `Github(` inside `ResourceAddress::Github(_)`. PR #13 F10 and T2 are the same shape. Today the exemption only needs a justification; nothing asks why the detector stays unrepaired.

Draft (`checkpointed-build` step 6, beside "relaxing required assertions … remains prohibited"): *A second exemption, allowlist entry, or special case for the same detector false positive is a detector repair: fix the detector, or record why the exemption is the correct boundary and the detector is not.*

### 3. Gate and budget wiring is itself unenforced

PR #1 F6/F7/F8/F10: budget assertions that were never compiled or run, a release-only `cfg!(debug_assertions)` gate, a 1 ms wall bound on shared runners, and a downstream step silently skipped — the gates existed but nothing proved the required check executed them. PR #1 F9/F13: an existing fence deleted and a golden assertion weakened with no covering record.

Draft (`checkpointed-build` step 5 Budget/Fence bullets, with `budgeted-plan` step 3): *Every assertion a slice relies on is compiled and executed by the check the plan names; state the command that runs it. Each wall-clock budget records the platform and the margin at which its threshold holds, so a shared-runner bound cannot flake.*

### 4. Fixture cost, scaffolding, and unnecessary work

PR #14 F14 (a fence armed through the process-global allocator, "fails with nothing pointing at the cause"), F28 (a boundary fixture regenerating 4 MiB per request inside a debug gate), F46 (an oracle constructed twice for one value), F30/F32/F43 (per-entry allocations and redundant locking inside a passing budget), F50 (`EXCLUDED` grows by literal every increment), PR #10 F12 (a fixture dropping the `TempDir`s its subject still holds).

Draft (`budgeted-plan` step 3 Stress fixture): *The fixture's own cost and construction are budgeted with the code's: no process-global instrumentation without a test seam, no per-request regeneration of a large payload, no value constructed twice, and a helper keeps alive every resource the subject holds.* Draft (`falsifiable-design` step 2): *A list that grows by convention on every increment is derived from the convention instead.*

## Placement / boundaries

Portable guidance only. Reuse the existing decision-cell enumeration, slice fields, and gate items; do not add a checklist, a new gate item per class, or a per-slice mandatory field beyond the ones already defined. The classes deliberately left out of scope remain the project's: the fail-fast diagnostic roster (issue 16), authoritative log recovery (issue 8), CI action versions and `ci.yml` contents, and native-runner behaviour.

Known overlap to resolve while working this: the host-axis clauses added to `falsifiable-design` step 2 and `budgeted-plan` step 3 (host trust policy, interpreter/tool version, checkout line-ending normalization) border issue 15's "fixture/API compatibility" boundary. If that overlap is judged to be issue 15's scope, relocate those clauses there rather than maintaining both.

## Acceptance criteria

- [ ] Each of the four groups lands as a clause or enumeration inside an existing field, with the stage and step named in the change, and no new mandatory per-slice field.
- [ ] Each group is demonstrated on the historical finding that motivated it: the amended text forces the decision the review had to make, shown by walking that finding's facts through the clause.
- [ ] The obligations added by the PR #1–#14 survey remain intact: gate items 10 and 11, the fence rule, the worst-shape budget, provider-sourced fixtures, and repair-scoped discrimination are not weakened or restated in a second place.
- [ ] Affected stage cross-references and counts remain consistent (`checkpointed-build`'s item total, `plan.md`'s slice-field count, the self-review criteria counts).
- [ ] The repository's own tests pass (`python3 tests/test_*.py`).

## Blocked by

None - can start immediately.
