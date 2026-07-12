---
title: Delivery Policy
summary: Executable rules for PR scope, branch naming, worktree isolation, commit discipline, merge gates, force-push, and drift disposition.
owners: [factory-operators]
applies_to: ["**"]
status: active
last_verified: 2026-07-12
---

# Delivery Policy

Exception process for every rule (unless marked "None"): ADR + owner approval.

## 1. One Work Order per PR; PR scope matches the WO

**Rule.** Every PR delivers exactly one Work Order and names it in the PR template.
Changes outside the WO's In Scope are removed or become a new WO
(`AGENTS.md`, non-negotiable 7) — the active WO never silently stretches.

- **Applies to.** `**`
- **Enforcement.** PR template Work Order field; `tools/agent/validate-work-order`
  (CI) checks the referenced WO exists and is in a mergeable state; convergence
  gate classifies `unrequested` changes (`.factory/README.md` §4).
- **Exceptions.** None.
- **Owner.** factory-operators

## 2. Branch naming: `wo-<id>-<slug>`

**Rule.** Delivery branches are named `wo-<id>-<slug>` (e.g.
`wo-1042-stream-cancellation`): lowercase, WO number without the `WO-` prefix
duplicated, short kebab slug.

- **Applies to.** all delivery branches
- **Enforcement.** Review until the lint lands (planned: branch-name check in the
  factory-gates CI workflow). The branch name is also how CI derives which WO to
  validate, so a misnamed branch loses its WO's completion gate.
- **Exceptions.** Non-WO branches: `release/**`; `hotfix/<slug>` per the
  break-glass hotfix lane (`docs/runbooks/break-glass.md` — retroactive WO within
  24h); `spike/<slug>` exploration branches, never merged
  (`.factory/README.md` §6).
- **Owner.** factory-operators

## 3. Isolated execution on a verified baseline

**Rule.** Each WO executes in a dedicated worktree (or dedicated branch when
worktrees are unavailable) with a clean, verified baseline before the first change
(`.factory/README.md` §6). A failing baseline is reported, never absorbed — you
cannot distinguish new failures from pre-existing ones otherwise.

- **Applies to.** all delivery work
- **Enforcement.** Checklist item (baseline verification with command + output);
  Gate C audits the record.
- **Exceptions.** None.
- **Owner.** factory-operators

## 4. Commits land at plan-declared boundaries

**Rule.** The implementation plan declares commit boundaries per step; commits land
at those boundaries, each message referencing the WO (`WO-<id>: <what>`). No
end-of-WO squash of unrelated steps; no drive-by commits outside the plan.

- **Applies to.** all delivery branches
- **Enforcement.** Review until the lint lands (planned: commit-message
  WO-reference lint in CI); boundary discipline checked at Gate B (the reviewer
  sees the commit list in the review package).
- **Exceptions.** Mechanical fixups (format, lint) may fold into the step commit.
- **Owner.** factory-operators

## 5. Merge requires the risk tier's full gate record

**Rule.** A PR merges only when every gate required by its risk tier has a passing
record in `state.yaml`. Gate definitions: `.factory/README.md` §4. Tier-to-gate
mapping: `.factory/config.yaml` `gates`. Nobody — human or agent — hand-picks gates.

- **Applies to.** `**`
- **Enforcement.** `tools/agent/validate-work-order` runs in CI on every PR and is
  a required status check.
- **Exceptions.** A HUMAN may waive a specific gate via the break-glass waiver
  protocol (`docs/runbooks/break-glass.md`): `update-state --gate <gate>=skipped
  --skip-reason "..." --approver "<name>"` — recorded in state.yaml and visible in
  the PR diff; agents cannot self-waive.
- **Owner.** factory-operators

## 6. No force-push to shared branches

**Rule.** No force-push to `main`, release branches, or any branch with an open PR
under review — rewriting reviewed history invalidates the append-only review log.
Recipe when history must change on a review branch: add commits; rebase only before
the first review round.

- **Applies to.** `main`, `release/**`, branches with open PRs
- **Enforcement.** Branch protection (GitHub settings); review-log rounds reference
  commit SHAs, so rewrites surface at final review.
- **Exceptions.** None.
- **Owner.** factory-operators

## 7. PR bodies link records; decisions live in records, not comments

**Rule.** Every record a PR references (WO, REQ/AC, blueprint, evidence) is a
**clickable link** — a full GitHub blob/tree URL at the PR's branch, not a
backticked path (GitHub does not resolve relative repo paths in PR descriptions).
The PR body is composed from `.github/PULL_REQUEST_TEMPLATE.md`. The PR thread is a
collaboration surface: a decision reached in PR comments is not real until it lands
in the authoritative record (`.factory/README.md` §7 precedence) — reviewers push
material findings into `review-log.md`, not just the conversation.

- **Applies to.** every PR
- **Enforcement.** PR template shows the link form; final review checks that
  material decisions in the thread were absorbed into records (no hidden
  source of truth in comments). A link-format lint is planned — review until it lands.
- **Exceptions.** None.
- **Owner.** factory-operators

## 8. GitHub review maps to the factory review record

**Rule.** The factory's review *gates* (Gate B, C, D, and the final round in
`review-log.md`) are the substance of review; the GitHub PR *approval* is the
enforcement act that branch protection requires. They are not duplicates: a
CODEOWNERS approver confirms the required gate records exist and are APPROVED
before approving the PR — the approval attests the record, it does not replace it.
This is the human backstop named in the enforcement boundary (`.factory/README.md`
§4): machine gates validate structure; a human review + CODEOWNERS approval catches
what structure cannot.

- **Applies to.** every PR touching product code or the control plane
- **Enforcement.** Branch protection: required status checks (`factory-gates`) +
  required CODEOWNERS approval (GitHub settings — see `CONTRIBUTING.md`).
- **Exceptions.** Break-glass admin-merge on the hotfix lane only
  (`docs/runbooks/break-glass.md`).
- **Owner.** factory-operators

## 9. Drift disposition is required on every PR

**Rule.** Every PR declares exactly one drift disposition: (a) no requirement or
blueprint drift, (b) blueprint updated in this PR, or (c) drift accepted with a
linked follow-up WO and owner. Silence is not a disposition.

- **Applies to.** `**`
- **Enforcement.** PR template Drift checklist; final review blueprint-alignment
  dimension verifies the declaration against the diff.
- **Exceptions.** None.
- **Owner.** factory-operators
