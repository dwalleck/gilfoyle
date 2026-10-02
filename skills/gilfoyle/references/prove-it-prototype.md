# prove-it-prototype

Resolve a specific existing-system or external fact whose answer could change the design. First use applicable documentation, source, current tests, or valid previous observations; when those do not answer it, run the smallest safe real observation. This stage produces evidence, not a production implementation or design.

## When this runs

Read [workflow contract](references/CONTRACT.md) and resolve the canonical artifact directory. `route.md`'s Empirical T1 evidence names unresolved premises. A premise qualifies only when it has an observable answer, the design depends on that answer, and applicable evidence does not already establish it. Feature requirements and choices about code not built yet belong to spec/design, not probes.

If existing valid evidence answers all questions before probing, return it to [`change-workflow`](references/change-workflow.md) for route correction. On re-entry, preserve settled premises and IDs; investigate only missing or invalidated facts. Choosing or approving a library does not prove unspecified runtime behavior and does not automatically invalidate unrelated evidence.

## Data safety

Use the smallest representative safe input that answers the question; production scale is necessary only when the premise concerns scale. Production-shaped samples, anonymized exports, or test-owned state may suffice. Existing code/environment state must not be mutated or deleted by a probe. A captured snapshot requiring access or risk approval needs that approval recorded. If no safe source exists, request one rather than touching production state.

## Process

### 1. Name the question and dependent decision

Read route evidence and applicable spec outcomes. Assign stable premise IDs, preserving existing ones. State the smallest factual question and which design choice would change with its answer. Discard non-premises without generating a mandatory N/A checklist.

**Completion:** each investigated premise has a concrete question and consequential design dependency.

### 2. Consult existing evidence

Read relevant documentation, dependency source, current tests, previous observations, and prior-art issue evidence. Reuse a spec's related-issue references instead of repeating its search. If none exist, discover the repository tracker and make a bounded search for the premise; record relevant findings or no matches. Assess source/revision/environment applicability under Evidence validity. An approved dependency name or an unsupported design assertion is not evidence for unspecified behavior.

**Completion:** each question is answered by applicable sources or has a named remaining uncertainty requiring observation.

### 3. Observe only the remaining uncertainty

Prefer an existing command/test or direct system observation. Write `probe.<ext>` only when needed for the smallest question; keep it standalone and disposable, without feature abstractions. Record exact inputs, source state/environment, command, and observed output. Never promote the probe into production code.

A direct observation may itself answer the question; a mandatory second oracle is not needed for every probe. If interpreting or transforming output could conceal a named relevant failure, cross-check with an independent reference, hand-derived result, or system fact. Use the design's ordinary-evidence principles: custom comparison/fuzz/mutation machinery needs a named uncovered mechanism or repository requirement. Apply the contract's Verification complexity stop before repeated checker hardening; record its technical disposition in the existing Oracle section when no design exists.

**Completion:** the smallest necessary observation ran safely and answers its named question with traceable evidence, or the exact unresolved fact and dependent work remain explicit.

### 4. Investigate disagreement

When observations contradict the premise or reference, determine whether the model, probe, reference, or underlying system is wrong. Correct instruments against independent facts, not merely to make outputs agree. Never edit production code, approved behavior, or recorded output to manufacture success. Record new learning. For an underlying defect or intended future work, reuse or file a verified tracker issue under the contract.

A false assumption may be discharged as new learning: the answer is known and design must use it. An unanswered fact remains `PENDING — owner/step`; a required failed premise is `FAIL`. Both block only dependent decisions/implementation. A product failure still blocks any completion that requires that behavior; a tracker ID is not a waiver.

**Completion:** disagreements have causes and resolutions, or a precise unresolved dependency. Unrelated valid evidence stays intact.

### 5. Record evidence.md

Use these applicable sections, omitting unused instrument fields:

- **Premises** — stable ID, factual question, dependent decision, conclusion/status.
- **Sources and observations** — source/revision, inputs/environment, relevant commands/results, and prior evidence links with applicability reasons.
- **Data** — source and safety or required approval for actual observations.
- **Probe** — path and mechanism only when a new probe was necessary.
- **Oracle** — named gap and comparison evidence only when required, including any complexity-stop disposition.
- **Validated / learned** — what the evidence established, including a corrected assumption.
- **Related issues** — prior-art references and any defects/future-work IDs.

**Completion:** every conclusion names evidence for what it actually establishes; unresolved dependencies are explicit rather than hidden by a successful unrelated run.

## Hand-off / Output

Hand off `evidence.md` to [`falsifiable-design`](references/falsifiable-design.md), naming resolved conclusions and any remaining facts with their dependent work. Design and implementation may proceed on settled parts; work relying on an unresolved fact waits. The empirical stage is fully complete only when all required premises are answered with valid evidence, not because a probe file or comparison template exists. Final workflow completion cannot leave a required premise unresolved. No design document, production code, or permanent feature tests are written by this stage.
