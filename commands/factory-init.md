---
description: Bootstrap or upgrade the Lepton factory harness in the current repo
---

Bootstrap (or, with `--upgrade`, update) the Lepton factory harness in the user's
current repository.

Run this command with the Bash tool from the repository root:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/factory_init.py" --target "$(pwd)" $ARGUMENTS
```

- Pass `--upgrade` through to `$ARGUMENTS` when the user asks to update an existing install.
- The script is stdlib-only Python 3; if `python3` is missing, tell the user to install Python 3.

After it runs, report to the user:
- On a fresh install: the harness is installed; point them to `/wo-author` to create their first Work Order and to `.factory/README.md` for the operating manual.
- If it listed "Preserved adopter-edited files": show that list and suggest moving their divergences into `.factory/overrides/`.
- Never hand-edit `.factory/README.md`, `.factory/policies/**`, or `tools/agent/**` — they are managed; edits go through `--upgrade` or overrides.
