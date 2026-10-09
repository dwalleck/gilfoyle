# falsifiable-design

Design the requested outcomes and choose evidence that can show when they are wrong. Claims cover consumer behavior, compatibility/safety boundaries, and plausible failure modes introduced by this change; the design is not an inventory of every enum, option, field-presence combination, or implementation branch.

## When this stage runs

Read [workflow contract](references/CONTRACT.md) first. This stage owns `design.md` for Structural and Empirical routes; Local uses normal repository fix/TDD and focused verification. Resolve the existing artifact directory under the contract, routing first if none exists.

Inputs are `route.md`, `spec.md` when required, and `evidence.md` when unresolved external premises have been investigated. A throwaway `probe.*` is needed only when the smallest sufficient observation required one. An unresolved premise blocks only design decisions and implementation dependent on its answer, not unrelated settled work. Design may record those dependencies as `PENDING`; completion must identify them rather than report whole-design proof.

## Verification ladder

Choose the lowest sufficient evidence for each claim:

1. **Existing behavioral tests** — reuse or extend established tests asserting consumer-visible outcomes.
2. **Real consumer execution** — drive the actual entry point to cover integration, lifecycle, host, and environment behavior. Required smoke/native runs remain necessary even when tests cover the logic.
3. **Captured reference outputs** — for stable ports, prefer representative inputs and reference outputs committed together with provenance (reference revision/version, capture command, relevant environment) and compare at the approved byte/value/behavior fidelity. Expected-output changes derive from the approved behavior contract or independently established reference evidence, never current implementation output alone. Goldens do not replace native lifecycle proof.
4. **Additional investigation or machinery** — live differential comparisons, custom oracles, fuzzing, and mutations require a named failure mechanism not covered above or an explicit repository requirement. Complexity or a high-risk label alone is not that gap. Prefer established references and tools; do not create a second implementation solely to prove the first. State the gap, relevant inputs, and expected discriminating result.

Use compiler/dependency checks and ordinary independent review for ownership; [module shape](references/module-shape.md) scopes that work. Omit inapplicable Oracle or Named mutation fields rather than filling repeated N/A cells. Explain a contested applicability choice once. Existing required coverage and repository gates cannot disappear through omission.

### Mutation sensitivity

Bug fixes require observed sensitivity to the real defect. Prefer the actual pre-fix red and post-fix green observations, with checked revisions and the intended observable. Reuse valid observations. If they are unavailable, use the smallest controlled reproduction or named fault that establishes the same defect sensitivity and state its limit. Routine review-requested coverage for already-correct behavior does not mandate mutation; record what it verifies and its result.

Additional named mutations are justified by a demonstrated blind/vacuous check, a named uncovered failure mechanism, or explicit repository requirements. A required mutation states the plausible defect, actual code change, and expected red observable. Compilation failure unrelated to the claim, unchanged observables, and two green runs do not demonstrate sensitivity. Preserve applicable red/restored-green evidence under the contract's Evidence validity. Proof is bounded to the declared obligation, not arbitrary future checker evasions. A focused test observed red against the pre-change code already shows sensitivity for its claim: record that run rather than naming a mutation for it. Name mutations only for claims whose tests could not run red first.

## Process

### 1. Read the inputs

Extract requested outcomes, compatibility/safety boundaries, important errors, scope, and real requester decisions from `spec.md`, or from `route.md`'s T4 evidence when behavior is already explicit. A grouped outcome contract is sufficient; no separate triple for every case is required. Link the source rather than copying it. Read applicable external-premise evidence and identify only unresolved facts whose answers could change this design.

Documentation, dependency source, current tests, and valid previous observations may resolve a premise. Selecting or approving a library does not establish its unspecified runtime behavior. A dependency change invalidates only conclusions whose assumptions it affects, not every prior decision or observation.

**Completion:** Route and inputs identifies the behavior source, relevant premise evidence, and any scoped unresolved dependency.

### 2. Identify outcome boundaries and introduced failure modes

Group equivalent inputs around requested outcomes and plausible regressions. Cover relevant empty/missing inputs, boundaries, important errors, concurrency, resource ownership, permission/tenancy, and representation fidelity where this change can affect them. Provider fixtures derive from captured payloads or the published contract, not the implementation's expectations.

Check caller-visible limits, controls, error classifications, dispatches, and representation changes when they can violate the requested outcome. A bound that materially restricts accepted behavior is a product tradeoff, not a hidden tuning choice. Reconcile relevant caller and enforcing boundaries, including framing overhead. Do not enumerate every variant or presence combination merely because it exists; group those with equivalent behavior and preserve the cases that distinguish a plausible failure.

**Completion:** the design identifies required outcomes/boundaries and plausible introduced failure mechanisms with sufficient representative cases to choose verification.

### 3. Preserve removed invariants

For a removed guard, serialization point, validation, ordering guarantee, or other constraint, identify what observable guarantees it enforced and inspect affected readers/mutators/callers. Moves and reroutes preserve predecessor behavior, important error taxonomy, and required serialized output unless an approved decision changes them. Record still-safe reasoning or verification for newly possible violations.

For changed verification machinery, name still-required outcomes and coverage, and where replacement evidence supplies them. Apply the contract's **Verification complexity stop** and **Approval semantics**: retiring a redundant checker is not itself a product-risk decision, but losing unique required coverage, real guards, or mandated checks is not a technical simplification.

