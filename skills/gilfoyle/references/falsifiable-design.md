# falsifiable-design

A design that cannot be proven wrong is a wish list. Most design documents are written so that any output the system later produces appears to confirm them. This stage writes the other kind: every claim paired with the experiment that would kill it, and the cheapest such experiment run before anyone approves.

## The rule

```
Every claim has a falsifier.
The cheapest falsifier runs before the design is approved.
```

## When this stage runs

After [`change-workflow`](references/change-workflow.md) has written `route.md` with route **Structural** or **Empirical**. Local routes take normal repository fix/TDD plus focused behavioral verification and produce no design artifacts.

Read [workflow contract](references/CONTRACT.md) first — it owns the shared definitions this stage depends on: gate states, the independent-oracle definition, the tracker taxonomy, artifact ownership, and approval semantics.

Resolve the artifact directory per the contract: exactly one `.<change-slug>/` matches the change — use it; several plausibly match — name them and ask; none exists — run [`change-workflow`](references/change-workflow.md) first.

Required inputs:

- `route.md` — always. Missing: stop and run [`change-workflow`](references/change-workflow.md).
- `spec.md` — when present (behavior was unresolved and interrogated). If the route requires a spec and none exists, stop. When the route records `spec.md: N/A — behavior fully explicit`, the behavior set is extracted from `route.md`'s T4 evidence (step 1).
- `evidence.md` and `probe.*` — Empirical routes. Missing on an Empirical route: stop; the empirical premise is unverified.

Target artifact: `.<change-slug>/design.md`.

## Verification ladder

Choose the lowest sufficient level for each claim before implementation; record the choice and covered inputs in its Falsifier cell:

1. **Existing behavioral test** — reuse or extend the established suite to assert the declared consumer-visible outcome.
2. **Ordinary consumer smoke** — drive the real entry point and check concrete results where tests leave an integration or environment gap. Required smoke runs remain additive even when level 1 suffices.
3. **Independent differential oracle** — compare the same inputs through a different failure mechanism. Required for exact parity, complex transformations, and claims explicitly classified high-risk in the request, repository policy, or design. Reuse an established reference/tool or independently derived fixtures first; bespoke machinery follows the contract's named-gap rule. Empirical premises retain the independent ground-truth check owned by `prove-it-prototype`; that does not require a custom oracle for every later claim.

Ordinary ownership verification follows [module shape](references/module-shape.md)'s **Design procedure**, not a bespoke source analyzer by default.

Decide Oracle and Named mutation applicability separately in their existing cells. An ordinary behavioral claim may record `N/A — ordinary behavioral verification sufficient: <named test/smoke, covered outcome, and why no independent comparison or mutation is needed>`. An ownership-only claim may instead record `N/A — ownership verification: <compiler/dependency check and review evidence specified by module shape>`. These choices are part of design approval, not checkpoint-time waivers. They leave falsifiers, applicable regression coverage, repository gates, and required smokes intact; a known product failure or failed required proof cannot be relabeled optional.

**Mutation sensitivity:** retain cheap named mutations when useful. Require them for a bespoke checker's declared detection obligations, a demonstrated blind/vacuous fixture, controlled latency qualification, or an existing mandatory mutation requirement. Otherwise ordinary behavioral coverage can justify the explicit Named mutation `N/A`. For an applicable mutation, name the plausible defect, code change, and expected red result; proof is bounded to the declared obligation, not every imaginable checker evasion.

New tests/fixtures, or changes to what they exercise or assert, introduced in response to a review finding require observed sensitivity to the intended defect: red, then green after correction or restoration. A valid actual pre-repair red/after-fix green receipt can supply this proof; otherwise use a cheap named mutation. Record the intended observable and both baseline revisions in the existing repair receipt. An ordinary Named mutation `N/A` cannot waive this requirement. Retain still-valid sensitivity proof; docs/comments/formatting alone do not invalidate it. This does not replace other independently required mutations or require extra mutation of unrelated ordinary features.

## Process

Each step ends with a completion criterion. Do not start the next step until the current one's criterion holds.

