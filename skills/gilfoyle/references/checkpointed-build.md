# checkpointed-build

You are not typing the plan. You are advancing the design hypothesis by one slice and checking it against reality. The plan is the current best guess. Reality is the authority. When they disagree, you stop.

Stopping is the most important step. Drift caught at slice N is cheap; drift caught at slice N+8 is the entire feature.

## When this stage runs

After [`budgeted-plan`](references/budgeted-plan.md) has produced a plan with all gates passing — not before. Without a plan you are improvising; we do not improvise. Before consuming `plan.md`, read [workflow contract](references/CONTRACT.md): it owns the gate-state vocabulary (`PASS` / `FAIL` / `N/A — reason`), the slice and independent-oracle definitions, branch discovery, the review-size tripwire, and tracker discovery used here.

## The gate — stated once

Slice completion is this stage's job, and this is the whole gate. One checkpoint per *completed* slice — never per unit-test cycle, never batched across slices. Every item is recorded as `PASS`, `FAIL`, or `N/A — reason` per [workflow contract](references/CONTRACT.md); a conditional item that does not apply is recorded as `N/A` with the plan, design, or route fact that makes it so.

1. **Affected unit tests** pass — or `N/A — reason` when the slice changes no executable behavior and `plan.md` records no affected tests.
2. **PENDING falsifiers** assigned to this slice run and pass — or `N/A — reason` when no falsifier is pending here. `PENDING` is a lifecycle status, not a gate state, per [workflow contract](references/CONTRACT.md): it marks a falsifier awaiting discharge by a named owner and step.
3. **Stress fixture** produces the plan's expected outcome — or `N/A — reason` when the plan records no fixture for this slice.
4. **Changed implementation vs independent oracle** agree on the plan's input.
5. **Production-scale budget** holds for every applicable loop and always-on phase, measured against the plan — with a separate `N/A — reason` for each budget class the plan marks inapplicable.
6. **Regression fence** green — or `N/A — approved risk: <reason>` when the design records that exact value in the claim's Regression fence cell and the Approval section.
7. **Named mutation** red, for every new fence this slice adds — or `N/A — approved risk: no fence to mutate` when the plan records that exact value.
8. **Fence restored** green — or `N/A — approved risk: no fence to restore` when item 6 carries an approved-risk `N/A`.

Item 2 is the design's one-shot falsifier experiment; items 6-8 are its permanent fence. A row can discharge its falsifier here and still owe its fence. When the pending falsifier and Regression fence name the same deterministic test, run it once and record that result for both items 2 and 6.

A `FAIL` on any applicable item stops the slice: no commit, no next slice. A failed gate never authorizes shipping. A known issue may explain a failure; it never waives it.

## Before the first slice: critique the plan

Read `plan.md` top to bottom. Flag any slice where a field that actually appears in the plan is implausible:

- A **loop budget** that misstates its own cost (`O(n)` over `files × symbols` is not `O(n)`).
- A **stress fixture** too gentle to fail a plausible bug (three items do not surface scaling bugs).
- An **oracle** coupled to the implementation (an oracle that calls the function the slice implements is not an oracle).
- **Documented preconditions** with missing or misclassified enforcement: a load-bearing-for-correctness precondition needs a runtime check that survives release builds; a sanity hint gets a `debug_assert!`.

Raise concerns before writing any code. The plan is allowed to be wrong; catching it now is free. If a field is absent, the plan's hard gate already refused it — do not invent substitute checks.

## Each slice, in order

### 1. Impact analysis — before implementing

If the slice changes the signature, name, or semantics of an existing function — public or private — enumerate the callers first. The list bounds the blast radius and names what else this slice must update.

Tooling, in preference order:

1. **Symbol-aware static analysis** (`lsp` references, `rust-analyzer` find-usages, IDE "find usages"). Use the qualified path when bare names are ambiguous.
2. **`grep`** for the name across the codebase — catches string-built dispatch and doc references static analysis misses.
3. **Both, when stakes are high.** Static analysis is the starting point; `grep` is the safety net.

