# tdd-scoped

Use focused tests to establish the behavior a caller needs. Unit checks do not alone prove real consumer integration, native lifecycle behavior, or an actual performance requirement; those remain with [`checkpointed-build`](references/checkpointed-build.md).

## When this stage runs

Inside a slice or bounded repair when new/fixed behavior needs focused coverage. Read [workflow contract](references/CONTRACT.md) and the relevant slice's Outcome, Changes, Verification, and any Dependencies. Reuse existing behavioral tests where they already cover the outcome; adding or editing a function alone does not require another test.

For bugs, preserve the real regression reproducer and observed defect sensitivity under [`falsifiable-design`](references/falsifiable-design.md)'s **Mutation sensitivity**. Routine review-requested coverage for already-correct behavior does not itself require a mutation. Required repository checks and named uncovered mechanisms retain their applicable additional proof.

## The cycle

### RED — establish the missing behavior

For behavior being added or fixed, run a focused existing or new test against the pre-change state and observe the intended failure, then preserve that evidence. A test green on the buggy baseline does not demonstrate repair. Prefer actual pre-fix red/post-fix green; if a baseline is unavailable, use the design's smallest controlled defect-sensitivity alternative and record the limitation.

Name observable behavior rather than implementation, and use real code where possible. Mocks are for genuinely external boundaries, not echoes of the implementation. Group equivalent cases; boundary cases should discriminate plausible consumer-visible failures. Coverage-only work on already-correct behavior records that fact and its observed result without inventing a red state.

### GREEN — implement the behavior

Write the simplest correct implementation that covers the behavioral class, not only the test's exact input. Observe the focused test pass and establish that affected coverage still passes. Reuse applicable evidence under Evidence validity; changes invalidate only dependent conclusions.

### REFACTOR — preserve the contract

Remove duplication, improve names and ownership, and reuse source/dependency helpers. Recheck evidence invalidated by the refactor. Keep reasonable algorithmic/resource behavior; performance verification is required for actual obligations in Verification, not a universal per-loop BUDGET step. A real performance bound remains part of correctness and uses the design's Performance-fence policy at the appropriate checkpoint.

When semantics change, check whether the symbol name still describes them. Rename misleading symbols with symbol-aware caller analysis and text-search safety nets; migrate every caller atomically. A name that remains accurate needs no receipt.

## Completion / Output

The relevant behavior is covered by existing or new tests, new/fixed behavior has observed sensitivity as applicable, affected checks pass with valid evidence, and cleanup/naming preserves all callers and obligations. Record results once in the owning slice/repair record, not per-function or per-loop template rows. Required consumer, native, assembled repository, and independent-review proof remains with checkpointed-build; a green unit test is not final workflow completion.
