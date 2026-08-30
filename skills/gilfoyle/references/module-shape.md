# Module shape

Use this reference only when `route.md` records a module-shape change under T2. It makes responsibility ownership, interface depth, protected-parent growth, and their enforcement explicit without treating line count as architecture.

## Trigger

Module shape applies when a change:

- adds or moves a responsibility between modules;
- introduces, removes, or changes a seam, interface, or dependency direction;
- adds a new responsibility cluster to an orchestrator, facade, or other file that already owns several clusters;
- splits, merges, or deletes a production module in a way that changes responsibility ownership or interfaces; or
- creates a production module expected to accumulate substantial implementation.

A local change within an existing responsibility does not trigger module shape solely because its file is large or its implementation grows behind an unchanged interface.

## Terms

- **Responsibility cluster** — behavior that changes for the same reason and is verified through the same interface.
- **Protected parent** — an existing file that may receive declarations or wiring but no new responsibility body.
- **Module ledger** — the approved table of modules, interfaces, owned and forbidden responsibilities, adapters, and test surfaces. `falsifiable-design` owns it in `design.md`.
- **Module growth ledger** — the slice-by-slice projection of responsibility, interface, and production-line changes. `budgeted-plan` owns it in `plan.md`.
- **Module-shape fence** — a deterministic non-production oracle comparing the source tree and diff with the approved module ledger.

File and line counts are tripwires. They can expose concentration or plan drift; they do not prove depth and never justify pass-through splitting.

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

### 5. Define a mechanical shape claim

Every ledger rule that can regress becomes a design claim. Its falsifier is a source/dependency/diff census, not reviewer intuition. The permanent fence SHOULD be an issue-local standalone oracle under `.<change-slug>/oracles/` and MAY use an issue-local data manifest when that keeps policy out of code.

The fence checks the applicable set of:

- required and forbidden paths;
- imports and dependency direction;
- forbidden symbol ownership;
- interface visibility or entry-point shape;
- protected-parent production deltas;
- required test locations; and
- planned file-growth tripwires.

It reports the claim ID and exact path/symbol/delta. It discovers the default/upstream branch through the workflow contract rather than hard-coding a branch. It never runs from production code or reads source text from a behavioral production test.

Each shape claim names a buggy source mutation such as moving a handler into a protected facade, importing a domain type into a transport adapter, widening an interface, or adding a hypothetical generic trait. The mutation must make the fence red; restoration returns it green.

**Criterion:** every mechanical ledger rule has a claim, decisive oracle, applicable named mutation, and expected localized red output; judgement-only risks are explicit in requester approval.

## Planning contract

Each slice records a **Module shape** field:

- responsibility added, moved, or deleted;
- interface change;
- owner after the slice;
- protected parents touched and their expected production delta; and
- exact module-shape fence command and expected result.

`plan.md` also carries the module growth ledger:

| Module | Baseline production lines | Projected final lines | Responsibility change | Interface change | Protected-parent rule |
|---|---:|---:|---|---|---|

Numeric projections are tripwires with rationale. Exceeding one requires inspecting the responsibility and interface change: revise the plan when placement still holds; return to design and requester approval when it does not.

**Criterion:** every slice preserves the approved ledger or completes an approved move atomically; every touched module appears in the growth ledger.

## Build contract

At each slice checkpoint:

- actual paths, responsibilities, interfaces, and dependency direction match the approved ledger;
- protected-parent deltas match the plan;
- the module-shape fence passes;
- every new shape-fence mutation is red and restoration is green; and
- any deviation in responsibility ownership returns to `falsifiable-design` rather than being rationalized as plan drift.

A numeric projection overrun with unchanged placement returns to `budgeted-plan`. A new responsibility, wider interface, different seam, or pass-through split returns to `falsifiable-design` and requester approval.

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

**Criterion:** every changed production module maps back to exactly one approved ledger row, every mismatch is resolved, and the recorded fresh-context comparison is `PASS` before completion.
