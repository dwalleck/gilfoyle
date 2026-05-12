---
name: tdd-scoped
description: A scoped TDD discipline. Use for unit tests inside a slice during checkpointed-build. Adds two mandatory steps beyond GREEN — BUDGET and ORACLE — and treats TDD as one tool in a larger spiral, not the whole methodology.
---

# tdd-scoped

TDD is fine for what it actually does. It is not, by itself, a software engineering methodology. We use it as one gear in the loop. We do not let it pretend to be the whole machine.

## What TDD is for

Verifying that a single function does what its caller expects, when called with inputs you've enumerated. A check on the unit's correctness against the unit's contract. Important. Limited.

## What TDD is NOT for

- Establishing that the design as a whole is correct. (That's `falsifiable-design`.)
- Establishing that the implementation matches the real system's behavior. (That's `prove-it-prototype`.)
- Establishing that the code is fast enough at production scale. (That's the budget from `budgeted-plan`.)
- Establishing that the feature actually works on production-shape data. (That's `checkpointed-build`.)

If you think "I have unit tests, therefore the feature works," you are misusing the tool. Unit tests proving things they don't prove is how features ship with the wrong algorithm.

## The rule

```
RED → GREEN → BUDGET → ORACLE → REFACTOR
```

The two new gates (BUDGET, ORACLE) are mandatory between GREEN and REFACTOR. Without them, you have not finished the test. You have made it pass.

## When this skill runs

Inside a slice during `checkpointed-build`, for any new function or any modified behavior of an existing function. The slice's contract (claim, fixture, oracle, budget) comes from `budgeted-plan` and is in scope for the entire cycle.

## The cycle

### RED — write the failing test

- One behavior per test.
- Clear name. Behavior described, not implementation.
- Real code where possible. Mocks only when the dependency is truly external (network, time, randomness).
- Watch it fail. **Mandatory.** If it passes immediately, the test is wrong.

### GREEN — minimal code to pass

Write the simplest implementation that makes the test pass. Minimal is fine *here*. The minimal implementation is allowed to be inefficient, ugly, or hyper-specific to this test. It is not allowed to be wrong.

Watch the test pass. Watch other tests still pass. **Mandatory.**

### BUDGET — does this fit the slice's complexity budget?

The slice has a loop budget and possibly a wall-clock budget from `budgeted-plan`. Now that the test passes, check:

- Every loop in the new code: state its complexity. Does it fit the slice's budget at production scale?
- If the slice has a wall-clock budget: measure with `time`/`hyperfine`/equivalent. Does it fit?

If no: **REWRITE.** The minimal implementation is wrong because it's over budget. Pick an algorithm that fits. Rerun the test. Rerun BUDGET.

This is the step "minimal code" alone gets wrong. "Minimal" optimizes for the test passing. "Minimal within budget" optimizes for the slice's contract. The contract is the goal.

### ORACLE — does the binary still agree with the prove-it-prototype oracle?

Rebuild the binary. Run the prove-it-prototype probe again. Compare to its oracle.

If they still agree: proceed.

If they drift: the implementation that just passed its unit test broke the slice's correctness contract. The unit test was passing for the wrong reason. **STOP.** Surface to the user via the `checkpointed-build` halt protocol.

This is the gate that catches "the unit test is fine but the integration is wrong." It exists because the test universe and the real universe are different universes.

### REFACTOR — clean up

After BUDGET and ORACLE both pass: clean up. Remove duplication. Improve names. Extract helpers. Keep tests green. Keep budget. Keep oracle agreement.

#### Semantic-name check

If this cycle changed a function's *semantics* (return type, error conditions, what "no match" means, etc.), explicitly ask: **does the function's name still describe its behavior?**

Examples that should trigger a rename:

- A `search_by_name` that used to return "first match" but now returns "unique match or None" — the name no longer signals the contract. Rename to `search_unique_by_name` or `find_unambiguous_by_name`.
- A `parse_X` that used to panic on malformed input but now returns `Result` — rename to `try_parse_X`.
- A `get_X` that used to assume cache presence but now does I/O — rename to `load_X` or `fetch_X`.

Renaming costs one signature change plus N call-site updates. Not renaming costs every future reader assuming the wrong contract from the name and being surprised by the behavior. The first cost is bounded and now; the second is unbounded over time.

If the name still fits, say so out loud (in a commit message or comment) so future-you knows the question was asked.

**When renaming, use the impact-analysis step from `checkpointed-build` a-1** to enumerate every call site. Static-analysis tool first (e.g. `tethys callers <Type::method>` or your IDE's find-usages), `grep` as the safety net. Update every site in the same commit. A rename committed with stale call sites is a half-rename, which is worse than no rename: future grep for the new name misses the old call sites, and future grep for the old name shows phantoms.

Then move to the next test in this slice, or close the slice and advance.

## Corrections to standard TDD practice

The standard TDD skill says:

> "Need to explore first" → Fine. Throw away exploration, start with TDD.

**Wrong.** Exploration was `prove-it-prototype`. You do not throw the probe away. You promote it to the persistent oracle. The probe stays. The agreement stays. TDD runs *on top of* the probe, not in place of it.

The standard TDD skill says:

> Minimal code. Just enough to pass.

**Insufficient.** "Just enough to pass the unit test" is not the bar. The bar is "just enough to pass the unit test, fit the slice's budget, and keep the oracle agreement." Three conditions, all required.

The standard TDD skill says:

> Tests use real code (mocks only if unavoidable).

**Correct but incomplete.** "Real code" here means "real code in the test fixture." The fixture is still a fixture. It is not production data. Unit tests using real code against a tiny fixture still cannot tell you anything about production-scale behavior. That's what BUDGET and ORACLE are for.

## Verification checklist

Beyond the standard "every function tested, watched it fail, watched it pass":

- [ ] Implementation fits the slice's loop budget at production scale
- [ ] Implementation fits the slice's wall-clock budget, if it has one
- [ ] prove-it-prototype oracle still agrees with the binary
- [ ] Any doc-comment precondition has matching enforcement (runtime check for load-bearing-correctness; `debug_assert!` for sanity-hint)
- [ ] Output streams classified correctly (data → stdout, diagnostics → stderr)
- [ ] If function semantics changed: name still describes the behavior (or renamed)

If you cannot check all six, the slice is not done. Do not commit.

## Red flags

- "Tests pass, ship it." Tests passing is necessary, not sufficient. Run the oracle.
- "I'll skip the BUDGET check, the test is fast." Tests are tiny. Production is not. Check anyway.
- "I'll skip the ORACLE check, this slice doesn't touch the resolver." Slices don't touch things in isolation. Run the oracle every slice. Yes, every.
- "Minimal code is the spirit of TDD." Wrong. The spirit is "the test proves something useful." Minimal code that's over budget proves you have unit tests. It does not prove the feature works.
- "The unit test passed, the oracle drifted, must be the oracle's fault." Be very, very suspicious of this conclusion. The oracle is independent by construction. If you find yourself revising the oracle to match the implementation, you have lost.

## What this skill is

A scoped version of TDD that does its actual job — unit-level correctness — without pretending to do jobs it can't do. It is one gear in the gilfoyle loop. It does not turn the wheel by itself.

## Output

For each test cycle: a failing test that became passing, an implementation that fits the budget, and a re-confirmed oracle agreement. If any of those three is missing, the cycle didn't finish. Finish it.
