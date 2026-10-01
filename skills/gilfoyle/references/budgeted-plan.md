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

After [`falsifiable-design`](references/falsifiable-design.md) produced an approved `design.md`. Read [workflow contract](references/CONTRACT.md) first — it owns the shared definitions this stage depends on: the slice definition, gate states, Evidence validity, Approval semantics, the review-size gate, the tracker taxonomy, artifact ownership, and checkpointed-build's exclusive ownership of slice completion.

Also enter when review repairs change plan scope, budget, or partition inputs, or require a plan update following an approved design/spec change. An implementation repair within the approved contract goes directly from [`assessing-review-feedback`](references/assessing-review-feedback.md) to checkpointed-build's bounded repair entry; it does not require this stage.

Resolve the artifact directory per the contract: exactly one `.<change-slug>/` matches the change — use it; several plausibly match — name them and ask; none exists — run [`change-workflow`](references/change-workflow.md) first.

Required inputs:

- `.<change-slug>/design.md` — required; it must satisfy [`falsifiable-design`](references/falsifiable-design.md)'s Output requirements. Verify in step 1 for initial planning, or use the scoped review re-entry below. Missing or invalid: stop and return to [`falsifiable-design`](references/falsifiable-design.md).
- `route.md` — the route and its evidence.
- `spec.md` — when present; its delivery increments shape the PR partition.
- `evidence.md` and `probe.*` — Empirical routes; the design's oracles may reference the evidence oracle.
- The review decision log — required on review re-entry, from the PR-native surface or `review-decisions.md`.

Target artifact: `.<change-slug>/plan.md`.

### Review re-entry mode

Use this mode only for changed plan inputs; the initial-planning Process below remains unchanged.

1. Read the compact repair record owned by [`assessing-review-feedback`](references/assessing-review-feedback.md). Identify affected design rows, owning slices, and changed planning inputs. A missing covering claim or changed approved behavior, ownership, interface, architecture, or risk returns to the owning spec/design stage before planning; apply the contract's Approval semantics.
2. Apply step 1's design criteria to affected rows and their dependencies, using Evidence validity for prior proof. Preserve the prior approval and checks for unaffected decisions by reference rather than rereading the whole design. Broaden the scope when dependencies or evidence applicability are uncertain; a known `FAIL` remains blocking.
3. Preserve unaffected slices and PR increments. Update affected fields in the owning slices; create a fully specified slice only when changed scope introduces a genuinely new atomic change. Preserve committed history by recording the affected plan amendment and its repair reference, not by declaring prior implementation complete again. Every changed or new field is traceable to the finding IDs and design claims; unchanged fields retain their approved values.
4. Apply steps 2–3 and 5–6 to the affected rows, slices, and changed text. Recheck global constraints only when their inputs change: coverage/dependencies, module growth, diff sum and churn margin, partition, and increment mergeability. Recompute affected totals with unchanged contributions retained; a total newly over 4,000 runs the **Size stop** unless the recorded requester choice already covers it. Record which checks changed and which prior conclusions remain applicable.
5. Save the affected update in `plan.md` and return to [`checkpointed-build`](references/checkpointed-build.md) with the existing compact repair record. This stage owns plan changes, not a second repair artifact or checkpoint result.

Criterion: changed inputs and their affected rows/slices satisfy the applicable initial-planning criteria; global constraints affected by those inputs are checked; unaffected fields and valid conclusions remain referenced; required approvals are recorded. An ordinary approved-contract repair needs neither a new fourteen-field slice nor a whole-plan/design reread.

## Process — initial planning

Each step ends with a completion criterion. Do not start the next step until the current one's criterion holds.

### 1. Verify the approved design

Read `design.md` top to bottom. Confirm every Falsification cell has its declared value or field-appropriate `N/A` under [`falsifiable-design`](references/falsifiable-design.md)'s **Verification ladder**, the cheapest falsifier's Status is `PASS`, no row has Status `FAIL`, every `PENDING` entry names its discharge owner and step, and Approval holds the requester's verbatim words, date, and risk-acceptance list. When T2 records a module-shape change or Length review trigger, confirm the approved ledger, protected parents, selected ownership verification, and triggered Length review; otherwise confirm T2's evidence-backed `N/A`. Return any row whose applicable check, mutation, or review lacks a concrete scope and expected result to `falsifiable-design`.

