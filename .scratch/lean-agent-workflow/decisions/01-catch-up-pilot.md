# Catch-up pilot decision — `advisor.syncBacklog`

**Decision:** Provisional keep (remove catch-up waiting) within the measured scope — bounded, mechanical, short-turn tasks. Not a global authorization: the reconciliation tradeoff for non-trivial work was not exercised.

**Date:** 2026-09-07
**Issue:** [`01-measure-advisor-catch-up-waiting-in-a-bounded-pilot`](../issues/01-measure-advisor-catch-up-waiting-in-a-bounded-pilot.md)

---

## Result in one paragraph

Catch-up waiting imposes real, measured foreground overhead — two `waitForCatchup(30_000, 3)` waits of 8.4 s and 10.5 s on a five-turn task (≈120 % of its 16 s active time), 13.7 s on a six-turn task, and repeated 30 s timeouts in sustained sessions — and in every run the advisor delivered **zero material correction** ("nothing to flag" / deferential disclosure). Disabling the gate (`syncBacklog: "off"`) collapses inter-request gaps to 0.02–0.14 s with no acceptance regression, no human interruption, and no reopening. The gate's supposed benefit — in-time delivery of a material advisor finding that would otherwise reopen completed work — never materialized because the advisor produced no material finding in any condition.

## What was varied and held fixed

| Control | Value |
|---|---|
| Varied | `advisor.syncBacklog`: `"3"` (baseline) vs `"off"` (comparison), via `--config` overlay only |
| Held fixed | `advisor.enabled: true`; advisor model `kimi-code/k3:high`; primary `deepseek/deepseek-v4-pro:high`; thinking level, tools, LSP, skills, and repo contents |
| Environment | Fresh git repo per run under `/tmp/omp-pilot{,2}/{baseline,comparison|base,off}`, same prompt file, headless `omp -p --advisor --auto-approve` |
| Persistent config | Unchanged — `~/.omp/agent/config.yml` still reads `advisor.syncBacklog: "3"`. The decision is a recommendation; no setting was mutated. |

## Mechanism (from source, not inference)

`SessionAdvisors.onPrimaryTurnEnd` (`packages/coding-agent/src/session/session-advisors.ts`) calls `AdvisorRuntime.waitForCatchup(30_000, threshold)` per advisor after every primary turn. The primary parks until the advisor backlog falls below `threshold` or 30 s elapse. Release paths: caught-up (`backlog < threshold`), 30 s timeout, or immediate on failing/halted/quota/disposed. A failing advisor never gates the primary.

## Measurements

### Bounded task A — trivial (`calc` package + `unittest`, "10 tests pass")

| Condition | main requests | main active | inter-request gaps | advisor | acceptance |
|---|---|---|---|---|---|
| `syncBacklog: "3"` | 5 | 19.0 s | 0.13 + 0.04 + **8.38** + **10.46** = 19.0 s | 5 req / 51.0 s | 10/10 pass |
| `syncBacklog: "off"` | 4 | 16.1 s | 0.06 + 0.02 + 0.14 = 0.22 s | 4 req / 20.9 s | 10/10 pass |

The 8.38 s and 10.46 s gaps are gate waits, confirmed by timestamp: the advisor's turn-2 and turn-3 "nothing to flag" notes land at 31.408 s and 43.293 s — exactly the gate-release instants (next primary request at 31.43 s and 43.29 s). Recovered foreground time ≈ **18.8 s**.

### Bounded task B — planted latent defect (`median` upper-middle vs midpoint)

| Condition | main requests | main active | max gap | advisor | planted-defect outcome |
|---|---|---|---|---|---|
| `syncBacklog: "3"` | 6 | 60.5 s | **13.66 s** (gate) | 10 req / 77.6 s | advisor did not flag; deferred ("disclosed", "test not modify") |
| `syncBacklog: "off"` | 4 | 23.4 s | 0.12 s | 4 req / 25.7 s | advisor did not flag; primary self-noted the semantics |

The planted defect did not yield a material advisor finding in either condition — the reconciliation path (a late finding that would reopen completed work) was therefore **not exercised**, not measured as zero.

### Sustained session (not a matched pair)

This session (`syncBacklog: "3"`, 109 primary turns) shows **16 gaps of 30.03–30.08 s** — the 30 s timeout signature — totaling ≈ 480 s during active periods. The prior Cyril recap independently reported **133 gaps of 29–31 s (66.6 min)**. These are the timeout regime; the bounded tasks above show the early-release regime.

## Observability limits (reported unavailable, not zero)

There is **no per-gate telemetry** in the current build. Directly observed: gap durations and advisor-finding timestamps. Inferred (not recorded): gate entry/exit boundaries, backlog at entry (from turn count), and release reason (gap < 30 s ⇒ caught-up; ≈ 30 s ⇒ timeout). This matches the Cyril recap's own caveat: "Fixed gaps are directly observed; attribution to the advisor catch-up gate remains an inference … not per-wait telemetry."

## Acceptance checklist

- [x] Workload and acceptance defined before comparison (tests pass; 10/10 in every run).
- [x] Gate waits observed in baseline (8.38 s, 10.46 s, 13.66 s; 30 s timeouts sustained).
- [x] Complete trace retrieved for both conditions (session JSONL + `stats.db` messages; advisor `__advisor.jsonl`).
- [x] Only `syncBacklog` varied; model/effort/config held fixed.
- [x] Savings exceed observed added work (≈13.7–18.8 s vs 0), no missed requirement, no interruption, no reopening.
- [x] No regression → no restore needed; persistent config untouched.
- [x] Decision + provenance below; no skills mutated, no issues published remotely.

## Limitations and follow-up

1. **Reconciliation unmeasured.** The advisor produced no material finding in any run, so "added reconciliation/repair = 0" reflects the advisor finding nothing, not proof that removing the gate is safe where it would flag a material defect. A follow-up pilot on non-trivial work (where a late material finding would reopen accepted work) is the honest next step before generalizing.
2. **Deferential advisor.** Even the planted `median` defect was waved through as "transparently disclosed." The gate's value proposition depends on the advisor actually raising material issues; these runs did not demonstrate that.
3. **Small samples.** Two bounded A/B pairs plus one sustained session; turn counts differed (5 vs 4, 6 vs 4). The gap signature is clean and reproducible, but a single pilot is not a general performance guarantee.

## Provenance

- Session A baseline: `01a07d81-af0d-7227-a1a7-179e78961c4f` (`--tmp-omp-pilot-baseline--`)
- Session A comparison: `01a07d86-3887-74c9-88ad-53f4ebf74de8` (`--tmp-omp-pilot-comparison--`)
- Session B baseline: `01a07d8e-b915-75a1-b173-9802a251761a` (`--tmp-omp-pilot2-base--`)
- Session B comparison: `01a07d92-0e9a-7282-a9ed-a3025415a330` (`--tmp-omp-pilot2-off--`)
- Ledger: `~/.omp/stats.db` (`messages` table), synced via `omp stats`.
- Source: `packages/coding-agent/src/session/session-advisors.ts`, `…/advisor/runtime.ts`, `…/config/settings-schema.ts`.
