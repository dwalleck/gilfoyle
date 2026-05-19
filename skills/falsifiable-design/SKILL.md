---
name: falsifiable-design
description: Replaces brainstorming for feature design. Produces a design where every claim is paired with an experiment that would prove it wrong, and the cheapest such experiment runs before the design is approved. Refuses to run until prove-it-prototype has produced agreement between probe and oracle.
---

# falsifiable-design

A design that cannot be proven wrong is not a design. It is a wish list.

Most design documents are written so that any output the system later produces will appear to confirm the design. This is the design-doc equivalent of horoscopes: vague enough to never be falsified. We do not write those.

## The rule

```
Every claim has a falsifier.
The cheapest falsifier runs before the design is approved.
```

## Tracker discipline (applies throughout)

This is a discipline that fires continuously while writing the design, not a discrete step.

Every time you write any of these phrases:

- `deferred`, `deferred to`, `defer until`
- `out of scope`, `out-of-scope`
- `tracked`, `tracked at`, `tracked by`, `tracked elsewhere`
- `follow-up`, `next PR`, `as part of`, `future work`
- `later`, `revisit if`, `optimize later`

…pause writing and resolve the deferral immediately, before the phrase is committed to the artifact:

1. **If the phrase cites a tracker ID** (e.g., `tracked at rivets-abc1`, `see #123`): verify the ID exists in the tracker AND its description covers the deferred thing. `rivets show <id>` or the tracker equivalent. If the ID doesn't exist OR its description doesn't cover the deferred work, treat as case 2.

2. **If the phrase names a deferred thing with no tracker citation**: file the issue *now*, before resuming the design. Put the new ID back into the design where the language was. The cost is two minutes; the cost of skipping is that the deferral rots in the design doc and is invisible to `rivets list` / `rivets ready` forever.

3. **If the phrase is settled rationale, not deferred work** ("we picked X over Y because Z"): no tracker needed. But check yourself — if the phrase names a *trigger condition* ("revisit if N exceeds 50," "fix when LSP lands"), it's case 2 in disguise. File the issue.

A phantom tracker reference and a silent deferral fail in the same way: future contributors looking at the tracker can't find the deferred work. The reference IS the durable surface; the prose around it is decoration.

## When this skill runs

After `prove-it-prototype` has produced a probe and an oracle that agree. Not before. If you don't have agreement, you have nothing to extend a design from.

## Inputs

- The probe and oracle from `prove-it-prototype`.
- Vague feature intent, refined by what the probe revealed.

## Process

### 1. Re-read the probe

The probe tells you what the system actually does. The design extends that. The design *may not contradict* the probe. If you want the design to claim something the probe disproved, either re-run the probe with new questions or rewrite the design.

### 2. Enumerate input shapes

Before writing claims, enumerate every distinct shape the feature's inputs can take. This step anchors the claim list to input-space coverage rather than output-space happy paths.

For every input the design touches:

- **Sum types (enums):** list every variant.
- **`Option<T>`:** list both `Some` and `None`.
- **`Vec<T>` / collections:** list empty, single-element, multi-element with distinct values, multi-element with duplicates.
- **Structs with optional fields:** list every cell of the field-presence matrix that is reachable in production. (e.g., `CrateInfo { lib_path, bin_paths }` has at least four reachable shapes: lib+bin, lib-only, bin-only, neither.)
- **Numeric:** list zero, negative, boundary values, max.
- **Strings / paths:** list empty, ASCII-only, Unicode, with spaces, relative vs absolute.

Each production-reachable shape gets at least one claim in step 3. Out-of-scope shapes are noted as such, with a one-sentence justification.

The cost of this step is 10 minutes. The cost of skipping it: claims cover the shape the workspace-under-test happens to contain, the cheapest falsifier passes against real data, and the latent bug for the missing shape ships to the implementation phase. Concrete example: a `src_root()` design with claims only for `lib_path = Some("src/lib.rs")` will pass its cheapest falsifier against a workspace whose crates all have that shape — and silently break on the first bin-only crate it encounters in implementation.

Red flag: if you can't list ≥3 shapes, you have not enumerated yet. Reach harder. The `None` branch counts, the empty case counts, the boundary value counts.

### 3. Enumerate claims