Criterion: the design satisfies [`falsifiable-design`](references/falsifiable-design.md)'s Output requirements, every row is specific enough to plan against, and the Module shape/Length-review branch is complete.

### 2. Decompose into slices at independently-green atomic seams

Start from the design's claim rows and decompose into slices, ordered by dependency:

- One slice per claim, or per group of claims that cannot land apart — a seam change plus every behavior it unblocks.
- All caller updates for a change land in the same slice as the change: a signature change, its migration, and every callsite are one slice regardless of file count.
- Slices follow the approved module seams. A slice may move one responsibility atomically across a seam, but may not mix unrelated runtime, domain, persistence, and presentation responsibilities merely because they share a caller.
- Every design row whose Status is `PENDING — <discharge owner/step>` is discharged by the slice implementing that claim: Commands and expected results carries the exact falsifier and expected outcome; Oracle carries the approved comparison or exact ladder-backed `N/A`.
- A slice's independent observable check must not depend on a later slice.
- A candidate slice that cannot leave the repository green in isolation, or that has no independent observable check, is not a slice: split or merge it. File counts, line counts, and time estimates are decomposition signals, never hard limits.

Criterion: the slice sequence covers every design row exactly once, follows the approved module seams, each slice is atomic and independently green with its own observable check, and every `PENDING` falsifier is assigned to the slice implementing its claim.

### 3. Fill the mandatory slice fields

For every slice, record each field before any implementation. Conditional fields carry `N/A — reason` per the contract.

```
## Slice N: <one-sentence purpose>

**Claim IDs:**             [C1, C3 — from design.md's table]
**Expected behavior:**     [the observable outcome this slice produces]
**Oracle:**                [approved design row's independent comparison or exact ladder-backed N/A]
**Stress fixture:**        [input designed to break a plausible bug, with expected outcome written now] | N/A — reason
**Regression fence:**      [existing or new deterministic fence path] or [controlled benchmark qualification — approved **Performance-fence policy** entry and threshold] | [exact ownership-verification or approved-risk N/A from design.md]
**Named mutation:**        [design row's mutation] | [exact ladder-backed or approved-risk N/A from design.md]
**Complexity/production scale:** [per new loop: asymptotic cost AND production-scale input sizes AND the resulting bound AND the slice's explicit maximum accepted cost with its rationale; performance claims reference the approved falsifiable-design **Performance-fence policy** entry for workload/concurrency and accepted cost] | N/A — reason
**Wall budget/phase:**     [phase: always-on | one-off; real-latency phases reference falsifiable-design's **Performance-fence policy** entry and approved wall budget/qualification; deterministic phases reference their deterministic fence; one-off phases without an explicit latency obligation record `N/A — reason: one-off phase; no wall budget`, while an explicit one-off latency obligation uses the policy qualification] | N/A — reason
**Module shape:**         [responsibility added/moved/deleted; interface delta; owner after slice; protected parents + expected production delta; selected checks/review and expected result; triggered **Length review** reference and approved disposition] | N/A — route/design record no module-shape change
**Files:**                 [exact paths to create or modify]
**Estimate:**              [time estimate — a signal, not a gate]
**Diff estimate:**         [changed lines: implementation + tests + fixtures]
**PR increment:**          [increment name from step 4]
**Commands and expected results:**
- [exact command or scoped ownership review] → [expected observable; applicable comparison/mutation result; real-latency qualifications use the policy-declared statistic, execution contract, and mutation]
- [exact command] → [behavioral expected result]
```

Field rules:

