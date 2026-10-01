# checkpointed-build

You are not typing the plan. You are advancing the design hypothesis by one slice and checking it against reality. The plan is the current best guess. Reality is the authority. When they disagree, you stop.

Stopping is the most important step. Drift caught at slice N is cheap; drift caught at slice N+8 is the entire feature.

## When this stage runs

After [`budgeted-plan`](references/budgeted-plan.md) has produced a plan with all gates passing — not before. Before consuming `plan.md`, read [workflow contract](references/CONTRACT.md): it owns the gate states, evidence validity, approval semantics, slice and independent-oracle definitions, branch discovery, review-size tripwire, and tracker discovery used here. Initial slices retain the full entry and critique requirements below; approved-contract review and qualification repairs use the bounded entry.

### Bounded repair entry

For a fix determined by the approved contract under its **Approval semantics**, consume only the covering claims or established obligations and owning slices:

- **Review finding:** consume the **Compact repair record** from [`assessing-review-feedback`](references/assessing-review-feedback.md), even if the owning slice is already committed. That stage owns the record's format and incorporates this stage's returned gate judgment.
- **Qualification failure during implementation or final integration:** stay in this stage. The existing owning slice record carries the failure, root-cause correction, governing obligation, and affected-check results and evidence disposition; name the responsible slices for a cross-slice interaction. Use this record even when the slice is already committed; no review finding or separate repair artifact is required.

Inherit unchanged approved plan fields by reference; critique only the affected inherited obligations. Perform the relevant impact analysis, helper search, implementation/TDD, symmetry audit, and proof steps below for the repair, not a fresh 14-field slice or a replay of the whole slice cycle. Reconcile all eleven gate states using fresh or valid retained evidence, then apply the relevant sweep, atomic commit, drift, and size obligations to the actual change.

Escalation follows the contract's **Approval semantics**; a changed or unresolved approved decision returns to the owning design/spec stage for approval and then `budgeted-plan` for the affected plan update. Changed plan scope, budget, or partition inputs go to the plan owner for an affected-only update. Bounded repair does not waive changed obligations or initial approval.

## The gate — stated once

Slice completion is this stage's job, and this is the whole gate. One checkpoint per *completed* slice or atomic bounded repair — never per unit-test cycle, never batched across slices. Every item is recorded as `PASS`, `FAIL`, or `N/A — reason` per [workflow contract](references/CONTRACT.md); a conditional item that does not apply is recorded as `N/A` with the plan, design, or route fact that makes it so. Apply the contract's **Evidence validity** rule to every result: run new or invalidated proof and retain applicable conclusions with a prior-result reference and short applicability reason. `N/A` never substitutes for missing proof.

