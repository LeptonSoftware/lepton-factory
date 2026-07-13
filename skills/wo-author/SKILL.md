---
name: wo-author
description: Use when a human asks to record new work — author a Work Order from an idea, feature request, review finding, or convergence gap. Run as /wo-author <intent> or invoke directly when the human has clearly requested a WO. NOT for mid-execution follow-ups (use the stub path — see below).
---

<!-- sizing/section craft adapted from 8090-inc/software-factory-plugin
work-order-writing-guide.md (MIT) -->

# Author a Work Order

A Work Order is a bounded delivery contract: it links records, it does not reproduce them. One coherent change per WO — split rather than pad.

**The top priority is connecting the right context.** Before wording anything, link the correct requirements and blueprints so the implementer reads the source records directly. Do not restate what a connected REQ or BP already says — reference it and describe only *this WO's specific delivery responsibility*.

**Right-size it.** A good WO is: precise enough to execute without clarifying questions; narrow enough to prevent incidental refactoring and scope drift; large enough to deliver a coherent result; grounded in connected records; and verification-focused (the E2E section proves how the ACs get validated). If it fails any of these, split or tighten it.

**Section craft** (fill `.factory/templates/work-order.md`):
- **Summary** — "what is being built or changed?" in 2–3 sentences of outcome and system impact; no broad background.
- **In Scope** — the responsibilities this WO owns (functional boundaries); do not restate ACs verbatim; avoid low-level steps unless they are essential constraints.
- **Out of Scope** — explicit exclusions that draw the boundary with adjacent WOs; anything discovered here later becomes a NEW WO.
- **Requirements / Blueprints** — by stable ID; one line per blueprint; commentary only where it *narrows* what this WO owns.
- **E2E Acceptance Tests** — one COV row per AC; the section proves how each AC is validated, not how the code is written.

What a WO is **not**: it carries no line-by-line coding instructions — that is the implementation plan's job, written after context and contract. Dependent WOs are sequenced (a later WO names the earlier ones it depends on), not merged.

**When to run this vs the stub path — the boundary is intent, not a tool lock.** Run this skill when a **human has asked to record new work** (an idea, feature request, or "make a WO for X") — authoring is the response to human intent, so you may invoke it directly then; you do not wait for the human to type the exact slash command. Do **not** invoke it to spawn work *no human requested*: a follow-up surfaced mid-execution — a convergence gap, an out-of-scope finding, an adversarial-QA leftover — is created via the **stub path** instead: `tools/agent/init-work-order` + `.factory/templates/work-order.md`, filling only the traced summary line, exactly as `converge-work-order` does. The stub keeps the executing agent from context-switching into a full authoring session; the human triages the stub later. The rule that protects scope is behavioral — *only author what a human asked for* — not a hard block on the skill.

1. If the intent is ambiguous (unclear outcome, scope, actor, or success signal), run the `clarify-intent` skill before anything else.
2. Verify upstream records exist: every behavior needs a REQ/AC in `docs/product/features/`; every structural decision needs a Blueprint in `docs/architecture/`. Missing product intent → STOP: draft the REQ/BP as a proposal and route it to humans (agents propose, humans approve — `AGENTS.md`). The WO stays unauthored or blocked until the record is approved; never invent REQ/AC IDs to fill the gap. **Before creating any architecture record, read `docs/architecture/README.md`** — do not rely on remembered conventions. Structure goes in a Blueprint; a *decision* (hard-to-reverse + surprising + a real trade-off) goes in an ADR **nested inside the blueprint it shapes**, not a free-standing file — write or extend the blueprint first, then add the ADR to it. Reserve `docs/architecture/decisions/` **only** for a decision that genuinely spans multiple *existing* blueprints. And before a blueprint claims any `applies_to` paths, check the `.factory/config.yaml` `blueprints:` map: never claim paths another blueprint already owns (duplicate ownership is a defect).
3. Allocate the next WO number: highest under `.factory/work-orders/` + 1, zero-padded to 4 digits, ignoring anything at or above the WO-9900 scratch floor (WO-9900+ is reserved for throwaway tooling tests). IDs are minted by directory creation on the shared branch, so two authors on parallel branches can mint the same number — check `.factory/indexes/work-orders.generated.md` (and open PRs) before finalizing. Then run `tools/agent/init-work-order --wo WO-NNNN --title "<title>"` to create the execution directory, and fill the generated `work-order.md` (template: `.factory/templates/work-order.md`): Summary, In Scope, Out of Scope (explicit — anything discovered there later becomes a NEW work order), Requirements and Blueprints by stable ID only.
4. Classify every decision in the Decision classification section: HITL (product judgment, un-blueprinted architecture, destructive operations — executing agents stop and escalate on these) vs AFK (everything else). This section is mechanically required — `validate-work-order` rejects a work-order.md without it. An empty HITL list is a claim night-shift will rely on — make it deliberately; night-shift treats a missing section as ineligible, a deliberately empty HITL list as eligible.
5. Give every listed AC at least one COV row in E2E Acceptance Tests, then run `tools/agent/check-traceability --wo WO-NNNN` and fix what it names.
6. Mark it ready: `tools/agent/update-state --wo WO-NNNN --status ready --phase start --next "run /wo-execute WO-NNNN"`.
