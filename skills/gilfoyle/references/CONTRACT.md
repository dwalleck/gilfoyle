# Gilfoyle workflow contract

Shared definitions and artifact ownership for the Gilfoyle workflow. The [orchestrator](SKILL.md) and every stage read this file before producing or consuming workflow artifacts. This file is the single source of truth for everything it names: change a definition here, never in a stage copy.

Verification is mandatory; bespoke oracles are conditional. Prefer established test frameworks, compiler/dependency checks, and observable consumer behavior. **Do not construct a second implementation solely to prove the first.** Bespoke verification needs a named gap these mechanisms cannot cover; its scope is that gap, not arbitrary future implementations. Choose evidence through [`falsifiable-design`](references/falsifiable-design.md)'s **Verification ladder**; required repository gates and consumer smoke runs remain mandatory.

## Artifact ownership

All artifacts for one change live directly in the canonical directory `.<change-slug>/`.

| Artifact | Owning stage | Contents |
|---|---|---|
| `route.md` | [`change-workflow`](references/change-workflow.md) | Selected route, criterion-by-criterion evidence, required artifacts, `N/A` rationale for skipped artifacts |
| `spec.md` | [`interrogated-spec`](references/interrogated-spec.md) | Observable behavior and verbatim requester approval |
| `evidence.md`, `probe.*` | [`prove-it-prototype`](references/prove-it-prototype.md) | Empirical premises, independent oracle, comparisons, validated/learned notes. Never a design doc |
| `design.md` | [`falsifiable-design`](references/falsifiable-design.md) | Placement, approved module ledger when applicable, claims, verification choices, falsifiers, conditional oracles/mutations, regression fences, approval |
| `plan.md` | [`budgeted-plan`](references/budgeted-plan.md) | PR increments, independently-green atomic slices, and module growth ledger when applicable |
| `review-decisions.md` | [`assessing-review-feedback`](references/assessing-review-feedback.md) | Per-finding decisions and bounded repair records; used when no PR-native decision surface is specified |

Single-owner rules:

- One owning stage per artifact. The owner writes; every other stage reads.
- [`change-workflow`](references/change-workflow.md) exclusively owns routes.
- [`checkpointed-build`](references/checkpointed-build.md) exclusively judges slice and bounded-repair verification. Run one checkpoint per completed atomic change, never per unit-test cycle; the artifact owner incorporates its result into the owning slice or repair record.
- [`prove-it-prototype`](references/prove-it-prototype.md) never writes a design doc. [`change-workflow`](references/change-workflow.md) never runs downstream gates.
- **Amend in place.** When a decision or result changes, rewrite the owning section to the current state; version control holds what it replaced, so active sections read as the current contract. A requester's words are quoted once, in the artifact that owns the decision; other artifacts cite that section. Evidence figures and hashes live in the evidence record of the revision that produced them, replaced when superseded.

## Artifact directory resolution

A downstream stage loaded directly consumes an existing artifact directory without rerunning routing:

- Exactly one `.<change-slug>/` matches the change under work: use it as-is.
- More than one plausibly matches: name the competing directories and ask. Never guess.
- None exists: run [`change-workflow`](references/change-workflow.md) first. Routing precedes all downstream artifacts.

## Gate states

- A gate is `PASS`, `FAIL`, or `N/A — reason`; `N/A — approved risk: <reason>` marks an obligation the requester explicitly accepted, and each acceptance is listed in its owning artifact's approval record.
- `PENDING` marks a falsifier awaiting discharge by a named owner and step; it is a lifecycle status, not a gate state.
- A failed mandatory gate never authorizes shipping. Known issues explain failures; they do not waive them.
- All conditional fields are present as `N/A — reason` or `N/A — approved risk: <reason>`, so completeness is mechanically checkable.
- No gate references an absent field, stage, artifact, skip list, estimate, or mutation.

## Evidence validity

Reuse a `PASS` only when its linked command/result identifies the checked source state, inputs, and relevant environment, and its assumptions still hold. Record the prior result link and a short applicability reason in the current gate; reference existing logs rather than copying them. Missing provenance or uncertain impact requires verification broad enough to establish the conclusion.

Revalidate conclusions affected by a changed production path, fence, fixture, oracle, dependency, configuration, or environment. Scope follows dependencies and observable behavior, not just edited filenames. An unrelated edit alone does not invalidate evidence. Apply this rule after repairs, merges/rebases, and integration as well as between slices.

