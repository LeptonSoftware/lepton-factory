---
name: compile-contract
description: Use when a Work Order enters the contract phase (Gate 0) — after context traversal is complete and before any planning. Compiles Requirement + Blueprints + Work Order into contract.md.
---
<!-- consistency checks adapted from github/spec-kit analyze.md (MIT) -->

# Compile the Execution Contract (Gate 0)

Compilation is derivation, not authorship: every entry cites the source ID it came from (REQ-, AC-, BP-, ADR-, or a WO section). A section you cannot fill from the records is a finding — record it under Known Unknowns or Human Decisions. Never leave it blank; never invent content to fill it. Compilation exists to surface specification holes before they become code.

## Fill .factory/templates/contract.md into .factory/work-orders/WO-XXXX/contract.md

1. **Acceptance criteria (verbatim)** — copy each linked AC exactly as written, with ID. This is the only sanctioned prose copy; reviewers check it against the source.
2. **Invariants** — from the blueprints: idempotency, ordering, transaction boundaries, consistency, failure semantics, compatibility. Cite the BP/ADR per line.
3. **Interfaces touched** — each public API, event, schema, or storage shape this WO may change, with its compatibility rule (breaking allowed? versioned? additive only?).
4. **Disallowed changes** — from the WO's Out of Scope plus the blueprint ownership map in `.factory/config.yaml`.
5. **Verification contract** — one row per AC: COV ID, automated test, runtime action, expected evidence, negative case. Every AC in the WO's E2E table lands here; this table is what Gate C audits.
6. **Known unknowns** — each with its resolution route: investigate during context / spike / escalate.
7. **Human decisions required (HITL)** — the WO's classification plus anything compilation surfaced. Execution stops on these; they are never resolved by iteration.

## Consistency checks (run during compilation; each hit becomes a contract entry or an escalation)

- **Duplication** — near-duplicate ACs or requirements; mark the lower-quality phrasing for consolidation upstream.
- **Ambiguity** — vague adjectives (fast, scalable, secure, intuitive, robust) lacking a measurable criterion; unresolved placeholders (TODO, TBD, ???, `<placeholder>`). → Known Unknowns, or a `clarify-intent` pass if human input is needed.
- **Underspecification** — an AC with a verb but no object or measurable outcome; WO references to components no blueprint defines.
- **Coverage gaps** — any AC without a credible verification-contract row; any COV with no mapped AC. Fix or escalate before planning.
- **Inconsistency** — terminology drift against `docs/domain/glossary.md`; WO scope contradicting a blueprint invariant.

## Record

Run `tools/agent/check-traceability --wo WO-XXXX`, then
`tools/agent/update-state --wo WO-XXXX --status contract --phase contract --gate contract=done --next "write implementation plan"`.
If HITL entries are unresolved: `tools/agent/update-state --wo WO-XXXX --status blocked --phase contract --blocked "<first unresolved decision>"` and escalate instead.
