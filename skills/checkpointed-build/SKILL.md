---
name: checkpointed-build
description: Replaces executing-plans. Executes slices one at a time. After each slice, runs the slice's stress fixture AND the prove-it-prototype oracle against the binary AND the budget check. If any of those fail, STOPS and surfaces the drift to the user. Treats the plan as a hypothesis, not a contract.
---

# checkpointed-build

You are not typing the plan. You are advancing the design hypothesis by one slice. After each slice, you go back to reality and check whether the design is still standing.

## The rule

```
For each slice:
  1. Implement.
  2. Run unit tests.
  3. Run the stress fixture.
  4. Run the prove-it-prototype oracle against the binary.
  5. Check the budget.
  6. If anything in 2-5 fails → STOP. Surface to user. Do not proceed.
  7. Else → commit. Next slice.
```

Stopping is the most important step. The standard convention is to push through drift and "fix it later." We do not. Drift caught at slice N is cheap. Drift caught at slice N+8 is the entire feature.

## When this skill runs

After `budgeted-plan` has produced a plan with all gates passing. Not before. If there's no plan, you're improvising. We do not improvise.

## Process

### 1. Load the plan. Critique it before starting.

Read the plan once, top to bottom. Flag any slice where:

- The complexity budget seems implausible. (A loop labeled `O(n)` over `files × symbols` is not `O(n)`.)
- The stress fixture is suspiciously gentle. (A fixture with three items doesn't surface scaling bugs.)
- The oracle seems coupled to the implementation. (If the oracle calls the same function the slice implements, it's not an oracle.)
- A doc-comment precondition has no `debug_assert!`.

Raise concerns with the user *before* writing any code. The plan is allowed to be wrong. Catching it now is free.

### 2. For each slice, in order

#### a-1. Impact analysis (before implementing)

If the slice changes the *signature, name, or semantics* of an existing function — public or private — list the callers BEFORE writing the change. The list bounds the change's blast radius and tells you what else this slice must update.

Tooling, in preference order:

1. **Static-analysis tool** (e.g., `tethys callers <Type::method>`, IDE "find usages," `rust-analyzer` references). Cheap, fast, and catches most callers. Use the qualified path when bare names are ambiguous.
2. **`grep`** for the function name across the codebase. Catches what static analysis missed (string-built dynamic dispatch, doc references, etc.).
3. **Both, when stakes are high.** Static analysis is the starting point; `grep` is the safety net.

Caveats on the static-analysis tool you're using:

- The tool's coverage is bounded by its own correctness. If you're modifying the resolver, the resolver's caller-analysis is what you're fixing. Use the tool as a HINT generator, not an oracle.
- Cross-crate edges may be missed or phantom-generated depending on the tool's resolver maturity. For intra-crate calls, accuracy is typically much higher.
- An empty caller list is suspicious. Either nothing calls the function (dead code — should you delete it?) or the index is stale (re-index and retry).

Output of this step: a short list (caller path + line) committed in the slice's plan or commit message. Future readers see what the change touched.

If the slice is adding a brand-new function with no existing callers, this step is a no-op — note that explicitly so the absence is intentional, not forgetful.

#### a0. Helper search (before implementing)

Before writing any utility code (path manipulation, string normalization, error wrapping, retry logic, common SQL fragments), `grep` the codebase for existing equivalents. If a helper exists with matching semantics, reuse it. If a helper exists with *close* semantics, either widen the helper or write a wrapper — do not duplicate.

Concrete checks:

- For path/string handling: search for normalization helpers (e.g., `normalize_*`, `to_str`, `canonical`).
- For SQL: search for shared column lists, query builders, parameter helpers.
- For error mapping: search for existing `From`/`map_err` patterns.

The cost of this check is 60 seconds of `grep`. The cost of duplicating a helper is: divergence when the original changes, two places to update for the next bug fix, reviewer time spent flagging the duplication. Spend the 60 seconds.

#### a. Implement

Write the code. TDD discipline applies for unit tests inside the slice (use `tdd-scoped`). The pre-typed code in the plan is advisory. You are permitted, encouraged even, to deviate if you spot a better algorithm or a missing edge case. The slice's *contract* is its claim, fixture, oracle, and budget — not its code blocks.

#### a2. Symmetry audit (when the slice adds a parallel code path)

If the slice introduces a new branch that parallels an existing one — e.g., a same-crate lookup alongside an existing unscoped lookup, a new retry path alongside an existing one, a new validation that mirrors a check elsewhere — list the existing path's behaviors and confirm the new path matches OR has a written justification for the divergence.

Specific checklist when adding a parallel path:

- **Error handling:** does the new path return the same error variant as the old one for the same failure mode? Or does it silently swallow what the old one logs?
- **Logging:** does the new path emit `warn!`/`debug!`/`info!` at the same severity as the old one for analogous events?
- **Fallback behavior:** does the new path fall through, return None, or return Err the same way the old one does?
- **Caller observability:** can a caller distinguish "new path succeeded" from "new path declined, old path took over" — and is that distinguishability the same as before?

Asymmetry is allowed. Unintentional asymmetry is the bug class this audit catches.

#### b. Run unit tests

`cargo nextest run` or the equivalent for your language. Output must be pristine: no errors, no warnings, no skips outside the documented skip list.

#### c. Run the stress fixture

The fixture from the plan, with the expected outcome from the plan. Compare actual to expected. Exact match required.

#### d. Run the prove-it-prototype oracle against the binary

This is the step you will be most tempted to skip. Do not skip it.

- Rebuild the binary.
- Run it against the same workspace that the prove-it-prototype probed.
- Run the oracle against the same workspace.
- Compare. They must still agree.

If they drift, this slice broke something earlier slices established. That is the highest-priority bug class. Stop here, regardless of whether unit tests pass.

#### e. Check the budget

For every loop the slice introduced, confirm the production-scale cost is what the plan budgeted. For an always-on phase, measure wall-clock against the budget. Use `time`, `hyperfine`, or a benchmark harness. Eyeballing it does not count.

#### f. If anything in (b)–(e) fails: STOP.

Do not commit. Do not advance to the next slice. Surface to the user:

```
Slice N halted.

- Unit tests:   [pass | fail with diff]
- Stress fixture: [pass | fail with diff]
- Oracle drift: [exact items where binary and oracle disagree]
- Budget:       [actual vs planned, with measurement]

The implementation, the oracle, or the design is wrong. Which is it?
```

The user picks. Possible outcomes:

- **Implementation is wrong.** Fix. Rerun gates. Stay on slice N.
- **Oracle is wrong.** Revise the oracle. Re-run `prove-it-prototype` to confirm the revised oracle still agrees with the probe. Stay on slice N.
- **Design is wrong.** Go back to `falsifiable-design`. The plan may need to be rewritten. Possibly the probe needs to be re-run.

Your job is to surface accurately, not to decide. Decisions about which thing is wrong are not yours to make from inside the executor.

#### f2. Stale-reference sweep (after gates pass, before commit)

The slice you just landed may have made earlier slice comments out of date. Scan every file modified by this slice — plus the files the slice depends on — for:

- **Forward-reference comments** like `// slice N hardens this` or `// to be implemented in step M`. If the future slice has now landed, rewrite the comment to describe current behavior in present-tense / past-tense factual terms.
- **Contract discoveries.** If a bug surfaced in this slice revealed a previously-implicit contract (e.g., "this function requires forward-slash paths"), that contract belongs in the function's doc-comment AND, if load-bearing, enforced per the doc-comment-as-contract rule. Update the doc in this same commit, not later.
- **Renames you should have done.** If this slice changed the semantics of an existing function, ask whether the function's name still describes its behavior. If the name is now misleading (e.g., `search_symbol_by_name` that now refuses ambiguity), rename in this commit. The longer a misleading name persists, the more callers depend on the wrong mental model.

Run `grep` for the slice number, for keywords like "TODO", "later", "future", and for any comment phrase that anticipated work that's now done. Fix what you find before committing.

#### g. If everything in (b)–(e) passes: commit

One commit per slice. Commit message references the design claim this slice implements.

### 3. Repeat until all slices complete

### 4. Final integration check

After every slice has passed: rebuild the binary. Run *every* oracle from `prove-it-prototype` and *every* falsifier from `falsifiable-design`. They must all still pass.

If any fail, you have a regression introduced somewhere in the slice chain. Bisect to find which slice. Stop. Surface.

## When to stop and ask, beyond the per-slice gates

- Implementation requires a decision the plan didn't make. Stop. Ask.
- A test fails for a reason the plan didn't anticipate. Stop. Ask. **Do not "fix" the test to make it pass.**
- A slice takes more than 2x its estimated time. Stop. Reassess.
- You're about to add a line of code you couldn't justify out loud to a stranger. Stop. Justify.

## Red flags

- "The oracle drifted by one item, I'll fix it on the next slice." No. Drift across slices is silent corruption. Stop now.
- "Unit tests pass but the integration check is slow. I'll run it at the end." No. The integration check IS the gate. Run it every slice.
- "The plan said to write this loop, so I wrote this loop, even though I see a better one." Wrong. The plan is advisory. Write the better loop. Note the deviation in the commit message.
- "I'll batch the next three slices and run gates at the end." No. Each slice gets its own gate. Batching is how drift becomes invisible.
- "The stress fixture passed but the unit test was wrong, so the test passed." Stop. The unit test was wrong. Fix the test before you advance.

## What this skill is not

This is not "follow the plan." This is "advance the design hypothesis by one slice and re-test it against reality." The plan is the current best guess. Reality is the authority. If they disagree, reality wins, and you stop until the user decides whether to revise the implementation, the oracle, or the design.

## Output

For each slice, one commit with all gates green. After the final slice, a clean run of every oracle and every falsifier against the assembled binary. If any of those is missing, the skill didn't finish. Finish it.
