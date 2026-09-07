# Share source-reader workspaces only under enforced authority

Status: ready-for-agent
State: open
Owning project/module: OMP resolved execution authority and dispatch; consuming repository hook and managed isolation recipe
Feasibility: plugin (hook/extension: isolation selection plus read-only tool-call blocking; full mutation-vector enforcement is the hard part.)
User stories covered: 5, 6, 7, 8

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Scheduling: Schedule issue 01 first; do not alter its shared configuration or measurement environment while it runs. This is not an extra blocking edge or a requirement for a positive pilot result.

## What to build

Allow a source-only exploratory reader to share the live source tree only when its effective execution authority is enforced as read-only. Keep mutable and unknown-authority agents isolated. Migrate the conflicting hook/recipe guidance to consume the enforced decision instead of granting exemptions by agent name.

This slice includes the complete dispatch-to-observation behavior: the selected agent definition, overrides and custom tools, the actual restrictions, workspace choice, and the returned finding. An exploratory finding about a changing tree is not acceptance evidence for an unidentified state.

## Placement / boundaries

“OMP resolved execution authority governs isolation; the project hook and managed recipe consume that decision. Replace blanket reader isolation and name-based exceptions.”

Do not relax a hook before the runtime authority boundary exists. Preserve writer isolation and restrictions on mutation outside assigned working state; a working copy is not a security sandbox. Update only relevant hook/recipe consumers, not an unrelated collection of project policies. Use existing dispatch lifecycle fixtures where possible.

## Acceptance criteria

- [ ] A restricted source reader observes the intended live tree without creating an unnecessary mutable working copy; its actual permitted operations cannot mutate source directly or indirectly.
- [ ] A writer-capable override named scout/reviewer, an unknown agent, and a custom-tool capability that cannot be proven read-only do not gain sharing authority from their names.
- [ ] Resolution and enforcement agree at dispatch and execution: do not classify an earlier definition and execute a later or broader one.
- [ ] Writers retain separate mutable working state. The sharing optimization does not exempt source readers from applicable security restrictions.
- [ ] Exploratory results identify their changing-tree limitation; an acceptance review still applies to an identified source/input/environment state without mandating a writable workspace for every reviewer.
- [ ] Migrate the affected hook and managed recipe without leaving a competing name allowlist or blanket reader-copy rule. Demonstrate the high-level dispatch cases and record setup-time/resource observations without extrapolating from directory counts.

## Blocked by

None - can start immediately, subject to the pilot-first scheduling rule above.
