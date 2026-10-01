# assessing-review-feedback

A reviewer gave you findings. Maybe a person, maybe a bot, maybe several. Each finding is a hypothesis with two parts that fail independently:

1. **Bug claim** — there is a problem at location X with property Y.
2. **Fix claim** — change Z correctly addresses it.

The reviewer can be right about the bug and wrong about the fix, or right about the fix and wrong about the bug (stale context, misread code). Apply a finding only after it survives verification, and decide per finding — never per batch. Most findings are real and most proposed fixes reasonable: the default is to engage seriously with every finding, and let evidence decide.

## When this stage runs

- After review feedback arrives and before applying any review-driven change: human PR comments, bot output (code-reviewer, Sonar, Copilot), PR-review toolkit output, drive-by suggestions in chat.
- CI failures are **observed facts, not findings**. The red check is evidence; the reviewer's diagnosis of its cause and the proposed fix are hypotheses to verify like any other claim.

## Contract

Read [workflow contract](references/CONTRACT.md) before producing or consuming any workflow artifact. It is the single source of truth for the definitions this stage applies — gate states, slice, checkpoint ownership, Evidence validity, Approval semantics, tracker taxonomy, artifact ownership, and the canonical `.<change-slug>/` directory. Point to it; never restate it.

## Process

### 1. Inventory the findings

- Enumerate every review comment into rows with stable IDs (`F1`, `F2`, …). One row per finding; the same comment repeated by several reviewers is one finding with several sources.
- For each finding, restate the bug claim and the fix claim in your own words. A comment with no fix claim is noted as such — the evaluation is then yours alone.
- Record each finding's **landing impact** in its row: once the evidence state is decided, the `note` opens with `blocking` or `non-blocking` — whether an unfixed instance must be fixed before this lands. Every row has one: a refuted claim and a permanent non-goal are `non-blocking` because nothing is left to fix, never because something was deferred. Deferral travels with the decision's tracker suffix, never with this value. The round's own verified judgment sets it, never the reviewer's severity label; naming the `blocking` rows first orders repair and verification so the branch stays landable throughout.
- **Completion:** every comment in the review appears in exactly one row, and each row states the claims it makes and its landing impact; the `blocking` rows are named first, and repair and verification order follow them.

### 2. Verify — assign exactly one evidence state

Check the claims against the code and record exactly one evidence state per finding:

- **Verified** — a reproduction or direct check demonstrated the claim. Name the reproduction (a test, command, query, or code reading with the reasoning that decided it).
- **Refuted** — a reproduction or direct check ran and did not exhibit the claimed behavior. Name the reproduction.
- **Unverified** — no reproduction or check was run yet; the claim is undecided. Name what is missing. **Unverified is not Refuted**: refuted is a negative result, unverified is no result. An unverified claim never authorizes a behavior-changing `Accept` or `Modify` — either gather the missing evidence (the state then moves to `Verified` or `Refuted`) or `Reject` with the rationale explicitly recording the claim as unverified.
- **Not-applicable** — the finding makes no factual claim to verify: pure preference, naming taste, process suggestion. The decision then rests on evaluation (step 3), not on verification.

CI failures: the failing check itself is observed fact; verify the diagnosis and the fix with the same reproductions — run the failing test or inspect the log — before accepting either.

**Checker scope:** a hypothetical evasion or untested-path note is not automatically a blocking product defect. For these findings, cite the declared **Verification obligation** in the row's evidence and require a demonstrated product defect or obligation violation for `blocking`; missing required coverage/evidence is such a violation. A demonstrated limitation outside that scope is `Verified` and `non-blocking`, not `Refuted`; an untested hypothesis remains `Unverified`. Prefer narrowing an overstated checker claim or simplifying the checker under **Approval semantics** to extending it for arbitrary future forms. This cannot narrow an existing product, security, or acceptance obligation by implication.

**Completion:** every finding has exactly one evidence state; `Verified` and `Refuted` rows name the reproduction that decided them; `Unverified` rows name what is missing.

### 3. Evaluate the proposed fix

A real bug does not make the proposed fix right. For each `Accept` or `Modify` candidate, judge root cause versus symptom, boundary effects, repository conventions, proportional size, and simpler alternatives. Record divergence from the proposed fix. Repeated oracle/checker repairs apply the contract's **Verification complexity stop** before further hardening.

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