Caveats: the tool's coverage is bounded by its own correctness (when you are modifying the resolver, the resolver's caller-analysis is what you are fixing); cross-crate edges, generated callsites, and re-exports may be missed or phantom-generated. An empty caller list is suspicious — dead code to delete, a stale index to refresh, or an exported/re-exported symbol whose consumers need a second lookup.

**Completion:** caller list (path + line) recorded in the slice's commit message; or an explicit note that the function is brand-new and has no callers.

### 2. Helper search — before implementing

Before writing any utility code (path handling, string normalization, error wrapping, retry logic, SQL fragments, encoding, hex/base64), check both parts of the codebase's vocabulary:

1. **In-source helpers** — `grep` for existing functions with matching or close semantics. Matching: reuse. Close: widen or wrap. Do not duplicate.
2. **Already-imported dependencies** — `grep` the manifests (`Cargo.toml`, `package.json`, `pyproject.toml`, `go.mod`) for crates whose API covers the utility. An already-imported dep is functionally part of the vocabulary at zero cost — no new audit, no dep evaluation — while reimplementing it is duplication just like reimplementing an in-source helper.

**Completion:** a reuse decision for each utility the slice needs. Partial fit: document the deviation inline before duplicating — a divergent reimplementation with an honest comment is acceptable; silent duplication is debt. Net-new deps are a separate decision and are not covered by this rule.

### 3. Implement — through tdd-scoped

Write the code. Unit-level work follows [`tdd-scoped`](references/tdd-scoped.md)'s inner cycle (RED → GREEN → local budget check when the cycle changed complexity → REFACTOR). The plan's pre-typed code is advisory: deviate if you spot a better algorithm or a missing edge case, as long as the slice's contract — claim, fixture, oracle, budget — holds.

**Completion:** the [`tdd-scoped`](references/tdd-scoped.md) cycle's checklist passes for the code written here.

### 4. Symmetry audit — when the slice adds a parallel path

If the slice introduces a branch that parallels an existing one (a scoped lookup beside an unscoped one, a new retry path beside an existing one, a validation that mirrors a check elsewhere), list the existing path's behavior and confirm the new path matches, or carry a written justification for the divergence:

- **Error handling:** same error variant for the same failure mode? Nothing silently swallowed that the old path logs?
- **Logging:** same severity for analogous events?
- **Fallback behavior:** falls through, returns `None`, or returns `Err` the same way?
- **Caller observability:** can a caller distinguish "new path succeeded" from "new path declined, old path took over" — and is that distinguishability the same as before?

Asymmetry is allowed. Unintentional asymmetry is the bug class this audit catches.

**Completion:** every parallel-path question above is answered, or a written divergence justification exists.

### 5. Run the gate — once, after the slice

Run the eight items from **The gate** in order and record each state as `PASS`, `FAIL`, or `N/A — reason`. The mechanics:

- **Affected unit tests.** Run the tests covering the slice's changed executable behavior. They must pass. A test rewritten to accept the bug is not a pass. If the slice changes no executable behavior and the plan names no affected tests, record the plan-backed `N/A — reason`.
- **PENDING falsifiers.** For every falsifier the plan assigns to this slice whose design Status is `PENDING` — the discharge owner and step named in design/plan per [workflow contract](references/CONTRACT.md) (`PENDING` is a lifecycle status, not a gate state) — run the falsifier with the exact command the plan's Commands and expected results field records. Record `PASS` or `FAIL`. A `FAIL` blocks the slice: the claim is falsified, and only a design revision (per the contract's approval semantics) re-opens it. Rows already `PASS` need no run; when no falsifier is pending here, record `N/A — reason`. Distinct from items 6-8: this runs the one-shot falsifier; those run its permanent fence.
- **Stress fixture.** Run the plan's fixture; compare actual to expected. Exact match required — or record the plan's `N/A — reason` when the plan records no fixture for this slice.
- **Changed implementation vs oracle.** Run the slice's changed implementation on the input recorded in the plan, then run the plan's independent oracle on that same input and compare their observable outputs item by item. On an Empirical route, include the workspace and evidence oracle established by [`prove-it-prototype`](references/prove-it-prototype.md); on a Structural route, use the design row's oracle and plan-defined input. The subject is the changed implementation, never the probe. They must agree.
- **Budget.** For every loop the slice introduced, confirm the production-scale cost against the plan's loop budget. For every always-on phase, measure wall-clock against the plan's wall budget. Record each applicable result separately; use the corresponding plan-backed `N/A — reason` only for a budget class the slice does not introduce. Measure with `time`, `hyperfine`, or a benchmark harness — eyeballing does not count.
- **Fence.** Run the regression fence this slice created for its claim — the named test from the plan's Regression fence field (the design's Falsification table names it). If the design records `N/A — approved risk: <reason>` for the claim's fence and records that acceptance in its Approval section, carry that exact value into the gate record; no run is owed.
- **Mutation.** For every NEW fence this slice adds: apply the exact buggy implementation the design's Named mutation field records for it, run the fence — it must go red — then restore the code and confirm the fence is green again. A fence that has only ever been seen green is not evidence. If the fence stays green under its own mutation, the fixture is blind to the bug: change the fixture, not the assertion, and do not skip the mutation because "the code is obviously right." If no mutation can turn the fence red without also turning a *different* assertion red, the fence is redundant with that assertion — cut it. Record each mutation and its result in the commit message. When the plan records `Named mutation: N/A — approved risk: no fence to mutate`, carry that exact value into item 7 and record `N/A — approved risk: no fence to restore` for item 8.

