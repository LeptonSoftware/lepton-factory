---
name: adversarial-qa
description: Use when the risk tier requires Gate D (high tier) — dispatch three clean-context falsification lenses in parallel against the landed change. At medium tier the lens briefs fold into the final review round instead.
---

# Adversarial QA (Gate D)

Lens tier: per `.factory/policies/model-routing.md` — never lighter than the implementer; lenses run in parallel.

Objective: falsification. Each reviewer's job is to find why this change should NOT be accepted; a change that survives honest attack earns approval.

## Controlled context (.factory/README.md §4, restated — every brief is self-contained)

Each lens is dispatched fresh-context and receives EXACTLY:

- the problem statement (WO Summary) and the verbatim ACs
- the invariants from contract.md
- run instructions — how to build, run, and drive the software
- the diff as a file, and the test commands

Each lens must NOT receive: the plan or its justification, prior review findings, other lenses' findings, or the implementer's narrative. Reviewers never modify product code.

## Dispatch by tier

- **high:** THREE reviewers in parallel — one message, three dispatches — one lens each (config gates `adversarial_behavior|operations|architecture`, merged into the single `adversarial_qa` state field by `synthesize-review`).
- **medium:** Gate D is not a separate gate — the three lens briefs below travel inside the final review round's dispatch (`wo-execute` step 10); do not run this skill standalone at medium tier.

Where the runner supports it, dispatch lenses (and the final falsification reviewer) on a different model family than the implementer — same-family reviewers share the implementer's blind spots.

## Lens 1 — Behavior & abuse

> Attack the behavior as a hostile user. Invalid and malformed inputs; out-of-order and repeated action sequences; authorization — walk every path reachable by someone who shouldn't reach it; stale state and stale reads; multiple users interleaving on shared data; cross-feature interaction with adjacent features. For each attack: what you did, what you observed, and which AC or invariant it breaks.

## Lens 2 — Failure & operations

> Attack the change as a hostile environment. Partial dependency failure; timeouts mid-operation; duplicate message delivery; retries — and whether every retried operation is idempotent; process crash midway through a multi-step write; rollback; migration failure halfway through; and observability — run each failure and report what the logs and metrics actually show: could an operator diagnose this at 3am?

## Lens 3 — Architecture & longevity

> Attack the change as its future maintainer. Hidden coupling introduced between modules; leaky abstractions; concepts duplicated instead of reused; ownership — code landed outside its blueprint's owned paths; the long-term consequences of any public API surface added; security boundaries crossed or widened; behavior at 10–100× current scale; drift from the Blueprints and from docs/domain/glossary.md terms.

Each lens reports findings (Blocking | Advisory, location, and the evidence — what was run and observed) and a verdict, exactly: APPROVED | CHANGES_REQUESTED. A CHANGES_REQUESTED verdict requires at least one Blocking finding — advisory-only findings mean APPROVED.

## Record

Collect the raw reports and hand them to `synthesize-review` — do not merge, rerank, or act on them yourself, and do not record the gate: `synthesize-review` is the sole writer of the `adversarial_qa` gate. Then
`tools/agent/update-state --wo WO-XXXX --phase adversarial --next "synthesize-review"`.
