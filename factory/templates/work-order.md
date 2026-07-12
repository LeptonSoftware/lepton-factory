# WO-XXXX: <Outcome, stated as a user-observable result>

<!-- A Work Order is a bounded delivery contract, not a Jira ticket and not an
implementation plan. It links records; it does not reproduce them. It must be
independently reviewable, narrow enough to prevent incidental refactoring, large
enough to deliver a coherent result. No line-by-line coding instructions here. -->

## Summary

<!-- 2-5 sentences: the outcome, why now, and the boundary of responsibility. -->

## In Scope

<!-- Bullet list. Concrete and checkable. -->

## Out of Scope

<!-- Explicit exclusions. Anything discovered here later becomes a NEW work order. -->

## Requirements

<!-- Links by stable ID only. Every listed AC must appear in the E2E section below.
- REQ-AREA-001 (docs/product/features/<feature>/requirements.md)
  - AC-AREA-001.1
  - AC-AREA-001.2
-->

## Blueprints

<!-- Every blueprint whose owned paths this WO touches, plus blueprints it must obey.
- BP-FEAT-<NAME> (docs/architecture/features/...)
- BP-COMP-<NAME> (docs/architecture/components/...)
-->

## Decision classification

<!-- HITL/AFK split, decided at authoring time:
- HITL (human-in-the-loop): decisions in this WO that REQUIRE a human (product
  judgment, un-blueprinted architecture, destructive operations). Executing agents
  stop and escalate on these; they never resolve them by iterating.
- AFK: everything else — safe for autonomous execution.
-->

- HITL decisions:
- AFK: all other execution decisions

## E2E Acceptance Tests

<!-- Coverage mapping. Every AC gets at least one COV row; details are compiled into
contract.md at execution time.
| COV ID | AC | Proves |
|---|---|---|
| COV-AREA-001.1 | AC-AREA-001.1 | <observable behavior> |
-->
