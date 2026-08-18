# Gilfoyle workflow contract

Shared definitions and artifact ownership for the Gilfoyle workflow. The [orchestrator](SKILL.md) and every stage read this file before producing or consuming workflow artifacts. This file is the single source of truth for everything it names: change a definition here, never in a stage copy.

## Artifact ownership

All artifacts for one change live directly in the canonical directory `.<change-slug>/`.

| Artifact | Owning stage | Contents |
|---|---|---|
| `route.md` | [`change-workflow`](references/change-workflow.md) | Selected route, criterion-by-criterion evidence, required artifacts, `N/A` rationale for skipped artifacts |
| `spec.md` | [`interrogated-spec`](references/interrogated-spec.md) | Observable behavior and verbatim requester approval |
| `evidence.md`, `probe.*` | [`prove-it-prototype`](references/prove-it-prototype.md) | Empirical premises, independent oracle, comparisons, validated/learned notes. Never a design doc |
| `design.md` | [`falsifiable-design`](references/falsifiable-design.md) | Placement, claims, falsifiers, independent oracles, named mutations, regression fences, approval |
| `plan.md` | [`budgeted-plan`](references/budgeted-plan.md) | PR increments and independently-green atomic slices |
| `review-decisions.md` | [`assessing-review-feedback`](references/assessing-review-feedback.md) | Per-finding accept/modify/reject decisions; used when no PR-native decision surface is specified |

Single-owner rules:

- One owning stage per artifact. The owner writes; every other stage reads.
- [`change-workflow`](references/change-workflow.md) exclusively owns routes.
- [`checkpointed-build`](references/checkpointed-build.md) exclusively owns slice completion and the gate that judges it. Run the checkpoint once per completed slice, never per unit-test cycle.
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

## Definitions

- **Independent oracle** — computes the same answer through a different failure mechanism than the production implementation and, when a probe exists, than the probe as well.
- **Slice** — the smallest atomic change that leaves the repository green and has an independent observable check. File, line, and time counts are decomposition signals, never hard limits.
- **Stage completion criterion** — the checkable end state under the stage's `Completion`, `Hand-off gate`, or `Output` heading.
- **Review-size gate** — projected or actual cumulative changed lines, including a documented churn margin, `> 4,000` requires independently mergeable PR increments.
- **Branch discovery** — use the repository's default/upstream branch; never hard-code `origin/main`.

## Tracker taxonomy

- **Permanent non-goal** — record the rationale in the artifact (design negative space, spec out-of-scope). No tracker issue.
- **Intended future work** — cite a verified tracker ID. Discover the repository's tracker and use its native command; never hard-code `rivets`. Verify the ID exists and its content covers the deferred work before citing; file one when no covering issue exists.

## Approval semantics

- User decisions are required only for specification, scope, architecture, or explicit risk acceptance.
- Agents diagnose and repair implementation and tool failures when the contract already determines the answer.
- Each artifact's owner records approval in the artifact: `spec.md` carries the requester's verbatim sign-off; `design.md` carries user approval. Re-interrogation or design revision re-records approval.
