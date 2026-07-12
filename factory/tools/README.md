# tools/agent — deterministic factory scripts

Scripts callable by humans and agents. Conventions (binding for new scripts):

- **Deterministic.** No LLM calls, no network, no prompts. python3 stdlib +
  bash/coreutils only — no jq/yq/pip. Shared helpers live in `_lib.py`
  (including a forgiving YAML-subset parser sized to our file shapes).
- **Exit codes are gates.** 0 = pass. Non-zero = fail, and every failure message
  names the next action ("checklist has 3 unchecked items in Phase 2 — complete
  or [SKIP] them with reasons"), not just the problem.
- **`--help` on everything; non-interactive; machine-friendly output.**
- Scripts are the only writers of `state.yaml`, `events.jsonl`, and
  `.factory/indexes/` — agents never hand-edit those.

## Inventory

| Script | Purpose |
|---|---|
| `init-work-order --wo WO-1042 [--title …]` | Create (or resume) a WO execution dir from templates. Idempotent — never clobbers. |
| `update-state --wo … [--status] [--phase] [--slice] [--gate NAME=VALUE] [--skip-reason] [--approver] [--next] [--blocked] [--plan-revision] [--commit] [--actor]` | The only writer of state.yaml (atomic, round-trip-checked); validates enums + lifecycle transitions (blocked records `blocked_from` and resumes only there; merged/released never re-enter). `human_approval=approved` requires `--approver` (a human). Any `--gate NAME=skipped` requires BOTH `--skip-reason` and `--approver` — a waiver is a human act (docs/runbooks/break-glass.md); recorded in `waiver_approvers`. Appends one events.jsonl line per call (with `actor`). |
| `validate-work-order --wo … [--strict] / --all [--tier-override t]` | THE completion gate: files, placeholders, checklist resolution, sections, verdict-inside-last-round, events integrity, status, per-tier gates (a required gate at `skipped` passes only with a recorded human waiver — skip_reasons + waiver_approvers; `--tier-override` may only raise). Low tier: context.md/contract.md/implementation-plan.md are optional (validated when present). Before in_review: reduced structural check unless `--strict`. CI runs `--all` (corrupt state = FAIL; merged/released = historical, parseability + events only). |
| `check-traceability [--wo …]` | REQ/AC/BP/COV graph: references resolve, ACs covered, no duplicate or malformed IDs. Scratch WOs excluded repo-wide. |
| `generate-indexes [--check]` | Regenerates `.factory/indexes/*.generated.md` + `docs/testing/test-catalog.generated.md` (atomic writes; scratch WOs excluded; polyglot test detection — suffixes, `test_*.py`, test dirs, Rust `#[test]` content probe; build/venv dirs pruned). `--check` = CI staleness gate. |
| `check-drift [--base ref] [--wo …]` | Blueprint↔code drift gate: touched blueprint-owned paths require an updated blueprint doc or a recorded disposition (`drift-accepted:` / `no-blueprint-change:`); docs pass WARNs on untouched docs whose `applies_to` matches the diff (`--strict-docs` to fail). |
| `review-package --wo … --gate <name> [--base ref] [--out dir]` | Assembles a controlled-context review bundle (diff + contract.md + brief stub with the gate's must/must-not-receive rules) under an output dir; pairs with `agent-review`. |
| `agent-review --list / --runner codex --brief f` | Cross-model review adapter: dispatches a self-contained brief to an external runner (read-only); caller appends the report to review-log.md. |
| `risk-tier --wo … [--base ref] [--write] [--verify] [--set t --approver n]` | Computes tier from changed paths (committed + working tree + untracked) × config risk rules; `--write` raises (never lowers) state.yaml risk_tier; `--verify` fails when the computed tier ranks above the recorded one (CI runs this; a human `--set` record is honored while the computed tier stays within what the human saw). `--set` + `--approver` is the ONLY lowering path — a HUMAN decision, events `risk_tier.lowered`; agents may not use it on their own judgment. |

## Gate name mapping

`.factory/config.yaml` `gates:` lists per-tier requirements. The high-tier lenses
`adversarial_behavior|operations|architecture` record their merged outcome in the
single state.yaml field `adversarial_qa` — `synthesize-review` merges lens reports
before the gate is set. At medium tier there is no separate adversarial gate: the
lens checklists and the convergence gap check fold into the final review round
(`.factory/README.md` §4); `adversarial_combined` stays mapped for compatibility.
`validate` means "this script ran" and is always satisfied by running it.

## Adding a script

Follow the conventions above, reuse `_lib.py`, add a row to the inventory table,
and exercise it end-to-end against a scratch WO (init → walk lifecycle → validate)
before committing. Scratch WOs use the reserved range `WO-9900`+
(`.factory/config.yaml ids.scratch_min`): indexes, traceability, and
`validate --all` ignore that range, so a forgotten scratch dir cannot become a
fake record — but delete them afterward anyway and re-run `generate-indexes`.

## Events

`events.jsonl` is written ONLY by these scripts — a hand-written event line is a
defect and fails `validate-work-order`'s events check (JSON per line, required
keys `ts`/`wo`/`event`, `wo` matching the directory, non-decreasing `ts`). The
authoritative event taxonomy lives in `_lib.append_event`'s docstring:
`wo.initialized`, `state.updated`, `risk_tier.raised`, `risk_tier.lowered`
(human `--set` only, carries `approver`). Every line records an
`actor` (default `$USER/agent`; `update-state --actor` overrides).
