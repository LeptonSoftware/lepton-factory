---
name: night-shift
description: Autonomous queue execution of AFK-only Work Orders while humans are away. Run as /night-shift [max-WOs].
disable-model-invocation: true
---

# Night Shift

Unattended execution policy: mechanics run at night, judgment waits for morning.

1. Build the queue from `.factory/work-orders/`: status `ready` AND the WO's HITL decision list empty or fully resolved. SKIP any WO whose `## Decision classification` section is missing entirely — the section is mechanically required (`validate-work-order`), and a missing section is not the same claim as a deliberately empty HITL list; only the latter is eligible. Order by explicit dependency, then WO number. Cap at the requested max (default 3).
2. One WO per session: run `/wo-execute WO-XXXX` to completion or to a stop condition before touching the next. Never run WOs in parallel.
3. Stop conditions — `update-state --status blocked --blocked "<reason>"`, record it, move to the NEXT queued WO: product ambiguity; un-blueprinted architecture decision; destructive-migration uncertainty; anything touching secrets or security-sensitive behavior; repeated unexplained test failure (a second `systematic-debugging` pass without a root cause); scope expansion beyond In Scope.
4. High-tier WOs end at `human_approval` — leave them in_review; never self-approve.
5. End of shift: full validation (build + all suites), `tools/agent/validate-work-order --wo <each touched WO>`, `tools/agent/generate-indexes`.
6. Handoff: one line per WO — `WO-NNNN: COMPLETE|BLOCKED - <summary or exact blocking question>` — plus, per WO, gates passed, evidence paths, and the state.yaml `next_action` a human or fresh agent resumes from. Queue totals: completed / blocked / not started.
