# interrogated-spec

Pin the requested observable outcomes in `spec.md`, asking only for unresolved behavior, compatibility, scope, safety, or accepted-risk decisions. Implementation choices belong to design; being measurable does not make an algorithm, internal state, knob, or cleanup timer an acceptance criterion.

## When this runs

Run when `route.md` requires a spec because a material outcome or boundary is unresolved, or when a signed spec no longer covers changed behavior or scope. Explicit behavior can skip interrogation even when expressed in ordinary prose. Adopt a signed spec that already covers the request.

Read [workflow contract](references/CONTRACT.md) first for artifact resolution, ownership, approvals, evidence validity, and tracker taxonomy. This stage owns `spec.md`; routing precedes it.

## The pinned bar

The spec is ready when:

- Requested outcomes, compatibility, important errors, safety boundaries, and scope are clear enough to implement and verify.
- Criteria describe consumer-visible results. Quantitative requirements name the actual consumer latency/safety or other performance need, units, and measurement; exact behavioral conditions need no invented numerical deadline.
- Equivalent cases are grouped. Given/when/then is useful where it clarifies a transition, not a required separate entry for every case.
- Material unresolved decisions and contradictions are resolved; internal implementation ambiguity alone does not block approval.
- Reference fidelity and any accepted risks are recorded when applicable.
- The requester has approved the decisions, verbatim and dated, or approval is recorded under the contract's delegated-approval rule.

## The artifact

Write the following sections in the canonical `spec.md`; omit inapplicable sections under the contract rather than filling them with repeated N/A rows:

- **Request (verbatim)** — the requester's words.
- **What this is / Behavior** — requested outcomes and relevant preconditions, triggers, results, important errors, and compatibility. Name audiences or roles where their distinction affects behavior.
- **Success criteria** — observable results and how to check them; numerical bounds only for actual requirements.
- **Out of scope** — the boundary of this change.
- **Related issues** — consulted prior decisions/defects and their bearing, or the search outcome.
- **Decisions** — only real product, compatibility, scope, safety, fidelity, and risk decisions: question, decision, rationale, implication.
- **Approval** — dated requester words or the contract's delegated approval; accepted risks explicitly identified.

## Process

### 1. Resolve the directory and read the route

Resolve the canonical directory under the contract. Read `route.md` and any current spec. Confirm which observable decisions remain unresolved; reuse settled decisions.

**Completion:** the route and applicable existing spec are identified, with a bounded set of material open decisions or a justified skip.

### 2. Search prior art

Before asking, discover the repository's tracker from its instructions, remote/CLI, manifests, or issue templates. Search relevant feature nouns and read matches bearing on the request. If the tracker cannot be discovered, ask rather than guessing its name. Adopt applicable prior decisions with source references; do not ask the requester to rediscover repository facts.

**Completion:** Related issues records consulted evidence and its bearing, or that no relevant prior art was found.

### 3. Build the open-question queue

Include only unresolved choices that could change observable behavior, compatibility, scope, safety, or accepted risk. Use the following edge checklist to discover relevant questions, not to generate a per-behavior decision/N/A matrix:

- empty, missing, or maximum supported input;
- concurrency, partial failure, retries, and idempotency;
- permission, authentication, and tenancy boundaries;
- deletion, time-zone/DST, replication lag, and cache consistency where consumers can observe them.

Group cases governed by the same decision. For a port or replacement, establish **reference fidelity**: byte-identical, equal parsed values/order, or equivalent behavior, and which reference defects are preserved versus fixed. Preserve the real compatibility tradeoff; the contract reserves this decision to the requester unless specifically delegated.

**Completion:** the queue contains material unresolved decisions, not every possible internal branch or wording ambiguity.

### 4. Ask and reconcile

Ask one highest-leverage question at a time. Present options as behavioral tradeoffs; never bundle an algorithm, internal state machine, tuning knob, or arbitrary timer into product approval. Seek a precise outcome, not a forced closed-form value when explanation is needed. A deadline question needs an actual consumer latency or safety requirement; otherwise leave timing strategy to design.

Record each decision immediately. Compare it with existing decisions, resolve contradictions with the requester, and add newly exposed material questions. Record prior-art decisions with their sources rather than re-asking them. Clarify audience only when it changes the outcome; generic role wording is not a refusal trigger.

**Completion:** the material queue is resolved and the decisions agree. Unspecified implementation detail remains for design.

### 5. Name the boundary and complete the artifact

Resolve real scope candidates into in-scope outcomes or the out-of-scope boundary. Apply the contract's tracker taxonomy to intended future work. Write the behavior and criteria in the clearest form; do not invalidate outcomes for lacking a separate given/when/then triple or for using a forbidden word.

**Completion:** the pinned bar holds except approval, with no missing required decision disguised as a placeholder.

### 6. Present and sign off

Summarize the behavior, compatibility, scope, important errors, and any fidelity/risk decisions. Ask whether the requester agrees; record the dated response under the contract. An objection reopens only affected decisions and their dependencies. Later changed product decisions require revised approval; technical implementation detail does not.

**Completion:** the spec's applicable decisions have valid approval.

## Refusal triggers

Surface to the requester when no observable success can be described, the request bundles separate features requiring separate scopes, or the requester explicitly cannot or will not decide a necessary behavior/safety/scope item. Explain the specific missing decision; do not manufacture refusal from wording or an unchosen implementation knob.

## Hand-off gate

`spec.md` exists, satisfies the pinned bar, records prior-art findings, and has valid approval. Hand off its path per `route.md`: Empirical → [`prove-it-prototype`](references/prove-it-prototype.md); Structural → [`falsifiable-design`](references/falsifiable-design.md). No unresolved required product decision crosses the hand-off.
