# Implementation Plan — WO-XXXX

<!-- Written AFTER contract.md exists and context traversal is complete; no
implementation file changes before this plan exists. Plans describe boundaries, not
full code: intent, files, interfaces, invariants, slices, verification. Pseudocode
only where genuine ambiguity remains. Revise this plan in place when reality
diverges — bump plan_revision in state.yaml; a stale plan blocks review. -->

## Summary

<!-- The approach in 3-6 sentences, and why this approach over the obvious alternative. -->

## Global constraints

<!-- Constraints every step must obey (from contract.md: invariants, disallowed
changes, compatibility rules). Stated once here, not repeated per step. -->

## Code Reuse And Package Structure

<!-- Mandatory before inventing anything. For each new abstraction:
- Existing components searched (list what you looked at)
- Analogous code inspected
- Decision: reuse directly | extract shared capability | follow existing pattern | new
- If new: why this layer, intended consumers, owner
-->

## Components And Flow

<!-- Named components, interfaces/signatures, call paths, data crossing boundaries.
This is where interface ambiguity dies — exact names and types for anything two
steps or two agents must agree on. -->

## Delivery strategy

<!-- Tracer-bullet sequencing: which thin vertical slice lands first and proves the
architecture end-to-end; migration/rollout ordering; compatibility approach. -->

## Steps

<!-- Small, independently verifiable steps grouped into slices. Each step:

### Step N: <reviewable outcome>
- Slice: S01
- Files:
- Change: <behavioral description, not code>
- Test-first seam: <yes: which test proves it red first | no: evidence instead>
- Verification: <exact command(s) or runtime action>
- Dependencies: <step numbers>
- Commit boundary: <yes/no>
-->

## Testing

<!-- Suites touched, new tests by COV ID, how the app itself will be run and observed.
The verification contract in contract.md is the source of truth; this section is the
execution ordering of it. -->

## Risks and stop conditions

<!-- What would force redesign mid-flight; conditions that trigger stop-and-escalate
(HITL list from the contract plus anything discovered while planning). -->
