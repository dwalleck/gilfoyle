# Retire owned temporary workspaces without losing retained work

Status: ready-for-agent
State: open
Owning project/module: Creating orchestration layer for owned temporary/manual worktrees, consuming the retained handoff from issue 03
Feasibility: plugin-conditional (retirement via worktree CLI/extension, but owner/purpose/retirement tracking depends on issue 03 (core).)
User stories covered: 36, 37, 38

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Scheduling: Schedule issue 01 first; do not alter its shared configuration or measurement environment while it runs. This is not an extra blocking edge or a requirement for a positive pilot result.

## What to build

Retire workflow-created temporary workspaces, including manual and nested worktrees, when their purpose is fulfilled and required output remains usable independently. Associate each with an owner, purpose, and retirement condition using existing task/session state.

Native task teardown and manual worktree retirement are different lifecycles. The user reported more than twenty ResourceFS workspaces at a historical session end and later cleanup; that does not identify the survivors or prove a native cleanup defect. Implement prospective owned retirement, not a destructive sweep of those historical directories.

## Placement / boundaries

“The creating orchestration layer owns workflow-created temporary workspaces, including manual/nested worktrees; native runner teardown remains native-owned. Reuse existing task/session ownership records and the appropriate workspace lifecycle operations.”

Consume issue 03's retained-output/baseline/target contract before removing temporary state. Distinguish the primary checkout, native sandbox, manual worktree, and retained evidence. Do not introduce a second workspace ledger, a fixed count/age threshold, or force removal of uncertain/unrelated work. Use the appropriate lifecycle operation so worktree metadata remains coherent.

## Acceptance criteria

- [ ] A workflow-created temporary manual worktree has an accountable owner, purpose, and retirement condition visible through existing task/session state.
- [ ] Retirement does not proceed while a writer or required review/recovery use is active, while required changes/output are unretained, or while ownership is unresolved.
- [ ] After purpose completion and safe retention through issue 03, actual manual-worktree removal succeeds and the retained output can still be inspected and integrated against its intended baseline/target.
- [ ] Exercise a real temporary-repository lifecycle with active-writer refusal, unretained-output refusal, successful retirement, unknown ownership, and failed removal. Native task-finally tests alone do not prove this path.
- [ ] Preserve the primary checkout and unrelated/unknown workspaces. Failed removal reports a retained workspace and actionable reason, not successful cleanup; Git metadata remains correct.
- [ ] Report remaining owned workspaces by their concrete purpose and resource use. Do not reconstruct historical survivors from current contents or delete them under this issue without separate ownership and authorization.

## Blocked by

- [03 — Integrate retained worker results through an explicit owner handoff](03-integrate-retained-worker-results-through-an-explicit-owner-handoff.md)