1. **Affected unit tests** pass — or `N/A — reason` when the slice changes no executable behavior and `plan.md` records no affected tests.
2. **Falsifiers** assigned to this slice pass: discharge `PENDING` falsifiers and rerun invalidated `PASS` falsifiers; retain still-valid `PASS` results — or `N/A — reason` when no falsifier applies here. `PENDING` is a lifecycle status, not a gate state, per [workflow contract](references/CONTRACT.md).
3. **Stress fixture** produces the plan's expected outcome — or `N/A — reason` when the plan records no fixture for this slice.
4. **Changed implementation vs independent oracle** agree on the plan's input when the approved design requires comparison; otherwise carry its exact ladder-backed `N/A` and concrete rationale.
5. **Approved module shape** holds: actual responsibility and interface ownership, dependency direction, protected-parent deltas, and paths match `design.md` and `plan.md`; the selected checks, including the per-slice ownership self-check, pass — or `N/A — route and design record no module-shape change`.
6. **Production-scale budget** holds for every applicable loop or phase the plan records with a production-scale or wall-clock budget, including explicit one-off latency obligations — with a separate `N/A — reason` for each budget class the plan marks inapplicable.
7. **Regression fence** green — or the design's exact ownership-verification or approved-risk `N/A` from its Regression fence cell.
8. **Named mutation** red when applicable: new or changed fences, or changed mutation applicability, require fresh proof; otherwise retain valid red evidence. For an inapplicable mutation, carry the design/plan's exact ladder-backed or approved-risk `N/A`.
9. **Fence restored** green after applicable mutation runs, or valid retained restoration evidence; if item 8 is `N/A`, record `N/A — no mutation required: <item 8 reference>`. Item 7 still establishes any required fence's green result.
10. **Parity and reuse** — the slice record lists, for every symbol the slice adds or changes (utility, constant, error constructor, validator, limit constructor, test helper) and for every construction the diff writes a second time instead of sharing (a copied helper body or preamble, a re-typed literal, a duplicated match over the same variants, a list that duplicates a convention), the sibling symbol it reuses (path and name) or the justification kept beside the divergent code — citing the approved claim, established obligation, or `N/A — approved risk` row that makes the divergence deliberate, with a verified tracker ID where it defers follow-up work — together with the search performed (symbol-aware, `grep`, or both). It also answers every symmetry-audit question (step 4 of this document) for each path added or repaired beside an existing one, and for each acceptance predicate or comparison it tightens or relaxes. `N/A — reason` only when the slice adds or changes no such symbol, writes no construction a second time, adds or repairs no parallel path, tightens or relaxes no acceptance predicate, and records no utility reuse decision. Record the receipt in the owning slice or repair record, like step 1's caller list; `budgeted-plan` names no field for it.
11. **Preserved enforcement** — the slice or repair record names every pre-existing gate, fence, validator, oracle, or policy file the diff repoints, relaxes, deletes, or leaves loaded by nothing, with the approved claim, established obligation, or `N/A — approved risk` row that authorizes it, and a verified tracker ID where the change defers work. Run the replaced revision's recorded cases for every still-required verification obligation. Explicitly account for any dropped detection case and its approved scope/risk decision; a narrower checker claim alone does not remove a product requirement. `N/A — reason` only when the diff touches or orphans no such artifact.

Item 2 discharges the design row's falsifier using its declared protocol; items 7-9 record regression coverage and applicable mutation proof; items 10-11 are receipts that neither a run nor a mutation can supply. Apply [`falsifiable-design`](references/falsifiable-design.md)'s **Verification ladder** rather than constructing infrastructure to fill eleven rows. When one check supplies multiple applicable items, run it once and reference the result in each.

A `FAIL` on any applicable item stops the slice: no commit, no next slice. A failed gate never authorizes shipping. A known issue may explain a failure; it never waives it.

## Before the first slice: critique the plan

Read `plan.md` top to bottom. Flag any slice where a field that actually appears in the plan is implausible:

- A **loop budget** that misstates its own cost (`O(n)` over `files × symbols` is not `O(n)`).
- A **stress fixture** too gentle to fail a plausible bug (three items do not surface scaling bugs), or a production budget measured on the cheapest admitted shape (one path segment against a one-entry tree bounds nothing).
- An **oracle** coupled to the implementation, a bespoke checker without a named gap, or an `N/A` that omits required comparison/mutation under the **Verification ladder**.
- **Documented preconditions** with missing or misclassified enforcement: a load-bearing-for-correctness precondition needs a runtime check that survives release builds; a sanity hint gets a `debug_assert!`.
- A **Module shape** field or growth-ledger projection that omits a touched module, permits a protected parent to gain responsibility, treats line count as proof of depth, or lacks checkable ownership verification. Read [module shape](references/module-shape.md) for the applicable contract.

Raise concerns before writing any code. The plan is allowed to be wrong; catching it now is free. If a field is absent, the plan's hard gate already refused it — do not invent substitute checks.

## Each slice, in order

### 1. Impact analysis — before implementing

