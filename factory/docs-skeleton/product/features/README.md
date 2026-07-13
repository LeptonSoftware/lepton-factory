---
title: FRD Authoring Guide
summary: How to write Feature Requirements Documents — REQ/AC format, user stories, authoring rules, and the requirements-quality checklist.
owners: [product-owner]
applies_to: ["docs/product/features/**"]
status: active
last_verified: 2026-07-12
---

<!-- authoring craft adapted from 8090-inc/software-factory-plugin
requirements-writing-guide.md (MIT) -->

# Writing Feature Requirements Documents

One FRD per feature at `docs/product/features/<feature>/requirements.md`. FRDs
hold the `REQ`/`AC` records that blueprints, work orders, and COV-tagged tests
trace to (`.factory/README.md` §1). ID grammar is machine-checked against
`.factory/config.yaml` `ids`.

Two layers of requirements. **Product Overview Documents** (`../overview/`) carry
the product-wide *why and what* in plain language for the whole company — Business
Problem, Current State, Personas, Product Description, Success Metrics, Technical
Requirements. They are durable motivation and context, not feature specs; they are
human-authored (agents propose, product approves). **FRDs** carry the localized
feature *why* (the user story) and *what* (the acceptance criteria) and are what this
guide is about.

## FRD structure

```markdown
## Overview        # 1-2 paragraphs: the feature, in persona terms
## Terminology     # feature-local terms; anything durable moves to docs/domain/glossary.md
## Requirements    # the REQ/AC records
```

## Requirement format

Each requirement is a `REQ-<AREA>-NNN` with a name, exactly one user story, and
atomic acceptance criteria:

```markdown
### REQ-STREAM-004: Stream Cancellation

As an operator, I want to cancel an in-flight agent stream, so that a runaway
agent stops consuming its session.

- AC-STREAM-004.1: When the operator cancels a running stream, the system shall
  stop emitting events for that stream within 2 seconds.
- AC-STREAM-004.2: When a stream is cancelled, the system shall release the
  stream's session and mark it `cancelled` in the session log.
- AC-STREAM-004.3: When cancellation is requested for an already-completed
  stream, the system shall return a no-op acknowledgement and change nothing.
```

- **User story**: `As a <role>, I want <action>, so that <outcome>.` The `<role>`
  must be a persona from `../overview/personas.md`.
- **AC**: `AC-<AREA>-NNN.N` in the form
  `When <condition>, the system shall <observable behavior>.` One behavior per AC.
  Modality: `shall` = binding, `should` = strong default, `may` = optional.

## Rules

- **IDs never change after publication.** Superseded requirements are marked
  `status: deprecated` in prose, never renumbered or reused
  (`.factory/README.md` §1).
- **Observable behavior only.** No implementation mechanisms (frameworks,
  storage, internal components) unless externally binding — a contractual API
  shape or a compliance obligation from
  `../overview/technical-requirements.md`.
- **Atomic ACs.** If an AC needs "and" between two behaviors, split it — each AC
  must be independently coverable by a `COV-` test.
- **No prose copying downstream.** Blueprints and WOs link IDs; the only
  sanctioned copy is the verbatim AC block in an execution contract
  (`.factory/templates/contract.md`).
- **Glossary terms exactly.** A concept without a glossary entry gets one in the
  same PR (`docs/domain/glossary.md`).

## Split, merge, or nest a feature

Getting the feature boundary right matters as much as the ACs:

- **Split** into separate FRDs when each part passes the feature test on its own
  (delivers value independently), or when different personas own different parts.
- **Keep as one** feature when the requirements break without each other, they
  complete one task together, or the whole thing fits in one sentence.
- **Nest** a child feature (its own FRD, IDs suffixed — `REQ-AUTH-PR-001` under an
  `AUTH` parent) when the parent already delivers value on its own, the child only
  *enhances* the parent, and the child is meaningless without it. A child that the
  parent needs in order to function is not a child — it belongs in the parent.

## Requirements-quality checklist

Unit tests for the English. Run before publishing or amending an FRD; every
finding cites the REQ/AC it questions. Items interrogate what is *written*
("Is 'fast' quantified?"), never the implementation ("Verify the page loads
fast").

- [ ] No vague adjectives — *fast, scalable, secure, intuitive, robust, seamless* —
  without a measurable criterion attached.
- [ ] No "handled appropriately"-type phrases; every failure path names its
  observable behavior.
- [ ] Every AC is testable: an observable condition and an observable behavior,
  measurable where quantity matters.
- [ ] No unresolved `[NEEDS CLARIFICATION]` markers. Unresolvable ones are moved
  to an explicit open-questions note with an owner, not left inline.
- [ ] No implementation details, unless externally binding (state which binding).
- [ ] Scope is bounded: out-of-scope behavior is stated explicitly, not implied.
- [ ] Edge cases present: empty, duplicate, concurrent, unauthorized, and
  already-done conditions each have an AC or an explicit exclusion.
- [ ] Traceability floor: every REQ has at least one AC; every AC belongs to
  exactly one REQ; at least 80% of review findings on this FRD cite a REQ/AC ID.
- [ ] Roles come from `personas.md`; terms come from the glossary.
