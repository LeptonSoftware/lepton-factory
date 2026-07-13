---
title: BP-FEAT-<NAME> — <Feature name>
summary: <one line naming the feature and the components it composes, written for grep>
owners: [<owner>]
applies_to: ["<path globs the feature's code touches>"]
status: draft
last_verified: YYYY-MM-DD
---

# BP-FEAT-<NAME>: <Feature Name>

<!-- A Feature Blueprint documents how components compose to deliver one feature.
Create only when the feature spans components or adds feature-specific ones
(docs/architecture/README.md). File name must match the BP ID. Link the FRD by
REQ IDs — never copy requirement prose. Delete all template comments. -->

## Feature Summary

<!-- 2-4 sentences: the feature (link REQ-<AREA>-NNN IDs) and the architectural
approach in one breath. -->

## Component Composition

<!-- Which existing BP-COMP-*/BP-CONT-* units this feature composes, and the flow
across them: prose relationship paragraphs with #ComponentName references. -->

## Feature-Specific Components

<!-- ```component blocks for components introduced by this feature alone. If one
becomes reusable, promote it to its own BP-COMP-* and link it here. -->

## Key Contracts

<!-- Promises this feature makes: user-observable invariants, cross-component
guarantees the composition must hold. -->

## Integration Contracts

<!-- New or changed boundary shapes this feature introduces, each with its
compatibility rule. -->

## ADRs

<!-- Feature-local decisions passing the three-gate test, numbered ADR-001 up.
Format: Decision / Rationale / Alternatives considered. -->
