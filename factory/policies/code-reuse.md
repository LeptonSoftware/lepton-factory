---
title: Code Reuse Policy
summary: Executable rules for shared packages, domain-model duplication, dumping grounds, and reuse-before-invention analysis in plans.
owners: [factory-operators]
applies_to: ["apps/**", "packages/**", "services/**", ".factory/work-orders/**"]
status: active
last_verified: 2026-07-12
---

# Code Reuse Policy

Exception process for every rule: ADR (format: `docs/architecture/README.md`) +
owner approval before the exception lands.

## 1. No shared package without two consumers or a platform contract

**Rule.** A package ships under `packages/` only when at least two real consumers
exist in-tree, or a Component Blueprint documents it as a platform contract with
named intended consumers and an owner. Until then, code lives beside its only
consumer.

- **Applies to.** `packages/**`
- **Enforcement.** Gate A (challenge-plan) rejects plans introducing single-consumer
  packages without a blueprint; Gate B verifies against the `blueprints:` map in
  `.factory/config.yaml`.
- **Exceptions.** ADR + owner approval.
- **Owner.** factory-operators

## 2. No duplicated domain models without a boundary reason

**Rule.** One domain concept, one model. Modeling the same concept in two packages
requires a recorded boundary reason (an ADR naming why the contexts diverge —
different invariants, different lifecycle, different owner). Otherwise the concept
is shared through the owning package's published contract.

- **Applies to.** `packages/**`, `apps/**`, `services/**`
- **Enforcement.** Review (Gate B spec-compliance + final review blueprint-alignment
  dimension), guided by `docs/domain/glossary.md`; no mechanical check exists yet.
- **Exceptions.** ADR + owner approval.
- **Owner.** factory-operators

## 3. No generic dumping grounds

**Rule.** Packages and top-level modules are named for a capability. `utils`,
`common`, `helpers`, `shared`, `misc`, and `lib` are forbidden as package or
top-level directory names. Recipe: name the capability the code provides; if you
cannot name it, it is not a package yet — keep it beside its only consumer.

- **Applies to.** `packages/**`, `apps/**`, `services/**`
- **Enforcement.** Path-name lint in CI (quality workflow); review until the lint
  lands.
- **Exceptions.** ADR + owner approval.
- **Owner.** factory-operators

## 4. Every shared package has a Component Blueprint and an owner

**Rule.** Every package under `packages/` has a `BP-COMP-*` in
`docs/architecture/components/` and an entry (paths + owner) in the `blueprints:`
map in `.factory/config.yaml`. No orphan shared code.

- **Applies to.** `packages/**`, `.factory/config.yaml`
- **Enforcement.** Review until the check lands (planned: ownership-map check on
  changed `packages/` paths in `tools/agent/validate-work-order`, failing unmapped
  paths — no such check exists today).
- **Exceptions.** ADR + owner approval.
- **Owner.** factory-operators

## 5. Reuse-before-invention analysis is required in plans

**Rule.** Before a plan introduces any new abstraction, its "Code Reuse And Package
Structure" section records: components searched, analogous code inspected, and the
chosen option among reuse / extract / follow-pattern / new — with layer
justification, intended consumers, and owner when the choice is "new". Defined in
`.factory/README.md` §6; this rule makes it a gate.

- **Applies to.** `.factory/work-orders/*/implementation-plan.md`
- **Enforcement.** Plan template section (`.factory/templates/implementation-plan.md`)
  must be substantively filled; Gate A (challenge-plan) returns `REVISE` when it is
  empty or placeholder text.
- **Exceptions.** None — a plan that invents nothing states so in one line.
- **Owner.** factory-operators
