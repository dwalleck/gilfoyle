# Module shape

Use this reference for T2's length-gate inspection or when `route.md` records a module-shape change or length-review trigger. It makes responsibility ownership, interface depth, protected-parent growth, and their enforcement explicit without treating line count as architecture.

## Trigger

Module shape applies when a change:

- adds or moves a responsibility between modules;
- introduces, removes, or changes a seam, interface, or dependency direction;
- adds a new responsibility cluster to an orchestrator, facade, or other file that already owns several clusters;
- splits, merges, or deletes a production module in a way that changes responsibility ownership or interfaces;
- creates a production module expected to accumulate substantial implementation; or
- reaches a length-review trigger defined below, including a threshold inherited from an earlier feature.

A local change within an existing responsibility stays Local despite its size or growth unless the requester answers a length-review trigger's **Size stop** with Reshape.

## Terms

- **Responsibility cluster** — behavior that changes for the same reason and is verified through the same interface.
- **Protected parent** — an existing file that may receive declarations or wiring but no new responsibility body.
- **Module ledger** — the approved table of modules, interfaces, owned and forbidden responsibilities, adapters, and test surfaces. `falsifiable-design` owns it in `design.md`.
- **Module growth ledger** — the slice-by-slice projection of responsibility, interface, and production-line changes. `budgeted-plan` owns it in `plan.md`.
- **Module-shape fence** — an optional automated tripwire for declared ledger violations, not proof of arbitrary source semantics.

File and line counts are tripwires. They can expose concentration or plan drift; they do not prove depth and never justify pass-through splitting.

## Length review

A length threshold is a **review tripwire**, not a permanent architectural maximum. Review when the contract's **Size stop** trigger applies. Check inherited repository gates as well as the current growth ledger; a future feature uses its own projection, not the old feature's size assumptions. An observed overrun during implementation triggers the same review before further growth or gate changes.

A **Length review** records: path, gate/policy owner and counting convention, baseline, current/projected size, threshold and margin, added feature/responsibility, and the requester's disposition. `change-workflow` records it in `route.md`'s T2 evidence when routing or Local work finds the trigger; `falsifiable-design` carries that record into `design.md`'s Module shape section, or records a later-found trigger there. The disposition comes from the contract's **Size stop**; present it before any redesign work:

- **Retain and raise** — record the new threshold and growth rationale, preserving the ownership and dependency rules.
- **Reshape** — run the Design procedure below on the affected module and candidate owners, assessing cohesion, interface depth, dependency direction, locality, and test surface against the new feature. Record the selected split or redesign (responsibilities, destination paths, interfaces, dependencies, tests through each seam), the resulting thresholds, and atomic migration slices; the redesign returns for approval with the design.
- **Defer** — record the accepted overrun and the verified tracker ID for the reshape.

`budgeted-plan` then updates affected projections/slices.

Preserve useful comments, normal formatting, and readable code. Removing useful comments, packing statements, changing counting exclusions, or creating pass-through files merely to pass a length gate is not a disposition. Simplification must earn its place through better design independently of line savings. The checkpoint's Module shape receipt records a diff inspection for these evasions and resolves any found before `PASS`.

Keep the threshold's scope, counting convention, rationale, and link to the approved review in the existing policy ledger (or the issue-local manifest when no shared gate exists). Gate diagnostics name the path, observed/projected size, threshold, and this review procedure so later features reach the same decision rather than treating the number as immutable.

**Criterion:** every triggered threshold has the requester's recorded retain-and-raise, reshape, or defer choice, corresponding policy/plan updates, and passing affected shape checks before the checkpoint completes.

## Design procedure

### 1. Inventory the current cluster

For every production module the change may touch, record:

- exact path and production-line count as a signal;
- interface, including invariants, ordering, errors, configuration, and performance facts callers must know;
- responsibility clusters;
- dependencies and dependency direction;
- callers and tests crossing the interface; and
- concrete adapters at each existing seam.

Classify each module `retain`, `deepen`, `split`, `merge`, `delete`, or `create`.

**Criterion:** every touched or candidate-owner module has one inventory row; no responsibility relevant to the change is implicit.

### 2. Test the proposed seams

Apply all four tests:

1. **Deletion test:** deleting the proposed module makes hidden complexity reappear across callers. If complexity vanishes, the module is pass-through.
2. **Interface test:** callers and tests exercise behavior through the same seam; tests do not require implementation internals.
3. **Adapter test:** a new generic seam has at least two real adapters. Otherwise prefer a concrete private module. An intrinsic ownership seam such as `Send` actor to serial mediator records that reason instead of inventing adapters.
4. **Locality test:** each responsibility has one owner and one primary verification location.

**Criterion:** every retained or new seam passes all applicable tests or the design changes.

### 3. Design it three ways when ownership is a decision

When a new seam, split, merge, or candidate owner has more than one plausible shape, produce three materially different alternatives:

1. minimize the interface and maximize leverage per entry point;
2. optimize the common caller and make its default path trivial; and
3. optimize extension flexibility without exposing implementation knowledge.

For each, show the interface, a caller example, hidden implementation, dependency/adapters strategy, and trade-offs. Compare depth, locality, seam placement, dependency direction, and test surface; select one with a reason. A capability that fits unambiguously behind an existing interface records `N/A — existing seam: <reason>`.

**Criterion:** every disputed ownership or new seam has three real alternatives and one selected shape; renamings of the same interface do not count.

### 4. Approve the module ledger

Record:

| Module/path | Interface | Owns | Hides/reuses | Must not own | Adapters | Tests through | Change |
|---|---|---|---|---|---|---|---|
| `<path>` | `<caller knowledge>` | `<responsibility clusters>` | `<internal modules>` | `<forbidden clusters/dependencies>` | `<real adapters or N/A>` | `<interface>` | `retain/deepen/split/merge/delete/create` |

For every protected parent, also record:

| Protected parent | Baseline responsibilities | Allowed change | Forbidden change | Exit condition |
|---|---|---|---|---|
| `<path>` | `<clusters>` | `<declarations/wiring>` | `<new responsibility bodies>` | `<checkable final shape>` |

**Criterion:** every responsibility has exactly one owner; every interface has a caller; every protected parent has a checkable exit condition; no module owns both sides of an approved seam.

### 5. Select structural verification

For every applicable ledger rule, record a claim with its observable, covered paths/symbols, and selected evidence in the Falsification table. Default to available compiler visibility/dependency checks plus an explicit per-slice ownership self-check by the implementer, with independent help allowed, covering what those checks cannot enforce. Record its performer, any helper, revision, inspected paths, responsibility owners, forbidden responsibilities, protected-parent deltas, and result in the owning checkpoint record. The final isolated design-conformance review is authoritative; this self-check is not independent evidence and cannot replace it.

Use an existing repository gate when it already owns the rule; extend its policy rather than forking a copy. A real ownership, visibility, or dependency violation is `FAIL`, not a reason to mark verification `N/A`. Gate changes follow `checkpointed-build`'s **Preserved enforcement** requirement; length thresholds follow **Length review**.

A custom source-analysis gate needs a named concrete gap left by these checks/review and a separate design justification for automation. Bound it to the declared paths, symbols, dependencies, test locations, deltas, or thresholds. Reuse an established analyzer where one covers the gap; **never build a language parser solely to enforce a small feature's placement**. Keep accidental-placement tripwires scoped to accidental violations. An explicitly declared adversarial/security obligation requires its own detection coverage and cannot be narrowed by calling it a tripwire.

An applicable fence reports the claim ID and exact path/symbol/delta, stays outside production code and behavioral production tests, and uses the contract's branch discovery. Select its mutation proof, or ordinary ownership-only `N/A` entries, through [`falsifiable-design`](references/falsifiable-design.md)'s **Verification ladder**; apply the contract's **Verification complexity stop** before further hardening.

**Criterion:** every applicable ledger rule has concrete verification coverage and expected results; every custom gate has a named gap and separate design justification. Ordinary ownership self-check needs no bespoke fence or risk acceptance, and actual ownership violations remain blocking.

## Planning contract

Each slice records a **Module shape** field:

- responsibility added, moved, or deleted;
- interface change;
- owner after the slice;
- protected parents touched and their expected production delta; and
- selected checks and scoped ownership self-check, or justified custom fence, with expected results.

`plan.md` also carries the module growth ledger:

| Module | Baseline production lines | Projected final lines | Responsibility change | Interface change | Protected-parent rule |
|---|---:|---:|---|---|---|

Numeric projections are tripwires with rationale; approaching or exceeding them follows **Length review**, then the plan owner incorporates the approved disposition.

**Criterion:** every slice preserves the approved ledger or completes an approved move atomically; every touched module appears in the growth ledger.

## Build contract

At each slice or bounded-repair checkpoint, establish these obligations with fresh or valid retained evidence under [workflow contract](references/CONTRACT.md)'s **Evidence validity** rule:

- actual paths, responsibilities, interfaces, and dependency direction match the approved ledger;
- protected-parent deltas match the plan;
- the selected checks and scoped ownership self-check pass, including any applicable shared or custom gate;
- applicable mutation/restoration proof satisfies the Verification ladder and Evidence validity; and
- any deviation in responsibility ownership returns to `falsifiable-design` rather than being rationalized as plan drift.

Numeric growth triggers follow **Length review** even when placement is unchanged. A new responsibility, wider interface, different seam, or pass-through split likewise returns to `falsifiable-design` and requester approval.

**Criterion:** module-shape gate is `PASS`, or `N/A — route and design record no module-shape change`; no placement deviation is deferred.

## Final design-conformance review

After the assembled implementation passes its behavioral gates, a reviewer who did not implement the change reconstructs from production code:

- each module's interface and responsibility clusters;
- dependency direction and concrete adapters;
- pass-through modules and hypothetical seams;
- protected-parent growth; and
- tests reaching past an interface.

The reviewer starts without the implementation transcript, plan rationale, or approved ledger. A separate reviewer is preferred; otherwise start a fresh process/context carrying only the production tree and this reconstruction task. After recording the reconstruction, reveal `design.md`, compare it with the approved ledger, and fix every mismatch or revise and reapprove the design. Inability to obtain an isolated context blocks completion; same-context implementer self-attestation is not a review.

The final checkpoint record names the reviewer or isolation method, carries the reconstructed module/interface/responsibility map, lists every mismatch and disposition, and records the final comparison result.

For a later repair or assembled checkpoint, retain a prior isolated review only when **Evidence validity** establishes that its reconstruction and comparison still apply; cite the record and the applicability reason. Rerun invalidated structural review in the isolated context above, covering the affected ownership/interfaces and broadening when impact is uncertain. Valid retention avoids repeated review, not the final assembled-tree conformance obligation.

**Criterion:** every changed production module maps back to exactly one approved ledger row, every mismatch is resolved, and the recorded fresh-context comparison is `PASS` before completion.
