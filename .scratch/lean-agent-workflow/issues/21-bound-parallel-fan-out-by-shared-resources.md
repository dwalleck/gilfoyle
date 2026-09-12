# Bound parallel fan-out by shared resources

Status: ready-for-agent
State: open
Owning project/module: OMP task-tool dispatch policy and controlled writer execution; repository format/codegen hooks
Feasibility: plugin (dispatch policy and hook behaviour; overlaps issues 02 and 05.)
User stories covered: 8, 9, 13, 29

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Evidence: a 50-finding review round on ResourceFS PR #14 ran 7 scouts + 5 writers + 6 reviewers + 4 full gate runs. Writers had to be barred from building; one gate run failed spuriously under three concurrent full suites (CPU contention against 3 s and 5 s test timeouts); and a post-edit hook running bare `rustfmt` (pre-2024 style) silently reverted import-block edits in three agents' files, each agent working around it differently.

Related slices: [02 — Share source reader workspaces only under enforced authority](02-share-source-reader-workspaces-only-under-enforced-authority.md); [05 — Return focused writer proof without build-state interference](05-return-focused-writer-proof-without-build-state-interference.md); [16 — Collect the complete independent native diagnostic roster](16-collect-the-complete-independent-native-diagnostic-roster.md).

## What to build

Fan-out is bounded by shared resources, not by parallelism.

- The build directory, the gate runner, and any format/codegen hook are **single-writer**. Read-only verifiers may run targeted probes; writing agents must not build, format, or run the repository gate — the orchestrator owns those runs.
- A post-edit hook that rewrites a file can silently revert an edit the tool reported as applied. After an edit under a hook, confirm the change landed (re-read the range or compare a hash) before building on it.
- Above roughly fifteen findings in one round, cluster verification one reader per file cluster rather than one reader per finding.

The portable skill already requires the *obligations* these controls serve (writer-local proof is not assembled proof; a false receipt fails the gate). This issue is the dispatch and hook behaviour that makes them achievable, so the rule lives with the runner, not in the skill text.

## Placement / boundaries

"portable proof/early-check guidance stays in Gilfoyle; native runner and gate-input changes belong with the owning project." Do not add per-slice fields or a universal preflight to the skill; do not weaken the validation ban by letting writers run full suites concurrently. Where a hook is repository policy, record the confirmation step with that repository rather than generalising a formatter policy.

## Acceptance criteria

- [ ] Concurrent full gate runs are impossible by construction, or the runner serialises them; a spurious failure under contention is not reported as a product defect.
- [ ] A writer's edit that a post-edit hook reverts is detected and reported instead of built on; the confirmation step is exercised against the real hook.
- [ ] Verification clustering above the threshold is demonstrated on a round of that size, with findings still individually dispositioned.
- [ ] No safety property is relaxed: writer isolation, the validation ban, and the orchestrator's ownership of assembled proof remain.
- [ ] The portable skill gains no new mandatory per-slice field as a result of this work.

## Blocked by

None - can start immediately, with issue 05's writer-proof boundary as the nearest neighbour.
