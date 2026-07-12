# The Factory — Operating Manual

This directory is the repository-local control plane: policies, templates, work-order
execution state, review evidence, feedback, and generated indexes. This document is the
single authoritative definition of the delivery lifecycle. Skills implement it; CI
enforces it; nothing overrides it except `docs/product/` intent and safety.

Derived from the 8090 Software Factory operating model (attribution:
[8090-inc/software-factory-plugin](https://github.com/8090-inc/software-factory-plugin),
MIT). We intentionally diverge: our own hidden `.factory/` root instead of `.sw-factory/`,
nested `work-orders/`, machine-readable state, and falsification gates. If any tool
tries to create `.sw-factory/`, that is a defect — CI blocks it.

## 1. Canonical artifacts

| Artifact | ID | Lives at | Meaning |
|---|---|---|---|
| Product Overview | — | `docs/product/overview/` | Durable product-wide context |
| Feature Requirements | `REQ-<AREA>-NNN` / `AC-<AREA>-NNN.N` | `docs/product/features/<feature>/requirements.md` | Externally observable behavior |
| Container Blueprint | `BP-CONT-<NAME>` | `docs/architecture/containers/` | A runnable/deployable unit |
| Component Blueprint | `BP-COMP-<NAME>` | `docs/architecture/components/` | An enduring reusable capability |
| Feature Blueprint | `BP-FEAT-<NAME>` | `docs/architecture/features/` | Composition of components for a feature |
| ADR | `ADR-NNN` | Inside its blueprint (cross-cutting: `docs/architecture/decisions/`) | An architectural decision |
| Work Order | `WO-NNNN` | `.factory/work-orders/WO-NNNN/` | Bounded delivery contract |
| Coverage | `COV-<AREA>-NNN.N` | Test tags + WO contract | Maps a test to an AC |

IDs never change after publication. Downstream artifacts reference upstream IDs; they
do not copy prose. Requirements state observable behavior only; blueprints state
structure, contracts, and invariants; work orders state scope.

## 2. Work Order execution directory

```
.factory/work-orders/WO-1042/
├── work-order.md          # Summary, In/Out of Scope, Requirements, Blueprints, E2E Acceptance Tests
├── context.md             # Entity index: every record read, code inspected, reuse found
├── contract.md            # Compiled execution contract (see §4, Gate 0)
├── implementation-plan.md # Plan (see template); revised in place, revision counted
├── checklist.md           # Live execution checklist; [x] or [SKIP] + reason, never blank
├── review-log.md          # Append-only review rounds; verdict APPROVED | CHANGES_REQUESTED
├── state.yaml             # Machine-readable phase/gate state (the resume point)
├── events.jsonl           # Append-only lifecycle events
└── evidence/              # Screenshots, outputs, benchmark results (no large binaries)
```

`state.yaml` is the source of truth for *where execution is*; the checklist is the
source of truth for *what has been verified*. Update both at every checkpoint, not
retrospectively. Any agent must be able to resume from these files alone —
conversation history is never the execution database.

## 3. Lifecycle

```
ready → context → contract → planned → in_progress → in_review → approved → merged → released
                                     ↑______________________|
                                        (changes requested)
any state → blocked (blocked_on set, human escalation)
```

Phase transitions are recorded by `tools/agent/update-state` (writes `state.yaml`,
appends to `events.jsonl`). `tools/agent/validate-work-order` is the completion gate;
CI runs it on every PR. A workflow written only in prose gets skipped under pressure —
that is measured, not hypothetical — so every gate below must leave a machine-checkable
record.

## 4. Gates

Ceremony is risk-tiered (§5). Gate order within the lifecycle:

**Gate 0 — Execution contract** (`compile-contract`). Before planning, compile
Requirement + Blueprint + Work Order into `contract.md`: verbatim ACs, invariants,
interfaces touched, disallowed changes, required evidence per AC (the verification
contract: automated test + runtime action + expected result + negative case), known
unknowns, and decisions requiring a human. Compilation surfaces specification holes
before they become code.

**Gate A — Plan challenge** (`challenge-plan`). A fresh reviewer attempts to *reject*
the plan: unverified assumptions, missing scenarios, regression surface, transaction/
retry/ordering/recovery semantics, simpler designs, migration credibility. Verdict:
`APPROVE | APPROVE_WITH_RISKS | REVISE | HUMAN_DECISION_REQUIRED`. The challenger is
never told the design is already approved.

**Gate B — Slice review** (`review-slice`). After each vertical slice: one reviewer,
two ordered verdicts — (1) spec compliance against the contract, (2) engineering
quality against policies. The reviewer receives the diff, the contract, and the review
brief — not the implementer's self-justification. A reviewer must flag defects even if
the plan mandates them.

**Gate C — Verification audit** (`audit-verification`). Audits the *proof*, not the
code: do tests fail when behavior is deliberately broken (mutate in a disposable
worktree, then revert)? Are assertions meaningful? Do production paths run? Does
evidence cover every AC and negative case? "All tests pass" is not accepted as input.

**Gate D — Adversarial QA** (`adversarial-qa`; separate gate at high tier only).
Clean-context reviewers whose objective is falsification, partitioned into three
independent lenses run in parallel: *behavior/abuse*, *failure/operations*,
*architecture/longevity*. They receive the problem statement, ACs, invariants, run
instructions, and diff — not the plan's justification, not each other's findings.
`synthesize-review` merges findings into `review-log.md` afterward. At medium tier
the three lens checklists fold into the final review round below.

**Convergence** (`converge-work-order`; separate gate at high tier only). Compare
landed reality against Requirements, Blueprints, plan, and tests. Gap types:
`missing`, `partial`, `contradicts`, `unrequested`. Legitimate remaining work becomes
new Work Orders — the active one never silently stretches. At medium tier the
convergence gap check folds into the final review round below.

**Final review round**. Durable, append-only, in `review-log.md`, across the six
dimensions: requirements alignment, blueprint alignment, architecture/conventions,
tests/build, user-visible verification, security/privacy/data. Verdict `APPROVED` or
`CHANGES_REQUESTED`. After changes, a fresh full round — not a comment-by-comment
recheck. The implementer never writes the verdict. **At medium tier** this round is
the one clean-context falsification pass: the reviewer's brief carries the three
adversarial lens checklists (Gate D) and the convergence gap check alongside the six
dimensions — one dispatch, full coverage. **At high tier** Gate D and convergence
stay separate gates and this round is the closing verdict on top of them. Where the
runner supports it, dispatch the final falsification reviewer on a different model
family than the implementer — same-family reviewers share blind spots.

**Review-loop cap.** After 2 repair→fresh-review cycles on the same gate, stop and
escalate (`update-state --status blocked --blocked "review loop exceeded — human
decision required"`) — a loop that survives two honest repairs needs a human, not a
third round.

### Enforcement boundary

Machine gates validate structure and make skipping visible in the diff:
`validate-work-order` checks files, sections, checklist resolution, verdict strings,
and a record for every tier-required gate — and refuses `skipped` for gates the tier
requires. They cannot verify reviewer identity or review quality. That layer is
enforced by PR review, `CODEOWNERS` routing, and branch protection — which must be
enabled on the repository; the harness assumes it (the exact settings:
`CONTRIBUTING.md`). The `human_approval` gate is
attested, not verified: a human records it (the approver's name is recorded with
it), and because all execution state lands in the PR diff, a forged record is
detectable in review even though no tool can detect it. When a gate is wrong or an
incident preempts the lifecycle, the sanctioned exception path — hotfix lane and
human gate waivers — is `docs/runbooks/break-glass.md`; there is no unsanctioned one.

## 5. Risk tiers

Computed by `tools/agent/risk-tier` from changed paths + `.factory/config.yaml` rules;
recorded in `state.yaml`; may be raised by humans, never lowered by agents. A HUMAN
may lower an over-computed tier via `risk-tier --set <tier> --approver "<name>"`
(recorded as `risk_tier.lowered` with the approver; agents may not use `--set` on
their own judgment) — protocol: `docs/runbooks/break-glass.md`, which also defines
the hotfix lane and the human gate-waiver protocol.

| Tier | Examples | Required gates |
|---|---|---|
| **low** | docs, runbooks, generated indexes — or any change a human tier-lowers via `risk-tier --set` | B (single review) + validate. `context.md`/`contract.md`/`implementation-plan.md` are optional (still validated when present) |
| **medium** | normal feature, API addition, UI flow, non-destructive migration | 0, A, B, C + final review = one clean-context falsification round carrying the adversarial lens checklists and the convergence gap check |
| **high** | auth(z), billing/money, data migration, public API, concurrency, security boundaries, statement/query semantics | 0, A, B, C, D (all three lenses) + convergence + final review + human approval |

The authoritative per-tier gate list is `gates:` in `.factory/config.yaml`; this
table is illustrative.

**The docs lane.** Pure `docs/**` edits (typo fixes, runbook updates, corrections to
descriptive text) are the one sanctioned path that does not require a Work Order —
CI does not demand one for them. The boundary: anything touching
`.factory/config.yaml`, `.factory/policies/`, `.factory/templates/`, `tools/agent/`,
`.claude/skills/`, `.github/workflows/`, or product code needs a Work Order.
Doc-class change authority (descriptive / architectural / product intent) still
applies per `docs/README.md`.

**The fast lane (low tier).** A cosmetic or trivially-scoped code change does not
re-derive the process — this is the whole recipe:

```
tools/agent/init-work-order --wo WO-NNNN --title "…"        # context/contract/plan optional at low tier
for st in context contract planned in_progress; do tools/agent/update-state --wo WO-NNNN --status $st; done
# make the change; run the targeted test; run the software
tools/agent/update-state --wo WO-NNNN --gate slice_reviews=approved   # after one independent review of the diff
tools/agent/update-state --wo WO-NNNN --status in_review
tools/agent/validate-work-order --wo WO-NNNN                # then PR
```

Fill work-order.md's six sections in a few lines each — Summary can be one sentence;
Decision classification "HITL: none / AFK: all" is valid when true. The status walk
stays one-step (the ledger is the point) but it is four seconds of shell, not
ceremony. Bug fixes are NOT cosmetic: they take their computed tier and the
regression-test-first seam rule (§6) regardless of size — small bug fixes are where
agent changes measurably fail most.

**Batch maintenance WOs.** Small unrelated fixes accumulate into one maintenance WO
(typically from `factory-sweep` findings): one WO, one slice per fix, each slice
independently reviewed and committed. This keeps tiny fixes traceable without one
WO's overhead per typo — but never batch anything above low tier into them.

## 6. Implementation rules

- **Plans describe boundaries, not full code**: outcome, files, interfaces, invariants,
  vertical slices (tracer bullets), per-step verification, dependencies, commit
  boundaries, stop conditions. Pseudocode only where ambiguity remains.
- **TDD at meaningful seams** (business rules, bug fixes, parsers, state transitions,
  contracts, persistence, algorithms, security logic, previously failing cases):
  red → green → refactor; violation is repaired by revert-and-verify, not delete.
  Wiring, generated config, mechanical migrations, spikes: evidence-first instead.
- **Run the software.** Web → drive the flow; API → invoke the endpoint; CLI → execute
  it; worker → run against a fixture; migration → apply and roll back on a disposable
  database. Record evidence in `evidence/` or the checklist.
- **Isolated execution**: dedicated branch/worktree, clean baseline verified before the
  first change.
- **Reuse before invention**: the plan must record components searched, analogous code
  inspected, and the chosen option among reuse / extract / follow-pattern / new
  (with layer justification, consumers, owner). See `.factory/policies/code-reuse.md`.

**Spikes.** Exploratory spikes are sanctioned on `spike/<slug>` branches: no Work
Order, no gates, no REQ required — hack freely. Spike branches are **never merged**;
their deliverable is knowledge, recorded as a feedback record, a draft REQ/Blueprint
proposal, or an ADR — then the branch is deleted and the real work ships through a
Work Order. Code that wants to merge is not a spike.

## 7. Precedence

When instructions conflict:

1. Safety, security, legal policy
2. Requirements (`docs/product/`)
3. Blueprints and their contracts
4. Work Order scope and exclusions
5. `AGENTS.md` and `.factory/policies/`
6. The approved implementation plan
7. Repository/domain skills
8. General engineering skills
9. Tool defaults

An implementation plan conflicting with an AC means the plan changes. A skill
conflicting with a policy means the policy wins. Agents propose; owners approve
material product and architecture judgment.

## 8. Feedback and factory learning

Execution friction, failures, and improvement proposals are recorded per Work Order in
`.factory/feedback/<YYYY-MM>/WO-*.yaml` (template in `.factory/templates/`). The
`factory-learn` orchestrator periodically synthesizes recurring records into skills,
templates, linters, scripts, docs, and CI checks. Feedback that implies a requirement
change is routed to `docs/product/`, never absorbed silently.

## 9. Compatibility notes (upstream 8090)

We keep: the four execution files' section structures, checklist `[x]`/`[SKIP]` +
reason discipline, append-only review rounds, verdict strings, `REQ`/`AC` ID grammar,
six review dimensions, WO document sections ending in `## E2E Acceptance Tests`.
We diverge: nested `.factory/work-orders/` layout under our hidden root, added `contract.md`/`state.yaml`/
`events.jsonl`/`evidence/`, `COV-` with dashes (upstream uses `COV_` underscores),
separated planning and implementation phases, mandatory (not "preferred") independent
review, reviewers never modify product code.
