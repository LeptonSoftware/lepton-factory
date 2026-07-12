---
name: converge-work-order
description: Use when implementation and review repairs are done (high tier — at medium tier the convergence gap check runs inside the final review round instead) — compare landed reality against Requirements, Blueprints, plan, and tests before the final review round.
---
<!-- adapted from github/spec-kit converge.md (MIT) -->

# Converge the Work Order

Assess the present state of the code against the records as the sole source of intent. This is not a diff review and not history archaeology. Scope is artifact-bounded: derive the files in scope from paths named in the plan and the blueprints, plus keyword search on record terms — do not infer scope beyond what the artifacts define.

1. **Build the intent inventory:** every linked AC, every blueprint contract and invariant the WO cites, every plan step's outcome, every verification-contract row — **and every promise made in the WO's cited sources** (the requirements, blueprints, and research/evidence the WO references), not only its own scope list. The `missing` gap type covers a deliverable a cited source commits to that never landed, even when the WO's scope bullets omitted it.
2. **Compare landed code and tests against each item.** Gap types:
   - `missing` — the required work is absent entirely
   - `partial` — exists but does not fully satisfy
   - `contradicts` — the code conflicts with stated intent or a blueprint invariant
   - `unrequested` — work no record called for (surfaced for awareness; convergence never deletes code)
3. **Disposition per gap — the active WO never stretches:**
   - legitimate remaining work → a new WO stub from `.factory/templates/work-order.md` via `/wo-author`, its summary line traced `<imperative description> per <source-id> (<gap-type>)` where source-id ∈ AC-, BP-, COV-, or a plan step
   - process or harness friction → a feedback record from `.factory/templates/feedback.yaml`
   - `contradicts` gaps are emitted first and marked CRITICAL
   - `unrequested` work → a review/justify-or-remove item in a new WO — never silent deletion
4. **Clean case:** everything satisfied → record "converged, no gaps" in checklist.md and change nothing else — no empty stubs, no placeholder records; existing artifacts stay byte-for-byte unchanged.
5. `tools/agent/update-state --wo WO-XXXX --phase converge --gate convergence=done --next "final review round"`.