**Completion:** all eight gate items recorded — each `PASS`, `FAIL`, or `N/A — reason`.

### 6. On any FAIL — one action

**STOP.** Do not commit. Do not advance. Do not "fix it later." The gate stays failed until the failure is fixed; a known issue may explain it but never waives it.

Classify the failure:

- **Implementation or tool failure** whose correct fix the contract already determines — diagnose and repair it yourself. Rerun the failed gate. Stay on this slice.
- **Specification, scope, architecture, or explicit risk acceptance** — surface to the user. Only they decide these.

If the failure matches a known issue in the tracker, record the relationship after the bounded tracker lookup defined in [workflow contract](references/CONTRACT.md). The issue explains the failure; the slice still does not ship with the gate failed. Either absorb the fix into this slice or surface the decision to the user.

A user risk decision does not waive the failed gate: it is recorded by revising the owning artifact — `spec.md`, `design.md`, or `plan.md`, per the contract's single-owner rules — for example as an approved `N/A — reason` for the gate. The gate then reruns against the revised artifact. A remaining `FAIL` never ships.

Never weaken a gate to green: no test rewritten to pass, no assertion relaxed, no mutation deleted because the code looks right.

### 7. Stale-reference sweep — gate green, before commit

Scan every file this slice modified — plus the files it depends on — for:

- **Forward-reference comments** (`// slice N hardens this`, `// to be implemented in step M`) whose future slice has now landed: rewrite to describe current behavior factually.
- **Contract discoveries** — an implicit contract this slice surfaced (e.g., "requires forward-slash paths") belongs in the doc comment, with classified enforcement: runtime check for load-bearing correctness, `debug_assert!` for sanity hints.
- **Misleading names** — if this slice changed a function's semantics and the name no longer describes the behavior, rename via the step 1 impact analysis (symbol-aware first, `grep` as safety net) and update every callsite in this same commit.
- **Tracker references** — classify every "deferred to", "tracked at", "out of scope", "follow-up" phrase in code or the commit message per [workflow contract](references/CONTRACT.md)'s tracker taxonomy: a **permanent non-goal** records its rationale where the phrase sits — no tracker issue; **intended future work** (including trigger-conditioned phrases) cites a verified tracker ID — discover the repository's tracker per the contract, use its native command, and if the ID does not exist, the issue does not cover the deferral, or the phrase has no ID, file the issue *now* and update the reference. Anonymous TODOs and phantom tracker IDs rot.

**Completion:** the sweep found nothing, or everything it found is fixed in this commit.

### 8. Commit

One commit per slice. The message names the design claim this slice implements and carries the step records: caller list (step 1), deviations from pre-typed code, mutation results (step 5), fence gaps.

### 9. Drift check — after commit, before the next slice

