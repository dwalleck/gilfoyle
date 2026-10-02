# checkpointed-build

Implement one atomic slice and check its delivered behavior against the approved contract. Reality decides whether the change works; a plan or historical green label does not.

## When this stage runs

Read [workflow contract](references/CONTRACT.md) first. Consume the compact slices from `plan.md`, relevant design obligations, and their evidence. Required unresolved premises block dependent implementation, not unrelated settled slices. This stage exclusively judges slice and bounded-repair completion; the artifact owner incorporates its result into the existing owning record.

### Bounded repair entry

For a review finding, consume the **Compact repair record** from [`assessing-review-feedback`](references/assessing-review-feedback.md). For an implementation/final-integration qualification failure, use the owning slice's record, naming responsible slices for a cross-slice interaction. Inherit unchanged Outcome, Changes, Verification, and Dependencies by reference; critique and repair only affected obligations. No new slice or replay of the entire workflow is required for a fix the approved contract already determines.

Changed behavior, scope, ownership/interfaces, architecture, or accepted risk returns to the appropriate owner under Approval semantics. Changed plan inputs go to `budgeted-plan` for an affected-only amendment. Technical verification simplification uses the contract's coverage-preserving rule, not automatic risk acceptance.

## The gate — stated once

An atomic change is complete only when its requested behavior is implemented, relevant checks pass, and no blocking defect or required check remains unresolved. Run one checkpoint per completed slice or atomic repair, not per unit-test cycle. Record only:

- **Delivered behavior** — the outcome actually implemented, relevant caller/ownership changes, and any deviation requiring a decision.
- **Performed checks and results** — commands or review scope, expected/observed results, and evidence references identifying the checked state, inputs, and environment. Reuse valid evidence with its applicability reason. Record a check once even when it proves several obligations.
- **Unresolved failures** — blocking defects, missing/stale required proof, and their responsible owner; state none when there are none. Pending final integration remains explicit at intermediate checkpoints.

Omit inapplicable fields/checks under the contract. An unavailable, stale, deferred, or failed required check remains explicit; omission is not a waiver. A failed mandatory gate blocks commit and advancement of the affected atomic change. Known issues explain failures but do not authorize shipping.

## Before implementation: critique affected plan obligations

Check that the Outcome is observable; Changes includes all callers and approved owners; Verification has discriminating expected results and real consumer proof where needed; Dependencies include unresolved facts or environments that actually matter. Reject implementation-coupled goldens, bespoke checkers without a named gap, hidden load-bearing preconditions, or impossible performance requirements. Read [module shape](references/module-shape.md) when ownership/interfaces change. Do not invent stress fixtures, loop budgets, or template fields merely because they are absent.

## Each slice, in order

### 1. Impact analysis and reuse

Before changing an existing signature, name, or semantics, enumerate relevant callers using symbol-aware references first, then text search for dynamic dispatch, generated edges, exports, and docs. Bound the migration; an unexplained empty caller list needs investigation. Record the consequential caller/compatibility conclusions in Changes or the repair record, not a receipt for every symbol.

Before utility work, check existing source helpers and already-imported dependency APIs. Reuse, widen, or wrap fitting functionality rather than copying it. Record consequential divergence beside the code with its governing behavior/architecture rationale. Net-new dependencies remain a separate design decision. No per-literal, per-symbol, or repeated-construction receipt is required.

**Completion:** the affected caller migration and reuse choices are understood and preserve the approved contract.

### 2. Implement through scoped behavior checks

Use [`tdd-scoped`](references/tdd-scoped.md) where new/fixed behavior needs focused tests. Existing behavioral coverage can cover multiple functions; no per-function test is required. Preserve real regression reproducers and observe bug sensitivity under the design's Mutation sensitivity rule. Implement the simplest correct behavior through approved owners/interfaces, including all caller migration atomically.

**Completion:** the slice's outcome is implemented and relevant focused checks pass; required dependent premise evidence was obtained before relying on it.

### 3. Audit parallel paths and enforcement

For new/repaired parallel paths and changed acceptance predicates, inspect relevant symmetry: important errors, logging, fallbacks, caller observability, resource discipline, guards, identity/confinement, and fail-closed policy. Check discriminating accepted/refused boundary cases where the predicate changed. Use ordinary tests/captured references first; a live differential harness requires a named uncovered mechanism or repository requirement. Explain intentional behavioral divergence and obtain approval when it changes the contract.

#### Preserved enforcement

For gates, fences, validators, or policy files repointed, relaxed, deleted, or orphaned by this change, account for the still-required behavior and coverage. Preserve real behavior/security guards and independently mandated repository checks. A redundant bespoke checker may be retired or replaced technically when established tests, consumer execution, compiler checks, or reviewed fixtures still establish its required outcomes; cite that evidence and the disposition in the affected record. Its full historical mutation vocabulary is not automatically a product requirement. Keep a real reproducer or unique required detection case in sufficient replacement coverage. Lost unique required coverage, changed behavior, or accepted risk follows Approval semantics; an unexplained narrowed checker claim cannot waive a product obligation.

**Completion:** relevant parallel-path behavior and required enforcement remain correct; any legitimate changed decision is recorded by its owner.

### 4. Resolve relevant verification

Use the plan's Verification and the design's **Verification ladder**, not a fixed list of gate states:

