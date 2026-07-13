---
description: Wizard — set up the Lepton factory in this repo and seed your first feature
---

You are running the Lepton factory onboarding wizard. Conduct a short interview using the
`clarify-intent` discipline — **one question at a time**, propose-and-confirm — then hand a
structured seed to the deterministic setup script.

## 1. Detect state
Run: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/factory_init.py" --target "$(pwd)"`
This scaffolds `.factory/`, the docs skeleton, routers, and tools. If `.factory/` already
existed, tell the user and offer `--upgrade` instead of re-seeding.

## 2. Interview (one question at a time; confirm each answer)
1. **Ambition tier** — internal app or production service? (Prototype is not yet supported by
   the wizard.) This sets rigor.
2. **Tech stack** — language/framework → `generic` or `node`.
3. **First outcome** — what is the very first thing to build? Use `clarify-intent` to sharpen it
   into ONE testable requirement with 1–3 acceptance criteria. Confirm the REQ + ACs verbatim.
4. **Architecture** — the top-level container this runs in (name, what path it owns). Draft a
   one-paragraph container summary; confirm.
5. **Domain terms** — 3–5 key terms + one-line definitions.

Do NOT invent requirements the user didn't intend. If anything is vague, ask.

## 3. Assemble the seed and run the setup
Build a seed JSON matching the contract in `scripts/seed.py` (tier, stack, area, feature{slug,
title,user_story,reqs[{id_seq,statement,acs[]}]}, container{slug,name,title,summary,owner,
applies_to[],body}, overview{...}, glossary[{term,definition}], and a `date` field = today).
Write it to `.factory/.seed.json`, then run:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/factory_init.py" --target "$(pwd)" --seed .factory/.seed.json --tier <tier> --stack <stack>`

## 4. Report
- If the script printed "Seed applied and validated" → tell the user their first feature is seeded
  and `WO-0001` is authored; point them to `/wo-execute WO-0001`.
- If it printed "Seed failed the validator gate" → show the output; the seed IDs/paths are
  inconsistent — walk back through the relevant answer and retry. Do not hand-edit generated files.
- Never fabricate approval: everything written reflects what the user confirmed in the interview.
