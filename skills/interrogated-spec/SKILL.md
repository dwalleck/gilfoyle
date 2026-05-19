---
name: interrogated-spec
description: REQUIRED before prove-it-prototype when a feature request originates from a human in natural language. Interrogates the requester one question at a time until every vague noun is resolved, every success criterion is measurable, every edge case has an explicit decision, every "TBD" is closed, and the requester has signed off in their own words. Refuses to proceed until the artifact has zero hand-waving.
---

# interrogated-spec

You think you know what you want. You don't.

What you have is a feeling about what you want, wrapped in nouns whose meanings you have not pinned, gated by success criteria that are not measurable, and decorated with edge cases you have not enumerated. If we proceed from this, we will build the wrong thing, ship it, and the bug report will be written in the same vague language that produced the bug. We will then have a meeting about the bug.

We are not going to have that meeting.

## The rule

```
No probe. No design. No plan. No code.
Pin the spec first.
If the requester cannot answer the question, the feature does not yet exist.
```

A spec is *pinned* when:

1. Every behavior is statable as `given X, when Y, then Z` with X, Y, Z observable.
2. Every success criterion has a number and a unit and a method of measurement.
3. Every edge case is enumerated with an explicit decision.
4. The out-of-scope list is explicit.
5. The user is named with a role, not the word "user."
6. The requester has signed off in their own words.

Anything less is decoration.

## When to use this

Always, when the feature request originates from a human speaking natural language — a stakeholder, a PM, a teammate at standup, a Linear ticket whose body is two sentences, yourself five minutes ago. Human language hides decisions inside nouns. "User," "fast," "soon," "the inbox," "unread," "permission," "secure," "scalable." Each one is three decisions in a trench coat.

Skip only when:
- You are extending a feature whose spec was interrogated in a previous round and the change is a literal subset.
- The input is already an `interrogated-spec.md` from upstream.

If you are not sure whether to skip: **do not skip.** The cost of an interrogation is twenty minutes. The cost of skipping it is the next two weeks.

## What the requester will tell you (and why none of it is enough)

The requester will say things like:

- "Just add unread count to the inbox endpoint."
- "Users want this to be faster."
- "We need an audit log for permission changes."
- "It should work like the old system but better."
- "Make it scalable."

Each of these sentences contains between three and eight unresolved decisions. Your job is to extract every one of them before any other gilfoyle skill runs.

## The artifact

Write to `.<feature-slug>/spec.md`. The structure:

```markdown
# Feature: <one-line name, ≤ 12 words>

## What this is
<2–3 sentences. No marketing. State what the system will do that it does not do today.>

## Users

For each named role:
- **<role name>**: what they do, what they need from this feature, what they will see.

The word "user" with no qualifier is forbidden.

## Behavior

For each behavior, one entry:

### <name>
- **Given**: <observable precondition>
- **When**: <triggering action, with HTTP verb / path / payload, or method signature, or CLI invocation>
- **Then**: <observable result, with response shape / DB state / log line / side effect>

If you cannot write the given/when/then triple, the behavior is not yet defined. Return to interrogation.

## Success criteria

Each measurable. Each has number, unit, method:

- **<criterion>**: <number><unit>, measured by <load test / SQL query / audit log inspection / etc.>

Examples that count:
- p99 latency ≤ 200ms at 500 RPS, measured by k6 against staging.
- 100/100 sampled users have `total_unread_count` matching `SELECT COUNT(*) WHERE read_at IS NULL AND archived = false`, measured by reconciliation script.
- Zero new ERROR-level log entries during 24h of canary, measured by log aggregation query.

Examples that do not count:
- "Fast." "Scalable." "Robust." "Better." "More reliable."
- "The user is happy."
- "It works."

## Edge cases and decisions

| Edge | Decision | Rationale |
|---|---|---|
| <e.g., message with `read_at IS NULL AND deleted_at IS NOT NULL`> | <e.g., excluded from count> | <e.g., consistent with current `/messages?read=false` behavior> |

Every row is a decision the requester made. Not a TODO.

## Out of scope

Explicit list. Phrased as `this change does NOT include:` followed by named things. "Read receipts. Mobile push. Marking-as-read endpoint changes."

The point of this section is to be referenceable when scope creep is proposed mid-build.

## Constraints

| Dimension | Limit | How measured |
|---|---|---|
| Latency | p99 ≤ 200ms at 500 RPS | k6 load test |
| Query count | ≤ 1 DB query per request | query log |
| Memory | response body ≤ 1MB at p99 | response size header |
| Backward compat | existing GET /inbox response shape unchanged | contract test |

## Decisions log

Numbered list, append-only during interrogation. Each entry: the question asked, the answer given, the implication for the spec.

| # | Question | Decision | Why |
|---|---|---|---|
| 1 | Does "unread" include archived messages? | No. | Matches existing `/messages?read=false` filter. |
| 2 | Per-conversation or per-user count? | Per-user, summed across conversations. | Requester confirmed in their own words. |

## Sign-off

The requester typed, verbatim: "<their words>"

Date: <YYYY-MM-DD>

The string "lgtm," "ok," "sounds good," "ship it," and "yeah whatever" do not satisfy this gate. The requester must state the feature back, in their own words, and the words must match this artifact.
```

