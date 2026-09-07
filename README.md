# gilfoyle

A workflow skill for building software that is *right*, not fast. The premise is that most of the bugs you ship come from process disciplines that audit themselves rather than reaching outside the design document to compare against reality.

Gilfoyle forces the reach.

## What we ship

- Reliable software.
- Software whose claims have been falsified before they were committed to.
- Software whose loops have asymptotic budgets stated in writing before any code was typed.
- Software whose tests are anchored to an independent oracle, not to an imagined model of the system.

## What we don't ship

- Fast software, at the cost of being wrong about what it does.
- Plans that audit themselves.
- Test suites whose fixtures are too small to surface the bugs the production data has.
- Features whose first encounter with reality is the smoke test at the end of the plan.
- "It works on my fixture" as a synonym for "it works."

## The philosophy, briefly

The standard software loop is: brainstorm → plan → execute → test → ship. Every gate in that loop is internal to the design document. The document audits itself. The plan audits the document. The implementation audits the plan. The tests audit the implementation. Nothing audits *the whole thing* against the system it's actually running on, until the very end, when fixing anything is expensive.

This suite reorders the work into a spiral whose every iteration ends with the binary touching reality and an independent oracle confirming what it produced. The unit of work is not a task. It is a *hypothesis with a named falsification experiment*. Slices replace tasks. Drift between binary and oracle is a stop condition, not a "fix later" item.

## The loop

```
interrogated-spec   →  every behavior observable, every criterion measurable
       ↓ (gate: requester signs off in their own words)
prove-it-prototype  →  oracle established, probe matches
       ↓ (gate: probe ↔ oracle)
falsifiable-design  →  every claim has a falsifier
       ↓ (gate: cheapest falsifier passes)
budgeted-plan       →  slices with budgets + stress fixtures
       ↓ (gate: every loop budgeted, every fixture adversarial)
checkpointed-build  →  per-slice: implement, recheck oracle, recheck budget
       ↓ (per-slice gate: oracle matches, budget holds)
       │
       ├─→ tdd-scoped              →  unit tests inside a slice, then BUDGET + ORACLE gates
       │
       └─→ assessing-review-feedback (when review feedback arrives)
                                   →  per-finding: verify, evaluate, accept / modify / reject
```

