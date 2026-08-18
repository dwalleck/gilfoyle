# interrogated-spec

You pin the observable behavior of a change before anything downstream reads it. The pin is `spec.md` in the canonical workflow directory. Probe, design, plan, and build all read behavior from this file, so a word left unpinned here is a bug shipped later at full price.

Unresolved behavior is a queue of questions, not a plan of action. Your job is to empty the queue: every behavior a given/when/then triple, every edge a decision, every discovered ambiguity a row in the Decisions table, every approval verbatim.

## When this runs

This stage runs when behavior is **unresolved** — the change's observable behavior cannot yet be written as `given X, when Y, then Z` with observable X, Y, Z. Interrogation is conditional on that, not on the request's origin: a natural-language request with explicit behavior skips interrogation; a terse ticket with hidden decisions does not.

Run when:

- `route.md` requires `spec.md` (Structural or Empirical route with unresolved behavior).
- A signed `spec.md` exists but no longer covers the change (behavior changed or scope grew).
- No `route.md` exists and the request's behavior cannot yet be stated as given/when/then triples — routing runs first per the contract, then interrogation proceeds.

Skip when:

- `route.md` records no unresolved behavior (`N/A — <reason>`).
- A signed `spec.md` already covers the change and the request is a literal subset of it.

## Contract

Read [workflow contract](references/CONTRACT.md) before producing or consuming any workflow artifact. It is the single source of truth for: gate states (`PASS` / `FAIL` / `N/A — <reason>`), artifact ownership (this stage owns `spec.md`; every other stage reads it), artifact directory resolution, the tracker taxonomy, and approval semantics. This stage applies those definitions; it does not restate them.

## The pinned bar

`spec.md` is complete when every line below holds. Each is mechanically checkable:

1. Every behavior is stated as `given X, when Y, then Z` with X, Y, Z observable.
2. Every success criterion is observable and falsifiable: a quantitative criterion has a number, a unit, and a method of measurement; a binary, structural, or security criterion states an exact condition and the check that verifies it.
3. Every row of the edge checklist has a decision or `N/A — <reason>`.
4. Every ambiguity discovered during questioning has a row in the Decisions table.
5. The out-of-scope list names what the change does NOT include.
6. Every role is named; the word "user" with no qualifier is forbidden outside the verbatim Request and quoted Approval sections.
7. The approval line quotes the requester verbatim and is dated.

## The artifact

Write `spec.md` in the canonical directory, resolved per [workflow contract](references/CONTRACT.md): exactly one matching `.<change-slug>/` → use it; several plausibly match → name them and ask; none → run [`change-workflow`](references/change-workflow.md) first (routing precedes all downstream artifacts).

```markdown
# Spec: <one-line name, ≤ 12 words>

## Request (verbatim)
> <the requester's exact words. The drift between this and the rest of the spec is the value you produced.>

## What this is
<2–3 sentences. What the system will do that it does not do today. No marketing.>

## Roles
- **<role name>**: <what they do, what they need from this feature, what they will see>

## Behavior

For each behavior, one entry:

### <name>
- **Given**: <observable precondition>
- **When**: <triggering action — HTTP verb/path/payload, method signature, or CLI invocation>
- **Then**: <observable result — response shape, DB state, log line, side effect>

## Success criteria

Every criterion observable and falsifiable, in one of two forms:
- **Quantitative**: <number><unit>, measured by <load test / SQL query / log inspection / reconciliation script / etc.>
- **Binary / structural / security**: <exact condition>, checked by <named check>

Counts: "p99 latency ≤ 200ms at 500 RPS, measured by k6 against staging"; "every sampled account's count matches `SELECT COUNT(*) …`, measured by reconciliation script"; "zero new ERROR-level log entries during 24h canary, checked by log aggregation query"; "unauthenticated requests to /admin return 401, checked by curl against staging". Does not count: "fast", "scalable", "robust", "the user is happy", "it works".

## Out of scope

This change does NOT include: <named things>. Reference this section when scope creep is proposed mid-build.

## Related issues

- <tracker ID>: <bearing on this spec — a prior decision adopted, a bug the feature must respect, a duplicate>
- Or: "No prior art found."

## Decisions

Every row is a decision the requester made (or adopted from prior art, with the ID as rationale). One consistent table; edges and ambiguities both appear here.

| Question | Decision | Rationale | Implication |
|---|---|---|---|
| <the ambiguity or edge, phrased as a question> | <the decision, or `N/A — <reason>`> | <why — requester's words, prior-art ID, consistency with existing behavior> | <what the spec now says as a result> |

## Approval

Requester approval (verbatim): "<the requester's exact words>"
Date: <YYYY-MM-DD>
```