- **Claim IDs** — every claim this slice implements, by ID from the design table.
- **Expected behavior** — the observable outcome that is the slice's independent check. If it cannot be stated, the slice is not decomposed.
- **Oracle** — copy the design row's comparison or exact ladder-backed `N/A`; a changed verification decision follows the contract's Approval semantics. Commands and expected results records the falsifier that `checkpointed-build` discharges, including required consumer smokes even when no oracle applies.
- **Stress fixture** — every slice implementing logic gets a fixture designed to fail under a plausible bug class: empty input, name collisions, a secondary key that never fires because the primary key is always unique, Unicode/spaces/backslashes, very large input. The expected outcome is written before implementation. A production budget is measured on the worst shape the design's admitted limits allow — maximum depth through maximum-width collections with provider-shaped content, citing the design's step-2 decision cells for those limits — because a bound established at one path segment against a one-entry tree bounds nothing. The fixture runs inside the gate that carries it and touches only state the test owns, keeping alive every resource the subject still holds for the whole test body. Provider- or host-derived material comes from a captured payload or the documented contract, never from the implementation's own expectation; where a fixture's acceptance is decided by the host rather than the test's oracle — a trust policy, an interpreter or tool version, checkout line-ending normalization — record that precondition with its enforcement or an explicit platform restriction. Slices of pure types or schema: `N/A — reason`.
- **Regression fence** — provide the claim's coverage in its implementing slice: reuse a sufficient existing fence or create one here, never defer it. Its assertion or qualification follows the design row's Regression fence rule. Copy an applicable ownership-verification or approved-risk `N/A` exactly.
- **Named mutation** — copy each design row's mechanical mutation or exact `N/A`. `checkpointed-build` proves applicable mutations red/restored-green under Evidence validity; a retained behavioral fence does not by itself require a new mutation.
- **Complexity/production scale** — per new loop: asymptotic cost, production-scale input sizes, the resulting bound, and the slice's explicit maximum accepted cost with the rationale that sets it. For a performance claim, reference the approved falsifiable-design **Performance-fence policy** entry for workload/concurrency and any latency qualification; this field records admitted scale and explicit cost, not a second timing policy. The budget is plan-specific: [`checkpointed-build`](references/checkpointed-build.md) passes it when the measured cost is at or under the recorded maximum, so the recorded maximum and its rationale make pass/fail checkable without a shared default. Slices with no new loop: `N/A — reason`.
- **Wall budget/phase** — classify every runtime phase the slice introduces. A phase is **always-on** when ordinary operation triggers it on every request, invocation, or background tick; it is **one-off** when it runs once per process, command, or discrete event. For a real-latency phase, reference falsifiable-design's approved **Performance-fence policy** entry and carry its wall budget/qualification; for a deterministic work/operation/virtual-clock claim, reference the deterministic fence instead. One-off phases without an explicit latency obligation record `N/A — reason: one-off phase; no wall budget`; an explicit one-off latency obligation uses the policy qualification.
- **Module shape** — copy the applicable responsibility and interface change from the approved module ledger, name the final owner, and record every protected parent's expected production delta plus the selected compiler/dependency checks, scoped ownership review, or justified fence and expected result; include any triggered **Length review** reference and approved disposition. Numeric deltas are tripwires, not permission for pass-through splitting. Use the route/design-backed `N/A` only when `design.md` carries that branch.
- **Commands and expected results** — exact verification commands and scoped review instructions with their expected observables, including oracle/mutation results only where applicable. Assert behavior rather than runner-format text or exact pass counts. Real-latency commands use **Performance-fence policy**; deterministic commands assert the claimed observable.

Criterion: every slice records all fourteen fields, with `N/A — reason` in conditional cells.

### 4. Sum the integration and module-shape budgets; partition into PR increments

- When module shape applies, read [module shape](references/module-shape.md) and build the module growth ledger before summing the diff:

| Module | Baseline production lines | Projected final lines | Responsibility change | Interface change | Protected-parent rule |
|---|---:|---:|---|---|---|
| `<path>` | `<count>` | `<range>` | `<add/move/delete>` | `<entry points/invariants>` | `<rule or N/A>` |

  Every module touched by a slice appears once. Projection ranges carry rationale and act as drift tripwires; they are not universal limits or evidence of depth. A predicted second responsibility cluster returns to design instead of being hidden by a larger range. When a projection trips the contract's **Size stop**, follow [module shape](references/module-shape.md)'s **Length review**, even when placement is unchanged; update this plan only after the requester's recorded choice. When module shape does not apply, record `Module growth ledger: N/A — route/design record no module-shape change`.
- Sum the slice Diff estimates.
- Add a documented churn margin: state the margin and why it is what it is. Plans drift upward.
- If the sum plus the margin exceeds 4,000 changed lines — exact, not approximate — run the contract's **Size stop** with a proposed partition, and record the requester's choice in `plan.md`. **Single PR** keeps one increment holding all slices; **Cut scope** removes the named slices and recomputes the sum. For **Partition**, split the slices into independently mergeable PR increments in dependency order. Each increment verifies without the increments after it (verification seams: types plus committed-capture fixtures verify alone; converters verify against fixtures; wiring verifies against the app). If the spec recorded delivery increments, the partition follows them; a conflict between spec increments and verification seams means one of them is wrong — reconcile before saving the plan.
- If the sum plus the margin is at or below 4,000, the plan has a single increment holding all slices.
- Every slice records its PR increment; every increment lists its slices, its mergeable definition, and what verifies it without the later increments. When an increment's mergeability is described against an upstream branch, discover the repository's default/upstream branch per the contract — never hard-code one.

