# Gilfoyle workflow contract

Shared definitions and artifact ownership for the Gilfoyle workflow. The [orchestrator](SKILL.md) and every stage read this file before producing or consuming workflow artifacts. This file is the single source of truth for everything it names: change a definition here, never in a stage copy.

## Artifact ownership

All artifacts for one change live directly in the canonical directory `.<change-slug>/`.

| Artifact | Owning stage | Contents |
|---|---|---|
| `route.md` | [`change-workflow`](references/change-workflow.md) | Selected route, criterion-by-criterion evidence, required artifacts, `N/A` rationale for skipped artifacts |
| `spec.md` | [`interrogated-spec`](references/interrogated-spec.md) | Observable behavior and verbatim requester approval |
| `evidence.md`, `probe.*` | [`prove-it-prototype`](references/prove-it-prototype.md) | Empirical premises, independent oracle, comparisons, validated/learned notes. Never a design doc |
| `design.md` | [`falsifiable-design`](references/falsifiable-design.md) | Placement, approved module ledger when applicable, claims, falsifiers, independent oracles, named mutations, regression fences, approval |
| `plan.md` | [`budgeted-plan`](references/budgeted-plan.md) | PR increments, independently-green atomic slices, and module growth ledger when applicable |
| `review-decisions.md` | [`assessing-review-feedback`](references/assessing-review-feedback.md) | Per-finding decisions and bounded repair records; used when no PR-native decision surface is specified |

Single-owner rules:

- One owning stage per artifact. The owner writes; every other stage reads.
- [`change-workflow`](references/change-workflow.md) exclusively owns routes.
- [`checkpointed-build`](references/checkpointed-build.md) exclusively judges slice and bounded-repair verification. Run one checkpoint per completed atomic change, never per unit-test cycle; the artifact owner incorporates its result into the owning slice or repair record.
- [`prove-it-prototype`](references/prove-it-prototype.md) never writes a design doc. [`change-workflow`](references/change-workflow.md) never runs downstream gates.

## Artifact directory resolution

A downstream stage loaded directly consumes an existing artifact directory without rerunning routing:

- Exactly one `.<change-slug>/` matches the change under work: use it as-is.
- More than one plausibly matches: name the competing directories and ask. Never guess.
- None exists: run [`change-workflow`](references/change-workflow.md) first. Routing precedes all downstream artifacts.

## Gate states

- A gate is `PASS`, `FAIL`, or `N/A — reason`.
- `PENDING` marks a falsifier awaiting discharge by a named owner and step; it is a lifecycle status, not a gate state.
- A failed mandatory gate never authorizes shipping. Known issues explain failures; they do not waive them.
- All conditional fields are present as `N/A — reason`, so completeness is mechanically checkable.
- No gate references an absent field, stage, artifact, skip list, estimate, or mutation.

## Evidence validity

Reuse a `PASS` only when its linked command/result identifies the checked source state, inputs, and relevant environment, and its assumptions still hold. Record the prior result link and a short applicability reason in the current gate; reference existing logs rather than copying them. Missing provenance or uncertain impact requires verification broad enough to establish the conclusion.

Revalidate conclusions affected by a changed production path, fence, fixture, oracle, dependency, configuration, or environment. Scope follows dependencies and observable behavior, not just edited filenames. An unrelated edit alone does not invalidate evidence. Apply this rule after repairs, merges/rebases, and integration as well as between slices.

| Evidence | Conclusion to preserve |
|---|---|
| Regression, implementation/oracle comparison, or budget check | The checked implementation still satisfies the behavior or bound on the relevant inputs and environment. |
| Mutation and restoration | The fence detects the intended defect and passes with correct code restored. New or changed fences, or changed mutation applicability, require renewed red/restored-green proof. |
| Empirical probe | The external/system premise still holds; repeat the probe only when its verified premise or supporting evidence is invalidated. |
| Independent review | The reviewed behavior, ownership, interfaces, dependencies, and assumptions still cover the delivered change. |

An invalidated result remains historical evidence, not a current `PASS`. Name the responsible verifier and required check; completion waits for its result. Use `N/A — reason` only for an inapplicable obligation, never for unavailable, deferred, failed, or stale proof. A retained `PASS` is still `PASS`, with its evidence link and applicability reason.

**Completion:** every applicable obligation has fresh or retained valid evidence for the state being judged; every invalidated obligation has been reverified; no unresolved `FAIL` remains.

## Definitions

- **Independent oracle** — computes the same answer through a different failure mechanism than the production implementation and, when a probe exists, than the probe as well.
- **Slice** — the smallest atomic change that leaves the repository green and has an independent observable check. File, line, and time counts are decomposition signals, never hard limits.
- **Stage completion criterion** — the checkable end state under the stage's `Completion`, `Hand-off gate`, or `Output` heading.
- **Review-size gate** — projected or actual cumulative changed lines, including a documented churn margin, `> 4,000` requires independently mergeable PR increments.
- **Branch discovery** — use the repository's default/upstream branch; never hard-code `origin/main`.
- **Evidence record** — the single owning record linking a claim to its checked source state, inputs, environment, and result. Plan, review, commit, and publication summaries reference it; none keeps its own editable copy of the record's changing contents.

## Tracker taxonomy

- **Permanent non-goal** — record the rationale in the artifact (design negative space, spec out-of-scope). No tracker issue.
- **Intended future work** — cite a verified tracker ID. Discover the repository's tracker and use its native command; never hard-code `rivets`. Verify the ID exists and its content covers the deferred work before citing; file one when no covering issue exists.

## Approval semantics

- User decisions are required only for specification, scope, architecture, or explicit risk acceptance.
- Agents diagnose and repair implementation and tool failures when the approved contract already determines the answer. The artifact owner records technical corrections to verification commands, paths, fixtures, or mutation mechanisms without renewed approval when approved behavior, oracle meaning, architecture, and accepted risk remain unchanged; revalidate affected evidence under Evidence validity. An established repository quality requirement or an existing approved obligation can determine a technical correction without a separate design claim for that correction; cite that requirement or obligation.
- Changes to approved behavior, responsibility ownership, interfaces, architecture, oracle meaning, or accepted risk return to the owning specification/design stage for approval. A repair whose correct outcome is not determined by an approved claim or established obligation also returns there; missing incidental detail alone is not a new design decision.
- Each artifact's owner records approval in the artifact: `spec.md` carries the requester's verbatim sign-off; `design.md` carries user approval. Re-interrogation or a changed approved decision re-records approval; a technical correction preserves the existing approval and records why it still applies.
- **Scoped shipping authorization** — publication runs under one explicit user approval naming the stack and the tracker records to close or update. Routine steps within its unchanged approved conditions proceed without re-asking. Changed scope, target, approved behavior, or risk requires renewed authorization; wrong-head status or unmet required acceptance blocks publication.
