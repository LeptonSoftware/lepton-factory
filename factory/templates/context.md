# Work Order Entity Index

<!-- status lives in state.yaml — do not duplicate it here -->

<!-- Entity index for WO execution. Record every authoritative record read and every
piece of code inspected — this is what makes the WO resumable by a different agent.
Entity lines use: - Title (`id-or-path`) -->

## Work Order

- WO-XXXX (.factory/work-orders/WO-XXXX/work-order.md)

## Requirements

<!-- Every requirement and AC read, verbatim IDs.
- Feature name (`REQ-AREA-001`)
  - AC-AREA-001.1
-->

## Blueprints

<!-- Blueprints directly linked from the WO. -->

## Referenced Blueprints

<!-- Blueprints reached by recursive traversal of references. Traversal is complete
only when no unvisited reference remains. -->

## Code Areas

<!-- Analogous code inspected, reusable components found, conventions observed.
- packages/<pkg>/ — <what was learned>
-->

## Delivery

- Branch:
- Worktree:
- Pull Request:

## Execution Notes

<!-- Append-only, timestamped journal of discoveries that changed the plan or
understanding. Keep entries to 1-3 lines.
### 2026-07-12T10:30Z
- Found shared cancellation helper in packages/runtime; plan updated to reuse it.
-->
