---
title: Product Documentation
summary: How product intent is recorded — the six overview docs and per-feature FRDs with REQ/AC records; human approval required for all changes.
owners: [product-owner]
applies_to: ["apps/**", "packages/**", "services/**"]
status: active
last_verified: 2026-07-12
---

# Product Documentation

Product-intent class: agents propose, a human approves (`docs/README.md`). These
docs outrank everything below safety in the precedence order
(`.factory/README.md` §7) — an implementation plan that conflicts with them is
wrong by definition.

Two kinds of record live here:

- **`overview/`** — durable product-wide context, in the six 8090 product-overview
  documents: business problem, current state, personas, product description,
  success metrics, technical requirements. Slow-changing; read before authoring
  any feature.
- **`features/<feature>/requirements.md`** — Feature Requirements Documents (FRDs)
  holding the `REQ-<AREA>-NNN` / `AC-<AREA>-NNN.N` records that Work Orders link
  to. Authoring guide: `features/README.md`.

## Assembly lines

An assembly line is a persistent product area with an accountable owner — its Line
Operator (`docs/domain/glossary.md`). Lines are defined in `.factory/config.yaml`
under a `lines:` block (to be added with the first product line; the Line Operator
owns the entry). Until the first line is declared, no line exists — the pilot Work
Order runs line-less by design.

Rules that apply everywhere here:

- IDs never change after publication (`.factory/README.md` §1).
- Requirements state observable behavior only; structure and mechanisms belong to
  blueprints (`docs/architecture/`).
- Use `docs/domain/glossary.md` terms exactly; a new term means a glossary change
  in the same PR.
- Feedback that implies a requirement change is routed here as a proposal, never
  absorbed silently (`.factory/README.md` §8).
