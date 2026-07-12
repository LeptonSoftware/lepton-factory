---
name: execute-slice
description: Use when implementing one vertical slice of an approved implementation plan — after Gate A, inside the Work Order's dedicated worktree.
---
<!-- revert-and-verify TDD repair and RED/GREEN evidence adapted from obra/superpowers test-driven-development (MIT) -->

# Execute a Slice

Implementer tier and parallel-slice rules: `.factory/policies/model-routing.md` — independent slices may run as parallel subagents in separate worktrees.

One slice, one pass: prove the baseline, test-first at the planned seams, implement, run the tests AND the software, keep the records live throughout.

1. **Baseline.** Confirm the worktree is clean and the relevant suites pass before the first change. A dirty baseline cannot distinguish new bugs from pre-existing ones — stop and report it instead of building on it.
2. **Set state.** `tools/agent/update-state --wo WO-XXXX --status in_progress --phase implement --slice S<NN> --next "implement S<NN>: <outcome>"`.
3. **Seam-based TDD.** For every step the plan marks test-first: write the test at the listed seam, run it, observe RED (a test that passes immediately proves nothing), implement minimally, observe GREEN with pristine output. Keep the RED and GREEN commands + output as evidence. Steps the plan marks evidence-first (wiring, generated config, mechanical migrations, spikes): record the verifying command and its output instead.
   **Violation repair:** implementation written before its seam test? Repair by revert-and-verify — set the implementation aside, write the test, observe it fail against the pre-change behavior, restore the implementation, observe it pass. Never delete the test; never backfill a green test and call it TDD.
4. **Run the software, not just the tests.** Per change type: drive the web flow, invoke the endpoint, execute the CLI, run the worker against a fixture, apply-and-roll-back the migration on a disposable database. Evidence into `evidence/` or the checklist.
5. **Records live, during the work — not retrospectively:**
   - checklist.md items checked the moment they complete
   - context.md Execution Notes for discoveries that change understanding
   - plan honesty: when reality diverges, revise implementation-plan.md in place and bump plan_revision via `update-state` — a stale plan blocks review
6. **Commit at the plan's commit boundaries.** Then `tools/agent/update-state --wo WO-XXXX --slice S<NN> --next "review slice S<NN> (Gate B)"` and hand off to `review-slice`.

Out-of-scope findings are filed (new WO via `/wo-author`, or a feedback record) — not implemented. A failure you cannot explain gets `systematic-debugging`, not fix-guessing. Record the slice's BASE commit before the first commit — Gate B reviews the diff from BASE, not HEAD~1.
