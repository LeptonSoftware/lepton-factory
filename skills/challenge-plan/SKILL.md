---
name: challenge-plan
description: Use when an implementation plan exists and the risk tier requires Gate A — dispatch an adversarial challenger against the plan before any implementation begins.
---
<!-- required-question framing informed by github/spec-kit analyze.md and obra/superpowers plan review practice (both MIT) -->

# Challenge the Plan (Gate A)

Challenger tier: per `.factory/policies/model-routing.md` — never lighter than the planner.

Dispatch ONE fresh-context challenger whose objective is to *reject* the plan. Never challenge your own plan. Independence rules from `.factory/README.md` §4 are restated here because the brief must be self-contained.

## What the challenger receives (compose the dispatch with exactly this)

- the linked Requirements (verbatim ACs) and Blueprints
- current system behavior in the touched area (paths, how to build and run it)
- `contract.md` and `implementation-plan.md`, handed as files
- the brief below

## What the challenger must NOT receive

- any statement that the design is approved, reviewed, or "looking good" — the challenger is never told the design is already approved
- the implementer's confidence, rationale narration, or conversation history
- prior review findings

## The brief (paste verbatim into the dispatch)

> You are challenging an implementation plan before any code exists. Your objective is to find the reasons this plan should be rejected; a plan you cannot fault after honest attack earns APPROVE. Answer every question, citing the plan section each finding concerns:
>
> 1. Which assumptions does the plan make that no cited record verifies?
> 2. Which scenarios required by the ACs and invariants are absent from the steps?
> 3. What is the regression surface — which currently-working behavior can these changes break, and where does the plan defend it?
> 4. Does any step violate a blueprint invariant or an entry under Disallowed changes in the contract?
> 5. Is there a simpler design that meets the same contract? Name it concretely.
> 6. Are transaction boundaries, retry, ordering, and recovery semantics defined everywhere the plan touches them?
> 7. Is the migration/rollout ordering credible, and is rollback stated where it must be?
> 8. What discovery mid-flight would force a redesign — and do the plan's stop conditions anticipate it?
> 9. Does the plan prove the user-visible outcome, or only code completion?
>
> Verdict, exactly one: APPROVE | APPROVE_WITH_RISKS | REVISE | HUMAN_DECISION_REQUIRED.
> APPROVE_WITH_RISKS names each accepted risk. REVISE names the specific plan changes required. HUMAN_DECISION_REQUIRED names the decision and why only a human can make it.

## Record

Append the verdict and findings to review-log.md (append-only), then
`tools/agent/update-state --wo WO-XXXX --gate plan_challenge=<approve|approve_with_risks|revise|human_decision_required>`.
REVISE → revise the plan in place (bump plan_revision), dispatch a *fresh* challenger against the revised plan.
HUMAN_DECISION_REQUIRED → `tools/agent/update-state --wo WO-XXXX --status blocked --blocked "<decision>"` and escalate.