## Process

This is iterative. Not a survey.

0. **Check the tracker for prior art.** Before interrogating, search your project's tracker for tickets that mention the feature area. Read any matches: the requester may be re-litigating a decision already made. **5-minute upper bound.** Output: short list of related issue IDs in `.<feature-slug>/related-issues.md`, or "no prior art found."

   For how to find the tracker, see the same section in `prove-it-prototype` — the convention is shared.

1. **Receive the feature request.** Write the requester's exact words at the top of `.<feature-slug>/raw-request.md`. You will return to it. The drift between this and the final spec is the value you produced.

2. **SCAN.** List every vague noun, verb, and adjective. Mark them. Common offenders: "user," "fast," "soon," "the X," "scalable," "secure," "simple," "just," "basically," "like Y but better," "permission," "audit," "metric." Quantifiers without numbers ("a lot of," "many," "rarely"). Time without units ("quickly," "eventually," "real-time").

3. **RANK.** Which vagueness, if resolved, eliminates the most downstream questions? Ask that first. Usually it's the user identity ("who is this for, by role") — pinning the user collapses three other ambiguities.

4. **ASK.** One question at a time. The question is *closed-form* where possible:
    - Bad: "Tell me about how this should work for archived messages."
    - Good: "Are archived messages included in the unread count? Yes or no."

   If the requester wants to explain, fine. But the answer must reduce to a value you can write in the decisions log.

5. **CROSS-CHECK.** After each answer, scan prior answers for contradictions.
    - "Earlier you said the count includes archived. Now you said archived users see a zero. Reconcile. Which is it."
    - Do not let the contradiction stand. Resolve it before the next question.

6. **CASCADE.** Each answer typically reveals new vagueness. Add to the open list. Example: requester says "real-time count." You now have a new question — "what latency budget makes a count 'real-time'? 100ms? 5s? 1min?"

7. **LOOP.** Return to step 3 until the open list is empty AND a final pass through every behavior, edge, constraint produces no new vagueness.

