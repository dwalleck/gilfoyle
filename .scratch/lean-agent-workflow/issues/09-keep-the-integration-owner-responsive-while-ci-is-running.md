# Keep the integration owner responsive while CI is running

Status: ready-for-agent
State: open
Owning project/module: Main orchestration and the OMP asynchronous CI observation/session boundary
Feasibility: plugin (custom async-observer tool plus orchestrator guidance (Gilfoyle); no core change.)
User stories covered: 29

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Scheduling: Schedule issue 01 first; do not alter its shared configuration or measurement environment while it runs. This is not an extra blocking edge or a requirement for a positive pilot result.

## What to build

Keep the integration owner available to resolve writer ownership questions while CI is running. Establish known shared fixture/helper seams before dispatch and route unexpected scope decisions to Main rather than leaving a writer to invent a duplicate implementation during a blocking watcher.

The ResourceFS transcript establishes a 17m01.6s synchronous watcher interval with pending writer decisions and subsequent redirection. It does not establish that the entire interval is recoverable. The feature is responsive coordination, not waived CI or a faster remote runner.

## Placement / boundaries

“Main's orchestration uses an asynchronous CI observer while writers need decisions; the harness exposes the necessary nonblocking observation/delivery boundary. Replace synchronous coordinator waits, not required CI checks.”

Prefer existing asynchronous facilities. Add only a missing supported observation path if necessary; do not introduce a second service, repetitive short polling, or a source worktree just to watch a run. Associate observations with the expected run/head and preserve session stop/reset rules.

## Acceptance criteria

- [ ] With a CI observation deliberately pending, a writer raises an ownership question and Main resolves it before the observed run completes.
- [ ] The same observer delivers a failure or terminal success without losing the result or requiring repeated foreground polling.
- [ ] Redundant observations of the same required run are coalesced; a superseded run/head event cannot satisfy current acceptance or trigger repeated publication actions.
- [ ] Main coordination does not bypass required exact-head CI, independently required reviews, writer ownership, or scoped shipping authorization.
- [ ] Exercise the coordinator/session boundary with pending observation, writer decision, failure/terminal delivery, and a stale-head event. Preserve user-stop/reset behavior rather than autonomously reviving stopped work.
- [ ] Record decision latency, duplicate observations, and corrective handoffs. Distinguish measured coordinator blocking from inferred end-to-end savings.

## Blocked by

None - can start immediately, subject to the pilot-first scheduling rule above.
