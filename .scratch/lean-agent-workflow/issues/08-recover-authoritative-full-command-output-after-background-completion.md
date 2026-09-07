# Recover authoritative full command output after background completion

Status: ready-for-agent
State: open
Owning project/module: OMP command execution, background completion, and artifact retrieval
Feasibility: plugin-conditional (tool_result hook can fix the pointer only if core already captures the authoritative log; otherwise core.)
User stories covered: 27, 28

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Scheduling: Schedule issue 01 first; do not alter its shared configuration or measurement environment while it runs. This is not an extra blocking edge or a requirement for a positive pilot result.

## What to build

Make the advertised full-output reference retrieve the authoritative retained command diagnostics for that exact execution, even when the inline result is truncated. Preserve the relationship among command execution, outcome, source/input/environment identity, and recoverable output across background completion.

The ResourceFS evidence establishes a persisted elision in an advertised full artifact and a surviving candidate diagnostic elsewhere. It does not establish that every original log was destroyed or that the candidate definitely belongs to the same run. Fix the recovery contract, not a special case for that artifact number.

## Placement / boundaries

“OMP command execution, background completion, and artifact retrieval preserve one authoritative log and associate its execution/outcome with the advertised recovery reference. Remove ‘full output’ pointers to truncated summaries.”

Capture before size-based presentation truncation. Reuse the existing command/artifact lifecycle rather than adding another log store. Distinguish summaries, complete logs, incomplete capture, and command outcomes. Security handling/redaction must be explicit; never expose credentials to satisfy full-output recovery.

## Acceptance criteria

- [ ] A real command emits enough safe output to force inline truncation and places a distinctive failure in the omitted region; the advertised reference retrieves that diagnostic after background completion.
- [ ] Two similar command executions have distinguishable output identity and outcomes; matching command text or neighboring artifact numbers cannot substitute one run for another.
- [ ] The full-output pointer resolves to the authoritative retained log, not a persisted truncated summary. Any summary is identified as such.
- [ ] Capture failure and unavailable output are explicit. A complete log from a cancelled command still records cancellation rather than success.
- [ ] Required stdout/stderr diagnostics and source/input/environment provenance remain available without leaking protected data. Consumers need no search through unrelated session files to recover the advertised output.
- [ ] Exercise command execution through retrieval at the highest existing harness seam; measure recovery attempts/diagnostic time without claiming a later PASS diagnosed the original historical failure.

## Blocked by

None - can start immediately, subject to the pilot-first scheduling rule above.