If the slice changes the signature, name, or semantics of an existing function — public or private — enumerate the callers first. The list bounds the blast radius and names what else this slice must update.

Tooling, in preference order:

1. **Symbol-aware static analysis** (`lsp` references, `rust-analyzer` find-usages, IDE "find usages"). Use the qualified path when bare names are ambiguous.
2. **`grep`** for the name across the codebase — catches string-built dispatch and doc references static analysis misses.
3. **Both, when stakes are high.** Static analysis is the starting point; `grep` is the safety net.

Caveats: the tool's coverage is bounded by its own correctness (when you are modifying the resolver, the resolver's caller-analysis is what you are fixing); cross-crate edges, generated callsites, and re-exports may be missed or phantom-generated. An empty caller list is suspicious — dead code to delete, a stale index to refresh, or an exported/re-exported symbol whose consumers need a second lookup.

**Completion:** caller list (path + line) recorded in the owning slice or repair record — or an explicit note there that the function is brand-new and has no callers. The commit references the record (step 8); it does not carry the list itself.

### 2. Helper search — before implementing

Before writing any utility code (path handling, string normalization, error wrapping, retry logic, SQL fragments, encoding, hex/base64), check both parts of the codebase's vocabulary:

1. **In-source helpers** — `grep` for existing functions with matching or close semantics. Matching: reuse. Close: widen or wrap. Do not duplicate.
2. **Already-imported dependencies** — `grep` the manifests (`Cargo.toml`, `package.json`, `pyproject.toml`, `go.mod`) for crates whose API covers the utility. An already-imported dep is functionally part of the vocabulary at zero cost — no new audit, no dep evaluation — while reimplementing it is duplication just like reimplementing an in-source helper.

**Completion:** a reuse decision for each utility the slice needs, recorded in item 10's receipt, which also covers the symbols and repeated constructions beyond this search's scope. Partial fit: widen or wrap the existing helper, or duplicate it as a divergence that item 10 requires you to justify beside the code. Net-new deps are a separate decision and are not covered by this rule.

### 3. Implement — through tdd-scoped

Write the code. Unit-level work follows [`tdd-scoped`](references/tdd-scoped.md)'s inner cycle (RED → GREEN → local budget check when the cycle changed complexity → REFACTOR). The plan's pre-typed code is advisory: deviate if you spot a better algorithm or a missing edge case, as long as the slice's contract — claim, fixture, oracle, budget — holds.

**Completion:** the [`tdd-scoped`](references/tdd-scoped.md) cycle's checklist passes for the code written here.

### 4. Symmetry audit — parallel paths and changed predicates

If the slice adds or repairs a branch that parallels an existing one (a scoped lookup beside an unscoped one, a new retry path beside an existing one, a validation that mirrors a check elsewhere), or tightens or relaxes an acceptance predicate, list the existing path's behavior and confirm the new path matches, or carry a written justification for the divergence:

- **Error handling:** same error variant for the same failure mode? Nothing silently swallowed that the old path logs?
- **Logging:** same severity for analogous events?
- **Fallback behavior:** falls through, returns `None`, or returns `Err` the same way?
- **Caller observability:** can a caller distinguish "new path succeeded" from "new path declined, old path took over" — and is that distinguishability the same as before?
- **Resource discipline:** does the new path run comparable work through the same mechanism the existing path uses — off-thread or blocking-pool execution, streaming versus materialized buffers, bounded concurrency — or does the divergence have a written justification?
- **Guard parity:** every guard, validation, identity check, confinement rule, and fail-closed policy the existing path enforces is either enforced on the new path or waived beside the divergence citing the approved claim, established obligation, or `N/A — approved risk` row that authorizes it, with a verified tracker ID where the waiver defers work; where both paths are production-reachable from one input, a differential fixture runs the same bytes through both and asserts both accept or both refuse.
- **Acceptance symmetry:** for a tightened or relaxed predicate or comparison, the inputs the earlier form accepted and this one now refuses, and the reverse — each with a control on the input that discriminates them.

