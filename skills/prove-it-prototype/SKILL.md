---
name: prove-it-prototype
description: REQUIRED before any design or plan when adding a feature to a system you did not personally write. Build a 30-50 line probe that produces the proposed feature's output against the real codebase, define an independent oracle that computes the same answer a different way, and refuse to proceed until probe and oracle agree.
---

# prove-it-prototype

You think you understand the system you're extending. You don't. Prove it.

Before any design, any plan, any task list, any TDD ceremony, you build a probe. The probe produces the smallest slice of the proposed feature's output against the actual system on actual data. Then you compute the same answer a *different way* — that's the oracle — and you compare. If they disagree, the design you're about to write is built on a fantasy.

## The rule

```
No design. No plan. No code. No tests.
Probe first. Oracle first. Agreement first.
```

If you cannot produce a 30-50 line probe and an independent oracle, you do not understand the feature well enough to design it. Go think harder. Come back.

## When to use this

Always, when adding a feature on top of a system whose behavior you can observe but did not write — a resolver, a parser, a database, a third-party API, somebody else's library, even your own code from six months ago. Anything where your mental model could be wrong and you wouldn't notice.

Skip only when writing a small standalone utility with no underlying system to depend on. If you're not sure whether to skip: don't skip.

**Upstream check.** If the feature request originated from a human in natural language (a stakeholder ask, a Linear ticket of two sentences, a Slack message), [[interrogated-spec]] runs *before* this skill. You cannot probe a feature whose definition is still mush — the probe will faithfully answer the wrong question. Confirm the upstream artifact exists at `.<feature-slug>/spec.md` with a verbatim sign-off line before proceeding.

## What counts as a probe

- Standalone script in the simplest language available.
- ≤ 100 lines. Preferably under 50.
- Uses no abstractions from the feature you're about to build. The probe is allowed to be ugly. It is required to be honest.
- Runs against the actual codebase, against actual production-shape data, not a hand-built fixture.

## What counts as an oracle

- An independent computation of the same answer.
- Built from a *different* mechanism than the probe. If the probe uses your AST resolver, the oracle uses `grep`. If the probe calls the HTTP API, the oracle hand-counts the database. The oracle is allowed to be tedious. It is required to be unaffected by the same bug.

Legitimate oracles:
- Shell pipelines (`grep | sort | uniq -c`)
- `cargo tree`, `git log`, `ls`, anything in `/usr/bin`
- A one-off Python or jq script
- Hand-counted spreadsheet
- Asking a human who knows
- An existing tool's output

Fake oracles, do not accept these:
- "The test fixture says so." The fixture is part of the system under test.
- "The design doc claims." The design doc is what you're trying to falsify.
- "Another part of the same tool computes it the same way." Same potential bug source.
- "It looks right." Sensible-looking output is how bugs survive.

## Process

0. **Check the tracker for prior art.** Before probing, search your project's issue tracker for tickets that mention the area or behavior you're about to investigate. Keyword-match on the function names, files, or symptoms involved. Read any matches: prior reviewers may have already filed the bug you're about to re-discover, and existing tickets carry context (PR comments, related fixes, reviewer rationale) that saves probe iterations. **5-minute upper bound — do not rabbit-hole.** Output: a short list of related issue IDs in your probe directory (e.g., `.<issue>/related-issues.md`), or an explicit "no prior art found" note.

   **How to find the tracker** (when not already known), in rough order of likelihood:
   - `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` often documents the tracker and how to query it. Check first.
   - A `gh` CLI + GitHub remote → GitHub Issues. Try `gh issue list --search "<keyword>"`.
   - A project-specific tracking CLI in the repo (e.g., `rivets`, `bd`, `beads`, `linear`). Check `Cargo.toml`, `package.json`, `Makefile`, or `bin/` for clues; the tool is often dogfooded.
   - `.github/ISSUE_TEMPLATE/`, `BUGS.md`, or `ISSUES.md` at the repo root.
   - When no formal tracker exists: skim recent PR reviews on adjacent files (`gh pr list --state all` + read the comments) and any `docs/` design notes. Same idea, different surface.
   - **If none of the above and you're unsure: ask the user.** Don't guess and don't skip.

