# gilfoyle

A skill suite for building software that is *right*, not fast. The premise is that most of the bugs you ship come from process disciplines that audit themselves rather than reaching outside the design document to compare against reality.

This suite forces the reach.

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

The loop has five mandatory gates that reach *outside the document*. Spec vs requester. Probe vs oracle. Falsifier vs claim. Budget vs scale. Per-slice oracle recheck. Each gate is a chance to catch a wrong assumption while it's still cheap. The first gate reaches outside the *requester's head*; the rest reach outside the *design document*.

`assessing-review-feedback` applies the same epistemic discipline to *incoming* review comments. A reviewer's finding is a hypothesis with two parts (the bug claim and the fix claim); the skill demands both be verified per finding before applying changes.

## The skills

| Skill | Replaces | Purpose |
|---|---|---|
| `interrogated-spec` | (nothing — this is new) | Grill the requester one question at a time until every vague noun is resolved, every success criterion is measurable, every edge has a decision, and the requester has signed off in their own words. |
| `prove-it-prototype` | (nothing — this is new) | Build a probe that runs against the real system, define an independent oracle, refuse to proceed until they agree. |
| `falsifiable-design` | brainstorming | Produce a design where every claim is paired with an experiment that would prove it wrong; cheapest falsifier runs before approval. |
| `budgeted-plan` | writing-plans | Decompose into slices, each with mandatory complexity budget, scale budget, and stress fixture. |
| `checkpointed-build` | executing-plans | Execute slices one at a time, run the oracle after each, stop on drift. |
| `tdd-scoped` | test-driven-development | Keep TDD doing what it's good at (unit correctness); add BUDGET and ORACLE gates between GREEN and REFACTOR. |
| `assessing-review-feedback` | (nothing — this is new) | Treat each PR review finding as a hypothesis with two parts (bug claim + fix claim). Verify both. Decide per finding whether to accept, modify, or reject. Decision log mandatory. |

## The rules, condensed

0. **No probe without a pinned spec.** Before you probe the system, pin the request. Every vague noun the requester uses ("user", "fast", "soon", "the inbox") is three decisions in a trench coat. Extract each decision before you write a probe — otherwise the probe answers the wrong question.

1. **No design without a probe.** A probe is the smallest possible program that produces the proposed feature's output against the real system. If you can't build one, you don't understand the feature well enough to design it.

2. **No probe without an oracle.** An oracle is an independent computation of the same answer using a different mechanism. If the probe matches its own logic, you've proven nothing.

3. **No claim without a falsifier.** A claim that can't be proven wrong is a wish. We don't plan against wishes.

4. **No loop without a budget.** Every loop in the plan states its asymptotic cost AND its production scale, before any code is written.

5. **No fixture without a bug to design against.** Happy-path fixtures confirm what you already believe. We pair every happy-path fixture with one designed to fail under a plausible bug.

6. **No precondition without an assertion.** "Callers must X" in a doc comment without `debug_assert!(X)` in the code is a lie.

7. **No slice without a checkpoint.** After every slice, the binary is run against the prove-it-prototype oracle. Drift is a stop condition.

8. **No "fix it later."** Drift caught at slice N is cheap. Drift caught at slice N+8 is the entire feature. We stop at slice N.

9. **No ceremony for ceremony's sake.** TDD is a tool. We use it for what it's good at. We do not pretend it's a substitute for verification against reality.

10. **We're done when it's right.** Not when the tests pass. Not when the plan's checkboxes are ticked. When the binary, run against the real system, at production scale, agrees with the oracle. Not before.

11. **Dogfood the static-analysis tools available to you.** Before changing a function's signature, name, or semantics: list its callers with whatever impact-analysis tool you have (project-local code-intelligence binary, IDE find-usages, `grep`). The list bounds the change's blast radius. Treat the tool's output as a hint generator, not an oracle — verify with `grep` when stakes are high.

## When to use this suite

When you are adding a feature on top of a system whose behavior you can observe but did not personally write. Which is most of the time.

If you are writing a small utility from scratch with no underlying system to depend on, this is overkill. Run TDD on its own. If you are extending tethys, rivets, the Linux kernel, your customer's database, anything where the system can surprise you — this is the loop.

## Voice

The skills are written in a tone that doesn't waste words. They state rules, list red flags, and refuse to soften their gates. The skills will not validate your enthusiasm. They will check your work.

If the tone reads as cynical: the cynicism is calibrated. We have seen too many features that "work on the test fixture" ship bugs that lived in the gap between the fixture and reality. The gates close that gap. The voice signals that we mean it.

## How to install

### As a Claude Code plugin (recommended)

The repo is structured as a Claude Code plugin and ships its own marketplace manifest. Install in any of these ways:

```bash
# From the marketplace (preferred — one-time setup, then easy updates)
/plugin marketplace add dwalleck/gilfoyle
/plugin install gilfoyle@gilfoyle

# Direct install from the GitHub remote
/plugin install https://github.com/dwalleck/gilfoyle

# From a local clone
/plugin install C:\path\to\gilfoyle
# or
/plugin install /path/to/gilfoyle
```

Once installed, the seven skills appear in your `Skill` tool's available-skills list. Invoke directly:

```
Skill interrogated-spec
Skill prove-it-prototype
Skill falsifiable-design
Skill budgeted-plan
Skill checkpointed-build
Skill tdd-scoped
Skill assessing-review-feedback
```

Or just describe what you're doing — Claude will pick the right skill from the skill's `description` frontmatter.

### As a bare skill directory (no plugin install)

If your agent doesn't support plugin installation, point its skill-search at this repo's `skills/` subtree manually. Each skill is a `SKILL.md` with `name` + `description` frontmatter. The skills cross-reference each other by name; the suite assumes you can invoke them in sequence and that each downstream skill enforces its gate against the upstream skill's outputs.

We are not going to write a configuration system. You can configure your tools.

## When to invoke

At the start of any non-trivial work:

- **Feature request from a human in natural language** ("we want unread count on the inbox," "make permissions auditable," "users are complaining about X") → start with `interrogated-spec`. Pin the spec before you probe the system.
- **New feature** on top of an existing system, with a spec already pinned → start with `prove-it-prototype`. Don't skip to design until probe and oracle agree.
- **Bug fix that spans multiple files** → start with `prove-it-prototype` against the bug itself; the probe + oracle pair becomes the regression test.
- **Refactor that changes public surface** → start with `falsifiable-design`; the cheapest falsifier is the smoke test that the refactor doesn't lose any caller.
- **PR review feedback arrives** → invoke `assessing-review-feedback` BEFORE applying any reviewer suggestions.

For trivial work (typos, single-function changes with no behavior change, doc edits), don't invoke the loop — it's process overhead for nothing.

## Hail Satan

Build the thing. Check it against reality. Stop when drift appears. Ship when it's right.

## Running the loop autonomously (Kiro)

The skills above are the methodology. `agents/` + `crew-dag-loop.json` package that methodology as an autonomous [Kiro CLI](https://kiro.dev) crew: after you sign off on the spec (the one human gate), a five-stage DAG — probe → design → plan → build ⇄ gate — runs unattended and **stops the moment a claim is falsified**, surfacing which leg (implementation / oracle / design / substrate) is implicated for you to adjudicate.

The crew rides along on this Claude Code plugin: a Kiro install step copies `agents/` into `.kiro/agents/`, `skills/` into `.kiro/skills/`, and `crew-dag-loop.json` alongside as a reference. Skills stay single-source here.

See **[KIRO-CREW.md](./KIRO-CREW.md)** for the architecture, the Class-A (self-heal) vs Class-B (halt) loop polarity, and usage.
