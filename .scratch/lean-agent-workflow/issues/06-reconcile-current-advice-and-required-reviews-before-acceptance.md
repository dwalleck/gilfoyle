# Reconcile current advice and required reviews before acceptance

Status: ready-for-agent
State: open
Owning project/module: OMP advisor runtime, primary-session reconciliation, and acceptance boundary
Feasibility: core (advisor reconciliation record and acceptance sit in advisor runtime; host hooks are internal, not loadable.)
User stories covered: 15, 16, 17

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Scheduling: Schedule issue 01 first; do not alter its shared configuration or measurement environment while it runs. This is not an extra blocking edge or a requirement for a positive pilot result.

Related slices: [07 — Reconcile late advice quietly and surface only material live issues](07-reconcile-late-advice-quietly-and-surface-only-material-live-issues.md)

## What to build

Reconcile relevant available advisory findings before acceptance without granting their severity labels veto authority. Preserve asynchronous advisor progress and require specifically mandated independent reviews to finish; catching up with every advisor's historical backlog is not an acceptance requirement.

Establish a durable reconciliation record associating finding identity and reviewed-state applicability with disposition, relevant new evidence, conversation epoch, and required-review completion. The late-advice issue extends this same record rather than creating a separate resolution system.

## Placement / boundaries

“OMP advisor delivery/completion carries enough reviewed-state context and reconciliation disposition to distinguish a current issue from a resolved repeat.”

Use the existing advisor/session and completion boundary. Primary reconciliation owns whether evidence establishes a live blocking failure; binding security and acceptance requirements remain authoritative. Keep this distinct from the catch-up setting experiment. Do not implement the post-completion quiet invocation path in this slice or add another approval ledger.

## Acceptance criteria

- [ ] Applicable, resolved, refuted, and insufficiently supported findings receive evidence-based dispositions tied to the reviewed state; severity alone neither establishes failure nor grants a waiver.
- [ ] The primary can progress while advisors work and reconcile relevant available findings in a bounded acceptance step without draining unrelated historical backlog.
- [ ] A specifically required independent review must complete before acceptance. Deadline/error/unresolved required proof cannot be converted into PASS or N/A merely to finish the bounded step.
- [ ] Reconciliation decisions persist with enough identity/applicability and conversation context for issue 07 to recognize repeats and genuinely new relevant evidence.
- [ ] Exercise the real advisor/session acceptance boundary with delayed review completion, irrelevant backlog, stale findings, and a confirmed binding failure. Do not substitute helper-return or prompt-wording assertions for acceptance behavior.
- [ ] Preserve user-stop/reset semantics and make no claim that this feature measures or eliminates historical fixed-duration gaps.

## Blocked by

None - can start immediately, subject to the pilot-first scheduling rule above.
