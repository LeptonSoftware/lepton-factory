---
title: Model Routing and Parallelization Policy
summary: Which model tier sits in which seat (orchestrator, judgment gates, implementer, mechanics) and what may run in parallel. Cheapen mechanics, never judgment.
owners: [factory-operators]
applies_to: [".claude/skills/**"]
status: active
last_verified: 2026-07-12
---

# Model Routing and Parallelization

<!-- principle and evidence adapted from obra/superpowers (MIT): their evals measured
judgment collapse with a cheaper model in the controller seat — a plan-mandated defect
shipped 4/5 runs and reviewers praised it as "as required" — while mechanical work lost
no quality on lighter models. -->

## 1. Cheapen mechanics, never judgment

**Rule.** Model tier is assigned by seat, not by convenience:

| Seat | Tier | Why |
|---|---|---|
| Orchestrator (`wo-execute` session) | Strongest available (Fable-class) | Holds every judgment point: gate interpretation, escalation, scope defense. |
| Judgment gates (`challenge-plan`, `audit-verification`, `adversarial-qa` lenses, final review round, `synthesize-review` verdicts, `clarify-intent`/HITL classification) | Strongest available — **never lighter than the implementer it judges** | A weaker reviewer is a rubber stamp. |
| Implementer (`execute-slice`) | Strong coder tier (Opus-class), required | Plans are seam-contracts, not code transcription (BP-COMP-FACTORY-HARNESS ADR-003) — implementers exercise real judgment. |
| Mechanics (index regen, catalog scrapes, bulk renames, formatting, running suites, evidence collection) | Lightest capable tier (Sonnet/Haiku-class) | Prefer a deterministic `tools/agent` script over ANY model when one exists. |

Cross-model diversity is **recommended** for the final falsification round:
`tools/agent/agent-review --runner codex --brief <file>` dispatches a self-contained
brief to an external runner (Codex, Claude, …) without the caller knowing its
incantations. It stays secondary, though — different models repeat the same errors;
independence of context and objective (mandated in every reviewer brief) is the
primary mechanism, model diversity a bonus layer.

- **Applies to.** Every subagent dispatch made by an orchestrator or gate skill.
- **Enforcement.** Review; dispatch-time model parameter where the runner exposes one;
  convention: the events.jsonl `actor` field carries the model/tier of the dispatch.
  Per-dispatch cost telemetry: WO-0002.
- **Exceptions.** ADR + factory-operator approval.
- **Owner.** factory-operators

## 2. Parallelization

**Rule.** Fan out what is independent; serialize what shares state:

- **May run in parallel:** the three adversarial lenses (one message, three
  dispatches); independent review dimensions; context-gathering reads; plan
  steps/slices with no shared files and no dependency edges — each in its own
  worktree.
- **Must stay serial:** anything writing `state.yaml`/`events.jsonl` for the same WO —
  one agent session owns a WO at a time; dependent plan steps; slices sharing files.
- **Parallel WOs = parallel workspaces/worktrees.** Never two agents inside one WO
  directory (a concurrent-writer index corruption was observed live during this
  harness's own review).

- **Applies to.** All orchestrators and phase skills.
- **Enforcement.** Review; single-writer discipline documented in `.factory/README.md`;
  file-locking lint is WO-0002 scope.
- **Exceptions.** ADR + factory-operator approval.
- **Owner.** factory-operators