### 1. Read the inputs and record the extraction

Read [workflow contract](references/CONTRACT.md), then `route.md`, then `spec.md` (when present) and `evidence.md` with its probe (Empirical routes). Extract: the route; the complete behavior set — from `spec.md` when present, or from `route.md`'s T4 evidence when `spec.md` is `N/A — behavior fully explicit`; the spec's edge-case decisions and delivery increments; every empirical premise, the independent oracle, and the comparisons from the evidence. Record the extraction in `design.md`'s **Route and inputs** section, with pointers to the source artifacts and `N/A — reason` for inputs that do not apply.

An explicit-behavior route enters design with the full behavior set, not a one-line request: if `spec.md` is `N/A — behavior fully explicit` and `route.md`'s T4 evidence does not carry the complete given/when/then behavior set, return to [`change-workflow`](references/change-workflow.md) with that evidence and request correction of the T4 verdict.

Criterion: the Route and inputs section records the route, the complete given/when/then behavior set (the set itself, or a pointer to the T4 evidence that carries it), and the empirical premises (or their source pointer); nothing the later steps rely on is left unrecorded.

### 2. Enumerate production-reachable input and decision shapes

Before writing claims, enumerate every distinct shape the feature's inputs can take — input-space coverage, not output-space happy paths. Sources: the spec's behaviors and edge-case decisions (when present), the `route.md` T4 behavior set (when the spec is `N/A — behavior fully explicit`), the evidence comparisons (Empirical), and the codebase.

For every input the design touches:

- Sum types: every variant.
- Option types: both branches.
- Collections: empty, single, multi with distinct values, multi with duplicates.
- Structs with optional fields: every cell of the field-presence matrix reachable in production.
- Numeric: zero, negative, boundary values, and the maximum the feature must handle.
- Strings and paths: empty, ASCII-only, Unicode, embedded spaces, relative versus absolute.
- Provider payloads the change reads: the provider's alternate shapes for one logical entity — an app or bot account beside a login, an entry whose link the format omits, a field the wire drops — each with the capture or the provider's published contract its fixture derives from. A fixture written from the implementation's own expectation records the implementation, not the provider.

In addition, enumerate the cells the feature's own decisions branch on:

- A classification predicate or allowlist over an enum: every variant it consumes, and the production conditions that arrive as each variant. An allowlist naming three error kinds still decides the outcome of the kinds it does not name, and two conditions sharing one variant are one cell until the predicate can tell them apart.
- A bound the design imposes on callers: the boundary value, plus either the caller-facing knob that raises it or an `N/A — approved risk` row recorded in the Approval section. A ceiling no configuration can raise is an accepted tradeoff only when that row exists; unrecorded, it reads as a tuning parameter. State the population and framing the bound measures, and reconcile it with every consuming boundary that enforces the same value, including that boundary's own fixed overhead.
- A capability or control offered to callers: every Resource or route that accepts it, each one enforcing it or refusing it.
- A dispatch over a sum: every arm, including the arms that refuse. An enum consumed as ordinary data belongs to the input list above; a sum the design itself dispatches over belongs here.
- A value crossing the boundary whose representation the outcome must preserve: what the wire actually carries against what the outcome assumes it carries — a name the wire conveys as bytes, a field the wire format does not contain, a bound the document must report, and, for the absent/null/present cells the input list enumerates, the distinction the outcome keeps. State what the representation loses or invents.

A production-reachable decision cell is a claim. `N/A — reason` is for a cell this change leaves outside its reach or scope, carrying the contract's taxonomy: a permanent-non-goal rationale or a verified tracker ID.

Record each shape and decision cell with a status in `design.md`:

- **Covered by a claim** — the shape or cell gets at least one row in the Falsification table (step 6).
- **`N/A — approved risk: <reason>`** — a bound or fence whose risk the requester accepted: the reason states the accepted risk, and the row appears in the Approval list.
- **`N/A — reason`** — the shape or cell is unreachable or deliberately out of scope. The reason is a permanent-non-goal rationale or an intended-future-work tracker ID, classified per step 8.

