---
title: Testing Policy
summary: Executable rules for seam-based TDD, false-confidence test patterns, COV tagging, and the generated test catalog.
owners: [factory-operators]
applies_to: ["apps/**", "packages/**", "services/**", "docs/testing/**"]
status: active
last_verified: 2026-07-12
---

# Testing Policy

Normative rules only. How to write tests well: `docs/testing/writing-tests.md`.
Exception process for every rule: ADR + owner approval.

## 1. Test-first at meaningful seams

**Rule.** The seams requiring test-first (red → green → refactor) and the
evidence-first alternative for everything else are defined in `.factory/README.md`
§6. Additionally: RED evidence (the failing run before implementation) and GREEN
evidence (the passing run after) are recorded in `checklist.md`; a violation is
repaired by revert-and-verify (revert the implementation, observe the test fail,
restore), never by deleting the test.

- **Applies to.** `apps/**`, `packages/**`, `services/**`
- **Enforcement.** Gate C (audit-verification) checks RED/GREEN evidence per seam;
  Gate B checks the plan's declared test-first seams were honored.
- **Exceptions.** ADR + owner approval; spikes and prototypes are already
  evidence-first per §6, not exceptions.
- **Owner.** factory-operators

## 2. Evidence-first work still produces evidence

**Rule.** Wiring, generated config, mechanical migrations, and spikes require
runtime evidence (command + observed output, or screenshot) recorded in
`evidence/` or `checklist.md` before the step is checked off. "It compiles" is not
evidence.

- **Applies to.** `apps/**`, `packages/**`, `services/**`
- **Enforcement.** `tools/agent/validate-work-order` rejects checklists with
  unchecked items (a blank-evidence lint is planned — review until it lands);
  Gate C audits the evidence itself.
- **Exceptions.** None.
- **Owner.** factory-operators

## 3. No false-confidence tests

**Rule.** These patterns are defects wherever they appear, even when a plan
mandates them (a reviewer must flag them regardless — `.factory/README.md` §4,
Gate B):

- Tests that cannot fail — no assertion, or the expected value recomputed the same
  way the code computes it.
- Mock-only assertions / testing the mock — asserting a mock was called instead of
  asserting observable behavior.
- Snapshot over-acceptance — regenerating snapshots without reading the diff.
- Flaky-retry masking — retry annotations or loops added to make a failing test
  pass instead of fixing the nondeterminism.
- Test-only methods on production classes.

Concrete examples of each: `docs/testing/writing-tests.md`.

- **Applies to.** `apps/**`, `packages/**`, `services/**`
- **Enforcement.** Gate C (audit-verification) mutates the behavior under test in a
  disposable worktree — tests that stay green are findings; Gate B flags the
  patterns on sight.
- **Exceptions.** ADR + owner approval.
- **Owner.** factory-operators

## 4. Tests covering ACs carry COV tags

**Rule.** Every test that proves an acceptance criterion carries its
`COV-<AREA>-NNN.N` tag (grammar: `.factory/config.yaml` `ids`) in the test's
framework-native metadata (tag, mark, annotation, or title string) **or in a
structured comment adjacent to the test** — never in the test's identifier, which
cannot carry the ID grammar in most languages. The per-framework realization is
the idiom table in `docs/testing/writing-tests.md`; the mechanical contract is
that the literal ID string (optionally `@`-prefixed) appears in the test file's
text. `REQ-*` / `AC-*` tags are optional navigation aids. One AC may have many
COV tests; a COV tag maps to exactly one AC.

- **Applies to.** `apps/**`, `packages/**`, `services/**`
- **Enforcement.** `tools/agent/generate-indexes` scrapes the tags into
  `docs/testing/test-catalog.generated.md`; `tools/agent/check-traceability`
  (CI, every PR) verifies every AC has at least one COV row in the WO's E2E
  table; it does not yet resolve COV tags to actual test files — that resolution
  is reviewed at Gate C until the tag-to-test check lands (planned:
  `check-traceability` extension).
- **Exceptions.** `[SKIP]` + reason in the WO checklist, audited at Gate C.
- **Owner.** factory-operators

## 5. The test catalog is generated, never hand-maintained

**Rule.** `docs/testing/test-catalog.generated.md` is written only by
`tools/agent/generate-indexes` from test-file tags. Test files are the source of
truth. Hand edits are defects.

- **Applies to.** `docs/testing/test-catalog.generated.md`, `.factory/indexes/**`
- **Enforcement.** CI regenerates and diffs; a dirty diff fails the build.
- **Exceptions.** None.
- **Owner.** factory-operators
