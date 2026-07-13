---
name: wayfinder
description: Use when entering unfamiliar territory — a source, domain, subsystem, or codebase area new to this Work Order — and you need to map it before committing to scope or a contract. Fires during clarify-intent and compile-contract when the way from here to the goal is fogged. Produces a destination-first fog map that marks each fact known / assumed / unknown, so the unknowns become explicit questions rather than silent gaps.
---
<!-- adapted from mattpocock/skills wayfinder (MIT) — kept the destination-first
fog-of-war mapping idea; dropped the issue-tracker machinery and the HITL/AFK ticket
classification (that classification lives in the Work Order template, not here). -->

# Wayfinder

A loose idea has arrived wrapped in fog: the way from here to where you're going isn't visible yet. Wayfinding **charts that way** before charging at it. Use it whenever a Work Order touches territory new to you — a forked source, an unfamiliar domain, a subsystem you haven't read — and the temptation is to guess. Name the destination, map the fog, and turn the unknowns into explicit questions the downstream contract or clarify session must resolve.

This is an *exploration* discipline, not a decision classification. It says nothing about who resolves each question — the HITL/AFK split lives in the Work Order's Decision classification section, not here.

## 1. Name the destination first

Naming the destination is the first act of charting — it fixes the scope, so every later judgment orients to it. State in one or two lines what reaching the end looks like: a compiled contract, a resolved decision, a landed migration, a mapped source. Everything past that line is out of scope and does not belong on the map.

## 2. Map the fog of war

Sweep the territory **breadth-first** — fan out across the whole space rather than deep on one thread — and mark every load-bearing fact into one of three zones:

- **Known** — you have read it and can cite where (file, record, source excerpt). Facts, not guesses.
- **Assumed** — you are proceeding as if it's true but haven't confirmed it. Each assumption is a risk; write down what would confirm or break it.
- **Unknown** — you can see the question is coming but can't answer it yet. These are the frontier.

The map is deliberately incomplete: don't chart what you can't yet see. The test for whether something is a sharp Unknown or still formless fog is whether you can *state the question precisely now* — not whether you can answer it.

## 3. Turn unknowns into questions

Each Unknown becomes an explicit question routed to where it gets resolved:

- A domain-level unknown (a term's meaning, a boundary between concepts) → hand it to `domain-model` and the glossary.
- A product/scope/decision unknown → a Known Unknown or HITL entry the contract will carry; put it to the human via `clarify-intent`.
- A code/source fact you can look up → resolve it now by reading, and promote it from Unknown to Known. Wayfinder never leaves a lookupable fact as an assumption.

An Assumption that stays unconfirmed at the destination is itself a Known Unknown — record it as one, don't bury it.

## Output

A short fog map — Destination, then Known / Assumed / Unknown lists — written into the artifact that owns the next step (the WO's context notes, the contract's Known Unknowns, or the clarify coverage report). It is a signpost, not a standalone deliverable: it exists to make the frontier legible before scope or contract is fixed, then it graduates into those records as the unknowns resolve.