| Evidence | Conclusion to preserve |
|---|---|
| Regression, implementation/oracle comparison, or budget check | The checked implementation still satisfies the behavior or bound on the relevant inputs and environment. |
| Mutation and restoration, when required by the declared verification | The fence detects the intended defect and passes with correct code restored. New or changed fences, or changed mutation applicability, require renewed red/restored-green proof for the applicable mutations. |
| Empirical probe | The external/system premise still holds; repeat the probe only when its verified premise or supporting evidence is invalidated. |
| Independent review | The reviewed behavior, ownership, interfaces, dependencies, and assumptions still cover the delivered change. |

An invalidated result is no longer a current `PASS`; under **Amend in place** its gate shows the required check, not the old result. Name the responsible verifier and required check; completion waits for its result. Use `N/A — reason` only for an inapplicable obligation, never for unavailable, deferred, failed, or stale proof. A retained `PASS` is still `PASS`, with its evidence link and applicability reason.

Evidence for a run that can silently skip — an environment gate, an ignored test, an early return, a missing prerequisite — carries a receipt proving the assertion executed; a prose sentence is not evidence for a row that did not run. Every figure, count, and head label in a record is anchored to the revision that produced it.

**Completion:** every applicable obligation has fresh or retained valid evidence for the state being judged; every invalidated obligation has been reverified; no unresolved `FAIL` remains.

## Definitions

- **Independent oracle** — computes the same answer through a different failure mechanism than the production implementation and, when a probe exists, than the probe as well.
- **Verification obligation** — an approved claim or established repository requirement, with its observable outcome, covered inputs, and required evidence. The owning design row or repository policy declares it; a checker's capabilities do not define product requirements.
- **Slice** — the smallest atomic change that leaves the repository green and has an independent observable check. File, line, and time counts are decomposition signals, never hard limits.
- **Stage completion criterion** — the checkable end state under the stage's `Completion`, `Hand-off gate`, or `Output` heading. It does not hold while its artifact carries a template placeholder (a `<…>` field, a `<<…>>` marker, `<pending>`). Outstanding work is written as `PENDING` with its owner and step, and any summary that declares completion — a final status, a hand-off, a close message — names every `PENDING` item rather than reporting the whole as `PASS`.
- **Baseline failure** — a required check that fails identically on the untouched base revision, with a verified tracker ID. The first time a change meets one, the requester chooses: fix it in this change, or carry it as `N/A — approved risk: baseline failure <id>`. `plan.md` records that choice once, with the exact failing test IDs and the base-revision receipt; later gates cite the record and `FAIL` on any failure outside the recorded set. An intermittent failure with no path through the diff, shown by an isolated rerun, is filed on its second occurrence and carried the same way after the requester's choice.
- **Review-size gate** — projected or actual cumulative changed lines, including a documented churn margin, `> 4,000` triggers the **Size stop**.
- **Branch discovery** — use the repository's default/upstream branch; never hard-code `origin/main`.
- **Receipt** — the record a stage produces for its own obligation, stating what it checked, against which revision, and with what result: a gate item's list, a repair record's block, or a run's result reference. A receipt is evidence for the checks it names and no others; it is not the artifact it proves.
- **Evidence record** — the single owning record linking a claim to its checked source state, inputs, environment, and result. Plan, review, commit, and publication summaries reference it; none keeps its own editable copy of the record's changing contents.

## Verification complexity stop

After **two substantial repairs to the same oracle or checker**, or when proof machinery dominates the change's implementation/review work, pause further hardening and return to `falsifiable-design` for the affected verification decision. Before a design exists, record that scoped decision in `evidence.md`'s Oracle section; normal design entry still waits for verified premises. Substantial means adding or reworking parsing, state models, or verdict machinery, not correcting a command or path. Count across slices and review rounds; a new round does not reset the history.

The owning evidence, slice, or repair record links the repairs and remaining gap. In the affected design decision, compare a simpler product model and established checks with narrowing, replacing, or deleting the bespoke machinery before adding cases. Record the selected disposition and why it covers every still-required verification obligation; apply **Approval semantics** to any changed decision. A stop is a redesign checkpoint, not permission to skip proof: known product failures, missing required evidence, and unresolved `FAIL` states still block completion.

## Repeated product-repair stop

After **two review rounds with verified product defects in the same claim or mechanism**, pause further local repairs for that claim or mechanism and return to `falsifiable-design` to compare a class-wide correction or simpler model against another local patch. Link the prior defects and repairs in the existing repair history; count across slices and rounds. Unrelated qualification failures, hypothetical checker evasion, and tests-only notes do not satisfy this trigger.

