# budgeted-plan

A plan is a sequence of falsifiable hypotheses, not a script of pre-typed code. The plan's job is to make every build-time condition checkable before the build starts: what each slice changes, how its success is observed, and where the change lands in review-sized increments.

## The rule

```
Plan unit = slice.
Slice = the smallest atomic change that leaves the repository green
        and has an independent observable check (contract definition).
Completion is checkpointed-build's to judge; this stage defines slices, not their completion.
```

## When this stage runs

After [`falsifiable-design`](references/falsifiable-design.md) produced an approved `design.md`. Read [workflow contract](references/CONTRACT.md) first — it owns the shared definitions this stage depends on: the slice definition, gate states, the review-size gate, the tracker taxonomy, artifact ownership, and checkpointed-build's exclusive ownership of slice completion.

Also enter when [`assessing-review-feedback`](references/assessing-review-feedback.md) hands off accepted behavior-changing fixes to an existing approved `plan.md`.

Resolve the artifact directory per the contract: exactly one `.<change-slug>/` matches the change — use it; several plausibly match — name them and ask; none exists — run [`change-workflow`](references/change-workflow.md) first.

Required inputs:

- `.<change-slug>/design.md` — required; it must satisfy [`falsifiable-design`](references/falsifiable-design.md)'s Output requirements, verified in step 1. Missing or invalid: stop and return to [`falsifiable-design`](references/falsifiable-design.md).
- `route.md` — the route and its evidence.
- `spec.md` — when present; its delivery increments shape the PR partition.
- `evidence.md` and `probe.*` — Empirical routes; the design's oracles may reference the evidence oracle.
- The review decision log — required on review re-entry, from the PR-native surface or `review-decisions.md`.

Target artifact: `.<change-slug>/plan.md`.

### Review re-entry mode

On review re-entry:

1. Run Process step 1 against the current approved design.
2. Preserve every unaffected slice and PR increment. Revise the uncommitted owning slice, or append one review-fix slice when that slice is already committed.
3. Name every resolved finding ID in the review-fix slice's Purpose. Map the root-cause behavior to existing design Claim IDs and fill all thirteen fields. No covering design row means the design is incomplete: return to [`falsifiable-design`](references/falsifiable-design.md) before planning the fix.
4. Apply Process step 3 to every changed or appended slice, then apply Process steps 4–6 to the whole plan.

Criterion: the plan changes only where the accepted findings require it; every review-fix slice is traceable to its finding IDs and design claims; every global plan criterion still holds.

## Process

Each step ends with a completion criterion. Do not start the next step until the current one's criterion holds.

### 1. Verify the approved design

Read `design.md` top to bottom. Confirm the Falsification table is complete (no empty cells, `N/A — reason` in conditional cells, `N/A — approved risk` in fence cells), the cheapest falsifier's Status is `PASS`, no row has Status `FAIL`, every `PENDING` entry names its discharge owner and step, and the Approval section holds the requester's verbatim words, the date, and the approved risk-acceptance list. Flag any design row whose oracle, mutation, or fence is not specific enough to check mechanically, and return it to [`falsifiable-design`](references/falsifiable-design.md).

Criterion: the design satisfies [`falsifiable-design`](references/falsifiable-design.md)'s Output requirements, and every row is specific enough to plan against.

### 2. Decompose into slices at independently-green atomic seams

Start from the design's claim rows and decompose into slices, ordered by dependency:

- One slice per claim, or per group of claims that cannot land apart — a seam change plus every behavior it unblocks.
- All caller updates for a change land in the same slice as the change: a signature change, its migration, and every callsite are one slice regardless of file count.
- Every design row whose Status is `PENDING — <discharge owner/step>` is discharged by the slice implementing that row's claim: the slice's Commands and expected results field carries the exact falsifier experiment and expected outcome, while its Oracle field carries the independent comparison mechanism.
- A slice's independent observable check must not depend on a later slice.
- A candidate slice that cannot leave the repository green in isolation, or that has no independent observable check, is not a slice: split or merge it. File counts, line counts, and time estimates are decomposition signals, never hard limits.