The projection is a budget; the actual cumulative diff and module shape are enforced by [`checkpointed-build`](references/checkpointed-build.md) per the contract's single-owner rules. **Length review** owns any threshold disposition before this plan incorporates it. This step only partitions the projection and records shape tripwires.

Criterion: the module growth ledger is complete or carries its evidence-backed `N/A`; every triggered Length review is recorded by reference to its approved disposition; partition arithmetic is recorded (sum, margin, total), with the requester's **Size stop** choice when the total exceeds 4,000; every slice names its increment; and every increment has a mergeable definition.

### 5. Apply the tracker taxonomy

Scan the draft for deferral phrases — the same list as [`falsifiable-design`](references/falsifiable-design.md) step 8. Classify each occurrence per the contract: a permanent non-goal records its rationale where it sits; intended future work files a tracker issue now via the repository's tracker native command, verifies the ID, and cites it. Trigger-conditioned phrases are intended future work.

Criterion: every deferral phrase in plan.md is classified; every intended-future-work item cites a verified tracker ID.

### 6. Self-review

Before saving `plan.md`, run this checkable list:

1. Every design row is assigned to exactly one slice; every slice's Claim IDs exist in the design table; every `PENDING` falsifier is discharged by the slice implementing its claim.
2. Every slice has all fourteen mandatory fields, with `N/A — reason` in conditional cells.
3. Every claim has its design-selected regression coverage in the implementing slice; Oracle, Named mutation, and Regression fence preserve the design's applicable checks or exact justified `N/A` values.
4. Every new loop states its complexity, production-scale cost, and explicit maximum accepted cost with rationale; every always-on real-latency phase has a wall budget with rationale, every deterministic phase references its deterministic fence, and every one-off latency obligation follows **Performance-fence policy**.
5. The Module shape field and growth ledger cover every touched module and protected parent; every triggered **Length review** is recorded and linked to the requester's retain-and-raise, reshape, or defer choice; no slice crosses an approved seam with unrelated responsibilities.
6. The partition arithmetic carries a documented churn margin and, over 4,000, the requester's recorded **Size stop** choice; every slice names its PR increment; every increment has a mergeable definition.
7. The tracker taxonomy is applied.
8. Every fence assertion satisfies [`falsifiable-design`](references/falsifiable-design.md)'s fence rule, every registered production budget is measured on the worst shape the design's admitted limits allow, and every real-latency qualification follows the approved **Performance-fence policy** entry.
9. The plan declares no slice complete — completion is [`checkpointed-build`](references/checkpointed-build.md)'s to judge.

Criterion: all nine hold. A failed check means the plan is incomplete; do not save it.

### 7. Write plan.md

`.<change-slug>/plan.md` contains: the module growth ledger or evidence-backed `N/A`; the partition arithmetic (diff sums, churn margin, total, any Size stop choice, increments); one section per slice with the step-3 template filled; and the self-review result.

Criterion: `plan.md` has one section per slice, every field filled, the applicable module growth ledger recorded, the arithmetic recorded, and the self-review list checked.

## Hand-off

[`checkpointed-build`](references/checkpointed-build.md) consumes `plan.md` and exclusively judges slice or repair completion per the contract. Initial planning hands off the full plan; review re-entry hands off the affected update and the compact repair record in the existing review decision surface. This stage defines checkable fields; it does not run or restate the checkpoint, and it never declares a slice or repair complete. Required proof remains a pre-commit gate.

## Output

For initial planning, `.<change-slug>/plan.md` with:

- one section per slice, every mandatory field filled, conditional fields as `N/A — reason`;
- the module growth ledger, or the route/design-backed `N/A`;
- the partition arithmetic — summed diff estimates, documented churn margin, total, and every PR increment with its mergeable definition;
- the self-review result.

If any initial-planning output is missing, that stage did not run. For review re-entry, preserve that complete plan and record only the affected amendments and scoped self-review described above; the compact repair record stays in its existing decision surface.