Asymmetry is allowed. Unintentional asymmetry is the bug class this audit catches.

**Completion:** every parallel-path question above is answered, or a written divergence justification exists; both forms are recorded in the slice or repair record, in item 10's receipt where that item applies.

### 5. Resolve the gate — once, after the slice or repair

Resolve the eleven items from **The gate** in order and record each state as `PASS`, `FAIL`, or `N/A — reason`. The commands below describe fresh proof; reuse qualifying results under **Evidence validity** instead of rerunning them. After any edit, rerun invalidated checks, including checks invalidated by a proof-fixture or cleanup change; broaden scope when dependencies are uncertain. Focus writer-local checks on the changed path and inherited obligations; assembled quality, platform, and cross-slice proof belongs to the final integration check.

- **Affected unit tests.** Run the tests covering the slice's changed executable behavior. They must pass. A test rewritten to accept the bug is not a pass. If the slice changes no executable behavior and the plan names no affected tests, record the plan-backed `N/A — reason`.
- **Falsifiers.** Run each assigned `PENDING` falsifier and each invalidated `PASS` falsifier with the plan's recorded command. Retain a still-valid `PASS` with its result reference and applicability reason; use `N/A — reason` only when no falsifier applies here. A `FAIL` blocks the slice: classify and resolve it under step 6 and the contract's approval semantics. Distinct from items 7-9: this checks the experiment's conclusion; those establish current regression coverage and defect sensitivity.
- **Stress fixture.** Run the plan's fixture; compare actual to expected. Exact match required — or record the plan's `N/A — reason` when the plan records no fixture for this slice.
- **Changed implementation vs oracle.** When comparison applies, run the slice's changed implementation and the plan's independent oracle on the same recorded input and compare their observable outputs item by item. Use the applicable evidence oracle on an Empirical route or the design row's reference on a Structural route. The subject is the changed implementation, never just the probe. Otherwise record the design/plan's explicit ladder-backed `N/A`; ordinary behavioral tests and required consumer smokes still run.
- **Module shape.** When the plan's Module shape field applies, read [module shape](references/module-shape.md), compare the actual production tree and diff with the approved module ledger and growth ledger, and perform the selected checks, including the per-slice ownership self-check. Check responsibility owners, interfaces, dependency direction, protected parents, required/forbidden paths, and numeric tripwires. Apply that reference's **Length review** to approaching or exceeded thresholds, including unchanged placement; other ownership/interface/seam deviations return to `falsifiable-design` and requester approval. Use the exact route/design-backed `N/A` only when module shape does not apply.
- **Budget.** For every loop or phase carrying a plan production-scale or wall-clock budget, including explicit one-off latency obligations, establish that the applicable budgets still hold under [`falsifiable-design`](references/falsifiable-design.md)'s **Performance-fence policy** and the plan's recorded run contract. Record measurements and execution-contract evidence for each budget class separately; retain applicable measurements under Evidence validity, using plan-backed `N/A — reason` only for an inapplicable class. A required qualification lane without valid evidence remains unresolved and blocks completion.
- **Fence.** Establish green regression evidence for each applicable named fence on the changed implementation under **Evidence validity**, whether created here or inherited. Otherwise carry the exact ownership-verification or approved-risk `N/A` from the design's Regression fence cell.
- **Suite before mutation.** Run the repository suite before mutation passes, so their load never reaches it. Rerun an intermittent failure in isolation and record that result, rather than rerunning the whole suite for a clean union.
- **Mutation.** For applicable Named mutation entries, apply the declared defect, observe the fence go red, restore the code, and observe green; retain still-valid mutation/restoration evidence where permitted. A required mutation that stays green exposes a blind fixture: repair it without weakening the asserted behavior. A compile failure unrelated to the claim or a mutation leaving the observable unchanged is not detection. Record technical corrections with the owning stage under **Approval semantics**; apply the contract's **Verification complexity stop** before further hardening. For inapplicable entries, carry the exact design/plan `N/A` into item 8 and its reference into item 9.