Write the design as a numbered list of claims. One sentence each. If a claim takes more than one sentence, split it. For each input shape from step 2, ensure at least one claim covers it.

Examples:

- "Ca for package P equals the count of distinct packages whose source files contain `use P::*` statements."
- "Re-indexing produces identical metrics."
- "Packages with no cross-crate dependencies have I = 0."

### 4. For each claim, write a falsifier

A falsifier is an experiment that, if it produced a specific result, would mean the claim is false. The falsifier names:

- The input that would trigger the test.
- The expected outcome under the claim.
- The result that would falsify the claim.

Examples:

- Claim: *Ca for P = count of distinct packages with `use P::*`.*
  Falsifier: *Construct a workspace where 3 packages each contain `use P::foo`. If Ca(P) ≠ 3, the claim is false.*

- Claim: *Re-indexing produces identical metrics.*
  Falsifier: *Run index twice on the same unchanged workspace. Diff metrics. If diff is non-empty, claim is false.*

- Claim: *Packages with no cross-crate deps have I = 0.*
  Falsifier: *Build a single-crate workspace. Run. If I ≠ 0, claim is false.*

If you cannot write a falsifier for a claim, the claim is unfalsifiable. Unfalsifiable claims do not go in the design. They go in a separate "TODO: turn into a real claim" list. The list is allowed to exist. It is not the design.

### 5. Rank falsifiers by cost

Sort by cost-to-run, ascending. Five minutes at the top, hours-to-days at the bottom.

### 6. Run the cheapest falsifier NOW

Before asking the user to approve the design. The cheapest falsifier costs almost nothing. It produces one of:

- **Passing result.** The cheapest claim survived its first attempt to kill it. Continue.
- **Failing result.** The design is wrong. Revise. Possibly re-run `prove-it-prototype`.

This is not optional. The single most informative thing you can do at design time is run the cheapest experiment that would prove your design wrong, and have it survive. Skipping this step is how designs that confirm themselves get approved.

### 7. Self-review (the new kind)

After writing the design but before showing it to the user:

1. **Claim count.** How many claims? Under 3: not designing a feature. Over 15: designing too much, split it.

2. **Falsifier independence.** For each falsifier, is its oracle independent of the system under test? If a falsifier's oracle is "another part of this feature," replace it.

3. **Falsifier non-vacuity.** For each falsifier, name a specific buggy implementation that would make it fail. If you can't, the fence is decoration — it passes today and would pass in any future where the bug returns. Two recurring shapes to watch for:

   - **Predicates the schema makes mutually exclusive.** Combining `column LIKE 'X%'` AND `other_column IS NOT NULL` looks like a tighter filter, but if the schema's UPDATE atomically nulls one column when setting the other (e.g., `UPDATE refs SET symbol_id = ?, reference_name = NULL`), the two predicates can never both hold. The filter is vacuous regardless of bug.
   - **Disjunctive assertions where one disjunct is also asserted standalone.** `assert!(A == 0 || B >= 1); assert!(B >= 1);` — the first cannot catch any bug the second misses. Looks like defense-in-depth, isn't.

   The TDD-inversion test surfaces both: if no code mutation makes the new assertion fail without also failing a *different* assertion in the same fence, it's vacuous. Cut or rewrite. Distinct from #3 (independence is about whether the oracle lives outside the SUT; non-vacuity is about whether the oracle can fire at all) and from #4 below (distinctness is about which claim failed; non-vacuity is about whether any claim *can* fail).

4. **Per-claim verification distinctness.** Each claim must have a *distinct* falsifier output — meaning if claim N fails, you can tell *which claim* failed by reading the oracle's output, without guessing. If two claims share a single oracle that produces one yes/no answer covering both, you have lost the ability to localize failures. Either split the oracle into per-claim outputs (e.g. distinct sections of a probe script, or distinct asserts in a test suite) or merge the claims into one.

5. **Cost distribution.** Any claims whose only falsifier is expensive (requires production data, multi-day soak)? Those are claims you cannot afford to be wrong about cheaply. Either find a cheaper falsifier or move that claim to "things we test in staging" with a written acceptance of the risk.

6. **Negative space.** What's NOT in this design? Write down at least three things the feature deliberately does not do. If you can't think of three, the design has no boundaries.

