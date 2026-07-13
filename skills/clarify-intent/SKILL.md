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

- Drive until the ambiguity is resolved, not to a fixed count. Order the Partial/Missing categories by Impact × Uncertainty and work down them relentlessly — the session ends when every high-impact category is Resolved or consciously Deferred with a rationale, however many questions that takes. Do not stop early because a quota is hit; do not manufacture questions once nothing material is left unclear.
- **Batch independent questions into one round.** Ask the questions that don't depend on each other *together*, as a numbered list (aim for 3–5 per round — readable at a glance), and let the human answer them in a single pass. Go one-at-a-time *only* when an answer genuinely forks the next question (a real dependency): ask that gating question alone, then batch the rest once it's resolved. Relentless total depth — many questions across several rounds — is the discipline; drip-feeding one question at a time is not, it just wastes the human's time.
- Each question is answerable by multiple choice (2–5 mutually exclusive options) or "answer in ≤5 words", with your recommended answer first: `**Recommended:** Option B — <reasoning>`. Recommended-first is what makes a batch fast: the human rubber-stamps the defaults (`1, yes, B, defer`) and argues only the ones they care about. Number the questions so answers map unambiguously.
- **Isolate the pivotal decision; batch the routine.** Batching + defaults invites rubber-stamping — people accept a pre-filled recommendation they'd have argued if asked alone. So the one or two questions with the highest Impact × Uncertainty are asked *singly and deliberately*, without a rubber-stampable default ("this one is load-bearing — how do you want it, and why?"), while the low-stakes independent questions batch with defaults. Never bury the decision that matters inside a list of five.
- **A batch is a round, not the end.** Read the answers before moving on: a surprising or load-bearing answer spawns a sharper follow-up round — that adaptive thread is where grilling earns its depth. Batching trades away *per-question* adaptivity for speed; keep it at the *round* level by always asking "does this answer change what I should ask next?"
- When the ambiguity is a domain term — a fuzzy, overloaded, or glossary-conflicting concept (category 8) — run the `domain-model` skill to challenge and sharpen it, and record the resolution in `docs/domain/glossary.md`. When the request enters territory new to this WO (an unfamiliar source, domain, or subsystem), run `wayfinder` first to map what is known / assumed / unknown, so the unknowns become explicit questions here rather than silent gaps.

## Route answers into records

After each round, write every accepted answer into the right record before opening the next round — don't let a batch of resolved decisions sit only in the chat:

- functional behavior → REQ/AC draft in `docs/product/features/` (marked proposed — humans approve product intent)
- structure or invariant → the owning Blueprint (marked proposed)
- scope or decision classification → the WO (In/Out of Scope, HITL list)
- terminology → `docs/domain/glossary.md`

If the answer invalidates an earlier statement, replace that statement — leave no obsolete contradictory text.

## Stop-gate

Do not proceed to authoring, contract, or plan until the human confirms shared understanding. End with a coverage report: each category Resolved / Deferred (with rationale) / Clear / Outstanding. Deferred high-impact items become Known Unknowns or HITL entries in the downstream contract.
