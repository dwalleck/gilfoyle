# change-workflow

Route first. Every downstream stage consumes the route; none re-derives it. Read [workflow contract](references/CONTRACT.md) before writing anything — it owns artifact names, directory resolution, gate states, and the definitions used here.

A change takes exactly one of three routes. The route decides which evidence the change must carry; the gates that check that evidence live in the owning stages and are never restated here. This routing stage depends on nothing downstream: routing reads only the change request, the repository, and [workflow contract](references/CONTRACT.md).

## The three routes

- **Local** — behavior explicit; no unverified external or system premise; no public API, schema, or module-boundary change; no cross-module placement change; no production-scale risk. Normal repository fix/TDD plus focused behavioral verification; `route.md` is the only artifact.
- **Empirical** — a design premise depends on existing-system or external behavior not covered by current applicable evidence. Sequence: interrogate unresolved behavior → probe/oracle evidence → design approval → plan → checkpointed build.
- **Structural** — every non-Local change without an unverified empirical premise: public API/schema/boundary changes, cross-module placement, or production-scale risk. Sequence: interrogate unresolved behavior → design approval → plan → checkpointed build.

## Route selection

Answer all four tests against the change request and the repository, and record every verdict with its evidence in `route.md`. Then apply precedence: Empirical > Structural > Local; the first test in precedence order that fires selects the route.

1. **T1 Empirical premise** — Does any design premise depend on existing-system or external behavior not covered by current applicable evidence? Applicable evidence is current repository evidence or an existing `evidence.md` that still covers the premise. Evidence is stale when the thing it verified has changed since it was recorded — code path, dependency version, external API, or data shape — so the premise no longer describes current behavior. Unverified or stale → **Empirical**. The evidence row names the premise and the evidence (or why it is stale).
2. **T2 Structural boundary** — Does the change alter a public API, schema, or module boundary, or require cross-module placement decisions? YES → **Structural**.
3. **T3 Production-scale risk** — Does the change carry production-scale risk: latency, throughput, memory, concurrency, or data volume? YES → **Structural**; record why — budget and stress-fixture machinery is required, and Local has none.
4. **T4 Explicit behavior** — Is the requested behavior fully explicit: observable given/when/then with no unresolved decisions? NO → **Structural**; record why — interrogation is required, and Local has none. When the verdict is yes, the evidence row records the complete observable behavior contract as given/when/then triples — the behavior source for [`falsifiable-design`](references/falsifiable-design.md) when `spec.md` is `N/A`.

T1=no, T2=no, T3=no, T4=yes → **Local**.

A test you cannot answer: record the unknown test and the reason in `route.md`, and take the higher-evidence route — Empirical > Structural > Local. T1 unknown → Empirical; any of T2–T4 unknown → Structural.

## Direct stage entry

Routing is a one-time decision recorded in `route.md`. A downstream stage loaded directly without routing consumes the existing artifact directory per [workflow contract](references/CONTRACT.md): unique match → use it; several matches → name them and ask; none → route first. An existing route for an unchanged request is adopted unless a downstream stage returns evidence that a recorded route-test verdict is wrong or stale; that correction reruns the affected test and precedence, then rewrites `route.md`. A materially changed request reruns all four tests.

## Process

1. **Read the contract.** [workflow contract](references/CONTRACT.md) owns everything this stage references.
2. **Name the change and locate the directory.** Derive `<change-slug>` from the change. Inspect `.<change-slug>/`: an existing `route.md` for the same change follows the adoption-or-correction rule above; a `route.md` for a different change in the same directory, or multiple plausible directories → stop and name the competing directories for the user.
3. **Run the four tests.** Gather evidence for each: the request text, the code paths and interfaces involved, and any commands run to verify behavior. Where a test needs an answer you cannot get, record it unknown.
4. **Select the route.** Apply the mapping in Route selection.
5. **Write `route.md`.** Fill the template below completely: every conditional field as `N/A — reason`.
6. **Hand off.** Local → implement with the repository's normal fix/TDD process, run the focused verification named in `route.md`, then return to this stage and append the command, date, and `PASS` or `FAIL` result under `Terminal criterion`; this stage owns that record. Structural or Empirical with unresolved behavior (T4 `no` or unknown) → read [`interrogated-spec`](references/interrogated-spec.md). Empirical with explicit behavior → read [`prove-it-prototype`](references/prove-it-prototype.md). Structural with explicit behavior → read [`falsifiable-design`](references/falsifiable-design.md). A receiving stage owns the next hand-off.

## Completion criterion

`route.md` exists with: all four tests answered (verdict + evidence), the selected route matching the verdict vector, the complete given/when/then behavior contract recorded in T4 evidence when the verdict is yes (the behavior source when `spec.md` is `N/A`), required artifacts listed with owners, and every skipped artifact carrying `N/A — reason`. The route's terminal criterion below is checked after routing: this stage records the Local result; downstream stages satisfy Structural and Empirical criteria.

## Terminal criteria per route

- **Local** — the focused behavioral verification named in `route.md` records `PASS`.
- **Structural** — every downstream artifact satisfies its owning stage's completion criterion, ending with no `FAIL` in [`checkpointed-build`](references/checkpointed-build.md)'s recorded gate.
- **Empirical** — [`prove-it-prototype`](references/prove-it-prototype.md) records `PASS` for every empirical premise, every later artifact satisfies its owning stage's completion criterion, and [`checkpointed-build`](references/checkpointed-build.md) records no `FAIL`.

## The `route.md` template

```markdown
# Route: <slug>

Change: <one-line description>
Date: <YYYY-MM-DD>

## Route tests

| # | Test | Evidence | Verdict |
|---|------|----------|---------|
| 1 | Empirical premise | <premise and the evidence covering it — current repository evidence or existing evidence.md — or why that evidence is stale> | no |
| 2 | Structural boundary | <APIs/schemas/modules touched, placement decisions needed> | no |
| 3 | Production-scale risk | <scale dimensions and the load they would see> | no |
| 4 | Explicit behavior | <given/when/then triples of the complete observable behavior contract when verdict is yes (behavior source, since spec.md is N/A); unresolved decisions when verdict is no> | yes |

Unknown tests: <none | T#: <reason the answer was unavailable>>

## Selected route

<Local | Structural | Empirical> — <one-line why>

## Required artifacts

| Artifact | Owner | Status |
|---|---|---|
| route.md | change-workflow | this file |
| spec.md | interrogated-spec | <required — unresolved behavior to interrogate (T4 verdict) | N/A — behavior fully explicit (T4 verdict)> |
| evidence.md, probe.* | prove-it-prototype | <required — Empirical route (T1 verdict) | N/A — no unverified premise (T1 verdict)> |
| design.md | falsifiable-design | <required | N/A — Local route: no design gate> |
| plan.md | budgeted-plan | <required | N/A — Local route: no plan gate> |

Oracle checkpoint in `checkpointed-build`: <required — Structural or Empirical route | N/A — Local route: checkpointed-build does not run>

## Downstream sequence

<interrogated-spec → prove-it-prototype → falsifiable-design → budgeted-plan → checkpointed-build | the applicable subsequence | none — implement with normal repository fix/TDD>

## Terminal criterion

<Local — the focused behavioral verification named here records PASS: <test or smoke run>; after the hand-off append `Result: <YYYY-MM-DD> | <command> | <PASS or FAIL>` | Structural/Empirical — every downstream artifact satisfies its owning stage's completion criterion, ending with no FAIL in checkpointed-build's recorded gate>
```
