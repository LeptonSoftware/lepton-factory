# vinxi-factory

The Vinxi software-factory harness as a Claude Code plugin: Work-Order lifecycle
skills, governance policies, artifact templates, and deterministic tools.

## Install

```
/plugin marketplace add LeptonSoftware/vinxi-factory
/plugin install vinxi-factory@vinxi-factory
```

Then, in any repo you want to run the factory in:

```
/factory-init
```

This copies the harness into your repo (`.factory/`, `tools/agent/`) and writes
`AGENTS.md` / `CLAUDE.md` routers. Requires **Python 3** on PATH.

## Update

```
/plugin update vinxi-factory
/factory-init --upgrade
```

`--upgrade` re-copies managed files and preserves anything you edited (it reports
those so you can move divergences into `.factory/overrides/`). Managed files should
not be hand-edited — `.factory/README.md` and `.factory/policies/**` carry a banner
marking them as managed; `tools/agent/**` are managed too (tracked in the manifest
and re-copied on `--upgrade`) but are not bannered so their shebangs stay intact.
`.factory/config.yaml` is yours and is never overwritten.

## What you get

- 19 skills (author/execute/review Work Orders + phase disciplines)
- The factory operating manual, policies, and artifact templates
- Deterministic tools in `tools/agent/` (exit codes are gates)