Per [workflow contract](references/CONTRACT.md) branch discovery, fetch the default/upstream branch. Diff from the merge-base — inspect *upstream movement* and *this slice's new divergence* since the last check, not the whole branch:

- Flag: upstream changed a file this branch also changed since the last check (conflict risk); this slice introduced divergence on generated or structured files (append-only JSONL, lockfiles, schema dumps); a file this slice did not touch shows large new divergence.
- Do **not** flag lockfile/JSONL changes the plan records as intentional branch changes — they are expected, not drift, and are not re-flagged every slice.

If anything is flagged: merge or rebase upstream before starting the next slice. Prefer a merge commit (preserves slice history) over a rebase (rewrites it, breaking pushed hashes other reviewers may be reading). After merging or rebasing, rerun the current slice's gate — the eight items — before advancing: upstream movement can change what the slice's checks observe.

### 10. Size tripwire — after commit, before the next slice

Cumulative changed lines since the upstream merge-base, checked after every commit. The tripwire compares against the plan-recorded estimate — summed slice diffs plus the plan's documented churn margin — and follows the plan-recorded partition policy.

- **Exact rule:** projected or actual cumulative changed lines `> 4,000` requires independently mergeable PR increments.
- **Crossed a plan partition boundary?** Ship point: open the PR for the completed group now and continue the remaining slices on a stacked branch. Do not "finish the feature first" — the partition exists so review fires while the code is fresh, before the next group replicates its mistakes.
- **Actual > 4,000 and the plan records no partition?** The projection was wrong. STOP: surface the actual number and a proposed partition of the remaining slices. This is the same stop as a budget overshoot, because it is one.
- **Draft PR no later than the first partition boundary.** CI legs you do not run locally (Windows runners, exotic targets) are oracles too, and they only fire on push.

## Final integration check

After every slice has passed, run the assembled implementation against every applicable oracle — the evidence oracle and every design row's oracle — then run every falsifier and every regression fence from the design's Falsification table. Compare each implementation/oracle pair on the same input; every comparison and check must pass.

The three are related but distinct: the **oracle** independently computes the implementation's observable answer; the **falsifier** is the experiment that would prove a claim false, often one-shot; the **regression fence** is the permanent form of the falsifier that catches future regressions. If the fence is the same artifact as the falsifier (both deterministic tests), run it once and count it as both.

If anything fails, the slice chain regressed: bisect to the slice, stop, surface.

## Red flags

- "The oracle drifted by one item; I'll fix it next slice." No. Drift across slices is silent corruption. Stop now.
- "I'll batch the next three slices and run the gate at the end." No. One checkpoint per completed slice. Batching is how drift becomes invisible.
- "The known issue explains the failure, so we ship." No. It explains; it does not waive. The gate stays failed until the failure is fixed or the owning artifact is revised and the gate reruns.
- "Unit tests pass, so the implementation-vs-oracle gate can wait." No. The gate runs every slice. Wait is not a gate state.
- "The fence stayed green under its mutation; the code is obviously right." No. The fixture is blind to the bug. Change the fixture.
- "The plan said this loop, so I wrote this loop even though I see a better one." Wrong. The plan is advisory; the contract is claim, fixture, oracle, budget.
- "I cited a tracker ID without checking it exists." Phantom references and silent deferrals fail the same way: future contributors cannot find the deferred work. Verify with the repository's tracker command before writing the reference, not after.
- "I grep'd the source for a helper and wrote it from scratch." Did you grep the manifests? An already-imported dependency's API is functionally part of the codebase's vocabulary. Hand-rolling what an imported crate already provides is the same class of duplication as hand-rolling a function that exists in `db/files.rs`.

## What this stage is not

This is not "follow the plan." This is "advance the design hypothesis by one slice and re-test it against reality." The plan is the current best guess. Reality is the authority. On disagreement you stop until the failure is fixed or the user decides — you never ship a failed gate.

## Output

For each slice: one commit, with the gate record attached (every item `PASS` or `N/A — reason`; no `FAIL`). After the final slice: a clean run of every implementation/oracle comparison, falsifier, and regression fence against the assembled implementation. If any of that is missing, the stage did not finish. Finish it.
