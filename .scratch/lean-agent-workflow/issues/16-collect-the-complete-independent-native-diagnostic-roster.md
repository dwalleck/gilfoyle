# Collect the complete independent native diagnostic roster

Status: ready-for-agent
State: open
Owning project/module: Owning project native test runner and qualification recipe, initially the Tethys native diagnostic path
Feasibility: project (Tethys native runner/recipe; not OMP.)
User stories covered: 14, 31

Source: [Lean workflow specification](../../../docs/specs/lean-agent-workflow.md). Vocabulary: [workflow glossary](../../../CONTEXT.md). Boundaries: [execution/integration ownership](../../../docs/adr/0001-execution-and-integration-ownership.md) and [advisor authority/completion](../../../docs/adr/0002-advisor-authority-and-completion.md).

Scheduling: Schedule issue 01 first; do not alter its shared configuration or measurement environment while it runs. This is not an extra blocking edge or a requirement for a positive pilot result.

Related slices: [15 — Run affected compatibility fences before broad repair qualification](15-run-affected-compatibility-fences-before-broad-repair-qualification.md)

## What to build

Collect the complete relevant independent native diagnostic roster after an initial failure, while respecting safety and prerequisite dependencies. Use focused checks during repair and retain the required assembled native acceptance once the source stabilizes.

The Tethys audit reports that fail-fast execution initially left seven remaining cases unexecuted, while later complete diagnostics improved the fault inventory. Inspect and reuse that later capability where it already exists; the deliverable is a reliable, documented diagnostic path, not gratuitous changes to an already-correct flag.

## Placement / boundaries

“The owning native test runner/qualification recipe executes the relevant independent diagnostic roster and reports unexecuted dependent cases explicitly.”

Do not introduce a global always-fail-fast or always-run-everything rule. Prerequisite failures still stop dependent work; safe independent diagnostic cases continue. Keep this in the project runner/recipe rather than another universal harness framework, and preserve the final platform acceptance owner.

## Acceptance criteria

- [ ] Exercise a failing native case followed by another independent failure and a passing case; the resulting report exposes the complete relevant independent roster.
- [ ] A case whose prerequisite is unmet is explicitly unverified rather than blindly executed or represented as accepted. Unsafe continuation is prevented.
- [ ] The recorded diagnostic output is complete and tied to the exercised state. Use a trustworthy existing capture path without making the general logging repair a prerequisite.
- [ ] After focused repair and restoration, required assembled/native acceptance still runs or consumes genuinely applicable proof. Local native-enabled tests do not masquerade as execution on another operating system.
- [ ] Preserve distinctions among feature behavior, operator invocation success, and recovered cleanup postconditions; one does not retroactively relabel another.
- [ ] Measure fault-discovery cycles and diagnostic runtime separately. Do not classify all native faults or intentional mutation reds as avoidable workflow waste.

## Blocked by

None - can start immediately, subject to the pilot-first scheduling rule above.