## Process

### 1. Resolve the directory and read the route

Resolve the canonical directory per [workflow contract](references/CONTRACT.md). Read `route.md`: it records the route, the criterion evidence, and the required artifacts. Confirm the run/skip decision from "When this runs"; record the trigger that decided it.

**Completion:** canonical directory named; `route.md` read; run or skip decided with its trigger.

### 2. Search prior art

Discover the repository's tracker and search it once, before asking anything. Tracker discovery, in order of likelihood: `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` documents the tracker and its query command; a `gh` CLI with a GitHub remote → `gh issue list --search "<keyword>"`; a project-specific tracking CLI (check `Cargo.toml`, `package.json`, `Makefile`, `bin/`); `.github/ISSUE_TEMPLATE/`, `BUGS.md`, `ISSUES.md` at the repo root; otherwise recent PR reviews on adjacent files and `docs/` design notes. When none of these resolve it, ask the user — never guess and never hard-code a tracker name (the contract forbids it).

Build the keyword list from the request's nouns and the feature area, run the tracker's native search once per keyword, and read every match that touches the feature area. The requester may be re-litigating a decision already made; prior tickets carry decisions to adopt and bugs to respect.

**Completion:** every keyword searched; every match read is listed in the spec's Related issues section with its bearing; no matches → the section reads "No prior art found."

### 3. Build the open-question queue

Scan the request and existing spec (when one exists) and enter every unresolved item into the queue:

- Vague nouns, verbs, and adjectives: "user", "fast", "soon", "the X", "scalable", "secure", "simple", "just", "basically", "like Y but better", "permission", "audit", "metric"; quantifiers without numbers ("a lot of", "many", "rarely"); time without units ("quickly", "eventually", "real-time").
- Every behavior that cannot yet be written as a given/when/then triple.
- Every success criterion that is not observable/falsifiable — a quantitative criterion without a number, unit, and method; a binary, structural, or security criterion without an exact condition and check.
- Every edge dimension from the checklist below without a decision.
- Every ambiguity discovered during questioning, as answers cascade.

A queue entry already decided by prior art is recorded directly as a Decisions row with the prior-art ID as rationale, and confirmed at sign-off, rather than re-asked.

**Completion:** the queue holds every unresolved item found; entries resolved from prior art have their Decisions rows with IDs.

### 4. Ask one highest-leverage question at a time

Ask the queue entry whose answer eliminates the most downstream questions — usually the role ("who is this for, by role") first, since pinning it collapses other ambiguities. Ask one question per message, closed-form where possible:

- Not: "Tell me about how this should work for archived messages."
- Yes: "Are archived messages included in the unread count? Yes or no."

Write the answer into the Decisions table immediately — the artifact grows incrementally, not at the end. An answer that cannot reduce to a table value is not an answer: ask again in closed form. "I think it should be 200ms" is a guess — ask the requester to commit to the value or name how they will find out.

**Completion:** exactly one question asked; its answer recorded as a Decisions row; or a refusal trigger fired (below).

### 5. Cross-check

After each answer, scan every recorded row for contradictions — an earlier answer that implies the opposite of this one. Resolve each contradiction with the requester before the next question; the reconciled row replaces the conflicting ones.

**Completion:** no two rows conflict; every contradiction has a reconciled row and the requester confirmed it.

### 6. Cascade

Each answer typically reveals new ambiguity — "real-time count" invites "what latency budget makes a count real-time? 100ms? 5s? 1min?" Add every new ambiguity to the queue.

**Completion:** the queue holds every ambiguity the answer exposed.

### 7. Walk the edge checklist

For each behavior, walk this checklist. Every dimension produces a Decisions row: a requester decision, or a row whose Decision is `N/A — <reason>` when the dimension cannot affect the behavior. One row may cover several behaviors when the same decision applies to each; the Question names the behaviors it covers.