Completeness is the criterion, not a count: every production-reachable shape and every decision cell has a recorded status, and no shape or cell is owned by two lists at once — where the input list and the decision list touch the same value, the input list enumerates it and the decision list records its verdict. When the enumeration feels short, re-check the spec's edge-case table and the probe's inputs rather than padding the list.

### 3. Sweep removed invariants (subtractive changes)

Classify the change's core move. It is **subtractive** when its essence removes a constraint: a serialization point, a guard, a validation, a precondition, an ordering guarantee, an at-most-one or uniqueness property. A change that looks additive is often subtractive underneath — freeing a loop to handle new commands removes the mutual exclusion that loop provided. Polarity is per behavior, not per change: a move, reroute, or re-homing of existing code carries the predecessor's observable behaviors, error taxonomy (category, reason, identity), and serialized output into claims that must still hold, however additive the surrounding change is. A weakened gate, fence, validator, or oracle is subtractive regardless of how the commit is framed: name what it detected, what it detects now, and which inputs the earlier form refused or accepted that this one does not. When the change is purely additive on every behavior it touches, write one sentence saying so and skip to step 4.

For a subtractive change, enumerate what the removed constraint was silently enforcing:

- Name the constraint in one sentence.
- List the "can't happen" facts it guaranteed and walk the chain: a blocking loop guarantees no other command runs mid-turn, which guarantees a mutable field cannot change mid-operation, which guarantees later reads see a consistent value. Each link is a separate assumption.
- For each fact, ask whether the thing it forbade can now happen; grep every reader and mutator of the state the constraint protected.

Each now-possible violation becomes a claim phrased as the property that must still hold, with verification selected by the **Verification ladder**. Invariants judged still-safe get a one-sentence note.

Criterion: every broken invariant has a claim row or a still-safe note; every moved, rerouted, or weakened behavior has a claim covering the predecessor behaviors, error taxonomy, and serialized output it must keep, or a recorded reason that one of them changes; a purely additive change has its one-sentence classification on record.

### 4. Place the design

This step anchors the design to structure — which module owns each capability, what interface callers and tests use, and what the implementer may not do. If the environment exposes a skill named `codebase-design`, read it before this step and use its vocabulary (module, interface, depth, seam, adapter).

Read `route.md`'s T2 evidence. When T2 records a **Length review** trigger, read [module shape](references/module-shape.md) and carry its Length review record and the requester's **Size stop** choice into `design.md`; a trigger with no recorded choice, or one found during design, runs the Size stop before any redesign work. When T2 records a module-shape change, or the requester chose Reshape, execute module shape's complete **Design procedure**: inventory the current cluster; test the seams; produce three materially different alternatives where ownership is a decision; approve the module and protected-parent ledgers; and select ownership verification. When T2 records neither a module-shape change nor a Length review trigger, record `Module shape: N/A — <the T2 evidence that responsibility ownership is unchanged>`.

For every new capability, including a capability behind an unchanged shape, answer:

- **Owner** — the existing module or crate that owns it. If more than one owner is plausible, the module-shape alternatives decide; one-sentence intuition is insufficient.
- **New seam** — the selected interface when no existing module can own it. A capability behind an existing interface says so. A generic seam with one real adapter is rejected unless an intrinsic ownership constraint recorded by the module-shape procedure makes the seam real.
- **Forbidden** — dependency directions, responsibility duplication, internal call sites, and implementation knowledge that must not cross the seam.

Each placement decision that could silently regress becomes a claim with the compiler/dependency check or explicit ownership self-check selected by module shape. Name the rule, inspected paths, and evidence that would establish a violation; "the reviewer will notice" without that scope is not verification.

Criterion: every new capability has Owner, New seam, and Forbidden recorded; T2's module-shape/Length-review branch is complete or carries its evidence-backed `N/A`; every structural claim has the selected ownership verification.

### 5. Write claims

One sentence per claim; split anything longer. Each claim covers at least one input shape (step 2), removed invariant (step 3), or placement decision (step 4). A claim that contradicts the evidence is a design error: re-run the evidence or rewrite the claim.

