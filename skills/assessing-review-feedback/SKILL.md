---
name: assessing-review-feedback
description: Use when responding to PR review feedback (human or bot) before applying any changes. Treats each finding as a hypothesis to verify, not an instruction to follow. Decides per finding whether the bug claim is real AND whether the proposed fix is right AND whether to accept, modify, or reject. Refuses to apply changes without per-finding verification.
---

# assessing-review-feedback

A reviewer gave you findings. Maybe a person. Maybe a bot. Maybe ten bots running in parallel. The instinct is to apply them all and move on. Resist it.

Each finding is a hypothesis with two parts:

1. **The bug claim:** there is a problem at location X with property Y.
2. **The fix claim:** the problem is correctly addressed by change Z.

Both can be wrong independently. The reviewer can be right about the bug but propose a fix that masks a deeper issue. The reviewer can propose a fine fix but the bug doesn't actually exist in your code today (vestigial finding from a tool with stale context). The reviewer can be right about both but the fix conflicts with project conventions you can't see from inside their analysis.

Treating "the reviewer said it" as sufficient grounds to apply a change is regression to the workflow that produced the original bugs. Verification still has to happen, the same way it did in `prove-it-prototype` and `falsifiable-design`.

## The rule

```
For each finding:
  1. Verify the bug claim. Reproduce the alleged problem before accepting it exists.
  2. Evaluate the proposed fix on its own merits. Is it the right fix, or a band-aid?
  3. Decide: accept, modify, reject. Document why.
  4. Apply only after step 3.

No applying without verifying. No "the reviewer said so."
```

## When this skill runs

After receiving review feedback on code that has passed `gilfoyle/checkpointed-build`. Before applying any review-driven changes.

Equally applicable to: human reviewer comments on a PR, bot review output (Claude code-reviewer, Sonar, GitHub Copilot), output from `/pr-review-toolkit:review-pr`, drive-by suggestions in chat.

Not applicable to: hard CI failures (failing tests, broken builds). Those are facts, not hypotheses.

## Process

### 1. Categorize each finding

Each finding falls into one of:

- **Bug claim** — "there is a defect at X." Requires verification.
- **Style / convention claim** — "this doesn't match project conventions." Requires checking the convention.
- **Design claim** — "this would be better structured as Y." Requires evaluation against project priorities.
- **Polish claim** — "this is fine but could be tighter." Subjective; verify the gain is real.

Different categories get different verification standards. A bug claim that can't be reproduced gets rejected. A style claim with no convention to point at is the reviewer's preference, not yours.

### 2. Verify the bug claim (for bug claims)

Before applying the fix, prove the bug exists:

- Construct an experiment that exhibits the alleged problem. Could be a unit test, a shell command, a database query, eyeballing the code with the claim in mind.
- Run it. Confirm the bug, refute it, or note "can't reproduce."
- If you can't construct an experiment, the bug claim is too vague. Push back on the reviewer for specifics OR mark as "speculation, not actionable."
- **Also search the tracker.** A reviewer finding often describes a known issue with a different framing. Keyword-match the finding against the project's issue tracker. If a match exists: the finding is "duplicate of <issue>" rather than a new bug to design a fix for. That's still a real signal (multiple readers flagging the same thing means it's observable), but the *decision shape* becomes "link the PR to the known issue and defer" or "absorb the known issue's scope into this fix" — not "design from scratch." Add a corresponding row category to the decision log: **"Duplicate of <id>"** with a one-line note on whether you're deferring or absorbing.

A reviewer who said "this might fail in production" without naming a reproduction is not a finding. It's a feeling.

### 3. Evaluate the proposed fix

Even if the bug is real, the proposed fix may be wrong. Check:

- **Root cause vs symptom.** Does the fix address the underlying cause, or paper over the symptom? Symptom fixes are tech debt accumulators.
- **Side effects.** Does the fix introduce new failure modes? Change behavior at the boundary in ways the reviewer didn't notice?
- **Project alignment.** Does the fix match how the codebase solves similar problems? Or does it introduce a one-off pattern?
- **Cost vs impact.** Is the fix proportional to the bug's severity? A fifty-line refactor for a one-character typo is wrong-sized.
- **Counter-proposals.** Is there a simpler, more correct, or better-localized fix?

If the reviewer's fix is wrong, write a better one. Document the divergence so the reviewer (when human) understands you considered their suggestion and chose differently.

### 4. Decide per finding

Three outcomes:

- **Accept.** Apply the reviewer's fix as written. Best when bug is real and fix is right.
- **Modify.** Apply a different fix that addresses the same bug. Best when bug is real but reviewer's fix is wrong, sub-optimal, or out of style.
- **Reject.** Don't apply. Best when bug claim isn't real, fix would make things worse, or scope is wrong for this PR.

Each decision is documented. One line per finding, kept with the code or PR. Future reviewers (and future you) need to see "we considered finding X and decided Y because Z."

**Deferral has a tracker-discipline tax.** Any decision that's effectively "real concern, defer to follow-up" — i.e., a **Reject (defer)** or **Modify (deferred work)** — must name a tracker ID in the decision log's `Note` column. The procedure:

1. Search the tracker for an existing issue covering the deferred work. Keyword-match against issue titles and descriptions.
2. **Found one:** reference its ID in the `Note` column. The decision becomes "Reject (defer): tracked at rivets-XXX."
3. **No match:** file the issue *before* finalizing the decision log. `rivets create --title "..." --type task --priority N --description "<one-line context + the finding's key claim>"`. Put the new ID in the `Note` column.

A "defer" decision with no tracker reference is a silent drop. Six months from now, no one knows the finding existed — and the next reviewer is likely to find it again, with both of you re-doing the same triage.

This is the same rule as `falsifiable-design`'s tracker discipline, applied to review-time deferrals.

### 5. Apply changes

Standard TDD discipline (`gilfoyle/tdd-scoped`) for any fix that introduces behavior change. Pure doc/comment edits don't need TDD but still need to be defensible.

If a fix turns out to be wrong during implementation, that's another iteration of step 3. Don't ship a fix you no longer believe in just because you already started writing it.

### 6. Decision log

The output of this skill is a decision log. Markdown is fine. A section in the PR description is fine. A comment thread is fine. The form matters less than the existence.

Example structure:

```markdown
## Review-feedback decisions

| # | Finding (one line) | Reviewer | Category | Verified? | Decision | Note |
|---|---|---|---|---|---|---|
| 1 | debug_assert on empty prefix → silent in release | silent-failure-hunter | Bug | Yes (read code; release builds skip the assert) | Modify | Runtime guard returning Ok(None); reviewer's instinct right, fix slightly different |
| 2 | Reuse normalize_path helper | code-simplifier + silent-failure-hunter | Style | Yes (db/files.rs:20-27 has identical semantics) | Accept | Two reviewers agreed; eliminates Linux asymmetry |
| ... |
```

## Hard gate

No fix gets applied until:

- [ ] Finding categorized
- [ ] Bug claim verified (or marked as un-reproducible)
- [ ] Fix evaluated (root cause? side effects? alignment? cost?)
- [ ] Decision recorded (accept / modify / reject + one-line rationale)
- [ ] **Every "Reject (defer)" or "Modify (deferred work)" decision names a verified tracker ID** in the `Note` column — either an existing issue whose content covers the deferred work, or a freshly-filed one

If you can't fill out all five, you're not ready to apply. Keep thinking.

## Red flags

- "Apply all the reviewer's suggestions." Wrong. You're the author, not the typist. Apply the ones that survive verification.
- "This reviewer is experienced, they're probably right." Probably is not yes. Verify.
- "Six findings, six accepts." Either every finding was right (unlikely in any but the smallest reviews) or you didn't really evaluate. Statistically, two or three of six should be reject / modify in a healthy review.
- "I'll just add the comment they suggested; the code is fine." If the code is fine, the comment is decoration. If the code is unclear enough to need the comment, the code can probably be clearer. Ask which.
- "The reviewer's fix is incomplete but I'll start there and iterate." No. Decide what the right fix is up front. Iteration here = scope creep.
- "Bot suggestions don't deserve verification." Yes they do. Bots emit volume; humans emit signal-to-noise judgment. Verify either way.
- "The fix doesn't change behavior, just style. Skip the verification." Style changes can still introduce bugs (renaming a function breaks callers, removing a comment loses context). Verify proportional to the change's blast radius.
- "Two reviewers agreed, so it must be right." Two reviewers can share the same blind spot. Verify the underlying claim, not the count.
- "Rejecting this — out of scope for the PR." Out of scope is not a synonym for "we'll never do this." Either file a tracker entry for the deferred work and reference its ID, or you've effectively decided the finding was wrong (in which case "Reject" with rationale, not "defer"). "Out of scope, no tracker" is a silent drop.

## What this skill is not

This is not "be contrarian for the sake of pushback." Most well-meaning reviewer findings are real and the proposed fixes are reasonable. The skill exists for the cases where they aren't — and to ensure the author thinks per-finding rather than batch-applying.

This is also not a license to ignore feedback. If you reject a finding, the rationale is part of the decision log. A future reviewer can challenge it. The asymmetry "easy to reject silently, harder to verify rejection" is exactly what causes findings to slip through.

## Output

A decision log committed to the repo or attached to the PR. Plus the actual code changes for accepted / modified findings, each in a separate commit (so the decision log lines up with git history).

If no findings were applied, the decision log alone is the output, and the reasoning is the artifact.
