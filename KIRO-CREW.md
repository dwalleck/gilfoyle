# gilfoyle-builder

An autonomous build crew that runs the [gilfoyle](https://github.com/…/gilfoyle) skill chain as a Kiro `subagent` DAG. After a human signs off on the spec, it runs unattended — probe, design, plan, build — **until a claim is falsified**. Modeled on `plugins/dotnet-test-creator`, with the loop polarity deliberately inverted (see below).

## The idea

gilfoyle is a chain of engineering-discipline skills. This plugin wires the post-sign-off skills into a self-driving crew:

```
interrogated-spec   ← HUMAN gate (orchestrator, interactive) — NOT a crew stage
        │  (.<slug>/spec.md + verbatim sign-off)
        ▼
  probe  →  design  →  plan  →  build  ⇄  gate
   │          │          │        │         │
prove-it   falsifiable budgeted  checkpointed-build   final integration
prototype   -design    -plan     + tdd-scoped          check + router
```

Stages hand off through `.<feature-slug>/` on the shared working directory (`spec.md`, `probe.*`, `design.md`, `plan.md`, `status.md`) — exactly like test-creator's `.testagent/`. The crew engine substitutes only `{task}` (the signed spec path) into each stage; forward `depends_on` edges do **not** pipe predecessor text. The one exception is the loop edge `gate → build`, which injects the gatekeeper's feedback as context.

## The loop polarity is inverted from dotnet-test-creator — on purpose

| | dotnet-test-creator | gilfoyle-builder |
|---|---|---|
| Gate failure means | "tests aren't done" → **always loop** to self-heal | depends on **which class** of failure |
| Self-heal loop | `validate → implement` on any `NEEDS_WORK` | `gate → build` on **Class-A only** |
| Terminal condition | all tests green | all green **or a claim falsified** |

test-creator self-heals on *any* failure because a failing test is unambiguously "implementation not done." gilfoyle's failures are mostly **ambiguous** — a gate failure can mean the implementation, the *oracle*, or the *design* is wrong, and `checkpointed-build` reserves that decision for a human ("*decisions about which thing is wrong are not yours to make from inside the executor*"; "*if you revise the oracle to match the implementation, you have lost*").

A plain implementation bug *also* makes the binary disagree with the oracle, so **"binary ≠ oracle" is not the discriminator.** The crew runs the oracle **on the failing input** and compares to the check's **expected** output:

- **Class A — implementation is behind the spec.** A unit test or stress fixture is red, `oracle(failing input) == the check's expected output` (the checks agree with ground truth, only the code is behind), *and* the fix stays within the slice's planned files. → gatekeeper fires `summary(resultType='changes_needed')` with `NEEDS_WORK` + categorized feedback; the engine re-runs `build`. **This is the "run until a claim is falsified" state — keep working.**

- **Class B — a claim is falsified.** `oracle(failing input) != the expected output` (a check/claim contradicts truth), the rebuilt binary **drifts** from the oracle in a way no single-slice edit resolves, a falsifier fires, a fence encodes a design-level contradiction, the probe disagrees with its oracle (substrate suspect), *or* a Class-A failure won't converge (persists across the loop bound, or needs edits outside the slice's planned files). → the stage writes `HALT_FALSIFIED` and calls `summary(resultType='terminal')`. **No loop.** The orchestrator surfaces it to the human, who decides which leg (impl / oracle / design / substrate) is wrong.

`NEEDS_WORK` = "implementation hasn't caught up to a claim yet, and the checks still match ground truth" (loop). `HALT_FALSIFIED` = "a check contradicts ground truth, the binary drifts un-fixably, or the loop won't converge" (stop, surface). Because the oracle is independent by construction, a disagreement between a *check* and the oracle means the check or claim is wrong, not the code — that is Class B.

### Halt propagation