- **Active Gilfoyle workflow** — detected by `route.md` and `plan.md` both present in the canonical `.<change-slug>/` directory: group accepted behavior-changing or technical-proof findings by atomic root-cause repair and prepare the compact record below in the existing decision surface. Read the covering design claims and owning slices, not the whole design or plan.
  - **Approved-contract repair:** when the implementation repair is covered by approved claims and preserves approved decisions, enter [`checkpointed-build`](references/checkpointed-build.md)'s bounded repair path directly, whether the owning slice is committed or not. Inherit unchanged approved plan fields by reference; no new fourteen-field slice or formal replanning is required. Technical proof repairs follow the contract's Approval semantics and are recorded by their artifact owner.
  - **Changed contract or unresolved obligation:** apply the contract's Approval semantics to determine whether the repair requires a new decision. Return first to the owning stage — [`interrogated-spec`](references/interrogated-spec.md) for behavior or [`falsifiable-design`](references/falsifiable-design.md) for design — for that approval. Then [`budgeted-plan`](references/budgeted-plan.md) updates only the affected plan.
  - **Changed plan inputs:** scope, budget, or partition inputs changing without a design change go directly to [`budgeted-plan`](references/budgeted-plan.md), the sole plan owner, for an affected-only update.
- **Proof:** use Evidence validity to rerun invalidated checks and retain applicable conclusions; broaden when impact is uncertain. Select oracle/mutation applicability through [`falsifiable-design`](references/falsifiable-design.md)'s **Verification ladder**, preserving approved choices subject to its **Mutation sensitivity** requirement for review-driven coverage. For a behavior-changing repair, use an existing or repaired permanent fence, or its exact approved-risk exception. For every repaired observable, prove the applicable fence red against the actual pre-repair implementation and green after the fix; record both baseline revisions. Two green runs do not prove a repair. Tightened or relaxed acceptance predicates carry controls in both directions over the shapes now distinguished; changed shared-helper answers, messages, or error categories are proved at every affected call site. Checkpointed-build judges the gate and returns its result to this stage's repair record.
- **Retained reviewer probes:** when differential fuzz exposes a real bug class, retain its reusable generator and reference comparison plus the reproducer in the repository, or reference an existing equivalent repository harness. Record its deterministic default seed/case range, reference provenance, run command, and any widening controls in the repair's Commands and results. Prove that the default range detects at least one named representative defect and every mutation the retained fuzz is declared to cover. A non-fuzz probe needs only a reproducible repository case, not a new generator. Run the retained probe before the next review, or before closure if no new review is needed; reuse it instead of rebuilding the same probe in each reviewer clone.
- **Repair re-review:** production-behavior changes or changes to verification meaning, scope, or risk require an independent repair-diff pass. Give it the diff and decision log to judge what was applied. A round limited to accidental-tripwire mechanics or tests for coverage notes closes without another fresh-context round only when findings are resolved, required checks and **Mutation sensitivity** proof pass, behavior and enforcement obligations remain unchanged, and prior independent review remains valid under Evidence validity. Record the bounded-close reason, checks, and retained review reference/applicability. Missing or invalidated independent review requires a fresh pass; this shortcut never replaces initial isolated structural conformance. Docs/comments/formatting-only rounds record `N/A — reason` only while required proof remains valid.
- **Outside the workflow** (no `route.md` + `plan.md`): use the repository's normal reproduce → fix → focused-verification process.
- Non-behavioral fixes (docs, comments, formatting) skip the checkpoint only when they leave required proof applicable under Evidence validity; they still carry their row in the decision log. Technical proof repairs use the workflow gate.
- A fix that fails during implementation returns to step 3: decide again; never ship a fix you no longer believe in.

**Completion:** every behavior-changing `Accept`/`Modify` repair passed its applicable pre-commit gate — checkpointed-build's bounded repair or updated-slice checkpoint, or the repository's focused verification — with fresh or retained valid evidence. Final assembled quality, platform, and integration proof is mandatory after the last slice or repair; earlier integration conclusions survive only under Evidence validity.

### 6. Commit by atomic change

