---
title: BP-COMP-<NAME> — <Component name>
summary: <one line naming the capability and who consumes it, written for grep>
owners: [<owner>]
applies_to: ["<path glob this component owns, e.g. packages/streams/**>"]
status: draft
last_verified: YYYY-MM-DD
---

# BP-COMP-<NAME>: <Component Name>

<!-- A Component Blueprint documents one enduring reusable capability. Required
before any shared package ships (.factory/policies/code-reuse.md §4). File name
must match the BP ID; mirror applies_to into .factory/config.yaml `blueprints:`
with an owner. Conventions: docs/architecture/README.md. Delete all comments. -->

## Capability Summary

<!-- 2-4 sentences: the capability, its consumers (named — at least two, or the
platform contract justifying fewer), and its boundary of responsibility. -->

## Core Components

<!-- One ```component block per runtime component, then prose relationship
paragraphs using #ComponentName references (format: docs/architecture/README.md). -->

## Key Contracts

<!-- Promises to consumers: the public interface, invariants, ordering/consistency
guarantees, error modes, performance characteristics callers may rely on. -->

## Integration Contracts

<!-- Concrete boundary shapes: exported types/schemas, events, file formats — each
with its compatibility rule (additive only? versioned? breaking allowed?). -->

## ADRs

<!-- Blueprint-local decisions passing the three-gate test, numbered ADR-001 up.
Format: Decision / Rationale / Alternatives considered. -->
