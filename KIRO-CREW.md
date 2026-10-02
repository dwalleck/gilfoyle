# gilfoyle-builder

An autonomous build crew that runs the [gilfoyle](skills/gilfoyle/SKILL.md) workflow as a Kiro `subagent` DAG. After the applicable outcome decisions are approved, its fixed probe, design, plan, build, and gate roles run with bounded implementation repairs and halt on contradictions or unresolved decisions outside the approved work.

## The idea

This plugin wires the applicable workflow stages into a self-driving crew. Fixed roles preserve the adapter's hand-off and permission boundaries; they do not require a second oracle, a cheapest-falsifier run before approval, stress fixtures, or per-loop budgets for every change. The [route](skills/gilfoyle/references/change-workflow.md#route-selection), [verification ladder](skills/gilfoyle/references/falsifiable-design.md#verification-ladder), and [compact slices](skills/gilfoyle/references/budgeted-plan.md#3-write-compact-slices) own those methodology decisions.

```
outcome decisions   ← orchestrator; interrogate material unresolved behavior only
        │  (.<slug>/route.md T4 or applicable spec.md; approval when required)
        ▼
  probe  →  design  →  plan  →  build  ⇄  gate
   │          │          │        │         │
scoped     approved   compact   checkpointed-build   assembled proof
premises    design     slices     + tdd-scoped          + router
```

Stages hand off through `.<feature-slug>/` on the shared working directory: the route, applicable spec/evidence/probe, design, plan, and adapter `status.md`. Reuse settled decisions and valid evidence; investigate only a specific missing or invalidated premise, blocking only its dependent work. The crew engine substitutes only `{task}` (the outcome-source path: route T4 or applicable spec) into each stage; forward `depends_on` edges do **not** pipe predecessor text. The one exception is the loop edge `gate → build`, which injects the gatekeeper's feedback as context.

## The loop polarity is inverted from dotnet-test-creator — on purpose

| | dotnet-test-creator | gilfoyle-builder |
|---|---|---|
| Gate failure means | "tests aren't done" → **always loop** to self-heal | depends on **which class** of failure |
| Self-heal loop | `validate → implement` on any `NEEDS_WORK` | `gate → build` on **Class-A only** |
| Terminal condition | all tests green | verified completion or an explicit blocked/halting report |

test-creator self-heals on *any* failure because a failing test is unambiguously "implementation not done." gilfoyle instead distinguishes a repair determined by approved behavior and applicable evidence from a contradiction or decision that the executor cannot resolve within its authorization. Technical corrections follow the [contract's approval semantics](skills/gilfoyle/references/CONTRACT.md#approval-semantics); changed behavior, architecture, scope, or accepted risk returns to its owner.

A failing implementation check is not by itself a reason to reopen design. Classify the failure against the approved outcome and relevant evidence; use an independent comparison only when the verification ladder or a repository requirement calls for it:

- **Class A — implementation is behind the approved contract.** A relevant check is red, the approved contract and valid evidence establish its expected outcome, and the fix stays within the existing slice's planned files. → the gatekeeper fires `summary(resultType='changes_needed')` with `NEEDS_WORK` + categorized feedback; the engine re-runs `build` within its configured bound. No additional oracle-on-the-failing-input ceremony is required.

- **Class B — the executor cannot resolve the failure within approved work.** A genuine contract/reference/substrate contradiction remains, the needed decision is not established, the repair requires edits outside the approved slice's planned files, or a Class-A repair exhausts its configured bound. → the stage writes `HALT_FALSIFIED` and calls `summary(resultType='terminal')`. **No loop.** The orchestrator surfaces the implicated implementation, verification, design, or substrate obligation for adjudication.

`NEEDS_WORK` requests an authorized implementation repair; `HALT_FALSIFIED` stops the crew and surfaces its unresolved obligation. Required failed or unavailable proof blocks completion, not merely a checker's hypothetical sensitivity limit. Final success requires the [assembled integration check](skills/gilfoyle/references/checkpointed-build.md#final-integration-check), including required consumer/native/repository proof and substantive independent review; historical results count only when still valid.

### Halt propagation

Because forward edges don't pipe text, a forward stage that reaches a terminal contradiction or unresolved authorization writes `HALT_FALSIFIED` to `.<slug>/status.md`. Every downstream stage reads that file first and, if the token is present, no-ops and re-echoes it via `summary(terminal)`. The halt cascades to the end of the crew and the orchestrator reports it instead of pretending the run succeeded.

## Layout

```text
gilfoyle/
├── .claude-plugin/                  # Claude Code marketplace and plugin manifests
├── plugin.json                      # Agent Plugins manifest
├── package.json                     # Oh My Pi package marker
├── skills/
│   └── gilfoyle/                    # sole discoverable skill
│       ├── SKILL.md                 # orchestrator
│       └── references/              # workflow contract and stage documents
├── crew-dag-loop.json               # probe→design→plan→build⇄gate DAG
├── agents/                          # Kiro agent configs
│   ├── gilfoyle-orchestrator.json
│   ├── gilfoyle-prober.json … gilfoyle-gatekeeper.json
│   └── prompts/
└── KIRO-CREW.md
```

The Kiro install step copies `agents/` into `.kiro/agents/`, `skills/gilfoyle` into `.kiro/skills/gilfoyle`, and `crew-dag-loop.json` alongside. Agent resources register the root orchestrator with `skill://.kiro/skills/gilfoyle/SKILL.md` and load their stage documents from `file://../skills/gilfoyle/references/`.

Only the orchestrator has the `subagent` tool and a `toolsSettings.crew` grant; the five stage agents are leaves that cannot spawn anything. Tool allow-lists are scoped per role (the implementer can write `**/*` and commit; the gatekeeper writes only `<rundir>/**` and never edits oracles).

## Deployment assumptions

- **One skill is installed.** The portable source is `skills/gilfoyle`. Kiro installs that directory at `.kiro/skills/gilfoyle`; each fixed-role agent registers the orchestrator and directly loads only its contract and applicable stage documents.
- **A tracker is expected.** The skills enforce a tracker discipline (deferrals must cite a real issue ID). These configs allow `rivets` and `gh issue`; adjust the shell allow-lists for your tracker.
- **Polyglot.** No language is hard-coded. Stages use the project's own relevant build/test/consumer commands and any justified probe/comparison tooling; required repository checks remain intact.
- **Kiro `subagent` crew support** with `loop_to` (trigger + `max_iterations`). The loop is bounded at `max_iterations: 5`.

## Usage

```
/agent swap gilfoyle-orchestrator
```

Then describe the feature. The orchestrator routes the request, reuses explicit outcomes and valid existing approvals, and asks one highest-leverage question at a time only for material unresolved decisions. After applicable approval it submits the fixed crew and reports either verified completion or an explicit blocked/`HALT_FALSIFIED` result with the implicated obligation for adjudication.

The `.<feature-slug>/` directory is the run's audit trail — add it to `.gitignore`; don't delete it.

## What this is NOT

- It does not replace required outcome approval or the adjudication of changed behavior, scope, architecture, or accepted risk. Explicit behavior and valid existing approval are reused rather than re-interrogated.
- It does not "retry until green." A `HALT_FALSIFIED` is the method working (it caught drift), not a transient failure to re-submit.
- The gatekeeper never edits oracles or weakens claims to make a run pass.

## Status

This is a **sketch/scaffold**. The DAG, agent configs, and prompts are complete and the JSON validates, but the crew has not yet been run end-to-end against a real feature. Treat the first few runs as calibration — especially the Class-A/Class-B boundary the gatekeeper draws and the halt-sentinel propagation across forward stages.
