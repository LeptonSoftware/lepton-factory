---
title: Domain Glossary
summary: Ubiquitous language for the Vinxi platform and its factory. One term, one meaning; use these terms exactly in records, code, and conversation.
owners:
  - factory-operators
applies_to:
  - "**"
status: active
last_verified: 2026-07-12
---

# Domain Glossary

A glossary and nothing else: terms and their single authoritative meaning. When a
conversation reveals a new or contested term, add or amend it here in the same Work
Order. Product-domain terms (kernel, ontology, statements, …) get added as the
platform is seeded — factory terms below are already binding.

## Factory terms

- **Acceptance Criterion (AC)** — an atomic, externally observable behavior a
  requirement demands: "When <condition>, the system shall <behavior>." ID `AC-<AREA>-NNN.N`.
- **ADR** — Architecture Decision Record; a decision recorded inside the blueprint it
  affects (cross-cutting: `docs/architecture/decisions/`). Format and the three-gate
  test: `docs/architecture/README.md`.
- **AFK decision** — a decision an agent may make autonomously during execution.
- **Assembly line** — a persistent product area with an accountable owner (Line
  Operator). Where lines are defined: `docs/product/README.md` ("Assembly lines").
- **Blueprint (BP)** — durable architecture record. Container (runnable unit),
  Component (enduring reusable capability), or Feature (composition of components).
- **Contract (Execution Contract)** — `contract.md`: the compiled obligations of a Work
  Order (verbatim ACs, invariants, interfaces, disallowed changes, verification contract).
- **Convergence** — post-implementation comparison of landed reality against records;
  gaps are `missing | partial | contradicts | unrequested`.
- **Coverage (COV)** — the mapping of one AC to its proving test(s). ID `COV-<AREA>-NNN.N`.
- **Drift** — divergence between two layers that should agree (requirement↔blueprint,
  blueprint↔code, plan↔implementation, AC↔coverage). Material drift blocks merge.
- **Factory Operator** — owner of the production system itself (policies, templates,
  skills, tools, CI).
- **Gate** — a mandatory, machine-recorded checkpoint (0 contract, A plan challenge,
  B slice review, C verification audit, D adversarial QA, convergence, final review).
- **HITL decision** — a decision that requires a human (product judgment,
  un-blueprinted architecture, destructive operations). Execution stops on these.
- **Line Operator** — accountable owner of one assembly line end to end. Where lines
  and their operators are recorded: `docs/product/README.md` ("Assembly lines").
- **Module** — the language's namespace unit *inside* a package (ES module, Python
  module, Rust `mod`, Java package). Modules are not units of ownership or
  distribution — ownership and blueprint mapping attach to the Package.
- **Package** — the unit of distribution and ownership: whatever the ecosystem's
  build tool treats as independently buildable/publishable — an npm package, a
  cargo crate, a Python distribution, a Maven/Gradle module. One directory under
  `packages/` is one package in exactly one ecosystem; `packages/` may hold
  packages of different ecosystems side by side.
- **Requirement (REQ)** — externally observable behavior with one user story and ≥1 AC.
  ID `REQ-<AREA>-NNN`. IDs never change after publication.
- **Risk tier** — low/medium/high ceremony level, computed from changed paths;
  humans may raise it, and only a named human may lower it (`risk-tier --set
  --approver`, recorded); agents may do neither on their own judgment.
- **Scratch Work Order (WO-9900+)** — a throwaway WO in the reserved `WO-9900`–`WO-9999`
  range, used only to exercise factory tooling; deleted afterward. Real Work Orders are
  allocated below the scratch floor.
- **Slice** — one vertical, independently verifiable increment of a plan (tracer bullet
  first).
- **Tracer bullet** — the thinnest end-to-end slice that proves the architecture before
  breadth is added.
- **Verification Contract** — the per-AC table {automated test, runtime action,
  expected evidence, negative case} inside `contract.md`; Gate C audits it.
- **Work Order (WO)** — the bounded delivery contract connecting intent and
  architecture to execution. ID `WO-NNNN`. The only task queue.

## Product terms

_To be populated as the platform is seeded (kernel, data fabric, ontology, statement,
trait, connector, agentic plane, …). Do not use a product term in a record before it
is defined here._
