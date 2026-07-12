---
name: finish-work-order
description: Use when every gate the Work Order's risk tier requires has passed and the final review round is APPROVED — completes the records, opens the PR, and hands off.
---
<!-- evidence-before-claims discipline adapted from obra/superpowers verification-before-completion (MIT) -->

# Finish the Work Order

Completion is validated mechanically, not claimed. Evidence before assertions: run each command below and read its output before checking anything off.

1. **Checklist resolution.** Every item in checklist.md ends `[x]` or `[SKIP]` with a `Skip reason:` on the next line. Unchecked items are execution failures, not TODOs to ignore.
2. **State and gates.** state.yaml gates match the tier's requirements (`.factory/config.yaml` gates:); every `skipped` gate has a skip_reasons entry AND a waiver_approvers entry (a human — `docs/runbooks/break-glass.md`); final_review is approved where the tier requires it (medium/high — low tier does not). High tier only: human_approval is recorded by a human, whose name lands in state.yaml via `update-state --approver` — never self-approved.
3. **Records honest.** implementation-plan.md reflects what actually landed (revised in place, plan_revision current); context.md entity index is complete; `evidence/` covers every verification-contract runtime action.
4. **Validate.** `tools/agent/validate-work-order --wo WO-XXXX` — fix what its error names and re-run until it exits 0. Then `tools/agent/generate-indexes`.
5. **Docs.** Update descriptive docs (`docs/testing/`, `docs/runbooks/`) directly, bumping their `last_verified` front matter; architectural or product-intent changes become proposals for review, never direct edits.
6. **Feedback.** Meaningful friction, failures, or rejected approaches → `.factory/feedback/<YYYY-MM>/WO-XXXX.yaml` from `.factory/templates/feedback.yaml`.
7. **PR.** Commit `.factory/work-orders/WO-XXXX/` with the change; create the pull request from `.github/PULL_REQUEST_TEMPLATE.md`, referencing WO-XXXX and the REQ/AC IDs it delivers. Record references are **clickable links** (full blob/tree URLs at this branch), never backticked paths — GitHub does not resolve relative repo paths in PR bodies (`.factory/policies/delivery.md` §7).
8. **Hand off.** `tools/agent/update-state --wo WO-XXXX --status in_review --phase handoff --next "await human review of PR <url>"`. Close with a resumable summary: WO, outcome, gate verdicts, evidence paths, PR link — everything a fresh agent needs to resume from the files alone.
