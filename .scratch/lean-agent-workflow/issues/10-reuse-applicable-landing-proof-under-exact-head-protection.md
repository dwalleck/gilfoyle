# Reuse applicable landing proof under exact-head protection

Status: ready-for-agent
State: open
Owning project/module: Cyril managed landing policy consuming portable evidence validity
Feasibility: managed-skill (Cyril landing policy; not OMP.)
User stories covered: 23, 33

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Scheduling: Schedule issue 01 first; do not alter its shared configuration or measurement environment while it runs. This is not an extra blocking edge or a requirement for a positive pilot result.

Related slices: [11 — Publish durable evidence references under one scoped authorization](11-publish-durable-evidence-references-under-one-scoped-authorization.md); [12 — Consolidate stacked-merge guidance against verified protocol behavior](12-consolidate-stacked-merge-guidance-against-verified-protocol-behavior.md)

## What to build

Land a stack using applicable existing local/platform proof after a rebase while rerunning missing or invalidated proof and satisfying every required exact-head remote check. Determine effective branch protection, required contexts, and base/refresh strategy early enough that landing does not rediscover known policy.

This is an evidence-applicability decision, not permission to reuse old-head status checks because two Git trees match. Native/application proof remains distinct from generic tests, and changed source, inputs, dependencies, configuration, or environment can invalidate it.

## Placement / boundaries

“Cyril's managed landing policy consumes portable Gilfoyle evidence validity instead of imposing blanket local-CI replay after each rebase.”

Do not reimplement the shared validity rule or relax native proof requirements. Update the owning landing policy and its affected consumers; do not impose Cyril-specific behavior on unrelated repositories. Keep exact-head remote CI, branch protection, stack safety, and the named shipping scope authoritative.

## Acceptance criteria

- [ ] For a concrete stack transition, classify the applicable local/platform receipts against the delivered state and record concise applicability reasons with existing source/input/environment provenance.
- [ ] Retain a genuinely unaffected result, rerun an invalidated result, and obtain a missing required result. Do not substitute a generic green suite for required native/application evidence.
- [ ] Missing new-head required status checks block landing even when content matches an earlier head; unchanged local evidence is not an old-head CI waiver.
- [ ] Carry effective protection and refresh requirements into the landing plan, preserving lower-stack order and all relevant branch safeguards.
- [ ] Demonstrate the acceptance decision with mixed valid/invalid/missing receipts and stale-head CI. Any live publication must already have explicit named authorization.
- [ ] Record avoided local commands, classification work, and defects found. If nothing can validly be reused, report that rather than forcing an improvement or claiming a blanket speedup.

## Blocked by

None - can start immediately, subject to the pilot-first scheduling rule above.
