---
name: wo-execute
description: Execute a Work Order end to end through every lifecycle gate. Run as /wo-execute WO-XXXX.
disable-model-invocation: true
---

# Execute a Work Order

Dispatch models per `.factory/policies/model-routing.md` — cheapen mechanics, never judgment.

The canonical execution flow (`.factory/README.md` §3–5). State moves only through `tools/agent/update-state`. To resume, read `.factory/work-orders/WO-XXXX/state.yaml` first — `next_action` names the step; never reconstruct position from memory.

1. `tools/agent/init-work-order --wo WO-XXXX`, then immediately `tools/agent/risk-tier --wo WO-XXXX` — the tier is computed FIRST because it drives context depth and every gate below (`.factory/config.yaml` gates:); humans may raise it, and only a named human may lower it (`risk-tier --set --approver` — `docs/runbooks/break-glass.md`); never lower it yourself. At low tier, pre-mark the checklist items belonging to non-required gates `[SKIP]` with reason "not required at low tier" now, so the checklist reflects the tier from the start. Then `update-state --wo WO-XXXX --status context --phase context`.
2. Gather context per checklist.md Phase 1: read the WO, every linked Requirement (ACs verbatim), every linked Blueprint with references traversed recursively until no unvisited reference remains, analogous code and conventions — all recorded in context.md. Depth is proportional to tier: at low tier the WO plus its directly linked records suffice.
3. Run `compile-contract` (Gate 0; medium/high tier). At low tier contract.md is optional (`validate-work-order` does not require it) — when ACs exist, a ~5-line contract (ACs/obligations plus one verification-contract row) is still worth writing. Unresolved HITL decisions → `update-state ... --status blocked --blocked "<decision>"`, escalate, stop.
4. Run `write-implementation-plan` — at low tier the plan file is optional; a single-step plan suffices when written — then `challenge-plan` (Gate A; medium/high tier only — Gate A is skipped at low tier per config). REVISE → revise and re-challenge fresh; HUMAN_DECISION_REQUIRED → block and escalate.
5. Create the dedicated branch/worktree; verify clean baseline (existing tests pass) and record it in checklist.md before the first change.
6. Per slice: `execute-slice`, then `review-slice` (Gate B). CHANGES_REQUESTED → repair, then a fresh review of the repaired diff. `update-state --slice` at every boundary.
7. Full validation: all suites for the affected area, and RUN the software; evidence into evidence/.
8. `audit-verification` (Gate C; medium/high tier). High tier only: `adversarial-qa` (Gate D, three lenses) then `synthesize-review`; repair Blocking findings and re-run exactly the gates synthesize-review names.
9. High tier only: run `converge-work-order` — gaps become new WOs or feedback records, never widened scope. At medium tier the convergence gap check runs inside the final review round below, not as a separate gate.
10. Final review round (medium/high tier): dispatch a fresh reviewer (never the implementer; prefer a different model family than the implementer where the runner supports it) with the diff, contract.md, and the six-dimension round template in `.factory/templates/review-log.md`. At medium tier this is THE clean-context falsification round — the brief also carries the three adversarial lens checklists (`adversarial-qa`) and the convergence gap check (`converge-work-order` gap types). Verdict must be APPROVED. CHANGES_REQUESTED → repair, then a fresh full round — not a comment recheck. Record with `update-state ... --gate final_review=<verdict>`.
11. Run `finish-work-order`.

**Review-loop cap:** after 2 repair→fresh-review cycles on the same gate, stop and escalate — `update-state ... --status blocked --blocked "review loop exceeded on <gate> — human decision required"` — never a third round on agent judgment alone.

Stop and escalate (`--status blocked --blocked "..."`) on judgment failures: product ambiguity, un-blueprinted architecture decisions, destructive-migration uncertainty, secrets, security-sensitive behavior, scope expansion. Continue through mechanical failures via `systematic-debugging`.