Record the selected disposition in the affected design decision and apply **Approval semantics** to changed decisions. A local correction may remain the justified choice; this checkpoint neither forces a redesign or new approval for unchanged decisions nor halts unrelated work. Required proof and unresolved failures still block completion.

## Size stop

A size threshold is a question for the requester, not a target to refactor toward. It covers a module/file-length gate (repository-owned or inherited), a growth-ledger projection, and the review-size gate. When current or projected size reaches or exceeds one, or remaining headroom is smaller than planned growth plus its uncertainty margin, stop before any work whose purpose is fitting the number: splitting, extracting, partitioning, or changing a gate. Gather only the evidence, then present it to the requester:

- path or scope, observed/projected size, threshold, counting convention, and owner (repository gate, plan tripwire, or this contract);
- the feature or responsibility driving the growth;
- the options below, each with a one-line cost and your recommendation.

| Threshold | Options |
|---|---|
| Length | **Retain and raise** — the module stays as is; record the new threshold and rationale. **Reshape** — run [module shape](references/module-shape.md)'s **Design procedure** to select a split or redesign. **Defer** — accept the overrun for this change and file intended future work. |
| Review size | **Partition** — independently mergeable PR increments; name the proposed cut. **Single PR** — one increment over the gate; record the accepted size. **Cut scope** — move named slices to intended future work. |

The requester may choose another path. The owning artifact records the evidence and the requester's verbatim choice: `route.md` for length triggers found while routing or during Local work, `design.md` for those found later, `plan.md` for review size. Later stages adopt a recorded choice rather than asking again; that choice is a scope or risk decision under **Approval semantics**. Refactor, partition, or gate-change work begins only after it is recorded.

## Tracker taxonomy

- **Permanent non-goal** — record the rationale in the artifact (design negative space, spec out-of-scope). No tracker issue.
- **Intended future work** — cite a verified tracker ID. Discover the repository's tracker and use its native command; never hard-code `rivets`. Verify the ID exists and its content covers the deferred work before citing; file one when no covering issue exists.
- **A verified tracker ID defers work; it authorizes nothing.** A changed behavior, a relaxed obligation, a dropped guard or fence, or an accepted risk needs the approval named in **Approval semantics**; the tracker ID accompanies that authorization as the deferral reference, and never substitutes for it.

## Approval semantics

- User decisions are required only for specification, scope, architecture, or explicit risk acceptance.
- **Delegated approval** — a requester may delegate routine sign-offs: spec and design approval, and recommended decisions an approved claim or obligation already constrains. Record each as `DG` with the delegation quoted, never as the requester's own words. Delegation stops short of **reserved decisions**, which reach the requester as a question however broad the delegation: the **Size stop**; the **reference fidelity** decision; any `N/A — approved risk`; an interrogated-spec refusal trigger, including a request that bundles separate features; and raising a requester-set attempt or review cap. A delegation that names one of these in its own words covers that one only.
- Agents diagnose and repair implementation and tool failures when the approved contract already determines the answer. The artifact owner records technical corrections to verification commands, paths, fixtures, or mutation mechanisms without renewed approval when approved behavior, oracle meaning, architecture, and accepted risk remain unchanged; revalidate affected evidence under Evidence validity. An established repository quality requirement or an existing approved obligation can determine a technical correction without a separate design claim for that correction; cite that requirement or obligation.
- Changes to approved behavior, responsibility ownership, interfaces, architecture, oracle meaning, or accepted risk return to the owning specification/design stage for approval. A repair whose correct outcome is not determined by an approved claim or established obligation also returns there; missing incidental detail alone is not a new design decision.
- Approaching or exceeded size thresholds follow the **Size stop** before any refactor, partition, gate change, or plan-only budget update, including when placement is unchanged. This trigger takes precedence over plan-only repair routing.
- Each artifact's owner records approval in the artifact: `spec.md` carries the requester's verbatim sign-off; `design.md` carries user approval. Re-interrogation or a changed approved decision re-records approval; a technical correction preserves the existing approval and records why it still applies.
- **Scoped shipping authorization** — publication runs under one explicit user approval naming the stack and the tracker records to close or update. Routine steps within its unchanged approved conditions proceed without re-asking. Changed scope, target, approved behavior, or risk requires renewed authorization; wrong-head status or unmet required acceptance blocks publication.
