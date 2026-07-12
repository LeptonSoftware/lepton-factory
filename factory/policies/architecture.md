---
title: Architecture Policy
summary: Executable rules for dependency direction, domain boundaries, blueprint coverage, and module depth in product code.
owners: [factory-operators]
applies_to: ["apps/**", "packages/**", "services/**"]
status: active
last_verified: 2026-07-12
---

# Architecture Policy

Each rule is executable: statement, scope, enforcement mechanism, exception process,
owner. "Review" as an enforcement mechanism means Gate B (review-slice,
engineering-quality verdict) plus the final review's architecture dimension —
used only where no mechanical check exists yet. Exception process for every rule:
record an ADR (format: `docs/architecture/README.md`) and obtain the owner's
approval before the exception lands.

## 1. Dependencies point downward

**Rule.** `apps/` and `services/` import from `packages/`. `packages/` never import
from `apps/` or `services/`. One runnable unit never imports another runnable unit's
internals — runnable units integrate through published contracts (APIs, events,
schemas), not source imports.

- **Applies to.** `apps/**`, `services/**`, `packages/**`
- **Enforcement.** Import-boundary lint in CI (quality workflow) once product code is
  seeded; review until the lint lands.
- **Exceptions.** ADR + owner approval.
- **Owner.** factory-operators

## 2. Cross-domain imports go through published contracts

**Rule.** A package imports another domain's package only through its published entry
point — whatever the ecosystem's visibility mechanism exports: the `exports` map
(npm), `pub` items of the crate root (cargo), the documented top-level module /
`__all__` (Python), exported packages or the API jar (Java). Deep imports into
another package's internals (`<pkg>/src/...` and equivalents) are forbidden.
"Package" is language-neutral: `docs/domain/glossary.md`.

- **Applies to.** `packages/**`
- **Enforcement.** Per-ecosystem boundary check, named per language in the owning
  container blueprint's toolchain ADRs — dependency-cruiser (TS/JS), import-linter
  (Python), cargo-deny + crate visibility (Rust), ArchUnit or jdeps (Java). Planned;
  review until the lint lands — a lint for one ecosystem does not satisfy this row
  for the others.
- **Exceptions.** ADR + owner approval.
- **Owner.** factory-operators

## 3. No circular dependencies

**Rule.** The package dependency graph is acyclic. A cycle between packages is a
defect regardless of whether the toolchain tolerates it.

- **Applies to.** `apps/**`, `services/**`, `packages/**`
- **Enforcement.** Dependency-cycle check in CI (quality workflow); review until the
  check lands.
- **Exceptions.** None — break the cycle by extracting the shared dependency downward
  or inverting it behind a contract.
- **Owner.** factory-operators

## 4. Structural changes require a blueprint

**Rule.** No new runnable unit without a `BP-CONT-*` and no new shared capability
without a `BP-COMP-*` before implementation code lands. Every blueprint gets an entry
in the `blueprints:` ownership map in `.factory/config.yaml` (paths + owner). An
un-blueprinted architecture decision mid-execution is a judgment failure — stop and
escalate (`AGENTS.md`, non-negotiable 8).

- **Applies to.** `apps/**`, `services/**`, `packages/**`, `.factory/config.yaml`
- **Enforcement.** Review until the check lands (planned: blueprint-path coverage
  in `tools/agent/validate-work-order` — it does not inspect the diff today);
  Gate B checks new structure against the ownership map.
- **Exceptions.** ADR + owner approval.
- **Owner.** factory-operators

## 5. Design deep modules (review guidance)

**Rule.** Reviewers evaluate module shape against these heuristics. They are
judgment calls, never hard violations; a documented repo standard overrides them.

- **Deletion test**: imagine deleting the module. If complexity vanishes, it was a
  pass-through; if complexity reappears across N callers, it was earning its keep.
- **Depth is leverage at the interface**: the behavior a caller (or test) can
  exercise per unit of interface they must learn. Prefer fewer, deeper modules.
- **The interface is the test surface**: needing to test past the interface means
  the module is probably the wrong shape.
- **One adapter means a hypothetical seam; two adapters means a real one**: don't
  introduce a seam unless something actually varies across it.

- **Applies to.** `apps/**`, `services/**`, `packages/**`
- **Enforcement.** Review (Gate B engineering-quality verdict; no mechanical check
  exists for module depth).
- **Exceptions.** Not applicable — guidance, not a gate.
- **Owner.** factory-operators
