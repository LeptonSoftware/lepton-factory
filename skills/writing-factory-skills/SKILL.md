---
name: writing-factory-skills
description: Use when creating or editing any skill in this repository — defines the taxonomy, frontmatter, size discipline, controlled-context rules for reviewer briefs, and the editing tests a skill change must pass.
---

# Writing Factory Skills

<!-- conventions adapted from mattpocock/skills writing-great-skills and
obra/superpowers skill-testing practice (MIT) -->

## Taxonomy — pick one

- **Orchestrator** (user-invoked): add `disable-model-invocation: true`. Owns
  sequencing only. Keep it a thin shell (10–25 lines) that invokes discipline skills
  and `tools/agent/` scripts in order. The disciplines hold the how.
- **Phase discipline** (model-invoked): carries the full protocol for one phase.
  Description must state WHEN it fires ("Use when…") with concrete triggers, because
  the description is all the model sees when routing.

Never let a skill create artifacts outside the canonical set (`.factory/README.md` §1–2)
or contradict the operating manual — the manual wins; fix the manual first if it's wrong.

## Writing rules

1. **Positive recipes.** Say "do X, then Y" — measured to outperform prohibition
   lists. Keep a short anti-pattern list only where reviewers need tripwires.
2. **Every line must change behavior.** The no-op test: if deleting a line wouldn't
   change what an agent does, delete it. The negation test: if the opposite of a
   sentence is something no one would ever do, the sentence is filler.
3. **Leading words matter.** Front-load the imperative ("Dispatch a fresh reviewer
   with…" not "It is important that reviewers are fresh…").
4. **Link, don't restate** — except reviewer/challenger briefs, which must be
   SELF-CONTAINED: the dispatched agent gets only the brief, so the brief carries its
   own rules, its controlled inputs (what it receives), and its exclusions (what it
   must NOT receive: implementer self-justification, prior verdicts, "this is
   approved" framing).
5. **Attribute transplants** with an HTML comment naming source and license.

## Before you ship a skill change

- Read the current version fully — skills evolve; don't edit from memory.
- Run the editing tests (no-op, negation, leading-word) on changed lines.
- For reviewer skills: run a planted-defect check — hand the skill a diff containing
  one known defect (ideally one the plan mandates) and confirm the reviewer flags it.
  A reviewer skill that praises a plan-mandated defect fails.
- Record the change's motivation in `.factory/feedback/` if it came from execution
  friction — that's the loop working.
