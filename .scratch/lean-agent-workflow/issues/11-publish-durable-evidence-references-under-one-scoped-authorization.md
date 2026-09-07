# Publish durable evidence references under one scoped authorization

Status: ready-for-agent
State: open
Owning project/module: Portable Gilfoyle checkpoint wording and managed publication workflow
Feasibility: skill (portable Gilfoyle checkpoint wording plus managed publication skills; not OMP core.)
User stories covered: 24, 25, 33

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Scheduling: Schedule issue 01 first; do not alter its shared configuration or measurement environment while it runs. This is not an extra blocking edge or a requirement for a positive pilot result.

Related slices: [10 — Reuse applicable landing proof under exact-head protection](10-reuse-applicable-landing-proof-under-exact-head-protection.md); [12 — Consolidate stacked-merge guidance against verified protocol behavior](12-consolidate-stacked-merge-guidance-against-verified-protocol-behavior.md); [13 — Show compact progress without losing current ownership or blockers](13-show-compact-progress-without-losing-current-ownership-or-blockers.md)

## What to build

Publish concise references to one durable owning evidence record instead of maintaining competing claim/proof narratives. Carry the required evidence/tracker references through the actual restacking operation, and execute routine publication steps under one explicit authorization for a named stack and named tracker records.

Remove the residual checkpoint caller-list duplication at its owning instruction. Preserve evidence applicability, historical-versus-current result distinctions, and audience access. A single shipping authorization is not permission to change scope, target, risk, or unrelated tracker records.

## Placement / boundaries

“Portable checkpoint wording and managed publication skills reference the owning proof record, consume scoped shipping authorization, and converge on one verified merge adapter.”

This slice owns proof references, authorization consumption, and record survival. The merge-adapter consolidation belongs to issue 12, and compact task-state presentation belongs to issue 13; neither is a prerequisite for improving this publication path with an already-supported safe operation. Required evidence/tracker references normally travel with the behavior-owning commit, not only an integration merge commit. Do not require every raw log to be committed or invent a second proof/authentication ledger.

## Acceptance criteria

- [ ] A repair/publication cycle maintains one authoritative claim-to-source/input/environment-to-result record; plan, review, commit, and publication summaries reference it instead of independently rewriting its changing contents.
- [ ] Required evidence and tracker references survive the chosen rebase/restack operation and remain accessible to the intended audience. Do not publish private transcript paths or credentials as if they were shared evidence.
- [ ] One explicit authorization names the stack and tracker records. Routine steps within unchanged approved conditions do not repeatedly ask for the same permission.
- [ ] Changed scope, target, behavior, or risk requires renewed authorization; wrong-head status and unmet required acceptance prevent publication. Unrelated tracker records and parent issues remain unchanged.
- [ ] Demonstrate a bounded authorized publication scenario and an out-of-scope rejection using a safe test target or suitable high-level harness. Existing configuration/permission tests alone do not prove this behavior.
- [ ] Retain the existing bounded-repair policy, evidence validity, conditional N/A fields, initial design approval, and 4,000-line partition rule. Measure independent narrative edits, confirmation count, and correction addenda without treating all documentation as waste.

## Blocked by

None - can start immediately, subject to the pilot-first scheduling rule above.