Performance-fence green/red/restored-green runs use the same recorded run contract and verdict rule from **Performance-fence policy**; a scheduler stall or harness timeout alone is not mutation detection.

- **Parity and reuse.** Produce item 10's receipt: for every symbol or repeated construction item 10 names, the sibling you searched for and either the reuse or the justification; for each new or repaired path beside an existing one, the symmetry answers. Name the search you ran — symbol-aware, `grep`, or both — so an empty result is distinguishable from an unperformed one.
- **Preserved enforcement.** Produce item 11's record for the artifacts it names, each with its authorizing claim, obligation, or risk row, and the deferral reference where work is deferred.

**Completion:** all eleven gate items recorded — each `PASS`, `FAIL`, or `N/A — reason`.

### 6. On any FAIL — one action

**STOP.** Do not commit. Do not advance. Do not "fix it later." The gate stays failed until the failure is fixed; a known issue may explain it but never waives it.

Classify the failure:

- **Implementation, tool, or technical-proof failure** whose correct fix the contract already determines — use the bounded repair entry in this stage. Diagnose the root cause, make the targeted correction, and recheck failed and newly invalidated evidence; retain applicable conclusions. Multiple distinct qualification failures do not themselves trigger redesign or reset evidence. Continuing oracle/checker repairs follow the contract's **Verification complexity stop**; repeated verified product defects follow its **Repeated product-repair stop** before another local repair. Other escalation depends on a changed or unresolved decision, not an arbitrary retry count.
- **Changed or unresolved specification, ownership, interface, architecture, oracle meaning, or explicit risk acceptance** — return to the owning artifact and user approval under the contract. Plan-only scope/budget/partition updates go to the plan owner.

If the failure matches a known issue in the tracker, record the relationship after the bounded tracker lookup defined in [workflow contract](references/CONTRACT.md). The issue explains the failure; the slice still does not ship with the gate failed. Either absorb the fix into this slice or surface the decision to the user. A failure that also fails on the untouched base, or recurs without a path through the diff, follows the contract's **Baseline failure** rule.

A user risk decision does not waive the failed gate: it is recorded by revising the owning artifact — `spec.md`, `design.md`, or `plan.md`, per the contract's single-owner rules — for example as an approved `N/A — reason` for the gate. Reconcile the gate against the revised artifact, rerunning invalidated checks and retaining valid evidence. A remaining `FAIL` never ships.

Never skip, disable, ignore, or exclude a failing required test, or edit an oracle or expected value merely to obtain green. Accepting incorrect behavior, relaxing required assertions, or deleting a required mutation remains prohibited.

A pre-existing fence failure remains `FAIL`. An implementation-only correction may use bounded repair when it stays within the owning slice's planned files and leaves the fence and its expected values unchanged. Otherwise stop automatic repair: changed file scope goes to the plan owner, and a demonstrated defect in the fence or its expectations goes to the proof artifact's owner.

The proof owner may correct obsolete golden expectations or incomplete fixtures against an approved claim or established obligation, never current implementation output alone. Record that governing evidence and preserve defect detection; revalidate under **Evidence validity** and applicable **Mutation sensitivity**. Changed verification meaning or accepted risk follows **Approval semantics**. Neither repair path permits advancing with an unresolved failed gate.

### 7. Stale-reference and dead-path sweep — gate green, before commit

Scan every file this slice modified, the files it depends on, and any document or example that describes the behavior it changed — for:

- **Falsified prose** — every comment, doc sentence, count, or example this slice's change makes untrue: a forward reference (`// slice N hardens this`, `// to be implemented in step M`) whose slice has now landed, an inverted rationale, a count or list the change moved, a documented behavior the change replaced. Rewrite each to describe current behavior factually, wherever it sits — the file you edited, the operator document beside it, or the example a caller copies.
- **Contract discoveries** — an implicit contract this slice surfaced (e.g., "requires forward-slash paths") belongs in the doc comment, with classified enforcement: runtime check for load-bearing correctness, `debug_assert!` for sanity hints.
- **Misleading names** — if this slice changed a function's semantics and the name no longer describes the behavior, rename via the step 1 impact analysis (symbol-aware first, `grep` as safety net) and update every callsite in this same commit.
- **Unreachable paths** — a branch, error arm, or checked operation this slice's own invariants make impossible: delete it, or enforce the precondition it assumes so the path becomes reachable. A guard no input can reach still reads as a live failure mode to the next reader.
- **Tracker references** — classify every "deferred to", "tracked at", "out of scope", "follow-up" phrase in code or the commit message per [workflow contract](references/CONTRACT.md)'s tracker taxonomy: a **permanent non-goal** records its rationale where the phrase sits — no tracker issue; **intended future work** (including trigger-conditioned phrases) cites a verified tracker ID — discover the repository's tracker per the contract, use its native command, and if the ID does not exist, the issue does not cover the deferral, or the phrase has no ID, file the issue *now* and update the reference. Anonymous TODOs and phantom tracker IDs rot.

**Completion:** the sweep found nothing, or everything it found is fixed in this commit and any evidence those fixes invalidated has been reverified.

### 8. Commit

One commit per slice or atomic bounded repair. The message names the governing design claim or established obligation under the contract's **Approval semantics** and references the owning slice/repair record: caller analysis, deviations, gate and mutation results, and fence gaps. Unchanged inherited records remain references. Required evidence and tracker references travel with this behavior-owning commit, so a later rebase or restack keeps them attached to the change they prove; an integration merge commit alone does not carry them. Cite shared, audience-accessible evidence; private transcript paths and credentials are not shared proof.

### 9. Drift check — after commit, before the next slice

Per [workflow contract](references/CONTRACT.md) branch discovery, fetch the default/upstream branch. Diff from the merge-base — inspect *upstream movement* and *this slice's new divergence* since the last check, not the whole branch:

- Flag: upstream changed a file this branch also changed since the last check (conflict risk); this slice introduced divergence on generated or structured files (append-only JSONL, lockfiles, schema dumps); a file this slice did not touch shows large new divergence.
- Do **not** flag lockfile/JSONL changes the plan records as intentional branch changes — they are expected, not drift, and are not re-flagged every slice.

If anything is flagged: merge or rebase upstream before starting the next slice. Prefer a merge commit (preserves slice history) over a rebase (rewrites it, breaking pushed hashes other reviewers may be reading). After merging or rebasing, reconcile all eleven gate states under **Evidence validity** before advancing: rerun checks invalidated by upstream movement and retain applicable results; broaden checks if the affected scope is uncertain.

### 10. Size tripwire — after commit, before the next slice

Cumulative changed lines since the upstream merge-base, checked after every commit. The tripwire compares against the plan-recorded estimate — summed slice diffs plus the plan's documented churn margin — and follows the plan-recorded partition policy.

- **Exact rule:** projected or actual cumulative changed lines `> 4,000` trigger the contract's **Size stop**; a requester choice recorded in `plan.md` covers the size it accepted.
- **Crossed a plan partition boundary?** Ship point: open the PR for the completed group now and continue the remaining slices on a stacked branch. Do not "finish the feature first" — the partition exists so review fires while the code is fresh, before the next group replicates its mistakes.
- **Actual > 4,000 and no recorded choice covers it?** The projection was wrong. STOP under the **Size stop**: surface the actual number, a proposed partition of the remaining slices, and the other options. The next slice waits for the requester's choice.
- **Draft PR no later than the first partition boundary.** CI legs you do not run locally (Windows runners, exotic targets) are oracles too, and they only fire on push.

