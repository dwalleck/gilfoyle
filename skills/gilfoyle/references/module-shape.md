# Module shape

Use this reference when a change affects responsibility ownership, interfaces, or dependency direction, or when an actual requester/repository size limit needs interpretation. Line count does not establish architecture.

## Trigger and terms

Module shape applies when responsibilities move, a seam/interface/dependency direction changes, a production split/merge/deletion changes ownership, a new module will own substantial implementation, or a new responsibility enters a multi-responsibility orchestrator/facade. Growth within an existing responsibility alone does not force structural redesign, a map, or an extra review.

- **Responsibility cluster** — behavior that changes for the same reason and is verified through the same interface.
- **Protected parent** — an existing file permitted declarations/wiring but no new responsibility body.
- **Module ledger** — the applicable ownership/interface decisions in `design.md`, including forbidden responsibilities/dependencies and test surfaces.
- **Module-shape fence** — an optional automated tripwire for declared constraints, not proof of arbitrary source semantics.

Read [workflow contract](references/CONTRACT.md) for ownership, Evidence validity, Approval semantics, Verification complexity stop, and Size stop.

## Length review

Inspect actual requester hard caps and independently enforced repository limits; retain their scope, counting convention, authority, and enforcement. Exceeding or changing a hard limit needs owner approval under Size stop. An inherited hard gate cannot be called soft because this workflow would prefer a smaller process.

For a supplied soft feature budget, distinguish production from tests/proof. An overrun needs a concrete responsibility/growth reason and why a simpler approach is unsuitable, recorded once in `plan.md` (or `route.md` for Local work). Unchanged scope/architecture can proceed without a requester round-trip. No per-module projections, churn arithmetic, or workflow-generated thresholds are required.

Keep useful comments, normal formatting, and readable cohesive code. Compression, changed counting exclusions, and pass-through splitting merely to fit a number are not valid dispositions. A reshape must earn its design value independently of line savings and follows ordinary architecture approval.

**Criterion:** real hard limits are satisfied or have authorized changes; any supplied soft-budget overrun has its single explanation; no count-fitting evasion is used.

## Design procedure

### 1. Identify relevant owners

Inspect touched and plausible owner modules for their interfaces, caller-visible invariants/errors/order, responsibility clusters, dependencies, callers/test surfaces, and real adapters. Record only the ownership facts needed to decide this change, not a mandatory production-line census. Classify relevant moves as retain, deepen, split, merge, delete, or create.

**Criterion:** responsibilities affected by the change and plausible owners are understood.

### 2. Test proposed seams

- **Deletion:** deleting a useful module exposes hidden complexity across callers; a pass-through adds no depth.
- **Interface:** callers and tests exercise behavior through the same seam rather than reaching into implementation details.
- **Adapters:** prefer a concrete private module over a generic seam with one real adapter unless an intrinsic ownership constraint justifies it.
- **Locality:** each responsibility has a coherent owner and primary behavioral test surface.

**Criterion:** applicable tests support the selected seam, or the design changes.

### 3. Compare genuine alternatives

When ownership is ambiguous, make a concise comparison of plausible owners/seams using interface depth, caller simplicity, dependency direction, locality, and testability. Select one with the consequential reason. No fixed number of alternatives or mandatory caller-example template is required. An unambiguous existing owner needs only its reason.

**Criterion:** the selected owner and interface have a defensible basis rather than a numeric alternatives quota.

### 4. Record applicable ownership constraints

In design.md's Module shape section, record the relevant modules/interfaces, owned and forbidden responsibilities, reuse/adapters, and tests through the seam. For protected parents, state allowed wiring, forbidden bodies, and checkable final ownership. Use a compact table when useful; a separate reconstruction map is not required.

**Criterion:** every moved/new responsibility has one approved owner; no module owns both sides of an approved seam; relevant protected-parent constraints are checkable.

### 5. Select sufficient verification

Default to available compiler visibility/dependency checks and ordinary independent review of the affected ownership/interfaces. Implementer self-checks support those checks but do not substitute for independent review. Reuse repository enforcement rather than forking it. Real ownership, dependency, or security violations remain blocking.

A custom source gate requires a named concrete coverage gap left by those mechanisms and a reason automation is needed. Bound it to the declared paths/symbols/dependencies; do not build a parser solely for a small feature's placement. Accidental-placement tripwires do not claim adversarial security coverage. Select additional mutation proof through [`falsifiable-design`](references/falsifiable-design.md)'s Verification ladder. Apply complexity-stop retirement/replacement when ordinary evidence establishes the required coverage; do not harden solely to detect more hypothetical evasions.

**Criterion:** real constraints have sufficient evidence and any bespoke machinery has a named gap. Required repository/security checks remain intact.

## Planning and build contract

Use each slice's **Changes** for relevant owners, interfaces, atomic caller migration, and protected-parent rules; **Verification** names selected checks and expected results. Reference approved constraints instead of copying them into extra fields. There is no module-growth ledger requirement.

At checkpoint, verify affected ownership/interfaces/dependencies and selected enforcement with fresh or valid retained evidence. Changed architecture returns to design for approval; implementation corrections stay bounded. A soft feature-budget overrun alone does not reopen architecture or stop implementation. Hard-limit changes follow Length review.

**Criterion:** delivered ownership matches approved decisions, relevant checks pass, and no required structural/security obligation remains unresolved.

## Final design-conformance review

Ordinary independent code review covers assembled behavior, ownership, interfaces, dependencies, and relevant design constraints. The reviewer may inspect approved design/context. Record reviewer, scope, inspected state, findings/dispositions, and result in the existing completion record. A module change alone does not force reconstruction, a separate map, or another review pass.

Use **isolated reconstruction** only when the requester explicitly requires it or a named unresolved architectural risk cannot be answered by ordinary review. Record that trigger and scope. In that branch, a non-implementer in an isolated context starts from production code without the implementation transcript or approved ledger, reconstructs the relevant ownership/interfaces/dependencies, then compares with the approved design. Record the reconstruction and mismatch dispositions. If required isolation is unavailable, its required review remains unresolved rather than being replaced by implementer self-attestation.

After repairs, independently inspect the repair diff and affected interactions; retain unaffected review under Evidence validity. Re-run full review only where changed assumptions invalidate its broader conclusions, not because an earlier round had blockers now repaired. Actual product/security defects and missing required evidence block completion; a checker sensitivity limitation blocks only when a named required coverage gap remains.

**Criterion:** substantive independent review is valid for the assembled change and all blocking findings are resolved; any specifically required isolated review is also satisfied.
