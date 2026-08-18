# tdd-scoped

TDD verifies that a single function does what its caller expects on inputs you have enumerated. That is its job, and it is a limited one: unit-level correctness against the unit's contract. It does not, by itself, verify the design, the real system's behavior, or production-scale performance.

What this cycle does NOT check — those gates belong to [`checkpointed-build`](references/checkpointed-build.md), once per completed slice, never per test cycle:

- Changed implementation versus independent oracle agreement.
- The plan-defined stress fixture.
- Regression-fence and named-mutation behavior.

If you think "unit tests pass, therefore the feature works," you are misusing the tool. Unit tests proving things they do not prove is how features ship with the wrong algorithm.

## When this stage runs

Inside a slice during [`checkpointed-build`](references/checkpointed-build.md), for any new function or any modified behavior of an existing function. Before the first cycle, read [workflow contract](references/CONTRACT.md) and the slice's section of `plan.md`; its claim, oracle, stress fixture, and budgets remain in scope for the entire cycle.

## The rule

```
RED → GREEN → BUDGET (when this cycle changed complexity) → REFACTOR
```

## The cycle

### RED — write the failing test

- One behavior per test. Clear name: behavior described, not implementation.
- Real code where possible; mocks only when the dependency is truly external (network, time, randomness).
- Watch it fail. **Mandatory.** A test that passes immediately has not demonstrated RED — either it never exercises the new behavior, or it already passes for the wrong reason. Fix the test until it fails for the intended reason.

### GREEN — minimal code to pass

Write the simplest implementation that makes the test pass. Minimal is allowed to be inefficient or unpolished here; it is not allowed to be hyper-specific to the test's inputs — the implementation must satisfy the behavior the test asserts, so other inputs of the same shape also pass. It is not allowed to be wrong.

Watch the test pass. Watch the affected unit tests still pass. **Mandatory.**

### BUDGET — local check, when this cycle changed complexity

If this cycle added or changed a loop, or otherwise moved algorithmic complexity: state each new loop's cost and confirm it fits the slice's loop budget from `plan.md` at production scale. The measured production-scale and wall-clock gates run once after the slice under [`checkpointed-build`](references/checkpointed-build.md); do not repeat them inside every unit-test cycle.

Over budget → **REWRITE.** The minimal implementation is wrong because it is over budget. Pick an algorithm that fits. Rerun the test. Rerun BUDGET.

If this cycle did not change complexity, record `N/A — reason` and move on.

### REFACTOR — clean up

After BUDGET passes: remove duplication, improve names, extract helpers. Tests stay green; the budget result stays.

**Semantic-name check.** If this cycle changed a function's *semantics* (return type, error conditions, what "no match" means, etc.), ask: does the name still describe the behavior?

Examples that should trigger a rename:

- A `search_by_name` that used to return "first match" but now returns "unique match or None" — the name no longer signals the contract. Rename to `search_unique_by_name` or `find_unambiguous_by_name`.
- A `parse_X` that used to panic on malformed input but now returns `Result` — rename to `try_parse_X`.
- A `get_X` that used to assume cache presence but now does I/O — rename to `load_X` or `fetch_X`.

When renaming, use [`checkpointed-build`](references/checkpointed-build.md)'s impact analysis: symbol-aware tooling first (`lsp` references, `rust-analyzer`, IDE find-usages), `grep` as the safety net. Update every callsite in the same change. A rename with stale callsites is a half-rename, worse than no rename: a grep for the new name misses the old sites, and a grep for the old name shows phantoms.

If the name still fits, nothing further is required — no comment, no commit-message note. The question was asked; the answer is the unchanged name.

## Verification checklist

For each cycle:

- [ ] The test went red, then green — both observations made
- [ ] Loop budget holds at production scale — or `N/A — reason` (cycle did not change complexity)
- [ ] Semantic-name check applied: renamed when the name misleads and all callsites updated atomically; otherwise the existing name was confirmed accurate

If any item fails, the cycle is not done. Fix it within the cycle — rewrite or refactor.

## Red flags

- "Tests pass, ship it." Tests passing is necessary, not sufficient — and the gates beyond this cycle are not waived by green tests.
- "I'll skip the BUDGET check, the test is fast." Tests are tiny. Production is not. The check is one line of complexity accounting; do it.
- "I'll rename and update the callers later." Later is never. A half-rename is worse than no rename.
- "The name is misleading but renaming is churn." Every future reader pays the wrong mental model. Rename — atomically, in this change.
- "Minimal code is the spirit of TDD." Wrong. The spirit is "the test proves something useful." Minimal code that is over budget proves you have unit tests. It does not prove the function fits its contract.

## What this stage is

A scoped version of TDD that does its actual job — unit-level correctness — as the inner cycle of a checkpointed slice.

## Output

Per cycle: a test that went red and then green, an implementation that fits the slice's local complexity budget (or a recorded `N/A — reason`), and either a refactor or an explicit finding that no cleanup is needed, with the semantic-name check applied atomically. If any of that is missing, the cycle did not finish. Finish it.
