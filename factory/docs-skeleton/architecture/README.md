---
title: Architecture Documentation Guide
summary: Blueprint taxonomy (Container/Component/Feature), component-block and graph-edge conventions, required contract sections, and ADR rules.
owners: [factory-operators]
applies_to: ["docs/architecture/**"]
status: active
last_verified: 2026-07-12
---

<!-- authoring craft adapted from 8090-inc/software-factory-plugin
blueprint-writing-guide.md (MIT) -->

# Architecture Documentation

Blueprints are the authoritative record of structure, contracts, and invariants
(`.factory/README.md` §1). Requirements say *what must be true*; blueprints say *how
the system is structured and behaves* to make it true. They trace up to Requirements
and down to code symbols, contracts, and runtime interactions. Architectural class:
propose + review (`docs/README.md`). Blueprints are written diagrams: structured
blocks define nodes, prose relationship paragraphs define edges.

## Blueprint taxonomy

| Type | ID | Lives in | Create one when… |
|---|---|---|---|
| **Container** | `BP-CONT-<NAME>` | `containers/` | A new runnable/deployable unit exists or is planned: an app, service, or worker with its own process, deploy, and infrastructure. |
| **Component** | `BP-COMP-<NAME>` | `components/` | An enduring reusable capability exists: a shared package or subsystem with more than one consumer, or a documented platform contract (`.factory/policies/code-reuse.md` §1). |
| **Feature** | `BP-FEAT-<NAME>` | `features/` | A feature composes multiple components, or introduces feature-specific components worth documenting. Thin features that fit inside one component don't need one. |

ID convention: `<NAME>` is upper-kebab (`BP-COMP-FACTORY-HARNESS`); the file name
matches the ID (`components/BP-COMP-FACTORY-HARNESS.md`). Each blueprint's front
matter `applies_to` lists the code paths it owns, mirrored in the `blueprints:`
map in `.factory/config.yaml` (config drives tooling; front matter drives
discovery — the two must agree; agreement is checked by review today, a
check-ownership lint is planned).

## Component blocks (nodes)

Runtime components are declared in fenced ` ```component ` blocks:

````markdown
```component
name: StreamRouter
container: agent-plane
responsibilities:
  - Routes inbound stream events to the owning session
  - Enforces per-session ordering
```
````

`name` is PascalCase and matches the code identity. A `component` block is a runtime
node that *does work*; `responsibilities` are what it is accountable for and may
mention elements or other components.

## Model blocks (domain data)

A canonical data/domain model that is central to implementation but is not itself a
runtime component gets a ` ```model ` block, not a `component` block:

````markdown
```model
name: Statement
store: Postgres
description: Canonical append-only statement asserted into the kernel.
fields:
  - id: UUID (required)
  - subject: EntityRef (required)
constraints:
  - statements are immutable once written
```
````

Include `name`, `store`, `description`, `fields`, and `constraints`. Reference a model
in prose as an element (plain backticks), not as a `#component`.

## Mention grammar

- `` `#ComponentName` `` — a runtime component that does work (defined by a
  `component` block in any blueprint).
- `` `ElementName` `` — a schema, config, domain type, enum, request/response model,
  exception, feature flag, permission matrix, or `model` block.
- `@BP-...` / `@WO-...` / `@REQ-...` — a factory entity (blueprint, work order,
  requirement, artifact) referenced by ID.

## Relationship paragraphs (edges)

Edges are prose, one relationship per paragraph, 2–4 sentences: name both
components early, use a direction verb (calls, publishes to, reads from, owns,
emits, transforms), name the contract crossed, and say why. Example:

> `#StreamRouter` publishes session-lifecycle events to `#SessionLedger` over the
> `SessionEvent` schema. The ledger is the only durable record of session state,
> so the router never persists state itself.

Do **not** restate a component's responsibilities in an edge — the edge is the
interaction, not the node. And if adjacency already makes direction, data flow, and
intent obvious, omit the paragraph; write edges for the non-obvious relationships.

## Required sections

Every blueprint has, after its type-specific summary sections (see the templates):

- **Key Contracts** — the promises this unit makes to its consumers: interfaces,
  invariants, ordering/consistency guarantees.
- **Integration Contracts** — the concrete shapes crossing the boundary: schemas,
  file formats, event streams, exit codes, with compatibility rules.
- **ADRs** — decisions local to this blueprint (below).

Templates: `containers/TEMPLATE.md`, `components/TEMPLATE.md`,
`features/TEMPLATE.md`. Each type also carries its own summary sections — a
container adds Infrastructure and Entry Points & Boundaries; a component leads with a
2–3 sentence Capability Summary; a feature leads with a user-centered Feature Summary
that references its FRD.

**Feature blueprints compose, they do not redefine.** A feature blueprint names the
component blueprints it uses (`@BP-COMP-...`), describes the feature-specific
configuration and composition of those capabilities, and gives full `component`
blocks only for components that exist *solely* for this feature (a panel, a page, a
feature-only service). Never restate a referenced component's internals — link it.
When a feature-only component starts being reused, it graduates into its own
component blueprint.

Before writing a feature blueprint, read its FRD and confirm every major requirement
theme has a technical path through the composed components.

## ADRs

**The three-gate test.** Write an ADR only when all three hold:

1. **Hard to reverse** — the cost of changing your mind later is meaningful.
2. **Surprising without context** — a future reader will wonder "why on earth did
   they do it this way?"
3. **A real trade-off** — genuine alternatives existed and you picked one for
   specific reasons.

If a decision is easy to reverse, skip it — you'll just reverse it. If it's not
surprising, nobody will wonder why. If there was no real alternative, there's
nothing to record beyond "we did the obvious thing."

**Format.** One paragraph can be a complete ADR. Structure:

```markdown
### ADR-NNN: <Title>

**Decision.** <what was decided>
**Rationale.** <why — the specific reasons, with evidence where it exists>
**Alternatives considered.** <each rejected option and why — so nobody suggests it again in six months>
```

ADR numbering is local to each blueprint (`ADR-001` restarts per blueprint).
Decisions spanning blueprints go to `decisions/` (see `decisions/README.md`).
IDs never change after publication; superseded ADRs are marked superseded, never
deleted — the history is the value.
