# assessing-review-feedback

A reviewer gave you findings. Maybe a person, maybe a bot, maybe several. Each finding is a hypothesis with two parts that fail independently:

1. **Bug claim** — there is a problem at location X with property Y.
2. **Fix claim** — change Z correctly addresses it.

The reviewer can be right about the bug and wrong about the fix, or right about the fix and wrong about the bug (stale context, misread code). Apply a finding only after it survives verification, and decide per finding — never per batch. Most findings are real and most proposed fixes reasonable: the default is to engage seriously with every finding, and let evidence decide.

## When this stage runs

- After review feedback arrives and before applying any review-driven change: human PR comments, bot output (code-reviewer, Sonar, Copilot), PR-review toolkit output, drive-by suggestions in chat.
- CI failures are **observed facts, not findings**. The red check is evidence; the reviewer's diagnosis of its cause and the proposed fix are hypotheses to verify like any other claim.

## Contract

Read [workflow contract](references/CONTRACT.md) before producing or consuming any workflow artifact. It is the single source of truth for the definitions this stage applies — gate states, slice, checkpoint ownership, tracker taxonomy, artifact ownership, and the canonical `.<change-slug>/` directory. Point to it; never restate it.

## Process

### 1. Inventory the findings

- Enumerate every review comment into rows with stable IDs (`F1`, `F2`, …). One row per finding; the same comment repeated by several reviewers is one finding with several sources.
- For each finding, restate the bug claim and the fix claim in your own words. A comment with no fix claim is noted as such — the evaluation is then yours alone.
- **Completion:** every comment in the review appears in exactly one row, and each row states the claims it makes.

### 2. Verify — assign exactly one evidence state

Check the claims against the code and record exactly one evidence state per finding:

- **Verified** — a reproduction or direct check demonstrated the claim. Name the reproduction (a test, command, query, or code reading with the reasoning that decided it).
- **Refuted** — a reproduction or direct check ran and did not exhibit the claimed behavior. Name the reproduction.
- **Unverified** — no reproduction or check was run yet; the claim is undecided. Name what is missing. **Unverified is not Refuted**: refuted is a negative result, unverified is no result. An unverified claim never authorizes a behavior-changing `Accept` or `Modify` — either gather the missing evidence (the state then moves to `Verified` or `Refuted`) or `Reject` with the rationale explicitly recording the claim as unverified.
- **Not-applicable** — the finding makes no factual claim to verify: pure preference, naming taste, process suggestion. The decision then rests on evaluation (step 3), not on verification.

CI failures: the failing check itself is observed fact; verify the diagnosis and the fix with the same reproductions — run the failing test or inspect the log — before accepting either.

**Completion:** every finding has exactly one evidence state; `Verified` and `Refuted` rows name the reproduction that decided them; `Unverified` rows name what is missing.

### 3. Evaluate the proposed fix

A real bug does not make the proposed fix right. For each `Accept` or `Modify` candidate, judge the fix on its own merits: root cause versus symptom, side effects at boundaries, alignment with how the codebase solves similar problems, proportional size, and whether a simpler or better-localized alternative exists. If the reviewer's fix is wrong, write the better one and document the divergence in the decision log.

**Completion:** every `Accept`/`Modify` finding names the fix applied; every divergence from the reviewer's proposed fix is documented.

### 4. Decide — exactly one of Accept, Modify, Reject

- **Accept** — apply the reviewer's fix as proposed.
- **Modify** — apply a different fix for the same claim.
- **Reject** — apply nothing; the rationale is recorded, including an explicit unverified rationale when the claim remains undecided.

Tracker duplicates are **modifiers on these decisions, never a fourth decision value**:

- `Accept (tracked at <id>)` — absorb the existing issue's scope into the fix being applied.
- `Modify (tracked at <id>)` — same, with a different fix.
- `Reject (tracked at <id>)` — the existing issue already covers the concern; defer to it.

Tracker taxonomy, per the contract:

- **Permanent non-goal / scope mismatch** — record the rationale in the `note`; no tracker issue is required.
- **Intended deferred work** — search the repository tracker for a covering issue and reference the verified ID; file one with the tracker's native command only when no match exists. Deferred work with no verified ID is a silent drop — not allowed.

**Completion:** every finding has exactly one decision from `{Accept, Modify, Reject}`; every tracked or deferred decision names a verified tracker issue ID; every permanent non-goal records its rationale.

### 5. Apply changes through the verification gates

