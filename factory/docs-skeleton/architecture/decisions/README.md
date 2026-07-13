---
title: Cross-cutting ADRs
summary: Architecture decisions that span multiple blueprints. Blueprint-local decisions live inside their blueprint, not here.
owners:
  - factory-operators
applies_to:
  - docs/architecture/**
status: active
last_verified: 2026-07-12
---

# Cross-cutting Architecture Decision Records

Most ADRs belong **inside the blueprint they affect** — keep the decision next to the
structure it shaped. Use this directory only when a decision genuinely spans multiple
blueprints (e.g. "all services use event-sourced persistence").

Format and the three-gate test (write an ADR only when the decision is hard to
reverse, surprising, and a real trade-off) are defined once, in
`../README.md` — this directory adds no rules of its own. ADRs here are numbered
`ADR-NNN` within this directory.