The selected route determines which gates apply: requester decisions, empirical premise evidence, falsifiable design, budgeted planning, and implementation verification. Each checks an obligation outside the document. The [workflow contract](skills/gilfoyle/references/CONTRACT.md#evidence-validity) defines when prior evidence remains valid and when changed assumptions require fresh verification.

`assessing-review-feedback` applies the same discipline to incoming comments: verify the bug claim and evaluate the fix separately. Repairs within approved claims use a [compact repair record](skills/gilfoyle/references/assessing-review-feedback.md#compact-repair-record) and scoped verification; changed approved decisions return for approval, and changed planning inputs receive affected-only updates.

## The orchestrator and stages

`gilfoyle` is the sole discoverable skill. It selects one entry branch, then progressively discloses only the stage needed for the current gate.

| Stage | Replaces | Purpose |
|---|---|---|
| `interrogated-spec` | (nothing — this is new) | Grill the requester one question at a time until every vague noun is resolved, every success criterion is measurable, every edge has a decision, and the requester has signed off in their own words. |
| `prove-it-prototype` | (nothing — this is new) | Establish missing or invalidated empirical premises with a real-system probe and independent oracle; retain valid premise evidence. |
| `falsifiable-design` | brainstorming | Produce a design where every claim is paired with an experiment that would prove it wrong; cheapest falsifier runs before approval. |
| `budgeted-plan` | writing-plans | Decompose new work into independently verifiable slices with applicable budgets and fixtures; amend only affected planning inputs on review re-entry. |
| `checkpointed-build` | executing-plans | Verify slices and bounded repairs, then establish assembled quality, platform, and integration proof. |
| `tdd-scoped` | test-driven-development | Prove changed behavior red/green and check changed complexity locally; checkpoints own the broader evidence. |
| `assessing-review-feedback` | (nothing — this is new) | Verify and decide each finding; group approved-contract repairs atomically in the existing decision surface. |

## The rules, condensed

0. **Pin unresolved behavior.** Resolve observable behavior before probing or designing. Reuse explicit behavior and approved decisions rather than interrogating them again.

1. **Empirical design needs valid premise evidence.** Probe an unverified or invalidated premise before relying on it. Structural and Local routes do not manufacture empirical work.

2. **No probe without an oracle.** An oracle is an independent computation of the same answer using a different mechanism. If the probe matches its own logic, you've proven nothing.

3. **No claim without a falsifier.** A claim that can't be proven wrong is a wish. We don't plan against wishes.

4. **No loop without a budget.** Every loop in the plan states its asymptotic cost AND its production scale, before any code is written.

5. **No fixture without a bug to design against.** Happy-path fixtures confirm what you already believe. We pair every happy-path fixture with one designed to fail under a plausible bug.

6. **No precondition without an assertion.** "Callers must X" in a doc comment without `debug_assert!(X)` in the code is a lie.

7. **Every slice or repair has a checkpoint.** Verify affected behavior against its applicable obligations, retain valid evidence by reference, and stop on unresolved failures. Writer-local proof does not replace assembled integration.

8. **No "fix it later."** Drift caught at slice N is cheap. Drift caught at slice N+8 is the entire feature. We stop at slice N.

9. **No ceremony for ceremony's sake.** TDD is a tool. We use it for what it's good at. We do not pretend it's a substitute for verification against reality.

10. **Completion requires current evidence.** The final assembled state satisfies every applicable behavioral, quality, platform, and integration obligation, with independent structural review when required. Historical green results count only when they still prove that state.

11. **Dogfood the static-analysis tools available to you.** Before changing a function's signature, name, or semantics: list its callers with whatever impact-analysis tool you have (project-local code-intelligence binary, IDE find-usages, `grep`). The list bounds the change's blast radius. Treat the tool's output as a hint generator, not an oracle — verify with `grep` when stakes are high.

## When to use this suite

When you are adding a feature on top of a system whose behavior you can observe but did not personally write. Which is most of the time.

If you are writing a small utility from scratch with no underlying system to depend on, this is overkill. Run TDD on its own. If you are extending tethys, rivets, the Linux kernel, your customer's database, anything where the system can surprise you — this is the loop.

## Voice

The orchestrator and stage documents are written in a tone that doesn't waste words. They state rules, list red flags, and refuse to soften their gates. Gilfoyle will not validate your enthusiasm. It will check your work.

If the tone reads as cynical: the cynicism is calibrated. We have seen too many features that "work on the test fixture" ship bugs that lived in the gap between the fixture and reality. The gates close that gap. The voice signals that we mean it.

## How to install

### Claude Code plugin

The root Claude Code manifest exposes the unified `gilfoyle` skill:

```bash
# Marketplace
/plugin marketplace add dwalleck/gilfoyle
/plugin install gilfoyle@gilfoyle

# GitHub
/plugin install https://github.com/dwalleck/gilfoyle

# Local clone
/plugin install /path/to/gilfoyle
```

### Agent Skills CLI

```bash
npx skills add https://github.com/dwalleck/gilfoyle --skill gilfoyle

# Local clone
npx skills add . --skill gilfoyle
```

### Oh My Pi

```bash
omp plugin install .
```

### Bare skill directory

Point the client's skill search at `skills`, or copy `skills/gilfoyle` into its skill directory.

Every installation exposes one skill:

```text
gilfoyle
```

Describe the change or review feedback. The orchestrator selects the applicable branch and discloses its stages in order.

## When to invoke

Invoke `gilfoyle` for a nontrivial code change or whenever review feedback proposes a code change. It routes implementation work through Local, Structural, or Empirical evidence and gives review feedback precedence over ordinary change work.

For trivial work such as typos, formatting, or documentation-only edits, use the repository's normal focused process.

## Hail Satan

Build the thing. Check it against reality. Stop when drift appears. Ship when it's right.

## Running the loop autonomously (Kiro)

The stage documents above are the methodology. `agents/` + `crew-dag-loop.json` package it as an autonomous [Kiro CLI](https://kiro.dev) crew: after you sign off on the spec (the one human gate), a five-stage DAG — probe → design → plan → build ⇄ gate — runs unattended and **stops the moment a claim is falsified**, surfacing which leg (implementation / oracle / design / substrate) is implicated for you to adjudicate.

The Kiro install step copies `agents/` into `.kiro/agents/`, the unified skill from `skills/gilfoyle` into `.kiro/skills/gilfoyle`, and `crew-dag-loop.json` alongside as a reference.

See **[KIRO-CREW.md](./KIRO-CREW.md)** for the architecture, the Class-A (self-heal) vs Class-B (halt) loop polarity, and usage.