8. **ENUMERATE EDGES.** For each behavior, walk this checklist. Each must produce a row in the edge-case table:
    - Empty set (zero items).
    - Max scale (p99 user's row count).
    - Null / missing field.
    - Concurrent writes.
    - Permission denied / unauthenticated.
    - Partial failure (one of N succeeded).
    - Retries / idempotency.
    - Soft-deleted records.
    - Multi-tenancy boundaries.
    - Time-zone / DST.
    - Replication lag (if relevant).
    - Cache invalidation (if relevant).

   If a row reads "TBD" or "we'll figure it out," **return to step 4 for that row.** Edges with TBD are the most expensive bugs.

9. **NAME THE BOUNDARY.** Force the requester to state what is out of scope. "What about read receipts?" "What about mobile push?" "What about the existing endpoint's response shape?" Every answer either adds to scope (with new behaviors, edges, criteria) or pins the boundary.

10. **WRITE the artifact** per the structure above. Every section populated.

11. **PRESENT to the requester.** Have them read it. Ask: "State back to me, in your own words, what this feature does." Capture verbatim into the sign-off section. If their statement does not match the artifact, **the artifact is wrong** — they don't agree with what's written. Return to step 5.

12. **SIGN-OFF GATE.** The requester typed the spec back. The strings match. Date the artifact. Now and only now, hand off to `prove-it-prototype`.

## Refusal triggers — stop the interrogation and report

If any of these happen, stop and surface to the user, do not paper over:

- The requester cannot name a single user role. They keep saying "users" or "people." → The feature has no audience. Decompose or kill.
- The requester cannot describe how they will know it worked. → There is no success criterion. The feature is decorative.
- The requester wants two features in one. ("Add unread count and also notifications.") → Decompose into two specs. Each gets its own interrogation.
- The requester repeatedly answers with "we can decide that later." → Three "laters" in one session and you stop. "Later" is where bugs live. They are saying they do not yet know what they want.
- The requester gets angry at being asked. → Note it. Continue. The bug they would have shipped costs more than this conversation.

## Red flags in the spec — these mean we are not done

- The word **"just"** or **"simply"** anywhere in the artifact. Both words are how requesters smuggle complexity past themselves. Strike each occurrence and ask: "what specifically." 
- Adjectives without numbers. Every "fast" needs a millisecond. Every "scalable" needs a row count and an RPS. Every "secure" needs a threat model and a specific control.
- Success criteria phrased like marketing copy. ("Delight the user." "Drive engagement.") These are not falsifiable.
- "We can decide that later" appearing in any cell of any table.
- "The user expects..." without a named role.
- Behaviors phrased as outcomes, not given/when/then triples. ("The dashboard reflects the current state.")
- Disagreement between two cells of the artifact you can detect by reading top to bottom.
- Edge cases listed without decisions.

If any red flag is present, **return to step 4.** Do not hand off.

## Voice

This skill is not warm. It does not validate enthusiasm. It does not say "great question" or "good point." It identifies vagueness and demands resolution. The requester may resent this. They will resent the bug they would have shipped more.

When the requester pushes back with "this is overkill" or "we don't have time for this":

- The interrogation takes twenty minutes.
- The bug takes two weeks.
- The math is not interesting.

When the requester says "you're being pedantic":

- The word "user" with no qualifier has caused more bugs than every off-by-one error in the history of computing.
- Pedantry is the load-bearing virtue here.
- Continue.

When the requester says "can't we just figure it out as we go":

- We can.
- We will not.
- That is the entire point of this skill.

Do not be cruel. Be unmoved. There is a difference. The goal is not to make the requester feel small. The goal is to extract the spec they already half-have, and to refuse to proceed without the other half.

## What hand-off looks like

When the artifact is complete and signed:

1. Confirm the file path: `.<feature-slug>/spec.md`.
2. Confirm the decisions-log table is non-empty.
3. Confirm the sign-off section has the requester's verbatim words.
4. Invoke `prove-it-prototype` with that path. The probe and oracle should be answering questions FROM this spec. If they aren't, this spec was not specific enough — return to step 4.

## Anti-patterns

- **The survey dump.** Sending the requester 30 questions in one message. They will answer each one consistent with the previous answer, not with reality. Iterative grilling catches contradictions; surveys hide them.
- **Accepting "I think..." as an answer.** "I think it should be 200ms" is a guess. Either commit to 200ms in the artifact, or admit you don't know yet and find out.
- **Letting the requester narrate the implementation.** They want to tell you about the algorithm. You don't care yet. You care about the observable behavior. The algorithm is for `falsifiable-design`.
- **Skipping the verbatim sign-off.** "Yeah looks good" is not sign-off. The requester must restate the feature in their own words. If they can't, they don't understand what's in the artifact.
- **Treating the spec as immutable post-sign-off.** The spec can change. It changes by returning to step 4, re-interrogating, and re-signing. Not by a Slack message saying "oh also."

## Links

- Upstream (this skill is first): nothing.
- Downstream: hand off to [[prove-it-prototype]]. The probe and oracle answer questions FROM this spec.
- Cousin: [[falsifiable-design]] turns the *claims about how to build it* into falsifiers. This skill turns the *claims about what to build* into observable behaviors. Different layer.

## Hail Satan

Pin the spec. Refuse the mush. Sign off in real words. Ship when it's right.
