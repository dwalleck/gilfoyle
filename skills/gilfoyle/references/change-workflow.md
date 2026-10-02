# change-workflow

Route first. Read [workflow contract](references/CONTRACT.md) for artifact ownership, evidence validity, approval, and directory resolution. Routing reads the request, repository facts, and contract; downstream stages own their gates.

## The three routes

- **Local** — explicit behavior within existing responsibility, no unresolved consequential external premise, no public interface/schema/ownership change, and no material production-scale risk. Use normal repository fix/TDD, focused behavioral verification, real consumer execution, and applicable repository checks; `route.md` is the only workflow artifact.
- **Empirical** — a specific unresolved existing-system/external fact could change design. Resolve it from existing evidence or the smallest necessary observation, then design, plan, and checkpoint the change. Only work dependent on the fact waits; unrelated settled decisions/evidence remain usable.
- **Structural** — a non-Local change without an unresolved empirical premise: public interface/schema, ownership/dependency changes, new responsibility clusters, material scale risk, or unresolved product decisions. Interrogate material behavior when needed, then design, plan, and checkpoint.

## Route selection

Record all four tests with evidence and apply precedence Empirical > Structural > Local:

1. **T1 Empirical premise** — Is there a specific unresolved fact about existing-system/external behavior whose answer could change design? Documentation, source, current tests, and valid previous observations can answer it. Name the question and dependent choice, not a generic need to investigate. Selecting/approving a library alone does not establish unspecified runtime behavior, and does not trigger global requalification. A genuine unresolved fact → Empirical.
2. **T2 Structural module shape** — Does the change alter a public interface/schema, seam, dependency direction, or responsibility owner; change ownership through a module split/merge/deletion; introduce substantial new module ownership; or add a responsibility cluster to an orchestrator/facade? Yes → Structural. Record affected owners/interfaces and relevant protected parents. A large file or growth within an existing owner alone does not change the route. Inspect actual requester/repository limits; read [module shape](references/module-shape.md)'s Length review when a relevant limit exists. Soft feature budgets need no module projections or requester tripwire; hard existing gates retain their authority under Size stop.
3. **T3 Production-scale risk** — Is there a concrete material latency, throughput, memory, concurrency, or volume risk introduced by this change? Yes → Structural; name the affected consumer outcome/boundary or plausible failure. This does not impose a budget on every loop or a stress fixture on every slice.
4. **T4 Explicit behavior** — Are requested observable outcomes, compatibility, scope, important errors, safety, and accepted-risk decisions sufficiently resolved? No → Structural and interrogation. Yes → record the complete outcome contract or its authoritative source in this evidence row. Group equivalent cases; prose or a behavior table is sufficient, and implementation knobs/timers do not become acceptance merely because measurable.

T1=no, T2=no, T3=no, T4=yes → Local. Investigate repository-answerable unknowns rather than asking the requester. A consequential unresolved external fact selects Empirical; unknown product/structural/scale decisions select Structural. An unspecified implementation detail alone does not force interrogation or a probe.

## Direct stage entry

Adopt an existing route for the unchanged request. Correct only a verdict shown wrong/stale by new evidence, then reapply precedence; a materially changed request reruns the tests. Exactly one matching artifact directory is adopted under the contract. None → route first; multiple plausible directories → name them and ask rather than guessing.

## Process

### 1. Resolve the change

Read the contract, request, repository instructions, and existing route when any. Identify the canonical `.<change-slug>/` directory.

**Completion:** change and route ownership are unambiguous.

### 2. Gather evidence and select

Answer T1–T4 from the request and relevant repository facts. Preserve settled behavior and valid evidence. Apply precedence, naming any unresolved decision or factual dependency precisely.

**Completion:** all route tests have verdicts and evidence; the selected route matches them.

### 3. Write route.md

Record:

- change and date;
- T1–T4 verdicts/evidence, with grouped behavior or its source in T4;
- selected route and reason;
- required artifacts and owning stages;
- the applicable downstream sequence and terminal criterion;
- supplied feature budget or hard-limit disposition only when relevant.

Omit inapplicable artifact rows, or give a short skip reason where it explains an applicability decision; no repeated N/A template is required. Never omit an existing required obligation to make routing appear complete.

**Completion:** `route.md` carries sufficient behavior and premise/ownership evidence for downstream stages without requiring implementation acceptance or mandatory shape enumeration.

### 4. Hand off

Local → implement with normal repository fix/TDD, perform the named relevant checks and real consumer execution, and return results to this route owner. During implementation recheck changed T1–T4 facts; material new ownership/behavior/risk corrects the route rather than being hidden. Apply hard limits and any supplied soft budget under Size stop, not a workflow-generated threshold.

Structural/Empirical with unresolved product decisions → read [`interrogated-spec`](references/interrogated-spec.md). Empirical with explicit behavior → read [`prove-it-prototype`](references/prove-it-prototype.md). Structural with explicit behavior → read [`falsifiable-design`](references/falsifiable-design.md). Each receiving stage owns its next hand-off; a scoped premise hand-off names dependent work still blocked.

## Routing completion

`route.md` exists with evidence-backed verdicts, the matching route, sufficient T4 outcomes, required artifact ownership, and a clear next stage. Routing completion does not mean implementation is complete.

## Terminal criteria per route

- **Local** — requested behavior and caller migration are delivered; relevant behavioral, consumer, and repository checks pass; required independent review is satisfied; no blocking defect or required proof remains unresolved. Record delivered behavior, performed checks/results, and unresolved failures in `route.md`. Any actual hard-limit change has owner authorization, and a supplied soft-budget overrun has its explanation. No count-fitting compression/pass-through split is used.
- **Structural** — required artifacts satisfy their owning criteria and checkpointed-build's final assembled behavior, consumer/platform/repository, and independent-review proof is valid, with no blocking defect or missing required check.
- **Empirical** — all required factual premises have valid answers, dependent implementation uses them, and Structural's final assembled criteria hold. An unneeded probe file or second oracle is not an acceptance requirement.
