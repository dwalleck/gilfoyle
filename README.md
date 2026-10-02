# gilfoyle

A workflow skill for building software that is right in real use. Define consumer-visible outcomes, resolve consequential unknowns, and verify delivery with evidence proportional to the change.

Gilfoyle makes required verification explicit without turning every change into a new proof framework.

## What we ship

- Reliable software.
- Software whose requested outcomes, compatibility, and safety boundaries are clear.
- Software verified through relevant behavioral tests, real consumer execution, and applicable repository checks.
- Software whose remaining uncertainty and required proof are explicit, not hidden behind a green label.

## What we don't ship

- Fast software, at the cost of being wrong about what it does.
- Plans that audit themselves.
- Tests that miss plausible consumer-visible bugs or important boundaries.
- Features built on consequential premises that nobody established.
- "It works on my fixture" as a synonym for "it works."

## The philosophy, briefly

The standard software loop is: brainstorm → plan → execute → test → ship. It can become self-confirming when each document or check merely repeats the implementation's assumptions. Gilfoyle anchors the work to requested outcomes and evidence that can expose a real failure.

The route determines the work. Reuse valid documentation, source, tests, and observations; investigate only consequential facts they do not answer. Deliver independently-green atomic slices with compact records, using ordinary verification first. Add custom machinery only for a named coverage gap or an explicit requirement, and stop the affected work when a required check fails.

## The loop

```text
change-workflow     →  select Local, Structural, or Empirical
       │
       ├─ Local     →  normal repository fix/TDD + relevant verification
       │
       └─ Structural / Empirical, as applicable:
          interrogated-spec   →  resolve material outcome/scope decisions
          prove-it-prototype  →  answer specific unresolved factual premises
          falsifiable-design  →  claims with sufficient verification
          budgeted-plan       →  compact independently-green slices
          checkpointed-build  →  implement and verify each atomic change
                 └─ tdd-scoped → focused behavioral RED / GREEN / REFACTOR

review feedback    →  assessing-review-feedback takes entry precedence
                      verify each finding, then accept / modify / reject
```

The selected route determines the applicable stages; already-settled behavior and valid evidence are retained. The [route selection](skills/gilfoyle/references/change-workflow.md#route-selection) and [workflow contract](skills/gilfoyle/references/CONTRACT.md#evidence-validity) own applicability and evidence reuse.

`assessing-review-feedback` applies the same discipline to incoming comments: verify the bug claim and evaluate the fix separately. Repairs within approved claims use a [compact repair record](skills/gilfoyle/references/assessing-review-feedback.md#compact-repair-record) and scoped verification; changed approved decisions return for approval, and changed planning inputs receive affected-only updates.

## The orchestrator and stages

`gilfoyle` is the sole discoverable skill. It selects one entry branch, then progressively discloses only the stage needed for the current gate.

| Stage | Replaces | Purpose |
|---|---|---|
| `interrogated-spec` | (nothing — this is new) | Resolve only material behavior, compatibility, scope, safety, and risk decisions; pin observable outcomes and obtain applicable approval. |
| `prove-it-prototype` | (nothing — this is new) | Answer a specific consequential factual uncertainty from valid sources or the smallest necessary observation; block only dependent work. |
| `falsifiable-design` | brainstorming | Group outcome claims and plausible introduced failures, choose sufficient verification, and approve the relevant design decisions. |
| `budgeted-plan` | writing-plans | Plan atomic slices with Outcome, Changes, Verification, and applicable Dependencies; record supplied feature budgets and delivery decisions once. |
| `checkpointed-build` | executing-plans | Verify delivered behavior per atomic change, then establish assembled consumer, native/platform, repository, and independent-review proof. |
| `tdd-scoped` | test-driven-development | Cover new/fixed behavior with focused tests and real defect sensitivity; broader verification stays at the checkpoint. |
| `assessing-review-feedback` | (nothing — this is new) | Verify and decide each finding; group approved-contract repairs atomically in the existing decision surface. |

## Evidence and completion

- **Outcomes first.** The [pinned bar](skills/gilfoyle/references/interrogated-spec.md#the-pinned-bar) distinguishes requested behavior from implementation choices.
- **Ordinary verification first.** The [verification ladder](skills/gilfoyle/references/falsifiable-design.md#verification-ladder) starts with behavioral tests, real consumer execution, and representative captured references. Custom oracles, live differential/fuzz machinery, and additional mutations are conditional on a named uncovered mechanism or repository requirement.
- **Real bugs need sensitivity.** [Mutation sensitivity](skills/gilfoyle/references/falsifiable-design.md#mutation-sensitivity) owns failing-before/passing-after proof and its bounded alternative; coverage-only work does not invent a red state.
- **Compact delivery records.** [Compact slices](skills/gilfoyle/references/budgeted-plan.md#3-write-compact-slices) define the work; the [checkpoint](skills/gilfoyle/references/checkpointed-build.md#the-gate--stated-once) records delivered behavior, performed checks/results, and unresolved failures once.
- **Analyze and migrate callers.** [Impact analysis and reuse](skills/gilfoyle/references/checkpointed-build.md#1-impact-analysis-and-reuse) uses symbol-aware references with text-search safety nets before signature, name, or semantics changes; affected callers migrate atomically.
- **Required proof remains required.** The [final integration check](skills/gilfoyle/references/checkpointed-build.md#final-integration-check) owns assembled repository gates, real consumer/native proof, and substantive independent review. [Design-conformance review](skills/gilfoyle/references/module-shape.md#final-design-conformance-review) makes isolated reconstruction conditional, not automatic.
- **Budgets follow their authority.** [Size stop](skills/gilfoyle/references/CONTRACT.md#size-stop) governs supplied soft feature budgets and explicit requester/repository hard limits. Readability, cohesive ownership, and required gate authority are preserved.

## When to use this suite

Use Gilfoyle for nontrivial changes to existing software, including changes where ownership, compatibility, scale, or external-system behavior could surprise you. Local changes use normal repository fix/TDD and focused verification; Structural and Empirical routes disclose only their applicable stages.

Trivial typos, formatting, and documentation-only edits use the repository's normal focused process.

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

The stage documents above are the methodology. `agents/` + `crew-dag-loop.json` package it as an autonomous [Kiro CLI](https://kiro.dev) crew: after the applicable spec sign-off, a fixed five-stage DAG — probe → design → plan → build ⇄ gate — runs with a bounded implementation-repair loop. Its fixed roles do not make optional evidence machinery mandatory; contract/reference/substrate contradictions or repairs outside the approved slice halt for adjudication.

The Kiro install step copies `agents/` into `.kiro/agents/`, the unified skill from `skills/gilfoyle` into `.kiro/skills/gilfoyle`, and `crew-dag-loop.json` alongside as a reference.

See **[KIRO-CREW.md](./KIRO-CREW.md)** for the architecture, the Class-A (self-heal) vs Class-B (halt) loop polarity, and usage.
