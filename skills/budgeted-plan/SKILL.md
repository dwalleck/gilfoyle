---
name: budgeted-plan
description: Replaces writing-plans. Decomposes a falsifiable design into small slices, each with mandatory complexity budget, scale budget, stress fixture, and oracle. Refuses to run until falsifiable-design has produced an approved design with a passing cheapest-falsifier.
---

# budgeted-plan

A plan is a sequence of falsifiable hypotheses, not a sequence of pre-typed code blocks.

The standard convention is a 2949-line plan that pre-types every line of code into checklist form, then "executes" by typing the code into source files. That is not planning. That is dictation. We do not produce dictation.

## The rule

```
Plan unit = slice.

Slice = (claim, falsifier, smallest code change, complexity budget, stress fixture).

A slice is done when:
  - its unit tests pass, AND
  - its stress fixture produces the expected result, AND
  - the prove-it-prototype oracle still agrees with the binary, AND
  - the complexity budget holds at the slice's scale.

Not before.
```

## When this skill runs

After `falsifiable-design` has produced an approved design with a passing cheapest-falsifier. Not before.

## Process

### 1. Decompose into slices

Take the claim list from the design. Each claim becomes one slice. If a claim is too big for one slice — more than ~50 lines of code, or touches more than 2 files — split the claim until it isn't.

A slice should be implementable in 30 minutes or less. If it takes longer, you have not decomposed enough.

### 2. Per-slice fields (mandatory)

Each slice has these fields *before* any code:

```
## Slice N: [one-sentence purpose]

**Claim:**           [the design claim this slice implements]
**Oracle:**          [independent computation; default = the prove-it-prototype oracle]
**Stress fixture:**  [input designed to break a plausible bug, not just exercise the code]
**Loop budget:**     [for each new loop: asymptotic cost AND production scale]
**Wall budget:**     [only for always-on phases: max wall-clock at production scale]
**Files:**           [exact paths to create or modify]

**Code (advisory):**
  ```
  [you may pre-type code here, but the implementer is permitted to deviate
   if the deviation keeps the slice within budget and the oracle passing]
  ```

**Verification:**
- [ ] Unit tests pass
- [ ] Stress fixture produces expected outcome
- [ ] prove-it-prototype oracle still agrees with binary
- [ ] Loop and wall budgets hold at fixture scale
```

If you cannot fill in all the mandatory fields, the slice is not ready. Do not fake it. Go think.

### 3. Loop budget rules

For every new loop the slice introduces:

- State the asymptotic cost in terms of the inputs. Examples: `O(files × crates)`, `O(symbols log symbols)`, `O(n + m)`.
- State the inputs' size at production scale. Examples: `files ≈ 50k, crates ≈ 200`.
- Compute the product. If it exceeds **10^6 operations** or **10^3 syscalls** in an always-on phase, the loop is over budget. Either justify in writing why this is fine, or pick a different algorithm.

A loop without a complexity statement is a budget violation. Do not write one.

### 4. Stress fixture rules

For every slice that implements logic (not pure types, not pure schema):

- Write down a fixture designed to *fail* if a plausible bug exists.
- Plausible bug classes to design fixtures against:
  - Two inputs with the same name in different scopes ("does the name-collision bug exist?")
  - The secondary sort key never fires because the primary key is always unique in the happy-path fixture ("is the tie-break actually wired up?")
  - Empty input ("does the empty-collection path exist?")
  - Unicode, backslashes, paths with spaces ("did you assume ASCII?")
  - Very large input ("is the loop budget honest?")

The stress fixture's expected output is written down *before* the implementation. Not after.

If you cannot think of a plausible bug for a slice, the slice is either too small to be worth its own test (combine with the next one) or you haven't thought hard enough (think harder).

### 5. Doc-comment-as-contract rule

For every doc comment in the slice that says "callers must X" or "Y is a precondition" or "Z must be non-empty," classify the precondition's enforcement strength FIRST, then enforce accordingly:

- **Load-bearing for correctness.** If violating the precondition would silently produce wrong output (e.g., empty prefix → SQL `LIKE '%'` matches everything), add a **runtime check** that survives release builds. Return an error or a documented refusal value. `debug_assert!` alone is wrong here — it compiles out in release and the contract becomes a fiction.

- **Sanity hint for callers.** If violating the precondition is "programmer error that would never reach production with a sane caller," `debug_assert!` is appropriate. Dev/test catches it; release tolerates it without semantic damage.

The test: ask "what does the function silently produce in release builds if this precondition is violated?" If the answer is "wrong output," you need a runtime check. If the answer is "nonsense that the caller would have caught upstream anyway," `debug_assert!` is fine.

A documented precondition without ANY enforcement is a documentation lie. We do not ship those.

### 6. Output stream rule

For every thing the slice writes to:

- Classify as **data** or **diagnostic**.
- Data goes to stdout. Diagnostics go to stderr.
- If you're not sure: ask "would a downstream pipe (`| jq`, `| grep`) want to see this?" If yes, data. If no, diagnostic.

If the rule is violated, justify it in writing in the slice. Don't ship an unexamined `println!` to a file descriptor.

### 7. Self-review

Before saving the plan, run these four lists:

1. **Every loop in the plan.** For each: complexity stated? Within budget at production scale?
2. **Every fixture.** For each: what bug class is it designed to fail under? Is it more than a happy-path exercise?
3. **Every doc-comment precondition.** For each: classified as load-bearing-correctness or sanity-hint? Where is the matching enforcement (runtime check for the former, `debug_assert!` for the latter)?
4. **Every write target.** For each: classified data or diagnostic?

If any of the four lists has gaps, the plan is incomplete. Don't save it.

## Hard gate

The next skill — `checkpointed-build` — refuses to run until:

- [ ] Every slice has all mandatory fields filled in
- [ ] Every loop has a complexity statement
- [ ] Every slice has a stress fixture
- [ ] The plan's claim coverage matches the design's claim list

## Red flags

- "I'll fill in the complexity budget later." Later is never. If you don't know the cost, you don't know what you're building.
- A slice that says "trivial, no fixture needed." Trivial slices don't get planned. They get inlined. If it's worth a slice, it's worth a fixture.
- A loop annotated `O(?)` or "depends on input." Write down what it depends on, and bound it.
- A slice touching more than 2 files. Split it.
- A slice estimated at more than 30 minutes. Split it.
- A "happy path" fixture with no adversarial counterpart. Add one.
- "Pre-typed code in the plan is mandatory." Wrong. Pre-typed code is advisory. The contract is the slice's claim, fixture, oracle, and budget.

## What this skill is not

This is not a script for an executor to type from. The plan is a hypothesis the implementer is allowed to update as they learn. Pre-typed code blocks are suggestions. If the implementer finds a better algorithm during execution, they take it — provided the oracle still passes and the budget still holds. The fields are the contract. The code blocks are scaffolding.

## Output

A plan document with:

- One section per slice.
- Each slice has filled-in mandatory fields.
- A `## Plan Self-Review` section at the bottom listing the four lists from step 7, all empty (no gaps).

If the plan has gaps, the skill didn't run. Run it.