Criterion: the slice sequence covers every design row exactly once, each slice is atomic, independently green, has its own observable check, and every `PENDING` falsifier is assigned to the slice implementing its claim.

### 3. Fill the mandatory slice fields

For every slice, record each field before any implementation. Conditional fields carry `N/A — reason` per the contract.

```
## Slice N: <one-sentence purpose>

**Claim IDs:**             [C1, C3 — from design.md's table]
**Expected behavior:**     [the observable outcome this slice produces]
**Oracle:**                [independent computation; default: the design row's oracle]
**Stress fixture:**        [input designed to break a plausible bug, with expected outcome written now] | N/A — reason
**Regression fence:**      [test path — created in THIS slice] | N/A — approved risk: <reason> (exact value from design.md's approved fence cell)
**Named mutation:**        [from the design row(s) — applied to the new fence by checkpointed-build] | N/A — approved risk: no fence to mutate (same Approval entry as the fence)
**Complexity/production scale:** [per new loop: asymptotic cost AND production-scale input sizes AND the resulting bound AND the slice's explicit maximum accepted cost with its rationale] | N/A — reason
**Wall budget/phase:**     [phase: always-on | one-off; always-on phases record the wall-clock budget at production scale] | N/A — reason
**Files:**                 [exact paths to create or modify]
**Estimate:**              [time estimate — a signal, not a gate]
**Diff estimate:**         [changed lines: implementation + tests + fixtures]
**PR increment:**          [increment name from step 4]
**Commands and expected results:**
- [exact command] → [behavioral expected result: the fixture's computed value, item-by-item agreement with the oracle, the fence going red under the named mutation]
- [exact command] → [behavioral expected result]
```

Field rules:

- **Claim IDs** — every claim this slice implements, by ID from the design table.
- **Expected behavior** — the observable outcome that is the slice's independent check. If it cannot be stated, the slice is not decomposed.
- **Oracle** — default is the design row's independent oracle; a different oracle must satisfy the contract's independence definition. For a design row with Status `PENDING — <discharge owner/step>`, the Commands and expected results field records the exact falsifier run that [`checkpointed-build`](references/checkpointed-build.md) must discharge at this slice's checkpoint.
- **Stress fixture** — every slice implementing logic gets a fixture designed to fail under a plausible bug class: empty input, name collisions, a secondary key that never fires because the primary key is always unique, Unicode/spaces/backslashes, very large input. The expected outcome is written before implementation. Slices of pure types or schema: `N/A — reason`.
- **Regression fence** — the slice that implements a claim also creates that claim's fence: fence creation is never deferred to a later slice. The fence is the permanent form of the design row's falsifier. A fence-less claim copies the design row's exact `N/A — approved risk: <reason>` value.
- **Named mutation** — the design row's mutation for each claim in this slice; [`checkpointed-build`](references/checkpointed-build.md) applies it to the new fence, confirms red, restores, and confirms green. A claim whose design row records `Named mutation: N/A — approved risk: no fence to mutate` records the same value here, covered by the same Approval entry as the fence.
- **Complexity/production scale** — per new loop: asymptotic cost, production-scale input sizes, the resulting bound, and the slice's explicit maximum accepted cost with the rationale that sets it. The budget is plan-specific: [`checkpointed-build`](references/checkpointed-build.md) passes it when the measured cost is at or under the recorded maximum, so the recorded maximum and its rationale make pass/fail checkable without a shared default. Slices with no new loop: `N/A — reason`.
- **Wall budget/phase** — classify every runtime phase the slice introduces. A phase is **always-on** when ordinary operation triggers it on every request, invocation, or background tick; it is **one-off** when it runs once per process, command, or discrete event. Always-on phases record a wall-clock budget at production scale with the rationale that sets it; one-off phases record `N/A — reason: one-off phase; no wall budget`.
- **Commands and expected results** — the exact verification commands and their expected results as behavioral outcomes: what the output must be (the fixture's computed value, item-by-item agreement with the oracle, the fence going red under the named mutation and green once restored) — not runner-format text such as exact pass counts.

Criterion: every slice records all thirteen fields, with `N/A — reason` in conditional cells.

### 4. Sum the integration budget; partition into PR increments

- Sum the slice Diff estimates.
- Add a documented churn margin: state the margin and why it is what it is. Plans drift upward.
- If the sum plus the margin exceeds 4,000 changed lines — exact, not approximate — partition the slices into independently mergeable PR increments in dependency order. Each increment verifies without the increments after it (verification seams: types plus committed-capture fixtures verify alone; converters verify against fixtures; wiring verifies against the app). If the spec recorded delivery increments, the partition follows them; a conflict between spec increments and verification seams means one of them is wrong — reconcile before saving the plan.
- If the sum plus the margin is at or below 4,000, the plan has a single increment holding all slices.
- Every slice records its PR increment; every increment lists its slices, its mergeable definition, and what verifies it without the later increments. When an increment's mergeability is described against an upstream branch, discover the repository's default/upstream branch per the contract — never hard-code one.

The projection is a budget; the actual cumulative diff is enforced by [`checkpointed-build`](references/checkpointed-build.md) per the contract's single-owner rules. This step only partitions the projection.

Criterion: the partition arithmetic is recorded (sum, margin, total), every slice names its increment, and every increment has a mergeable definition.

### 5. Apply the tracker taxonomy

Scan the draft for deferral phrases — the same list as [`falsifiable-design`](references/falsifiable-design.md) step 8. Classify each occurrence per the contract: a permanent non-goal records its rationale where it sits; intended future work files a tracker issue now via the repository's tracker native command, verifies the ID, and cites it. Trigger-conditioned phrases are intended future work.

Criterion: every deferral phrase in plan.md is classified; every intended-future-work item cites a verified tracker ID.

### 6. Self-review

Before saving `plan.md`, run this checkable list:

1. Every design row is assigned to exactly one slice; every slice's Claim IDs exist in the design table; every `PENDING` falsifier is discharged by the slice implementing its claim.
2. Every slice has all thirteen mandatory fields, with `N/A — reason` in conditional cells.
3. Every claim's fence is created in the slice implementing it; every new fence carries its named mutation from the design; every fence-less claim copies `Regression fence: N/A — approved risk: <reason>` and records `Named mutation: N/A — approved risk: no fence to mutate`.
4. Every new loop states its complexity, production-scale cost, and explicit maximum accepted cost with rationale; every always-on phase has a wall budget with rationale.
5. The partition rule was applied with a documented churn margin; every slice names its PR increment; every increment has a mergeable definition.
6. The tracker taxonomy is applied.
7. The plan declares no slice complete — completion is [`checkpointed-build`](references/checkpointed-build.md)'s to judge.

Criterion: all seven hold. A failed check means the plan is incomplete; do not save it.

### 7. Write plan.md

`.<change-slug>/plan.md` contains: the partition arithmetic (diff sums, churn margin, total, increments); one section per slice with the step-3 template filled; the self-review result.

Criterion: `plan.md` has one section per slice, every field filled, the arithmetic recorded, and the self-review list checked.

## Hand-off

[`checkpointed-build`](references/checkpointed-build.md) consumes `plan.md` and exclusively judges slice completion per the contract. This stage defines slices and their checkable fields; it does not run or restate that checkpoint, and it never declares a slice complete.

## Output

`.<change-slug>/plan.md` with:

- one section per slice, every mandatory field filled, conditional fields as `N/A — reason`;
- the partition arithmetic — summed diff estimates, documented churn margin, total, and every PR increment with its mergeable definition;
- the self-review result.

If any of these is missing, the stage did not run.
