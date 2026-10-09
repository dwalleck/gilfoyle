# Gilfoyle workflow contract

Shared definitions and artifact ownership for the Gilfoyle workflow. The [orchestrator](SKILL.md) and every stage read this file before producing or consuming workflow artifacts. This file is the single source of truth for everything it names: change a definition here, never in a stage copy.

Verification is mandatory; bespoke oracles are conditional. Prefer established test frameworks, compiler/dependency checks, and observable consumer behavior. **Do not construct a second implementation solely to prove the first.** Bespoke verification needs a named gap these mechanisms cannot cover; its scope is that gap, not arbitrary future implementations. Choose evidence through [`falsifiable-design`](references/falsifiable-design.md)'s **Verification ladder**; required repository gates and consumer smoke runs remain mandatory.

## Artifact ownership

All artifacts for one change live directly in the canonical directory `.<change-slug>/`.

| Artifact | Owning stage | Contents |
|---|---|---|
| `route.md` | [`change-workflow`](references/change-workflow.md) | Selected route, criterion-by-criterion evidence, required artifacts, `N/A` rationale for skipped artifacts |
| `spec.md` | [`interrogated-spec`](references/interrogated-spec.md) | Observable behavior and verbatim requester approval |
| `evidence.md`, `probe.*` when needed | [`prove-it-prototype`](references/prove-it-prototype.md) | Specific unresolved premises, sources or observations, and validated/learned notes. Never a design doc |
| `design.md` | [`falsifiable-design`](references/falsifiable-design.md) | Outcomes, placement, claims, verification choices, conditional oracles/mutations, regression coverage, approval |
| `plan.md` | [`budgeted-plan`](references/budgeted-plan.md) | Independently-green atomic slices, delivery increments and supplied feature budget when applicable |
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
- Omit inapplicable conditional fields. Record an applicability reason when it explains a disputed or previously required check. Omission never hides an existing required obligation: unavailable, deferred, failed, or stale proof stays explicit and blocks its dependent completion.
- Gates consume applicable obligations, not the presence of template fields. Record a check once and reference its result wherever it supplies evidence.

## Evidence validity

Reuse a `PASS` only when its linked command/result identifies the checked source state, inputs, and relevant environment, and its assumptions still hold. Record the prior result link and a short applicability reason in the current gate; reference existing logs rather than copying them. Missing provenance or uncertain impact requires verification broad enough to establish the conclusion.

Revalidate conclusions affected by a changed production path, fence, fixture, oracle, dependency, configuration, or environment. Scope follows dependencies and observable behavior, not just edited filenames. An unrelated edit alone does not invalidate evidence. Apply this rule after repairs, merges/rebases, and integration as well as between slices.

| Evidence | Conclusion to preserve |
|---|---|
| Regression, implementation/oracle comparison, or budget check | The checked implementation still satisfies the behavior or bound on the relevant inputs and environment. |
| Mutation and restoration, when required by the declared verification | The fence detects the intended defect and passes with correct code restored. New or changed fences, or changed mutation applicability, require renewed red/restored-green proof for the applicable mutations. A mutation's RED stays valid while its mutated line and the assertions that turned it red are unchanged; new tests beside them and repairs elsewhere leave it valid. Cite the earlier run with an applicability line; rerun only mutations whose line or fence changed, never as a final pass. |
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
- **Feature budget** — an approximate feature-level budget supplied by the requester or repository, distinguishing production from tests/proof. There is no universal line target. Soft overruns follow **Size stop**; explicit hard caps and independently enforced repository limits remain hard.
- **Branch discovery** — use the repository's default/upstream branch; never hard-code `origin/main`.
- **Receipt** — the record a stage produces for its own obligation, stating what it checked, against which revision, and with what result: a gate item's list, a repair record's block, or a run's result reference. A receipt is evidence for the checks it names and no others; it is not the artifact it proves.
- **Evidence record** — the single owning record linking a claim to its checked source state, inputs, environment, and result. Plan, review, commit, and publication summaries reference it; none keeps its own editable copy of the record's changing contents.

## Verification complexity stop

After **two substantial repairs to the same oracle or checker**, or when proof machinery dominates the change's implementation/review work, pause further hardening and return to `falsifiable-design` for the affected verification decision. Before a design exists, record that scoped decision in `evidence.md`'s Oracle section. Substantial means adding or reworking parsing, state models, or verdict machinery, not correcting a command or path. Count across slices and review rounds; a new round does not reset the history. Only implementation dependent on an unresolved premise waits; unrelated settled work and valid evidence remain usable.