**Completion:** relevant guarantees remain enforced and verified, or their changed product/risk decision has approval.

### 4. Place the design

Use T2's ownership/interface evidence. When module shape changes, read [module shape](references/module-shape.md) and execute its Design procedure. Use a concise comparison when ownership is genuinely ambiguous; no fixed number of alternatives is required. An obvious existing owner needs a reason, not an alternatives exercise.

For capabilities record **Owner**, **New seam** when any, and **Forbidden** responsibilities/dependency directions where relevant. Prefer an existing cohesive owner and concrete interface. Reject generic seams with one adapter unless an intrinsic ownership constraint makes the seam real. Select concrete compiler/dependency checks or scoped review for ownership constraints that could regress. Apply the contract's Size stop only according to the threshold's actual authority; no module-growth projection is mandatory.

**Completion:** relevant ownership and interfaces are clear, approved seams remain cohesive, and real structural constraints have checkable coverage.

### 5. Write claims and verification

Assign claim IDs (`C1`, `C2`, …) to outcomes, compatibility/safety boundaries, and plausible introduced failures. Group cases sharing an outcome and verification. Use this compact Falsification table:

| ID | Claim and covered cases | Falsifier / verification | Regression coverage | Status |
|---|---|---|---|---|

The **Falsifier / verification** names the relevant test, consumer run, captured comparison, or other justified check, its expected result, and what would falsify the claim. Anchor at the level claimed: an internal helper check alone cannot prove a public-entry-point promise. Where a check could pass for the wrong reason, add the discriminating case or positive control that resolves that ambiguity, particularly for absence assertions and guards hidden behind upstream rejection.

**Regression coverage** references sufficient existing or new behavioral coverage; no per-function test mandate applies. Preserve required regression reproducers. A permanent behavioral fence omitted despite a required obligation needs explicit risk approval, not an empty cell. Ownership-only claims can use compiler/dependency checks and independent review. State **Oracle** or **Named mutation** alongside the row only when selected under the ladder, and include the required protocol. A reference capture must carry its inputs/provenance and approved fidelity.

**Status** is `PASS` with evidence, `FAIL`, or `PENDING — owner/step`. Planned implementation checks can remain pending until their implementing slice; there is no mandatory cheapest-falsifier run before design approval. A real failing requirement remains blocking until corrected or legitimately changed under Approval semantics.

**Completion:** every claim has relevant verification and regression coverage, applicable additional machinery has a named gap/requirement, and pending checks have owners. No required obligation is hidden by an omitted conditional field.

### 6. Resolve specific uncertain premises

When an external/system fact remains unresolved and its answer could change this design, return the factual question to [`prove-it-prototype`](references/prove-it-prototype.md), correcting T1 through the route owner if needed. Use existing sources first, then the smallest real observation. Block only dependent implementation; retain unrelated decisions and valid evidence. Library selection alone neither answers a runtime premise nor triggers global requalification.

**Completion:** decisions relying on uncertain facts either have valid evidence or an explicit pending dependency. Do not approve that uncertain choice as settled; unaffected design decisions may proceed.

### 7. Apply tracker taxonomy and self-review

Classify permanent non-goals with their rationale and intended future work with verified tracker IDs. Check that the design covers requested outcomes and relevant failures, preserves enforcement and caller compatibility, selects sufficient ordinary evidence before bespoke tools, and identifies real approvals and pending dependencies. Resolve contradictions rather than adding a superseding paragraph.

**Completion:** the design is coherent, scoped, and explicit about required proof and pending work.

### 8. Write and approve design.md

The artifact contains **Route and inputs**, **Claims / Falsification**, **Placement**, applicable **Module shape**, **Non-goals and future work**, evidence links for performed investigations, and **Approval**. Omit inapplicable sections. Present the behavior, ownership/interfaces, relevant tradeoffs, verification choices, and explicit risk acceptances. Record dated requester approval or delegated approval under the contract; identify any pending dependency and the decisions it blocks.

Technical verification corrections preserve approval when the contract permits them. Changed behavior, scope, architecture, required comparison meaning, or accepted risk returns for the relevant decision only.

**Completion:** settled decisions are approved, required pre-implementation premises are resolved before dependent work, and remaining implementation checks have named discharge owners.

## Performance-fence policy

Apply only to an actual performance requirement, not every loop or cleanup timer. Prefer deterministic work/operation or virtual-clock assertions when they establish the requirement; preserve relevant concurrency. For real latency, use controlled qualification with runner/resource class, profile, warmup, repetitions, statistic, workload/concurrency, execution mode, calibrated threshold and variance margin. Record the command, source/environment, samples, and rationale once in the claim's verification. Missing required calibration or environment remains pending and blocks performance qualification; timeouts are hang guards, not latency proof. Run the declared protocol rather than retrying until green or widening the bound. An applicable named latency mutation must be detected under that same protocol. The plan references this evidence from Verification, not a separate budget template.

## Hand-off / Output

[`budgeted-plan`](references/budgeted-plan.md) receives `design.md` with approved outcomes/placement, scoped claims and checks, applicable module ownership, non-goals/future work, and identified pending dependencies. No global cheapest-check PASS is required. Each slice inherits relevant obligations by reference; dependent implementation waits for its required premise evidence. [`checkpointed-build`](references/checkpointed-build.md) judges the delivered behavior and performed verification, including required regression, consumer/native, performance, repository, and independent-review evidence.
