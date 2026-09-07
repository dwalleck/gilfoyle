# Publish durable evidence references under one scoped authorization

Status: ready-for-agent
State: closed
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

- [x] A repair/publication cycle maintains one authoritative claim-to-source/input/environment-to-result record; plan, review, commit, and publication summaries reference it instead of independently rewriting its changing contents. (CONTRACT.md `Evidence record` definition; checkpointed-build caller-list single-homed.)
- [x] Required evidence and tracker references survive the chosen rebase/restack operation and remain accessible to the intended audience. Do not publish private transcript paths or credentials as if they were shared evidence. (checkpointed-build §8; landing skill post-rebase check; demonstrated — see [ac5-demonstration](../ac5-demonstration.md).)
- [x] One explicit authorization names the stack and tracker records. Routine steps within unchanged approved conditions do not repeatedly ask for the same permission. (CONTRACT.md `Scoped shipping authorization`; 0 re-asks in the authorized demonstration run.)
- [x] Changed scope, target, behavior, or risk requires renewed authorization; wrong-head status and unmet required acceptance prevent publication. Unrelated tracker records and parent issues remain unchanged. (Out-of-scope run: 1 targeted renewal request, 03-gamma withheld; exact-head SHA pinned in lease and merge request.)
- [x] Demonstrate a bounded authorized publication scenario and an out-of-scope rejection using a safe test target or suitable high-level harness. Existing configuration/permission tests alone do not prove this behavior. (Local git fixture + logging `gh` shim; three subagent runs including pre-change baseline; see [ac5-demonstration](../ac5-demonstration.md).)
- [x] Retain the existing bounded-repair policy, evidence validity, conditional N/A fields, initial design approval, and 4,000-line partition rule. Measure independent narrative edits, confirmation count, and correction addenda without treating all documentation as waste. (Policy anchors verified present; measurements recorded in the demonstration note.)

## Blocked by

None - can start immediately, subject to the pilot-first scheduling rule above.

## Comments

**2026-09-07 — completed.** Wording changes and demonstration evidence: [`ac5-demonstration.md`](../ac5-demonstration.md).

Outcome: **one owning evidence record and one scoped shipping authorization are now the single sources.** `CONTRACT.md` defines the `Evidence record` (summaries reference it, never copy it) and `Scoped shipping authorization` (routine steps consume it without re-asking; changed scope/target/behavior/risk renews; wrong-head or unmet acceptance blocks). `checkpointed-build.md` single-homes the caller list in the owning slice/repair record and attaches evidence/tracker references to the behavior-owning commit so they survive restack. The three managed publication skills consume the authorization and verify reference survival. Demonstrated on a local fixture with three subagent runs: the authorized run completed with zero re-asks and trailers verified on the rebased head; the out-of-scope run produced exactly one targeted renewal request and left the unnamed record untouched; the pre-change baseline performed no reference validation at all. Limitations recorded in the demonstration note: canned `gh` shim (no real CI/merge-async), fixture records not atomically inside each behavior commit, and no baseline re-ask contrast because both arms received an explicit written instruction. Merge-adapter consolidation (issue 12) and compact progress presentation (issue 13) were left to their owning slices.
