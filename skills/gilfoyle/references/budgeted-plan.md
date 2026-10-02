# budgeted-plan

Turn approved outcomes into independently-green atomic slices. The plan says what changes, where it belongs, and how delivery will be verified; completion is [`checkpointed-build`](references/checkpointed-build.md)'s judgment.

## When this stage runs

Read [workflow contract](references/CONTRACT.md) first and resolve the canonical directory. Consume `route.md` and approved `design.md`, with `spec.md` and empirical evidence by reference when applicable. Missing required decisions return to their owner. A pending external premise blocks only slices dependent on it; pending implementation checks are assigned to their slices.

Review repairs enter here only when scope, dependencies, supplied budget, or delivery partition changes, or an approved spec/design change needs an affected plan update. An implementation or technical verification repair already determined by the contract goes directly from [`assessing-review-feedback`](references/assessing-review-feedback.md) to checkpointed-build's bounded repair entry.

## Process

### 1. Verify the design inputs

Confirm the relevant behavior and ownership decisions are approved, claims have concrete checks and expected results, required uncertain premises are resolved before dependent implementation, and remaining checks have discharge owners. Ordinary tests, captured references, and consumer runs are sufficient when the design's Verification ladder says so. There is no pre-approval cheapest-falsifier requirement or mandatory Oracle/Named mutation placeholder.

**Completion:** design decisions are sufficient to plan, with scoped dependencies explicitly identified and no known failure represented as valid proof.

### 2. Decompose at atomic seams

Group outcomes/claims into the smallest independently-green changes with observable checks. A signature or interface change and every caller migration land together, regardless of file count. Follow approved responsibility seams; do not combine unrelated responsibilities merely because they share a caller. A slice's check cannot depend on a later slice. A claim implemented across slices has one owning completion record, with prerequisite checks referenced rather than duplicated.

**Completion:** every requested outcome and required design check has an owning slice; dependencies are coherent; each completed slice can leave the repository green.

### 3. Write compact slices

Use only these fields; dependencies are conditional:

```markdown
## Slice N: <purpose>

**Outcome:** <observable result; relevant design claim references>
**Changes:** <owners, files, interfaces, and all caller migration; approved placement references>
**Verification:**
- <relevant check or existing evidence reference> → <expected result>
**Dependencies:** <only when any: prerequisite slice, unresolved premise, or required environment>
```

Verification includes relevant regression/boundary checks, real consumer or native execution, repository requirements, and any design-required captured comparison, performance qualification, oracle, or mutation. Reuse existing coverage. New tests target behavior or plausible failure boundaries, not one test per function. Stress fixtures, per-loop budgets, and wall-clock phases are not mandatory fields; include them only when an actual requirement or named uncovered failure mechanism needs them. Provider/host fixtures use captured or documented contracts, safe owned state, and enforced host preconditions. Performance checks reference the design's Performance-fence policy.

Changes carries relevant ownership, forbidden dependency, and protected-parent constraints by reference, not a second module ledger. Reuse existing helpers/dependencies and analyze affected callers during implementation; neither needs a per-symbol or per-literal planning receipt.

**Completion:** every slice states Outcome, Changes, and Verification, plus Dependencies when any. Omitted inapplicable fields do not erase an existing required obligation.

### 4. Record delivery and supplied feature budgets

Keep one delivery increment unless requested delivery or genuinely independent review/merge seams warrant several. Name each increment's slices, dependencies, and how it verifies without later increments; respect spec delivery decisions and discover the actual upstream branch. Do not impose a universal changed-line gate.

When the requester or repository supplies a feature budget, record its approximate production versus tests/proof scope once. A soft overrun records the concrete growth-driving responsibility and why a simpler approach is unsuitable; unchanged scope/architecture may proceed. Explicit requester hard caps and independently enforced repository limits follow the contract's Size stop and need owner authorization to change. No mandatory per-module growth ledger, analog measurement, or churn arithmetic is required. Preserve cohesive ownership and readability rather than splitting or compressing to fit a count.

**Completion:** delivery dependencies are clear; supplied budgets have the appropriate soft explanation or hard-limit authorization, without invented thresholds.

### 5. Apply tracker taxonomy and save

Permanent non-goals keep their rationale; intended future work cites verified tracker IDs under the contract. Check atomic caller migration, relevant coverage, approved ownership, scoped pending dependencies, and required consumer/platform/repository proof. Save `plan.md` with its slices and applicable delivery/budget decisions. This stage never declares implementation complete.

**Completion:** the plan covers the approved work and its relevant checks, with no unresolved decision hidden by a missing field or template placeholder.

## Review re-entry

Read the compact repair record, covering claims, and affected slices. Preserve unaffected decisions and valid evidence by reference. Update only changed Outcome, Changes, Verification, or Dependencies fields and affected delivery/budget decisions; create a slice only for a genuinely new atomic change. Broaden review only when dependency impact is uncertain. A changed product, architecture, or risk decision returns to its owner before updating the plan; a soft budget explanation alone does not require that approval.

Return the affected amendment and existing repair-record reference to checkpointed-build. Repairs update the affected completion record rather than re-declaring previous slices complete.

## Hand-off / Output

`plan.md` contains compact atomic slices, applicable delivery/budget decisions, and identified pending dependencies. Hand off to [`checkpointed-build`](references/checkpointed-build.md). It returns a completion record of delivered behavior, performed checks/results, and unresolved failures to the artifact owner. Record a check once and reference valid evidence rather than duplicating gate states across plan, repair, and publication summaries.