## Final integration check

After every slice has passed, establish proof for the **assembled implementation**, not just individual writer worktrees. The integration owner (Main when work is delegated) accounts for every applicable implementation/oracle comparison, design falsifier, regression fence, repository quality check, required consumer smoke, target-platform check, and cross-slice interaction. Run missing or invalidated checks on the assembled state; reuse prior results only when **Evidence validity** establishes that they still prove that state. Required oracle comparisons use the same inputs. All applicable results must be `PASS`; retain explicit contract-backed conditional `N/A` fields.

A shared deterministic test may supply both falsifier and regression results. Use the contract's **Evidence validity** distinctions to decide which experiments need fresh execution; final integration alone does not invalidate an empirical premise or mutation proof.

When module shape applies, satisfy [module shape](references/module-shape.md)'s **Final design-conformance review**, including its isolated-review and evidence-retention criteria. This is the authoritative review record for assembled structural conformance.

Writer-local receipts alone do not prove assembled quality, platform behavior, or integration. A task instruction banning writer validation transfers the missing proof to Main; it cannot authorize a verified gate or completion. Missing proof blocks completion until the integration owner supplies it.

If any applicable qualification check fails, locate the responsible slice or interaction, stop, and resolve it under step 6 through the bounded repair entry. Final status is verified only after every applicable obligation has fresh or valid retained proof.

## Red flags

- "The oracle drifted by one item; I'll fix it next slice." No. Drift across slices is silent corruption. Stop now.
- "I'll batch the next three slices and run the gate at the end." No. One checkpoint per completed slice. Batching is how drift becomes invisible.
- "The known issue explains the failure, so we ship." No. It explains; it does not waive. Resolve the failed obligation and reverify invalidated evidence against the owning artifact.
- "Unit tests pass, so a required oracle comparison can wait." No. Resolve all eleven states with valid evidence or the approved design's explicit applicability decision; waiting is not a gate state.
- "The fence stayed green under its required mutation; the code is obviously right." No. The fixture is blind to the declared defect. Repair that gap.
- "The plan said this loop, so I wrote this loop even though I see a better one." Wrong. The plan is advisory; the contract is claim, fixture, oracle, budget.
- "I cited a tracker ID without checking it exists." Phantom references and silent deferrals fail the same way: future contributors cannot find the deferred work. Verify with the repository's tracker command before writing the reference, not after.
- "I grep'd the source for a helper and wrote it from scratch." Did you grep the manifests? An already-imported dependency's API is functionally part of the codebase's vocabulary. Hand-rolling what an imported crate already provides is the same class of duplication as hand-rolling a function that exists in `db/files.rs`. Item 10's receipt records the search and its result.
- "All writers reported green, so integration is verified." Their local results need assembled-state applicability; Main supplies missing quality, platform, and cross-slice proof.
- "The falsifier passed before, so changed inputs do not matter." Reuse requires evidence validity, not a historical green label.

## What this stage is not

This is not "follow the plan." This is "advance the design hypothesis by one slice and re-test it against reality." The plan is the current best guess. Reality is the authority. On disagreement you stop until the failure is fixed or the user decides — you never ship a failed gate.

## Output

For each slice: one commit and all eleven gate states returned to the owning slice-record author. For each bounded repair: one atomic commit and those states returned to its record owner — `assessing-review-feedback` for review repairs, the owning slice-record author for qualification repairs — with inherited plan references instead of a new slice template. Every item is `PASS` or justified `N/A — reason`; no `FAIL` or missing proof. After the final slice or repair: verified assembled quality, applicable platform and cross-slice checks, implementation/oracle comparisons, falsifiers, and regression fences, plus the valid isolated design-conformance record when module shape applies. Fresh and retained results satisfy **Evidence validity**; writer receipts or validation prohibitions alone do not complete the stage.
