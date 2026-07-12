---
name: clarify-intent
description: Use when the intent behind a request, Requirement, or Work Order is ambiguous — before authoring records, compiling a contract, or planning. Use when a record contains vague adjectives, unstated scope, missing acceptance signals, or decisions only a human can make.
---
<!-- adapted from mattpocock/skills grilling (MIT) and github/spec-kit clarify.md (MIT) -->

# Clarify Intent

Interview the human relentlessly about every aspect of the intent until you reach a shared understanding, then write each answer into the authoritative record. The output is edits to REQ/AC records (`docs/product/features/`), Blueprints (`docs/architecture/`), the WO, or `docs/domain/glossary.md` — never a standalone brainstorm doc.

## Facts vs decisions

If a *fact* can be found by exploring the codebase or the records, look it up rather than asking. The *decisions* are the human's — put each one to them and wait for the answer. A clarifier that answers its own questions has broken the protocol.

## Scan before asking

Scan the record or request across these 11 categories, marking each Clear / Partial / Missing:

1. Functional scope & behavior (including explicit out-of-scope declarations)
2. Domain & data model (identity, uniqueness, lifecycle, state transitions, volume)
3. Interaction & UX flow (error, empty, and loading states)
4. Non-functional qualities (performance, reliability, observability, security/privacy, compliance)
5. Integration & external dependencies (failure modes, versioning)
6. Edge cases & failure handling (concurrency, rate limits, conflict resolution)
7. Constraints & tradeoffs (including rejected alternatives)
8. Terminology & consistency (against `docs/domain/glossary.md` — use its terms exactly)
9. Completion signals (testable ACs, measurable definition of done)
10. Placeholders & vague adjectives ("fast", "robust", "intuitive" with no measurable criterion)
11. Human-decision surface (product judgment, un-blueprinted architecture, destructive operations)

## Ask

- Maximum 5 questions per session. If more categories are Partial/Missing, take the top 5 by Impact × Uncertainty; the rest are Deferred.
- One question at a time, waiting for the answer before continuing — multiple questions at once are bewildering. Never reveal queued questions in advance.
- Each question is answerable by multiple choice (2–5 mutually exclusive options) or "answer in ≤5 words", with your recommended answer first: `**Recommended:** Option B — <reasoning>`. A plain "yes" accepts the recommendation.

## Route each answer immediately

After EACH accepted answer, write it into the right record before asking the next question:

- functional behavior → REQ/AC draft in `docs/product/features/` (marked proposed — humans approve product intent)
- structure or invariant → the owning Blueprint (marked proposed)
- scope or decision classification → the WO (In/Out of Scope, HITL list)
- terminology → `docs/domain/glossary.md`

If the answer invalidates an earlier statement, replace that statement — leave no obsolete contradictory text.

## Stop-gate

Do not proceed to authoring, contract, or plan until the human confirms shared understanding. End with a coverage report: each category Resolved / Deferred (with rationale) / Clear / Outstanding. Deferred high-impact items become Known Unknowns or HITL entries in the downstream contract.