First consider established behavioral tests, real consumer execution, compiler/dependency checks, and reviewed fixtures. Retire or replace redundant bespoke machinery when those establish the required outcomes and coverage. Record the disposition and supporting evidence once in the owning record. Continue hardening only for a named remaining product-coverage gap; detecting more hypothetical mutations alone is not such a gap. Technical verification simplification is not automatically risk acceptance or architecture change. Real product failures, loss of unique required coverage, removing behavior, or removing an independently mandated repository check still require resolution under **Approval semantics** and block completion while unresolved.

## Repeated product-repair stop

After **two review rounds with verified product defects in the same claim or mechanism**, pause further local repairs for that claim or mechanism and return to `falsifiable-design` to compare a class-wide correction or simpler model against another local patch. Link the prior defects and repairs in the existing repair history; count across slices and rounds. Unrelated qualification failures, hypothetical checker evasion, and tests-only notes do not satisfy this trigger.

Record the selected disposition in the affected design decision and apply **Approval semantics** to changed decisions. A local correction may remain the justified choice; this checkpoint neither forces a redesign or new approval for unchanged decisions nor halts unrelated work. Required proof and unresolved failures still block completion.

## Size stop

Use a requester/repository-supplied approximate feature budget when one exists; distinguish production code from tests and proof. Do not manufacture a workflow threshold, per-module projection, or churn margin.

A **soft overrun** needs a concrete explanation of the responsibility driving growth and why a simpler approach is unsuitable, recorded once in the existing `plan.md` (or `route.md` for Local work). Work may proceed with unchanged scope and architecture; no requester round-trip is required solely for that overrun.

An **explicit requester hard cap or independently enforced repository limit** requires its owner's approval before exceeding or changing it. Record scope/path, observed or projected size, counting convention, owner, and the approved disposition in the owning route/design/plan record. Offer retaining with an authorized limit change, a cohesive reshape, an independently mergeable partition, or a scope decision as appropriate. A hard existing gate cannot be relabeled soft for convenience.

Preserve readable code, useful comments, normal formatting, and cohesive ownership. Compression and pass-through splitting to fit a count are not dispositions. Architecture or scope changes still follow **Approval semantics**, regardless of size.

## Tracker taxonomy

- **Permanent non-goal** — record the rationale in the artifact (design negative space, spec out-of-scope). No tracker issue.
- **Intended future work** — cite a verified tracker ID. Discover the repository's tracker and use its native command; never hard-code `rivets`. Verify the ID exists and its content covers the deferred work before citing; file one when no covering issue exists.
- **A verified tracker ID defers work; it authorizes nothing.** Changed behavior, a relaxed required obligation, or accepted risk needs the approval named in **Approval semantics**. Technical retirement of redundant verification follows that section's coverage-preserving rule, not risk acceptance by default.

## Approval semantics

- User decisions are required only for specification, scope, architecture, or explicit risk acceptance.
- **Delegated approval** — a requester may delegate routine sign-offs: spec and design approval, and recommended decisions an approved claim or obligation already constrains. Record each as `DG` with the delegation quoted, never as the requester's own words. Delegation stops short of **reserved decisions**: changing an explicit requester hard cap or independently enforced repository limit under **Size stop**; **reference fidelity**; any `N/A — approved risk`; an interrogated-spec refusal trigger, including a request that bundles separate features; and raising a requester-set attempt or review cap. A delegation that names one of these in its own words covers that one only. Repository-owned authorization must also come from its authorized owner.
- Agents diagnose and repair implementation and tool failures when the approved contract already determines the answer. The artifact owner may correct commands, paths, fixtures, or mutation mechanisms, and retire or replace redundant bespoke verification, without renewed approval when required behavior, coverage, architecture, and accepted risk remain unchanged. Cite the governing claim or repository obligation and replacement evidence; revalidate affected results under Evidence validity. A different instrument proving the same outcome is not a changed oracle meaning.
- Changes to approved behavior, responsibility ownership, interfaces, architecture, required comparison meaning, or accepted risk return to the owning specification/design stage for approval. Loss of unique required coverage or an independently mandated repository check is not a technical retirement. A repair whose correct outcome is not determined by an approved claim or established obligation also returns there; missing incidental detail alone is not a new design decision.
- Apply **Size stop** according to the threshold's actual authority: a soft feature-budget explanation goes to the plan owner; hard-cap changes require owner approval. Unchanged scope and architecture do not need renewed approval for workflow-generated estimates.
- Each artifact's owner records approval in the artifact: `spec.md` carries the requester's verbatim sign-off; `design.md` carries user approval. Re-interrogation or a changed approved decision re-records approval; a technical correction preserves the existing approval and records why it still applies.
- **Scoped shipping authorization** — publication runs under one explicit user approval naming the stack and the tracker records to close or update. Routine steps within its unchanged approved conditions proceed without re-asking. Changed scope, target, approved behavior, or risk requires renewed authorization; wrong-head status or unmet required acceptance blocks publication.