- Run affected behavioral/boundary/regression tests and assigned design checks. Reuse valid prior results; reverify conclusions affected by production, fixture, dependency, environment, or cleanup changes. Broaden when impact is uncertain.
- Drive the changed implementation through the real consumer entry point for required integration/lifecycle/host proof. Writer-local tests do not replace final assembled execution.
- For stable ports, compare representative captured reference inputs/outputs at approved fidelity, with provenance. Correct expected values only against the behavior contract or reference evidence, never today's output alone. Goldens do not prove native lifecycle behavior.
- Run live comparisons, custom oracles, fuzz, and named mutations only where a named uncovered mechanism or explicit repository requirement calls for them. A required named mutation must make the intended observable red, followed by restored green; retain valid sensitivity evidence where applicable. An unrelated compile failure, scheduler stall, or timeout is not defect detection. Apply the contract's Verification complexity stop before further bespoke hardening.
- Check actual ownership/interfaces, dependency directions, and protected parents against approved constraints when relevant. Compiler/dependency checks and ordinary review are the default; no extra reconstruction is implied by a module change.
- Verify actual performance obligations under the design's Performance-fence policy, preserving required workload and concurrency. A new loop alone creates no performance-budget field. Missing required calibration/qualification remains blocking.
- Run relevant repository-required tests/lints/builds/checks at their required scope. Before mutation passes, run any required suite separately from mutation load; never present injected-defect failures as product-suite results. Investigate intermittent failures under the contract's Baseline failure rule, not by retrying the suite until green.

**Completion:** the owning record describes delivered behavior, performed checks/results, and unresolved failures. The atomic gate passes only when relevant checks are valid and no blocking obligation is unresolved.

### 5. Resolve failures

Stop the affected atomic change; do not commit or advance it while its mandatory gate fails. Diagnose root cause and repair within the approved contract through bounded entry, retaining unrelated valid evidence. Multiple qualification failures do not by themselves require redesign. Apply the separate **Verification complexity stop** to checker repairs and **Repeated product-repair stop** to real product defects.

Changed product/architecture/risk decisions return to the owning stage. A baseline failure follows the contract's approval and tracker rule. Tracker IDs do not waive checks. Never skip, disable, or rewrite a failing required test merely to obtain green. An implementation correction stays with its owning slice; changed file scope goes to the plan owner, and a demonstrated fixture or expectation defect goes to its proof owner. That owner may correct obsolete expectations against approved behavior, recording the governing evidence and preserving needed defect detection. Coverage-preserving technical retirement is allowed under Preserved enforcement, but real failures and missing unique required evidence remain blocking.

**Completion:** affected required checks pass against the corrected contract/implementation, or the change remains explicitly blocked with the needed decision or evidence named.

### 6. Sweep stale references and dead paths

Before commit, update comments, docs, examples, counts, names, and callers made false by the change. Record newly discovered load-bearing preconditions with runtime enforcement; sanity hints may use debug-only assertions. Delete paths made obsolete by the cutover and enforce preconditions for live ones. Rename misleading symbols with atomic caller updates. Classify permanent non-goals and intended future work under the contract's tracker taxonomy; verify tracker IDs rather than leaving phantom deferrals. Reverify any evidence invalidated by this cleanup.

**Completion:** the changed behavior, consumers, and documentation agree; obsolete cutover paths are gone and required proof remains valid.

### 7. Commit atomically

One commit per independently-green slice or atomic repair. The message names governing claims/obligations and references the single owning completion record rather than copying results. Include required evidence and tracker references with the behavior-owning change so rebase/restack preserves them. Cite shared accessible evidence, not credentials or private transcript paths. Publication remains subject to scoped shipping authorization.

### 8. Check drift and delivery boundaries

Fetch the discovered upstream branch and inspect movement since the previous checkpoint: overlapping upstream changes, unexpected generated/structured divergence, or unrelated file drift. Planned lockfile/JSONL edits are not repeatedly flagged as drift. Resolve material upstream conflicts before dependent work, preferring a merge when it preserves reviewed history. After merge/rebase, reverify invalidated conclusions and retain applicable evidence; no fixed gate-state replay is needed.

At a planned delivery boundary, open the independently mergeable increment and continue the remaining work on its planned stack. Push in time to obtain required remote CI/platform evidence, not after declaring completion. Apply supplied feature budgets under the contract's Size stop: record a soft-overrun reason once in the plan, and obtain owner authorization for a hard-limit change. No universal cumulative-line tripwire or per-module arithmetic applies.

## Final integration check

The integration owner (Main when delegated) establishes proof for the assembled implementation: requested behavior, all caller migrations, relevant cross-slice interactions, required consumer/native execution, repository tests/lints/build/CI, platform checks, regression coverage, and any genuinely required comparisons or qualifications. Run missing or invalidated checks; retain prior evidence only when it still proves the assembled state. A worker prohibition on validation transfers proof to the integration owner and cannot authorize completion.

Obtain substantive **ordinary independent review** covering behavior, ownership, interfaces, dependencies, and relevant risks. Reviewers may read approved design/context. [Module shape](references/module-shape.md)'s Final design-conformance review scopes structural concerns within this review; a module change alone requires no extra reviewer, reconstruction, or map. Isolated reconstruction is conditional on an explicit requester requirement or named unresolved architectural risk that ordinary review cannot answer.

After repairs, independently review the repair diff and affected interactions; broaden only when changed assumptions invalidate earlier review beyond that scope. Previously blocking findings now repaired do not automatically require another full round. Checker sensitivity is distinct from product failure and blocks only when required coverage is missing. Actual security bypasses, product failures, and missing required proof remain blocking.

## Output

Return the compact completion record to its owner: delivered behavior, performed checks/results, and unresolved failures. Repairs amend the affected record with valid retained references rather than duplicating completion. Final completion requires the assembled behavior and all applicable consumer/platform/repository/review obligations to be satisfied, with no blocking defect or required check unresolved. Intermediate green slices never imply final integration is complete.
