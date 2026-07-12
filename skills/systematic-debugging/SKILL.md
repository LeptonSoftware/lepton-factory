---
name: systematic-debugging
description: Use when a test fails, a build breaks, behavior doesn't match expectations, or any bug or unexpected error appears — before proposing any fix.
---
<!-- adapted from obra/superpowers systematic-debugging (MIT) and mattpocock/skills diagnosing-bugs (MIT) -->

# Systematic Debugging

NO FIXES WITHOUT ROOT CAUSE. Symptom patches mask the defect and create new bugs; systematic debugging is FASTER than guess-and-check thrashing, including in emergencies.

## Phase 1 — Read, then reproduce (this is the skill; everything else is mechanical)

1. Read the error message completely — the whole stack, the actual values.
2. Build a red-capable feedback loop FIRST: one command — a failing test, a curl, a CLI run against a fixture — that goes red on THIS bug, deterministic, fast, and that you have already run at least once (keep the invocation and its output). Tighten it: a 2-second deterministic loop is a debugging superpower; a 30-second flaky one is barely better than none. For non-deterministic bugs, raise the reproduction rate rather than chasing a perfect repro.
3. **No red-capable command, no hypothesis phase.** Catching yourself reading code to build a theory before this command exists — stop; jumping straight to a hypothesis is the exact failure this skill prevents.

## Phase 2 — Hypotheses

Generate 3–5 ranked falsifiable hypotheses before testing any of them — single-hypothesis generation anchors on the first plausible idea. Each states its prediction: "If X is the cause, then changing Y will make the bug disappear / changing Z will make it worse." A hypothesis with no prediction is a vibe — sharpen it or discard it.

## Phase 3 — Experiments

- One variable per experiment; run the loop after each change.
- Instrument at component boundaries: log what enters and what exits, run once to see WHERE it breaks, then analyze. Never "log everything and grep".
- Tag every debug log with a unique prefix, e.g. `[DEBUG-a4f2]` — cleanup becomes a single grep. Untagged logs survive; tagged logs die.
- Performance regressions: measure first, then bisect.

## Phase 4 — Fix and prove

1. State the confirmed root cause before writing the fix.
2. Write a regression test at a correct seam that fails for the root-cause reason; then fix; observe it pass. If no correct seam exists, that itself is a finding — file it as a feedback record or a new WO.
3. Prove the test guards: revert the fix, the test MUST fail, restore, the test passes.
4. Remove every `[DEBUG-` line (one grep). State the winning hypothesis in the commit message so the next debugger learns.

**3+ failed fixes = wrong architecture, not a failed hypothesis.** Stop, record it, and escalate — do not attempt a fourth fix.