1. **State the smallest possible question the feature answers.** Not the whole feature. The smallest factual question. (For coupling: "what packages does this workspace contain?" not "what are the coupling metrics?")

2. **Write the probe.** Aim for under 50 lines. Run it against the real codebase.

3. **Pick an oracle.** Write down — in one sentence — how you will compute the same answer independently.

4. **Run the oracle.** Compare output item by item to the probe's output.

5. **If they disagree:** the probe is wrong, the oracle is wrong, or the underlying system is broken. Investigate. Repeat until they agree.

6. **If they agree on the smallest question:** expand by one. New question. New probe slice. New oracle check. Continue until the probe covers enough of the feature's output that you trust the design will be standing on solid ground.

## When the probe and oracle disagree

This is the most important moment in the entire feature. Do not paper over it.

Causes, in descending order of how often they're the real reason:

1. **The underlying system is broken** in a way you didn't know about. **Before filing a new bug, search the tracker for an existing ticket describing the symptom.** Drift in your probe may be a re-discovery of work someone already filed. If found: link to the existing ticket from your design doc; if the existing ticket is closed-but-not-applied (an incomplete fix), note the residual gap. Otherwise file the bug. Either way: pause this feature until that bug is filed and either fixed or scoped around.

2. **Your model of the system is wrong.** The system does something you didn't predict. Update your model. Write down what you learned.

3. **The probe is wrong.** Fix it.

4. **The oracle is wrong.** Fix it. (Last resort. The oracle's job is to be independent. If you're "fixing" the oracle to match the probe, you have lost.)

If cause 1 fires: **stop**. You cannot build a feature on a broken substrate. Either fix the substrate or rescope the feature so it doesn't depend on the broken part.

## Hard gate

The next skill — `falsifiable-design` — refuses to run until you can answer yes to all of these:

- [ ] Probe written and runs against the real codebase
- [ ] Oracle defined and produces output
- [ ] Probe and oracle agree on at least one non-trivial slice
- [ ] You wrote down, in one sentence, what you learned that you didn't know before running the probe

If you learned nothing new, you didn't probe hard enough. Try again with a sharper question.

## Red flags

- "The system definitely works this way, I don't need to probe." Wrong. Probe anyway. Take five minutes. If you're right, you've cost five minutes. If you're wrong, you've saved a quarter.
- "The probe matches the oracle, but they're computing the same thing." If they're computing the same thing, the oracle isn't independent. Find a different oracle.
- "I'll skip the oracle and just check that the probe output looks sensible." Sensible-looking output is how bugs survive eleven review rounds. Pick an oracle.
- "The disagreement is small, I'll proceed and come back." No. Disagreement is information. The information goes upstream, not downstream.
- "There's no oracle available for this." Then your feature has no ground truth, which means it's not falsifiable, which means it's not engineering. Find a way.
- "I went straight to probing without checking the tracker." Everyone files surprising findings; some of them will be yours. Step 0 is bounded — five minutes — and catches the case where you're about to re-discover prior work. Do it.

## What this skill is not

This is not exploration. Exploration is "let me poke at the system to see how it works." Probing is "let me build the smallest possible version of the feature's output and check it against ground truth." Exploration is fine; it produces vibes. Probes produce evidence. Vibes are not allowed to gate downstream skills.

## Output

The artifacts of running this skill:

- `probe.{sh,py,rs,…}` — the probe code, committed to the repo (or attached to the design doc).
- A one-paragraph "Oracle" section in the design doc, naming the oracle and showing it agrees with the probe on at least one slice.
- A one-sentence "What I learned" note that wasn't obvious before the probe ran.

If any of those three artifacts don't exist, the skill didn't run. Run it.
