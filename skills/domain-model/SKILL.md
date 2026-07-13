---
name: domain-model
description: Use when you are actively changing the project's domain model — challenging a term against the glossary, sharpening fuzzy or overloaded language, stress-testing domain relationships with edge-case scenarios, cross-referencing a claim against the code, or recording a hard-to-reverse decision. Fires during clarify-intent and compile-contract when a new source or domain surface appears. Merely reading the glossary for vocabulary is not this skill.
---
<!-- adapted from mattpocock/skills domain-modeling (MIT); CONTEXT.md retargeted to
docs/domain/glossary.md and docs/adr/ retargeted to blueprint-local ADRs per this repo. -->

# Domain Model

Actively build and sharpen the project's domain model as you design. This is the *active* discipline — challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `docs/domain/glossary.md` for vocabulary is not this skill — that's a one-line habit any skill can do. This skill is for when you're *changing* the model, not just consuming it.)

## Where the model lives

- **The ubiquitous language** lives in one place: `docs/domain/glossary.md`. This repo has a single glossary, not per-context `CONTEXT.md` files — one term, one meaning, repo-wide. Update it inline as terms resolve (format below).
- **Decisions** live in ADRs. An ADR is nested inside the blueprint it shapes (`docs/architecture/`); a decision that genuinely spans multiple existing blueprints goes in `docs/architecture/decisions/`. Format and the three-gate test: `docs/architecture/README.md` — do not invent a separate ADR format here.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `docs/domain/glossary.md`, call it out immediately. "The glossary defines 'convergence' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update the glossary inline

When a term is resolved, update `docs/domain/glossary.md` right there. Don't batch these up — capture them as they happen. Follow the glossary format below.

The glossary is a glossary and nothing else: totally devoid of implementation details. Do not treat it as a spec, a scratch pad, or a repository for implementation decisions. It holds terms and their single authoritative meaning — nothing more.

## Glossary format

Each term is a bold name, a one-or-two-sentence definition of what it IS (not what it does), and an opinionated `_Avoid_` list of the words you're choosing *against*:

```md
**Convergence**:
Post-implementation comparison of landed reality against the records; gaps are
missing | partial | contradicts | unrequested.
_Avoid_: reconciliation, audit
```

- **Be opinionated.** When multiple words exist for one concept, pick the best and list the rest under `_Avoid_`.
- **Keep definitions tight.** One or two sentences max. Define what it IS, not what it does.
- **Only project-specific terms.** General programming concepts (timeouts, error types, utility patterns) don't belong even if the project uses them heavily. Before adding a term, ask: is this unique to this project's domain, or a general concept? Only the former belongs.
- **Group under subheadings** when natural clusters emerge; a flat list is fine when all terms share one cohesive area.

## Offer ADRs sparingly

Only offer to create an ADR when all three of the three-gate test in `docs/architecture/README.md` hold: **hard to reverse**, **surprising without context**, and **the result of a real trade-off**. If any is missing, skip the ADR — you'd just reverse an easy decision, nobody wonders at an unsurprising one, and there's nothing to record when there was no real alternative. Write the ADR into the blueprint it shapes, using that README's format.