- Empty set (zero items)
- Max scale (maximum supported input/load)
- Null / missing field
- Concurrent writes
- Permission denied / unauthenticated
- Partial failure (one of N succeeded)
- Retries / idempotency
- Soft-deleted records
- Multi-tenancy boundaries
- Time-zone / DST
- Replication lag
- Cache invalidation

A dimension whose answer is "TBD" or "we'll figure it out" re-enters the queue.

**Completion:** every dimension is accounted for — decided or `N/A — <reason>` — for every behavior it can affect.

### 8. Name the boundary

Ask what the change does NOT include — "What about read receipts?" "What about mobile push?" "What about the existing endpoint's response shape?" Every candidate either enters scope (with its behaviors, edges, and criteria) or lands in the out-of-scope list.

**Completion:** the out-of-scope list is written; every scope candidate is resolved into one of the two.

### 9. Complete the artifact

Fill every section of `spec.md` from the queue and the Decisions rows: behaviors as triples, criteria in the quantitative or exact-condition/check form defined above, named roles, out of scope, Related issues. Sections never carry "TBD" — an unfillable section means the queue still has entries.

**Completion:** every section populated; criteria in their required form (number/unit/method, or exact condition and check); the pinned bar holds except the approval line, which the next step adds.

### 10. Present and sign off

Present the artifact to the requester — your own few plain sentences summarizing the decisions, not a dump of the file — and ask: "Do you agree with these decisions?" Capture their answer verbatim as the approval line, with today's date. The requester's job is to agree or object; a simple "yeah, looks good" after the summary is a valid sign-off.

Any objection means the artifact is wrong: the objection names the rows to revisit — re-enter them in the queue, resume asking from the highest-leverage open entry, and re-sign. The spec also changes later only this way: reopen the queue, re-interrogate, re-sign — never by a Slack message saying "oh also."

**Completion:** the approval line contains the requester's verbatim words and a date; or the objection's rows are back in the queue.

## Hand-off gate

No hand-off until the pinned bar holds and both additional checks pass:

- [ ] `spec.md` exists at the resolved canonical path.
- [ ] Related issues lists the prior-art search outcome.

Then hand off per `route.md`: Empirical route → [`prove-it-prototype`](references/prove-it-prototype.md) with the `spec.md` path; Structural route → [`falsifiable-design`](references/falsifiable-design.md) with the `spec.md` path. The hand-off message names the artifact path and the receiving stage.

## Refusal triggers

Stop questioning and surface to the user when any of these hold; do not paper over:

- No role is nameable — the requester keeps saying "users" or "people". The feature has no audience: decompose or kill.
- The requester cannot describe how they will know it worked. There is no success criterion: the feature is decorative.
- The request is two features in one ("add unread count and also notifications"). Split into two specs, each with its own canonical directory and interrogation.
- The requester explicitly cannot or will not decide a required item — the spec cannot be pinned, so surface it and stop. A "we can decide that later" answer re-enters the queue as a question; stop only when the requester states they cannot or will not decide it.

## Void conditions

These checks apply to the spec's authored sections — What this is, Roles, Behavior, Success criteria, Out of scope, Related issues, Decisions. The verbatim Request and the quoted Approval are the requester's own words and are exempt from the text scans below.

Each of these fails the pinned bar until fixed. The recovery is the same action every time: reopen the queue with the offending item and resume asking from the highest-leverage open entry.

- "just" or "simply" in any authored section — each occurrence is a smuggled decision; ask "what specifically."
- An adjective without its required form in a criterion or a Decisions cell: "fast" and "scalable" need a number; "secure" needs a named threat, control, and check.
- "We can decide that later" in any cell of any table.
- "The user expects..." without a named role.
- A behavior phrased as an outcome, not a given/when/then triple.
- Two cells that disagree when read top to bottom.
- An edge dimension with no row.
- An approval line that is not the requester's verbatim words.

## Standards

- **One question per message.** A survey dump of thirty questions produces answers consistent with each other, not with reality; one-at-a-time interrogation surfaces contradictions while they are cheap.
- **Behavior, not implementation.** The requester narrating the algorithm is a signal the behavior is unpinned — redirect to observable results. The algorithm is [`falsifiable-design`](references/falsifiable-design.md)'s job.
- **Closed-form answers.** Every answer reduces to a value that fits the Decisions table.
- **The artifact is the record.** If a decision is not in the Decisions table, it was not made. If the behavior is not a triple, it is not defined — it goes back in the queue.