7. **Tracker references.** Final safety net for the tracker discipline. Grep the design for the trigger-phrase list above. Each match must either cite a verified tracker ID OR be settled rationale (case 3). If you wrote a deferral phrase at any point during steps 1-7 without verifying or filing, do it now. A design that ships with un-tracked deferrals is shipping invisible technical debt.

### 8. Write the design doc

Standard sections — purpose, architecture, components — with one mandatory new section:

#### Falsification

```
| # | Claim | Falsifier | Oracle | Cost | Status | Regression fence |
|---|-------|-----------|--------|------|--------|------------------|
| 1 | ...   | ...       | ...    | 5m   | passed | unit test `foo::bar` |
| 2 | ...   | ...       | ...    | 30m  | pending | integration test `floor_check` |
| 3 | ...   | snapshot pre/post, diff | SQL count | 45m | pending | needs CI test (see below) |
| ... |
```

The cheapest claim's status must be `passed` before the design moves to planning.

**The `Regression fence` column** answers: "If this claim regresses after the PR merges, what test would fail?" Two rules:

1. If the `Falsifier` is a one-shot empirical measurement (snapshot pre/post, %delta, count diff), the `Regression fence` **must** point at a deterministic CI test that asserts the measured floor/ceiling. Empirical measurements live in audit-trail markdown forever, but they don't fail CI — a future change can silently re-introduce the bug the PR fixed, and all existing tests will still pass. The fence is the permanent form of the measurement.

2. If the `Falsifier` is itself a deterministic test (unit test, integration fixture), the `Regression fence` can be the same test — name it explicitly in the column.

A claim with `Regression fence: manual` is allowed but requires explicit user approval before merging. The default for measurement-based claims is "needs CI test before merge."

The fence's fixture should embed the bug class being fixed. For a "hardcoded-path-is-wrong" fix, the fixture's directory layout should defeat the hardcode (e.g., workspace root with no `src/`). Pre-fix code fails the fence; post-fix code passes. This makes the test a true regression sentinel — it won't trivially pass on whatever workspace it's pointed at.

## Hard gate

The next skill — `budgeted-plan` — refuses to run until:

- [ ] **Every production-reachable input shape is covered by at least one claim** — or explicitly noted as out-of-scope with a one-sentence justification
- [ ] Every claim in the design has a falsifier in the table
- [ ] Every falsifier names an independent oracle
- [ ] **Every claim has a distinct verifiable output** — if claim N fails, the oracle's output tells you it was claim N specifically (not "something in the feature broke")
- [ ] **Every measurement-based claim has a `Regression fence` entry** pointing at a deterministic CI test, OR explicit `manual` with documented user approval
- [ ] **Every deferral / out-of-scope / tracked-elsewhere reference in the design names a verified tracker ID** (existence checked, not assumed); deferrals without a citation have had their issue filed
- [ ] The cheapest falsifier has been run and passed
- [ ] The "Negative space" list has at least three entries

## Red flags

- "This claim is obvious, no falsifier needed." Wrong. Obvious claims are the ones most likely to be subtly false. Falsify it.
- "The falsifier is the unit test." The unit test was written from the same model as the claim. It is not independent. Find a real oracle.
- A claim phrased so vaguely you can't write a falsifier. Rewrite the claim. Vagueness is where bugs hide.
- "Negative space is hard to enumerate." Then the design has no boundaries. That is a planning bug worse than any algorithm bug.
- "We'll write the falsifiers when we get to that section." No. Falsifiers are part of the design, not its appendix.
- "One probe run covers all claims; if it passes, all claims pass." Wrong. If the probe passes you learn nothing per-claim. If it fails, you don't know which claim failed. Each claim needs its own observable output. Split the probe into per-claim sections, or write per-claim asserts. Localization at observation time is worth more than terseness at design time.

## What this skill is not

This is not brainstorming. Brainstorming optimizes for "what if we did X?" — a creative skill. This optimizes for "what would prove X wrong?" — an epistemic skill. You can brainstorm before invoking this, fine. But only this skill produces an approved design.

## Output

- The design doc with a `## Falsification` table that includes the `Regression fence` column.
- The cheapest falsifier run, with its passing result recorded in the table.
- The "Negative space" section listing what the feature deliberately won't do.
- The "Input shapes" enumeration (can be a list immediately above the claim list, or its own subsection).

If any of those four are missing, the skill didn't run. Run it.
