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

## When this skill runs

After `prove-it-prototype` has produced a probe and an oracle that agree. Not before. If you don't have agreement, you have nothing to extend a design from.

## Inputs

- The probe and oracle from `prove-it-prototype`.
- Vague feature intent, refined by what the probe revealed.

## Process

### 1. Re-read the probe

The probe tells you what the system actually does. The design extends that. The design *may not contradict* the probe. If you want the design to claim something the probe disproved, either re-run the probe with new questions or rewrite the design.

### 2. Enumerate claims

Write the design as a numbered list of claims. One sentence each. If a claim takes more than one sentence, split it.

Examples:

- "Ca for package P equals the count of distinct packages whose source files contain `use P::*` statements."
- "Re-indexing produces identical metrics."
- "Packages with no cross-crate dependencies have I = 0."

### 3. For each claim, write a falsifier

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

### 4. Rank falsifiers by cost

Sort by cost-to-run, ascending. Five minutes at the top, hours-to-days at the bottom.

### 5. Run the cheapest falsifier NOW

Before asking the user to approve the design. The cheapest falsifier costs almost nothing. It produces one of:

- **Passing result.** The cheapest claim survived its first attempt to kill it. Continue.
- **Failing result.** The design is wrong. Revise. Possibly re-run `prove-it-prototype`.

This is not optional. The single most informative thing you can do at design time is run the cheapest experiment that would prove your design wrong, and have it survive. Skipping this step is how designs that confirm themselves get approved.

### 6. Self-review (the new kind)

After writing the design but before showing it to the user:

1. **Claim count.** How many claims? Under 3: not designing a feature. Over 15: designing too much, split it.

2. **Falsifier independence.** For each falsifier, is its oracle independent of the system under test? If a falsifier's oracle is "another part of this feature," replace it.

3. **Per-claim verification distinctness.** Each claim must have a *distinct* falsifier output — meaning if claim N fails, you can tell *which claim* failed by reading the oracle's output, without guessing. If two claims share a single oracle that produces one yes/no answer covering both, you have lost the ability to localize failures. Either split the oracle into per-claim outputs (e.g. distinct sections of a probe script, or distinct asserts in a test suite) or merge the claims into one.

4. **Cost distribution.** Any claims whose only falsifier is expensive (requires production data, multi-day soak)? Those are claims you cannot afford to be wrong about cheaply. Either find a cheaper falsifier or move that claim to "things we test in staging" with a written acceptance of the risk.

5. **Negative space.** What's NOT in this design? Write down at least three things the feature deliberately does not do. If you can't think of three, the design has no boundaries.

### 7. Write the design doc

Standard sections — purpose, architecture, components — with one mandatory new section:

#### Falsification

```
| # | Claim | Falsifier | Oracle | Cost | Status |
|---|-------|-----------|--------|------|--------|
| 1 | ...   | ...       | ...    | 5m   | passed |
| 2 | ...   | ...       | ...    | 30m  | pending |
| ... |
```

The cheapest claim's status must be `passed` before the design moves to planning.

## Hard gate

The next skill — `budgeted-plan` — refuses to run until:

- [ ] Every claim in the design has a falsifier in the table
- [ ] Every falsifier names an independent oracle
- [ ] **Every claim has a distinct verifiable output** — if claim N fails, the oracle's output tells you it was claim N specifically (not "something in the feature broke")
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

- The design doc with a `## Falsification` table.
- The cheapest falsifier run, with its passing result recorded in the table.
- The "Negative space" section listing what the feature deliberately won't do.

If any of those three are missing, the skill didn't run. Run it.
