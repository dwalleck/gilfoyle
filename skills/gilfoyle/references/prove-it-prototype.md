# prove-it-prototype

An empirical premise is a claim about existing-system or external behavior that the design depends on and that no applicable existing evidence verifies. A premise can be true and still be unverified; unverified premises are how features get built on fantasy. You discharge them: a probe computes the smallest observable answer against the real codebase, an independent oracle computes the same answer through a different failure mechanism, and the comparison lands in `evidence.md`.

Evidence before design: probe the real codebase, check an independent oracle, record the comparison. Validated prior understanding and new learning are both completion; an unverified premise is not.

## When this runs

Run when:

- `route.md` routes Empirical. Its T1 evidence names the unverified premise(s); the checklist starts there. Apply the router's evidence-currentness rule. If current applicable evidence already covers every premise, return to [`change-workflow`](references/change-workflow.md) with that evidence and request route correction instead of probing again.

Skip when:

- `route.md` routes Local or Structural with no empirical premise (`N/A — <reason>`).

This stage produces evidence only. It never writes a design doc ([`falsifiable-design`](references/falsifiable-design.md) owns claims about how to build), never writes production implementation, and never writes feature tests. Probing is not building: the probe is a throwaway instrument, not the seed of the feature.

## Contract

Read [workflow contract](references/CONTRACT.md) before producing or consuming any workflow artifact. It is the single source of truth for: gate states (`PASS` / `FAIL` / `N/A — <reason>`), artifact ownership (this stage owns `evidence.md` and `probe.*`; every other stage reads them), the independent-oracle definition (a different failure mechanism than the probe *and* the production implementation), artifact directory resolution, and the tracker taxonomy. This stage applies those definitions; it does not restate them.

## Completion

The stage is complete when every empirical premise is discharged and `evidence.md` records it. Discharged means one of:

- **Validated prior understanding** — probe and oracle agree; the premise holds. Recorded as `PASS`. No requirement to have been wrong: a clean confirmation is a completed premise.
- **New learning** — probe and oracle disagreed, and investigation reached agreement: the probe or oracle was wrong (fixed and re-run), the model of the system was wrong (updated, learning recorded), or the underlying system is broken (handled below). Recorded as `PASS` with the learning.
- A premise that cannot reach agreement is `FAIL`: record the cause; file or cite a tracker ticket when the failure reveals an underlying-system defect or intended future work (the contract's tracker taxonomy); a failed premise blocks hand-off. Known issues explain a `FAIL`; they do not waive it.

`evidence.md` is the only prose output of this stage. Never write a design doc; never restate the spec; never propose an implementation.

## Data

The probe runs against the real codebase on **safe production-shaped data or an approved snapshot**:

- **Production-shaped data** — same shape as production (schema, scale, distribution) without touching production state: anonymized or sampled exports, or data generated to production shape. The probe never writes, mutates, or deletes anything the codebase or environment owns.
- **Approved snapshot** — a captured data export the user approved for this run. Record who approved it and when in `evidence.md`.
- Neither available → ask the user to approve a snapshot or name a safe source. This is a risk-acceptance decision; record the outcome.

## Empirical-premise checklist

Enumerate premises before writing any probe. A premise is empirical when all of these hold:

- It is a claim about existing-system or external behavior — a resolver, parser, database, third-party API, library, or code written earlier (including your own code from six months ago).
- The design depends on it — a wrong answer changes the design.
- Current applicable evidence does not cover it (freshness is owned by the router's T1 test).
- It is a question with an observable answer.

Non-premises are recorded as `N/A — <reason>` in the checklist rather than probed: behavior already decided in `spec.md` (the spec's job), claims about the feature being built (nothing exists yet), and performance or scale targets (design and checkpoint territory).

## The artifact

Write `evidence.md` and `probe.<ext>` in the canonical directory, resolved per [workflow contract](references/CONTRACT.md): exactly one matching `.<change-slug>/` → use it; several plausibly match → name them and ask; none → run [`change-workflow`](references/change-workflow.md) first (routing precedes all downstream artifacts).

```markdown
# Evidence: <change-slug>

## Premise checklist
| ID | Candidate premise | Smallest question | Verdict |
|----|-------------------|-------------------|---------|
| P1 | <claim to classify> | <the smallest factual question, or why this is not an empirical premise> | PASS / FAIL / `N/A — <reason>` |

## Data
- Source: <production-shaped | approved snapshot>
- Shape: <schema / scale / distribution it matches>
- Safety: <how production state stays untouched> | Approval: <who approved, when>

## Probe
- File: `probe.<ext>`
- Mechanism: <how it computes the answer>
- Run: <exact command>

## Oracle
- Mechanism: <how it computes the answer; why this differs from the probe's failure mechanism>
- Run: <exact command>

## Comparisons
| ID | Probe output | Oracle output | Verdict |
|----|--------------|---------------|---------|

## Validated / learned
- P1: <validated prior understanding — probe and oracle agree on …> | <learning — believed X, observed Y, so …>

## Related issues
- Consulted: <IDs from upstream evidence or this run's search; "no prior art found" when none>
- Filed: <new ticket IDs — underlying-system defect or intended future work — with the premise each concerns>
```

## Process

### 1. Resolve the directory and read the route

Resolve the canonical directory per [workflow contract](references/CONTRACT.md). Read `route.md`: its Empirical-premise row seeds the checklist. Read `spec.md` when the route required one — its behaviors bound what the premises serve.

**Completion:** canonical directory named; route read; the premise list is seeded from the route's evidence; `spec.md` read or `N/A — <reason>` recorded.

### 2. Enumerate the premise checklist

Run the Empirical-premise checklist over the route's evidence, the request, and `spec.md`. Give every checklist entry a stable ID (P1, P2, …). Reduce each empirical premise to the smallest factual question — "what does this resolver do with an empty prefix?", not "how does parsing work?". Record non-premises as `N/A — <reason>`. If every entry is a non-premise, return to [`change-workflow`](references/change-workflow.md) with the classification evidence and request route correction.

**Completion:** every checklist entry has an ID; every empirical premise has a smallest question; every non-premise carries `N/A — <reason>`; at least one empirical premise remains or route correction has been requested.

### 3. Reuse related-issue evidence

When `spec.md` exists with a Related issues section, copy it into `evidence.md` — do not repeat the tracker search. When no upstream evidence exists (no `spec.md`, or the section is absent), run one bounded search: discover the tracker and search it once, keyword list derived from the premises (tracker discovery: see Search prior art in [`interrogated-spec`](references/interrogated-spec.md); the contract forbids hard-coding a tracker name). Read every match that touches the premises.

**Completion:** `evidence.md`'s Related issues records the upstream evidence or this run's search outcome; no upstream search was repeated.

### 4. Secure the data

Per the Data section: name the source, confirm it is production-shaped or user-approved, and record shape and safety in `evidence.md`. Ask the user when neither a safe source nor an approved snapshot exists.

**Completion:** the data source is named in `evidence.md` with shape and safety or approval.

### 5. Write the probe

Use one probe per premise, or one probe for several premises only when the same execution answers them without extra branches. The probe is standalone, uses the simplest language available, avoids abstractions from the feature to be built, and runs against the real codebase on the secured data. Setup or branching that obscures the factual question means the premise or probe must be split. Save it as `probe.<ext>` in the canonical directory. Never modify production code to make the probe run.

**Completion:** `probe.<ext>` exists at the canonical path, directly answers its named premise(s), and runs against the real codebase without touching production code.

### 6. Define the oracle

Write down, in one sentence, how the same answer is computed through a different failure mechanism than the probe and the production implementation. If the probe uses the AST resolver, the oracle uses `grep`; if the probe calls the HTTP API, the oracle hand-counts the database. The oracle may be tedious; it must be unaffected by the same bug.

Legitimate oracles: shell pipelines; existing CLI tools (`cargo tree`, `git log`, `jq`); a one-off script in a different approach or language; a hand-counted table; a human who knows the system.

Not legitimate — these share the probe's failure mechanism: "the test fixture says so" (the fixture is part of the system under test); "the design doc claims" (the doc is what you are trying to falsify); "another part of the same tool computes it the same way"; "it looks right" (sensible-looking output is how bugs survive).

**Completion:** the oracle mechanism is stated, and it differs from both the probe's mechanism and the production implementation's.

### 7. Run both and compare

Run the probe and independent oracle for every empirical premise, then compare their outputs item by item. Record both outputs and a `PASS` or `FAIL` verdict. Checklist entries marked `N/A — <reason>` are non-premises and are not probed.

**Completion:** every empirical premise has a comparison row with both outputs and a `PASS` or `FAIL` verdict; every non-premise retains its `N/A — <reason>`.

### 8. Investigate disagreement

Disagreement is information; it goes upstream, never downstream. The causes, in order of likelihood:

1. **The underlying system is broken.** Before filing anything, check `evidence.md`'s Related issues for an existing ticket describing the symptom — the drift may be a re-discovery of filed work. Link the existing ticket and note the residual gap; when no ticket exists, file one with the tracker's native command. Record the ticket ID. The premise cannot be validated on a broken substrate: either the feature rescopes around the broken part (a user decision) or the premise stays `FAIL`.
2. **The model of the system is wrong.** The system does something unpredicted. Update the model and record the learning.
3. **The probe is wrong.** Fix it and re-run.
4. **The oracle is wrong.** Fix it and re-run. Last resort: the oracle's job is independence — an oracle "fixed" to match the probe is no oracle.

Never edit production code, the spec, or recorded outputs to obtain agreement.

**Completion:** every disagreement has a recorded cause and resolution; every `FAIL` has its cause, with a ticket ID when it reveals an underlying-system defect or intended future work; every learning is recorded.

### 9. Record validated / learned notes

For each `PASS` premise, record in `Validated / learned` either "validated prior understanding" (probe and oracle agree; name the output items they agree on) or the learning (what was believed, what was observed, what changed). Both are completion; there is no requirement to have been wrong, and no requirement to invent a sharper question.

**Completion:** every `PASS` premise has exactly one validated or learned entry; non-premise `N/A` rows require none.

## Hand-off gate

No hand-off while any line below fails. Before handing off, confirm:

- [ ] `evidence.md` exists at the resolved canonical path.
- [ ] Every checklist ID has a verdict: `PASS`, `FAIL`, or `N/A — <reason>`; no entry is unrecorded.
- [ ] Every empirical premise is `PASS`; every `N/A` entry is classified as a non-premise; no `FAIL` remains.
- [ ] `probe.*` artifacts exist for every empirical premise, directly answer their named premise(s), and run against the real codebase.
- [ ] Each empirical premise's oracle mechanism is stated and differs from the probe's mechanism and the production implementation's.
- [ ] Every `PASS` premise has a comparison row with both outputs.
- [ ] Every observed `FAIL` has a recorded cause and a tracker ID when it revealed an underlying-system defect or intended future work; no active `FAIL` reaches hand-off.
- [ ] Data source is recorded (production-shaped or approved snapshot).
- [ ] Related issues records the upstream evidence or this run's search; no upstream search was repeated.
- [ ] No design doc was written; no production code changed; no feature tests added.

Then hand off to [`falsifiable-design`](references/falsifiable-design.md) with the `evidence.md` path. The hand-off message names the artifact path and the receiving stage.

## Void conditions

Each of these voids the run until fixed. The recovery is the same action every time: fix the voided item, then re-run the comparison.

- Probe setup or branching obscures the premise being answered — split the premise or probe until the execution has one legible factual purpose.
- The oracle shares the probe's failure mechanism — "the probe matches the oracle, but they're computing the same thing" is not agreement; find a different oracle.
- The oracle is skipped — "I'll check that the output looks sensible" is not a check; sensible-looking output is how bugs survive review.
- The disagreement is small — "I'll proceed and come back" carries the information downstream instead of upstream; investigate it now.
- "There's no oracle available" — a premise with no independent ground truth is not falsifiable; find a way or split the question.
- Production code, the spec, or recorded outputs were edited to obtain agreement.
- A design doc was written, or the probe was promoted into production code.

## Probing is not exploration

Exploration is "let me poke at the system to see how it works" — it produces vibes. Probing is "let me build the smallest possible version of the premise's answer and check it against ground truth" — it produces evidence. Vibes do not gate downstream stages; evidence does. If the probe and oracle agree and nothing about the premise changed, that is a completed premise: validated prior understanding, recorded.