Criterion: every recorded shape, invariant, and placement decision is claimed or carries its `N/A — reason`.

### 6. Write the Falsification table

Every claim gets one row, and every row records every field in `design.md` — no empty cells; conditional fields carry `N/A — reason` per the contract.

| # | Claim | Input shape | Falsifier | Oracle | Named mutation | Regression fence | Cost | Status |
|---|---|---|---|---|---|---|---|---|

- **# / Claim** — the claim ID (`C1`, `C2`, …) and its one sentence. [`budgeted-plan`](references/budgeted-plan.md) and [`checkpointed-build`](references/checkpointed-build.md) reference claims by ID.
- **Input shape** — the step-2 shape(s) the claim covers, or the invariant or placement it guards.
- **Falsifier** — the experiment that would prove the claim false. It names the input, the expected outcome under the claim, and the result that would falsify the claim. If you cannot write one, the claim is unfalsifiable: rewrite the claim or cut it. Then name at least one **other** cause that would produce the same observation. If one exists, the falsifier is not decisive — strengthen it until the control under test is the only explanation. A shared error category, an upstream guard that fires first, or an input the control never sees all make an assertion pass for the wrong reason. A falsifier asserting **absence** — an empty log, a zero counter, an unfound sentinel — additionally requires a positive control proving the observed thing can occur at all. **Anchor the falsifier at the level the claim names.** A claim about a public entry point is not proved by a fence on the implementor beneath it: every hop between them can drop, replace, or ignore what the claim asserts, and a fence anchored below the claim's level cannot see that. When the claim says "the tool does X", drive the tool.
- **Oracle** — the independent comparison selected by the **Verification ladder**, with its required comparison branch or named gap; otherwise the ladder's explicit `N/A` and concrete coverage rationale. An applicable oracle satisfies the contract's independence definition; "another part of this feature" does not.
- **Named mutation** — the ladder's explicit `N/A`, or the specific buggy implementation that would make the regression fence fail: file, change, and expected red output. The mutation edits code that exists when its fence runs and changes the observable that the fence measures; a compile failure unrelated to the claim is not detection. When the row's Regression fence is `N/A — approved risk`, record `N/A — approved risk: no fence to mutate`, covered by the same Approval entry.
- **Regression fence** — the permanent check that fails when the bug class returns; reuse an existing behavioral test where sufficient. A deterministic work/operation/virtual-clock assertion in the concurrent functional suite is the fence when it proves the claim; preserve the workload's concurrency. A real-latency claim follows **Performance-fence policy** below. Ownership-only claims may record `N/A — ownership verification: <selected checks/review>` under module shape; an omitted behavioral fence requires `N/A — approved risk: <reason>` recorded in Approval (step 11). Assert the claim's observable: category, reason, limit kind, computed value, request count, or — when the claim itself is cardinality, existence, or acceptance — that result. Any applicable mutation must change that observable.

- **Cost** — what running the falsifier costs: minutes-to-hours or the resource it needs. An estimate, not a gate.
- **Status** — `PASS`, `FAIL`, or `PENDING — <discharge owner/step>`. Per the contract, `PENDING` marks a falsifier awaiting discharge by a named owner and step — it is a lifecycle status, not a gate state. `PASS`: the falsifier ran and the claim survived. `FAIL`: the claim was falsified — the design must change. `PENDING — <discharge owner/step>`: the falsifier has not run yet, and the entry names who discharges it and where — for example `PENDING — checkpointed-build, per-slice gate (slice assigned in plan.md)`. [`budgeted-plan`](references/budgeted-plan.md) assigns every PENDING falsifier to the slice implementing its claim, and [`checkpointed-build`](references/checkpointed-build.md) discharges it at that slice's checkpoint. `N/A` never appears in Status: a falsifier that has not run is `PENDING`, not `N/A`. A `FAIL` row never ships.

Criterion: every claim has a complete row and a ladder-backed verification choice; each applicable oracle is independent; each applicable mutation is mechanical; every fence is a deterministic assertion or controlled benchmark qualification proving its claim, or carries the applicable ownership/risk `N/A`; fence-risk rows carry the matching Named mutation value.