- **Active Gilfoyle workflow** — detected by `route.md` and `plan.md` both present in the canonical `.<change-slug>/` directory: every behavior-changing `Accept`/`Modify` fix becomes an atomic review-fix slice. Return to [`budgeted-plan`](references/budgeted-plan.md), the sole owner of `plan.md`: revise an uncommitted owning slice, or append a fully populated slice when the owning slice is already committed. Scope it to the root-cause fix and every finding it resolves. If the fix changes approved behavior, architecture, or design claims, return first to the owning stage — [`interrogated-spec`](references/interrogated-spec.md) for behavior or [`falsifiable-design`](references/falsifiable-design.md) for architecture/design — and re-record approval per the contract. Then read and execute [`checkpointed-build`](references/checkpointed-build.md) for that slice and run its checkpoint once. Run final integration when every plan slice is complete, not after each edit.
- **Regression fence**: a `Verified` reproduction seeds the slice's fence but is not automatically one. Convert it into a permanent automated check — a committed test that goes red on the original bug and green on the fix — or carry a design-approved `N/A` risk in the slice instead.
- **Outside the workflow** (no `route.md` + `plan.md`): use the repository's normal reproduce → fix → focused-verification process.
- Non-behavioral fixes (docs, comments, formatting) skip the checkpoint but still carry their row in the decision log.
- A fix that fails during implementation returns to step 3: decide again; never ship a fix you no longer believe in.

**Completion:** every behavior-changing `Accept`/`Modify` fix passed its applicable verification gate — its workflow checkpoint, or the repository's focused verification — before commit; final integration passed after the last workflow slice.

### 6. Commit by atomic change

- Group commits by atomic change (the contract's slice definition), not by finding: one commit per atomic change. Several findings sharing one atomic change land in one commit; one finding spanning several atomic changes is named in all of them.
- Each commit message names the atomic change and lists **every finding ID it addresses** (e.g. `fix(parser): reject empty prefixes — F1, F3`).

**Completion:** every `Accept`/`Modify` finding is addressed by commits whose messages list its ID, and every commit lists the finding IDs it addresses.

### 7. Decision log

The output is a decision log: a section in the PR description, a comment thread, or — when no PR-native surface is specified — `review-decisions.md` in the canonical workflow directory defined by [workflow contract](references/CONTRACT.md). Exact schema, one row per finding:

| finding-id | finding | reviewer | evidence-state | evidence | decision | fix | note |
|---|---|---|---|---|---|---|---|

- `finding-id` — the stable ID from step 1.
- `finding` — one-line restatement of the reviewer's bug claim and proposed fix.
- `reviewer` — the source (human name, bot name, tool).
- `evidence-state` — exactly one of `Verified`, `Refuted`, `Unverified`, `Not-applicable`.
- `evidence` — the reproduction or check that decided the state; `N/A — <reason>` when `Not-applicable`; for `Unverified`, what is missing.
- `decision` — exactly one of `Accept`, `Modify`, `Reject`, optionally suffixed ` (tracked at <id>)`.
- `fix` — the applied change for `Accept`/`Modify`, naming its atomic change; `N/A — <reason>` for `Reject`.
- `note` — one-line rationale; permanent non-goals record the rationale justifying no tracker issue.

**Completion criterion:** every finding from step 1 appears in exactly one row; every row has exactly one `evidence-state` value and one `decision` value from the closed sets; every `Verified`/`Refuted` row names its evidence; every tracked or deferred decision carries a verified issue ID; every permanent non-goal records its rationale; every behavior-changing fix's row names the verification gate it passed.

## Hard gate

No behavior-changing fix is committed until:

- [ ] Every finding has exactly one evidence state and exactly one decision.
- [ ] No behavior-changing `Accept`/`Modify` rests on an `Unverified` claim.
- [ ] Every `Verified`/`Refuted` row names its evidence; every `Unverified` row names what is missing.
- [ ] Every tracked or deferred decision names a verified tracker issue ID; every permanent non-goal records its rationale.
- [ ] The applicable pre-commit verification passed: the review-fix slice's workflow checkpoint, or the repository's focused verification.
- [ ] Final integration passed when this is the last workflow slice; otherwise record `N/A — later plan slices remain` and run it after the last slice.
- [ ] Commits are grouped by atomic change and list the finding IDs they address.

A failed gate never authorizes shipping: known issues explain a failure; they do not waive it.

## Dispositions

- **Verify the claim, not the source or the count.** A senior human's word and a bot's word enter the same evidence states; two reviewers can share one blind spot.
- **Own the fix.** Decide the right fix up front rather than starting from the reviewer's fix and iterating into scope creep.
- **Verify proportionally to blast radius.** Style and comment changes can still break things — a rename touches callers, a deleted comment loses context.
