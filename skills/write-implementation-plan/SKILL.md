---
name: write-implementation-plan
description: Use when a Work Order has a compiled contract and needs its implementation plan — before any implementation file changes exist. Fills implementation-plan.md.
---
<!-- Global Constraints / Interfaces discipline and type-consistency self-review adapted from obra/superpowers writing-plans (MIT); tracer-bullet and expand–contract rules adapted from mattpocock/skills to-tickets (MIT) -->

# Write the Implementation Plan

Plans describe boundaries, not full code: outcome, files, interfaces, invariants, vertical slices, per-step verification, commit boundaries, stop conditions. Pseudocode only where genuine ambiguity remains. Fill every section of `.factory/templates/implementation-plan.md` into `.factory/work-orders/WO-XXXX/implementation-plan.md`; a finished plan contains no placeholder text.

## Global constraints

State once, up front, every constraint each step must obey — invariants, disallowed changes, compatibility rules, version floors, naming rules — with exact values copied verbatim from contract.md. Every step's requirements implicitly include this section; nothing here is repeated per step.

## Reuse before invention (mandatory, before designing anything new)

For each new abstraction, record in Code Reuse And Package Structure: existing components searched (list what you looked at), analogous code inspected, and the decision — reuse directly | extract shared capability | follow existing pattern | new. "New" requires layer justification, intended consumers, and an owner. See `.factory/policies/code-reuse.md`.

## Interfaces

In Components And Flow, give exact names, signatures, and types for anything two steps or two agents must agree on — what each component consumes and produces. A slice's implementer sees only its own steps; this block is how it learns the names and types its neighbors use.

## Slice as tracer bullets

- Each slice cuts a narrow but COMPLETE path through every layer — vertical, not a horizontal slice of one layer.
- A completed slice is demoable or verifiable on its own.
- Each slice is sized to fit a single fresh context window.
- Prefactoring first: make the change easy, then make the easy change.
- **Wide refactors are the exception.** One mechanical change whose blast radius fans across the codebase cannot land as a vertical slice — sequence it as expand–contract: *expand* (add the new form beside the old so nothing breaks), *migrate* call sites in batches sized by blast radius (each batch its own step, CI green throughout because the old form still exists), *contract* (delete the old form once no caller remains).

## Steps

Small and independently verifiable, grouped into slices, in the template's step shape: files, behavioral change (not code), test-first seam (yes: which test goes red first | no: what evidence instead), exact verification command, dependencies, commit boundary. Right-size: split only where a reviewer could meaningfully reject one step while approving its neighbor. List real deliverable files only — not incidental files that change from formatting, barrel exports, or generated code.

## Self-review (before the plan leaves your hands)

1. **Coverage:** point to the step that satisfies each AC and each verification-contract row. An AC with no step is a hole in the plan.
2. **Placeholder scan:** "TBD", "TODO", "add appropriate error handling", "handle edge cases", "similar to step N" are defects — replace each with the specific behavior.
3. **Type consistency:** a function called `clearLayers()` in step 3 but `clearFullLayers()` in step 7 is a bug — reconcile every name and type across steps.

## Record

`tools/agent/update-state --wo WO-XXXX --status planned --phase plan --next "challenge plan (Gate A)"`.
When reality diverges during execution, revise this plan in place and bump plan_revision (`update-state`) — a stale plan blocks review.