#### Performance-fence policy

Use the cheapest fence that proves the claim:

- **Deterministic fence** — In the concurrent functional suite, assert work/operation counts, virtual-clock transitions, queue/permit state, or another deterministic observable when it proves the claim. Preserve the workload's concurrency; do not serialize it to stabilize timing.
- **Latency qualification** — A real-latency claim remains a controlled benchmark qualification, not a deterministic wall-clock test. Its Falsifier and Regression fence name the CI runner/resource class, build profile, warmup, exact repetitions, statistic, variance margin, workload concurrency, and execution mode (normal suite parallelism or an explicitly enforced dedicated lane). Calibrate the correct implementation under that intended CI contention; the Falsifier field links the calibration command, source/environment, sample results, and rationale for the threshold and variance margin. Preserve the approved latency bound and require the threshold to detect the named mutation. Missing calibration keeps the row `PENDING — <owner/step>`; an invented margin is not evidence.
- **Evidence and readiness** — Assign setup and expected result to Falsifier, independent comparison/statistic to Oracle, regression mechanism to Named mutation, the permanent assertion or benchmark qualification and threshold to Regression fence, resource cost to Cost, and readiness to Status. Timeouts are hang guards, not latency evidence. Run declared repetitions as declared: record a failed qualification rather than retrying until green, widening the threshold with arbitrary slack, or ignoring a required qualification. A required unavailable environment, runner, lane, or setup remains `PENDING — <owner/step>`, never `N/A`. Plan entries reference this policy from `Complexity/production scale`, `Wall budget/phase`, and `Commands and expected results`; do not add a timing-specific template.

### 7. Run the cheapest falsifier

Sort rows by Cost, ascending, and run the cheapest falsifier now — before the design goes to approval. One of:

- **PASS** — the cheapest claim survived its first attempt to kill it. Record the run (command and result) in the falsifier-run log.
- **FAIL** — the claim is wrong. Revise the design — re-running the evidence if needed — until the cheapest falsifier passes.

Criterion: the cheapest falsifier's Status is `PASS`. There is no waiver: a design whose cheapest falsifier cannot run before approval cannot be approved — find a cheaper falsifier or revise the design.

### 8. Apply the tracker taxonomy

Scan the draft for deferral phrases — "deferred", "out of scope", "follow-up", "future work", "later", "revisit if", "tracked at", "next PR", "as part of". Classify each occurrence per the contract:

- **Permanent non-goal** — the thing will never be done; the decision is settled. Record the rationale where the phrase sits (the `N/A — reason` cell or the non-goals section). No tracker issue. A trigger-conditioned phrase ("revisit if N exceeds 50") is not settled: it is intended future work.
- **Intended future work** — the thing will be done, or is conditioned on a trigger. File the tracker issue now per the contract's tracker taxonomy, then cite the verified ID where the phrase sits.

Criterion: every deferral phrase is classified, and every intended-future-work item cites a verified tracker ID.

### 9. Self-review

Run this checkable list before writing `design.md`:

1. Every step-2 shape has a status: a claim row, an `N/A — approved risk` row recorded in the Approval list, or an `N/A — reason` carrying the contract's taxonomy.
2. Every step-2 decision cell has a status: each variant of a classification predicate's domain together with the production conditions that arrive as that variant, each bound's raising knob or `N/A — approved risk` row, each accepting Resource for an offered control, every arm of a dispatch including the arms that refuse, and a verdict for each boundary-representation case step 2 enumerates.
3. Every table row has every field filled with the applicable value or explicit `N/A` defined by its field.
4. Every falsifier records the lowest sufficient verification level; required independent comparisons and every bespoke tool's named gap are explicit.
5. Every Named mutation cell contains a mechanical mutation or the ladder's justified `N/A`; fence-risk rows carry the matching `N/A — approved risk: no fence to mutate`.
6. Every fence assertion satisfies the fence rule stated in the Falsification table's Regression fence field.
7. Every falsifier's output or review record identifies its own claim: if claim N fails, the result says claim N, not "something broke" — and a failing fence prints the state that decided it with diagnostics that cannot abort while unwinding. Split or merge rows until localization holds.
8. Every measurement-based falsifier has a deterministic regression fence that proves the claim, a controlled benchmark qualification satisfying **Performance-fence policy**, or the explicit fence-risk acceptance defined in the Regression fence field; a required unavailable qualification remains `PENDING — <owner/step>`, not `N/A`.
9. Every deferral phrase is classified with a verified tracker ID or a permanent-non-goal rationale.
10. Every new capability has Owner, New seam, and Forbidden; every structural claim has selected ownership verification.
11. Every triggered Length review records its evidence and the requester's **Size stop** choice. When T2 records a module-shape change or the requester chose Reshape, the inventory, alternatives, approved ledger, protected parents, and selected verification satisfy [module shape](references/module-shape.md); otherwise the section cites T2's `N/A`.
12. The cheapest falsifier has run and passed; no row has Status `FAIL`; every `PENDING` row names its discharge owner and step.

Criterion: all twelve hold. A failed check means the design is wrong — fix it, do not waive it.

### 10. Write design.md

`.<change-slug>/design.md` contains, in order:

- **Route and inputs** — the step-1 extraction (route, behavior set, empirical premises, source pointers).
- **Input shapes** — the step-2 enumeration of input shapes and decision cells, with statuses.
- **Placement** — Owner, New seam, and Forbidden per capability.
- **Module shape** — current cluster, alternatives, approved module ledger, protected parents, and selected ownership verification when the Design procedure ran; a **Length review** record with the requester's choice when its trigger applies; or `N/A —` T2 evidence.
- **Claims** — the numbered claim list.
- **Falsification** — the step-6 table.
- **Non-goals and future work** — permanent non-goals with rationale; intended future work with verified tracker IDs.
- **Falsifier run log** — the cheapest falsifier's command and result.
- **Approval** — the step-11 record.

Criterion: every section is populated; the table has no empty cells; the Module shape/Length-review section satisfies its branch.

### 11. Get requester approval

Present the design to the requester: claims, placement, the Module shape ledger and protected parents, any triggered **Length review**, the Falsification table, non-goals, the cheapest falsifier's result, and every risk acceptance (each row carrying `N/A — approved risk`, whether a fence cell or a step-2 decision cell). Ask for approval in their own words.

Record in the Approval section:

- the requester's verbatim approval words, in quotes;
- the date;
- the list of risk acceptances the requester approved, or `None`.

Resolve requester objections before hand-off. Changes to approved decisions follow [workflow contract](references/CONTRACT.md)'s **Approval semantics** and re-record approval; technical verification corrections follow that same boundary rather than restarting design.

Criterion: the Approval section contains the requester's dated, verbatim words and the approved risk-acceptance list.

## Hand-off

[`budgeted-plan`](references/budgeted-plan.md) consumes a design satisfying the Output requirements below. [`checkpointed-build`](references/checkpointed-build.md) reads the Oracle, Named mutation, and Regression fence columns from the Falsification table and applies **Performance-fence policy** for timing claims. Their owner records corrections under [workflow contract](references/CONTRACT.md)'s **Approval semantics** and revalidates affected results under **Evidence validity**; changing an approved decision requires revision and re-approval.

## Output

`.<change-slug>/design.md` carrying:

- the Falsification table — every row with Claim, Input shape, Falsifier, Oracle, Named mutation, Regression fence, Cost, and Status, every cell filled;
- the cheapest falsifier run, with a `PASS` recorded in Status and the run log;
- the non-goals/future-work section with the tracker taxonomy applied;
- the placement decisions (Owner / New seam / Forbidden);
- the approved module ledger, protected parents, and selected ownership verification when T2 applies, with the **Length review** record when its trigger applies, or the evidence-backed `N/A`;
- the Approval section with the requester's verbatim words, the date, and the approved risk-acceptance list.

If any of these is missing, the stage did not run.
