---
title: BP-CONT-<NAME> — <Container name>
summary: <one line naming the runnable unit and its purpose, written for grep>
owners: [<owner>]
applies_to: ["<path glob this container owns, e.g. services/agent-plane/**>"]
status: draft
last_verified: YYYY-MM-DD
---

# BP-CONT-<NAME>: <Container Name>

<!-- A Container Blueprint documents one runnable/deployable unit. File name must
match the BP ID. Mirror applies_to into .factory/config.yaml `blueprints:` with an
owner. Conventions: docs/architecture/README.md. Delete all template comments. -->

## Container Summary

<!-- 2-4 sentences: what this unit runs, for whom, and its boundary of
responsibility. Link the REQ/BP-FEAT records it serves by ID. -->

## Infrastructure

<!-- Runtime, deployment target, scaling model, persistence it owns, external
services it depends on. -->

## Commands

<!-- REQUIRED. The canonical, exact commands for this container — gate briefs
(Gate B/C/D run instructions) and slice baselines read from HERE; reviewers and
implementers run these, never improvised equivalents. Keep them copy-pasteable.

- Build: `<exact command>`
- Test: `<exact command>` (unit; add the integration/e2e command if separate)
- Run: `<exact command>` (locally, against what fixture/config)
- Lint: `<exact command>` (include format check if separate)
-->

## Entry Points And Boundaries

<!-- How traffic/work enters (APIs, queues, schedules) and what is explicitly
outside this container's responsibility. -->

## Core Components

<!-- One ```component block per runtime component, then prose relationship
paragraphs using #ComponentName references (format: docs/architecture/README.md). -->

## Key Contracts

<!-- Promises to consumers: interfaces, invariants, ordering/consistency
guarantees, failure semantics. -->

## Integration Contracts

<!-- Concrete boundary shapes: schemas, event streams, endpoints, exit codes —
each with its compatibility rule (additive only? versioned? breaking allowed?). -->

## ADRs

<!-- Blueprint-local decisions passing the three-gate test, numbered ADR-001 up.
Format: Decision / Rationale / Alternatives considered. -->
