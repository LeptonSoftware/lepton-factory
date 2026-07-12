---
name: wo-review
description: Run independent review gates on demand against an existing Work Order. Run as /wo-review WO-XXXX [gates].
disable-model-invocation: true
---

# Review a Work Order

1. Read `.factory/work-orders/WO-XXXX/` (state.yaml, contract.md, review-log.md); establish the diff to review from the WO's recorded base commit — an empty diff is an error, report it.
2. Determine gates: those named in the arguments, else every review gate the risk tier requires (`.factory/config.yaml` gates:, tier from state.yaml — never lowered).
3. Dispatch each gate through its own skill, which carries the self-contained brief: `review-slice` (Gate B, whole-diff scope), `audit-verification` (Gate C), `adversarial-qa` (Gate D per tier).
4. Run `synthesize-review` to merge findings into a fresh append-only Round in review-log.md and emit repair items to checklist.md.
5. Verdicts land via `tools/agent/update-state --wo WO-XXXX --gate <gate>=<verdict>` — each gate's own skill records it; `synthesize-review` is the sole writer of `adversarial_qa`. Reviewers never modify product code; repairs belong to the implementer.
