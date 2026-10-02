---
name: gilfoyle
description: Evidence-routed implementation and review-feedback verification. Use for nontrivial code changes or whenever review feedback proposes a code change.
---

# Gilfoyle

One portable orchestrator. Stage documents are disclosed only when their branch runs.

## Contract

Read the [workflow contract](references/CONTRACT.md) before loading a stage. It owns artifact paths, ownership, gate states, shared definitions, tracker taxonomy, and approval semantics.

Every link in this skill is relative to this skill root. Load only the selected stage document and references it explicitly requires for the active branch. A hand-off follows the current stage's completion or hand-off criterion; a scoped hand-off names unresolved dependencies and never declares their work complete.

## Select the first matching entry branch

- **Review feedback is present** — read and execute [assessing review feedback](references/assessing-review-feedback.md). This branch owns its decision log and any review-fix hand-off.
- **Planning or implementation work** — read and execute [change workflow](references/change-workflow.md). It selects Local, Structural, or Empirical from repository evidence and names the next stage, if any.

The selected entry branch, current stage, and — on change branches — recorded route are the complete execution path.

## Completion

- A change branch finishes only when `route.md`'s terminal criterion holds.
- A review branch finishes only when every finding has one evidence state and decision, accepted behavior-changing or technical-proof repairs have passed applicable checks and independent review, and no blocking defect or required evidence remains unresolved.

If the active stage's completion or hand-off criterion does not hold, resume that stage rather than reporting completion.
