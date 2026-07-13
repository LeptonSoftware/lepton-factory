---
description: Wizard — set up the Lepton factory in this repo and seed your first feature
---

You are running the Lepton factory onboarding wizard. Conduct a short interview using the
`clarify-intent` discipline — **one question at a time**, propose-and-confirm — then hand a
structured seed to the deterministic setup script.

## 1. Detect state (lightweight — do not run the script yet)
Check whether the repo is already initialized with a plain filesystem check, e.g.
`test -d .factory && echo present || echo absent` (or just inspect the directory listing).
Do NOT run `factory_init.py` here — the real scaffold+seed happens once, in Step 3.
- If `.factory/` is **absent**: proceed to the interview.
- If `.factory/` is **present**: tell the user the factory is already installed and offer to
  run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/factory_init.py" --target "$(pwd)" --upgrade`
  instead of re-seeding. Only continue into the interview if they explicitly want to seed a
  new feature on top of the existing install.
  Note: re-running with `--seed` overwrites `docs/product/overview/*` and
  `docs/domain/glossary.md` with the new seed content — use `--upgrade` (no `--seed`) if you
  only want to refresh the harness itself without touching those files.

## 2. Interview (one question at a time; confirm each answer)
1. **Ambition tier** — internal app or production service? (Prototype is not yet supported by
   the wizard.) This sets rigor.
2. **Tech stack** — language/framework → `generic` or `node`.
3. **Area code** — derive a short UPPERCASE alphanumeric code for the ID namespace (e.g. CORE,
   AUTH) from the feature/domain being seeded. It feeds `REQ-<AREA>-NNN`, `AC-<AREA>-NNN.M`, and
   `BP-CONT-<NAME>` ids, must be uppercase alphanumeric only, and must NOT contain the substring
   "REQ". Propose one from the interview so far and CONFIRM it with the user before moving on.
4. **First outcome** — what is the very first thing to build? Use `clarify-intent` to sharpen it
   into ONE testable requirement with 1–3 acceptance criteria. Confirm the REQ + ACs verbatim.
5. **Architecture** — the top-level container this runs in (name, what path it owns). Draft a
   one-paragraph container summary; confirm.
6. **Domain terms** — 3–5 key terms + one-line definitions.

Do NOT invent requirements the user didn't intend. If anything is vague, ask.

### Derive-and-confirm the remaining seed fields
The seed schema needs a few fields the interview above doesn't ask for directly. Draft each
from the answers already given and confirm them together (not one-at-a-time) before assembling
the seed:
- `feature.slug` — kebab-case slug of the first outcome (e.g. `greeting-cli`).
- `feature.title` — short human title for the feature.
- `feature.user_story` — one-line "As a ... I want ... so that ..." derived from the first
  outcome.
- `container.slug` — kebab-case slug for the container's doc filename.
- `container.title` — human title for the container.
- `container.body` — the one-paragraph container summary drafted in Q5, reused as the doc body.

## 3. Assemble the seed and run the setup
Build a seed JSON matching the contract in `scripts/seed.py` (tier, stack, area, feature{slug,
title,user_story,reqs[{id_seq,statement,acs[]}]}, container{slug,name,title,summary,owner,
applies_to[],body}, overview{...}, glossary[{term,definition}], and a `date` field = today).
Write it to `.factory/.seed.json`, then run (this single invocation does the scaffold AND the
seed — there is no earlier scaffold-only run):
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/factory_init.py" --target "$(pwd)" --seed .factory/.seed.json --tier <tier> --stack <stack>`

## 4. Report
- If the script printed "Seed applied and validated" → tell the user their first feature is seeded
  and `WO-0001` is authored; point them to `/wo-execute WO-0001`.
- If it printed "Invalid seed:" → this is a schema validation failure (missing/malformed field,
  caught before the validator gate even runs). Read the listed errors, fix the corresponding
  seed field with the user, and re-run the command in Step 3. Do not hand-edit generated files.
- If it printed "Seed failed the validator gate" → this is a later, semantic failure (the seed
  was well-formed but the generated artifacts don't pass `check-traceability` /
  `validate-work-order`). Show the output; walk back through the relevant interview answer and
  retry. Do not hand-edit generated files.
- Never fabricate approval: everything written reflects what the user confirmed in the interview.
