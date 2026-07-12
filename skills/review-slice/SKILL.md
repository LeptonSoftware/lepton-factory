---
name: review-slice
description: Use when a slice is implemented and needs Gate B review, or when wo-review requests a diff review. Dispatches one independent reviewer producing two ordered verdicts.
---
<!-- two-ordered-verdicts shape, Do-Not-Trust-the-Report, and plan-mandated-defect tripwire adapted from obra/superpowers subagent-driven-development task-reviewer prompt (MIT); smell baseline adapted from mattpocock/skills code-review (MIT), after Fowler -->

# Review a Slice (Gate B)

Reviewer tier: per `.factory/policies/model-routing.md` — never lighter than the implementer.

Dispatch ONE fresh-context reviewer producing TWO ORDERED verdicts: spec compliance first, then engineering quality. Independence rules from `.factory/README.md` §4, restated because this brief must be self-contained: the reviewer is never the implementer; reviewers never modify product code; a reviewer must flag defects even when the plan mandates them.

## What the reviewer receives

- the diff as a file — from the slice's recorded BASE commit, not HEAD~1 (multi-commit slices stay intact) — with commit list and stat
- `contract.md` (verbatim ACs, invariants, disallowed changes, verification contract)
- `.factory/policies/` and the smell baseline below, pasted in full — the reviewer has no other access to it
- build/test/run instructions

## What the reviewer must NOT receive

- the implementer's self-justification or report — "kept it simple deliberately" is the implementer grading their own work; a stated rationale never downgrades a finding
- conversation history
- any instruction about what not to flag. If the dispatch you are writing contains "do not flag", "don't treat X as a defect", or "at most Advisory" — stop: you are pre-judging.

## The brief (paste into the dispatch)

> Review this diff in two ordered parts; report Part 1 before Part 2.
>
> **Part 1 — Spec compliance against contract.md.** *Missing:* ACs or contracted behavior skipped, or claimed without implementation. *Extra:* behavior no record asked for — scope creep, over-engineering. *Misunderstood:* the right feature built the wrong way. For each AC in scope for this slice, report satisfied / not satisfied / cannot-verify-from-diff (⚠) with acceptance evidence at file:line. Every ⚠ must be resolved by the dispatcher before the slice is marked complete.
>
> **Part 2 — Engineering quality against .factory/policies/.** Placement (right layer and package per blueprint ownership); interfaces (names and types match the plan's Components And Flow); reuse (new code duplicating an existing capability is a finding); error handling; tests (assert real behavior, not mock call counts; negative cases present; output pristine). Then the smell baseline — each smell is a judgment call, a documented repo policy overrides it, and skip anything tooling already enforces: Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest.
>
> If the plan or contract explicitly mandates something this rubric calls a defect, that IS a finding — report it labeled plan-mandated. The plan's authorship does not grade its own work; the human decides.
>
> Severity per finding: Blocking (this slice cannot be trusted until fixed) or Advisory — with file:line, what, why, and the required correction. Verdict per part, then overall, exactly: APPROVED | CHANGES_REQUESTED.

## Record

Append the two verdicts and findings to review-log.md (append-only, dated, reviewer identified); emit each Blocking finding as a repair item in checklist.md; then
`tools/agent/update-state --wo WO-XXXX --gate slice_reviews=<approved|changes_requested>`.
CHANGES_REQUESTED → the implementer repairs, then a FRESH review of the repaired diff — not a comment-by-comment recheck.