- Group commits by atomic change (the contract's slice definition), not by finding: one commit per atomic change. Several findings sharing one atomic change land in one commit; one finding spanning several atomic changes is named in all of them.
- An atomic change is a unit of repair, not of staging. Where repairs share a file such that no intermediate state is independently green, they land in one commit whose message lists each repair and its finding IDs — never produce a commit whose state was never checked, which is a false receipt for every finding it lists. The compact repair records stay one per atomic repair whatever the commit grouping.
- Each commit message names the atomic change and lists **every finding ID it addresses** (e.g. `fix(parser): reject empty prefixes — F1, F3`).

**Completion:** every `Accept`/`Modify` finding is addressed by commits whose messages list its ID, every commit lists the finding IDs it addresses, and every behavior-changing repair passed step 5 before commit.

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
- `note` — one-line rationale opening with `blocking` or `non-blocking`; permanent non-goals record the rationale justifying no tracker issue.

A finding whose claim is wrong is already `Refuted`. Record separately, under a **Review errors** heading beside the rows, the review's own errors in statements no row covers — a stale anchor, a wrong count or symbol, an impact that does not exist, or a fixture derived from the implementation rather than the provider. The next round reads this log: an unrecorded error is re-derived.

Record the round's repair re-review beside the rows: reviewer, scope, isolation, and result; or the explicit `N/A` with supporting evidence allowed by step 5's **Repair re-review**.

### Compact repair record

For an active workflow, maintain one record per atomic behavior-changing or technical-proof repair beside the finding rows in this same decision surface; create no separate repair artifact. Other non-behavioral fixes need only their finding rows. Prepare the repair's scope and expected results before applying it, then record actual results:

- **Finding IDs and ownership:** all resolved finding IDs; covering design Claim IDs and owning `plan.md` slice references. For a technical correction determined by an established obligation under the contract's Approval semantics, cite that obligation and use `N/A — technical correction governed by <reference>` for an inapplicable Claim ID. Inherit unchanged approved fields from those references.
- **Root-cause change and affected paths:** the atomic repair and exact production/proof paths it changes; required approval or affected plan update reference; the contract's complexity-stop and **Repeated product-repair stop** histories and dispositions when triggered.
- **Commands and results:** exact affected checks, expected and observed results or evidence links, including the repository artifacts, default configuration, and provenance required by **Retained reviewer probes**.
- **Fence mutation receipts:** record required repair discrimination and applicable injected-fault red/restored-green proof with baseline revisions, satisfying **Mutation sensitivity** and **Retained reviewer probes**. Retain still-valid evidence by reference; design-backed `N/A` must remain permitted by the Verification ladder. Unrun required proof leaves the round incomplete, never commit-ready.
- **Evidence disposition:** invalidated evidence and replacement results; retained evidence references with applicability reasons under the contract's Evidence validity. Conditional non-applicable proof carries explicit `N/A — reason` (fence/mutation risk uses the exact approved values).
- **Record reconciliation:** every figure, count, and head label re-anchored to the post-repair revision or marked superseded; every claim of performed verification names the receipt and the revision that performed it; and every `Accept`/`Modify` row's `fix` value and every Commands and results field names at least one artifact that exists in the post-repair revision — a path with symbol, a test name, or a line. A repair recorded from intent rather than from the applied diff is a false receipt and fails the hard gate.

[`checkpointed-build`](references/checkpointed-build.md) consumes this record and returns its checkpoint judgment to this stage for incorporation; this stage remains the decision surface's sole writer. Each finding's `fix` points to every repair addressing it; several findings may share one repair.

**Completion criterion:** every finding from step 1 appears in exactly one row; every row has exactly one `evidence-state` value, one `decision` value from the closed sets, and a landing impact; every `Verified`/`Refuted` row names its evidence; every tracked or deferred decision carries a verified issue ID; every permanent non-goal records its rationale; the log carries the review's own errors and the round's repair re-review; every active-workflow behavior-changing or technical-proof repair has its compact record, names an applied artifact for its fix, carries its fence mutation receipts, and references the verification gate it passed.

## Hard gate

No behavior-changing fix is committed until:

- [ ] Every finding has exactly one evidence state and exactly one decision.
- [ ] No behavior-changing `Accept`/`Modify` rests on an `Unverified` claim.
- [ ] Every `Verified`/`Refuted` row names its evidence; every `Unverified` row names what is missing.
- [ ] Every tracked or deferred decision names a verified tracker issue ID; every permanent non-goal records its rationale.
- [ ] The applicable pre-commit verification passed: checkpointed-build's bounded repair or updated-slice checkpoint, or the repository's focused verification. Required proof is supplied before completion even when a delegated worker was prohibited from running checks; missing proof is not a verified result.
- [ ] Final assembled quality, required smoke, platform, and integration proof is valid after the last workflow slice or repair. Before that milestone, name its owner and leave final verification pending; a completed intermediate repair does not declare the workflow complete.
- [ ] Commits are grouped by atomic change and list the finding IDs they address; no commit's state went unchecked.
- [ ] Every `Accept`/`Modify` row's `fix` value and every Commands and results field names an artifact that exists in the post-repair revision.
- [ ] Required repair discrimination and applicable mutation/restoration have valid proof; conditional entries carry the design's justified `N/A`. Retained reviewer probes satisfy step 5.
- [ ] The repair re-review entry satisfies step 5's pass or bounded-close criteria; checker-scope decisions satisfy step 2.

A failed gate never authorizes shipping: known issues explain a failure; they do not waive it.

## Dispositions

- **Verify the claim, not the source or the count.** A senior human's word and a bot's word enter the same evidence states; two reviewers can share one blind spot.
- **Own the fix.** Decide the right fix up front rather than starting from the reviewer's fix and iterating into scope creep.
- **Verify proportionally to blast radius.** Style and comment changes can still break things — a rename touches callers, a deleted comment loses context.