Because forward edges don't pipe text, a forward stage that falsifies (probe ≠ oracle; cheapest falsifier fails) writes `HALT_FALSIFIED` to `.<slug>/status.md`. Every downstream stage reads that file first and, if the token is present, no-ops and re-echoes it via `summary(terminal)`. The halt cascades to the end of the crew and the orchestrator reports it instead of pretending the run succeeded.

## Layout

```
gilfoyle/                            # this repo (a Claude Code plugin)
├── .claude-plugin/                  # Claude Code plugin manifest (unchanged)
├── skills/                          # the 7 gilfoyle skills — single source of truth
│   ├── interrogated-spec/ … assessing-review-feedback/
├── crew-dag-loop.json               # the 5-stage DAG (probe→design→plan→build⇄gate); installed as a reference
├── agents/                          # Kiro agent configs (installed into .kiro/agents/)
│   ├── gilfoyle-orchestrator.json   # owns interrogated-spec (human) + submits the crew
│   ├── gilfoyle-prober.json         # prove-it-prototype
│   ├── gilfoyle-designer.json       # falsifiable-design
│   ├── gilfoyle-planner.json        # budgeted-plan
│   ├── gilfoyle-implementer.json    # checkpointed-build + tdd-scoped
│   ├── gilfoyle-gatekeeper.json     # final integration check + crew router
│   └── prompts/
│       ├── gilfoyle-orchestrator.md
│       ├── gilfoyle-prober.md … gilfoyle-gatekeeper.md
└── KIRO-CREW.md                     # this document
```

The agents and skills ride along on the Claude Code plugin: a Kiro-specific install step copies `agents/` into `.kiro/agents/` and `skills/` into `.kiro/skills/`, and copies `crew-dag-loop.json` alongside as a reference. That is why the agent configs reference skills via `skill://.kiro/skills/<skill>/SKILL.md` — the *installed* location — even though the source lives in `skills/` here.

Only the orchestrator has the `subagent` tool and a `toolsSettings.crew` grant; the five stage agents are leaves that cannot spawn anything. Tool allow-lists are scoped per role (the implementer can write `**/*` and commit; the gatekeeper writes only `<rundir>/**` and never edits oracles).

## Deployment assumptions

- **Skills are single-source and installed for you.** The 7 skills live only in this repo's `skills/`. The Kiro install step places them at `.kiro/skills/`, which is what every agent's `skill://.kiro/skills/<skill>/SKILL.md` reference resolves against — no vendoring, no per-project copying by hand.
- **A tracker is expected.** The skills enforce a tracker discipline (deferrals must cite a real issue ID). These configs allow `rivets` and `gh issue`; adjust the shell allow-lists for your tracker.
- **Polyglot.** No language is hard-coded. Stages use the project's own build/test/probe commands; the shell allow-lists cover dotnet/npm/pnpm/yarn/pytest/go/cargo/maven/gradle plus probe/oracle tooling (`bash`, `python3`, `jq`, `grep`, `git`).
- **Kiro `subagent` crew support** with `loop_to` (trigger + `max_iterations`). The loop is bounded at `max_iterations: 5`.

## Usage

```
/agent swap gilfoyle-orchestrator
```

Then describe the feature. The orchestrator interrogates you one question at a time (interrogated-spec), refuses to proceed until you sign off in your own words, then submits the crew and reports either **all-green** or a **`HALT_FALSIFIED`** with the implicated leg for you to adjudicate.

The `.<feature-slug>/` directory is the run's audit trail — add it to `.gitignore`; don't delete it.

## What this is NOT

- It does not automate the spec sign-off or the falsification halt. Both are human decisions by design.
- It does not "retry until green." A `HALT_FALSIFIED` is the method working (it caught drift), not a transient failure to re-submit.
- The gatekeeper never edits oracles or weakens claims to make a run pass.

## Status

This is a **sketch/scaffold**. The DAG, agent configs, and prompts are complete and the JSON validates, but the crew has not yet been run end-to-end against a real feature. Treat the first few runs as calibration — especially the Class-A/Class-B boundary the gatekeeper draws and the halt-sentinel propagation across forward stages.
