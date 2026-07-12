---
name: factory-sweep
description: Periodic cross-commit maintenance sweep for drift no single review sees. Run as /factory-sweep [area].
disable-model-invocation: true
---

# Factory Sweep

A read-only survey across commits and PRs. Findings become new Work Orders or feedback records — never direct fixes.

1. Scope: the area given, else the whole repo. Read `docs/domain/glossary.md` and the blueprint ownership map in `.factory/config.yaml` first.
2. Sweep for cross-commit drift:
   - duplicated abstractions landed by different PRs (same capability, two homes)
   - architecture erosion: code violating a blueprint contract or living outside its blueprint's owned paths
   - dependency cycles between packages
   - naming inconsistency against the glossary
   - test gaps: behavior with no COV coverage; suites that stopped running
   - doc drift: descriptive docs whose `last_verified` predates changes under their `applies_to` globs
3. Run `tools/agent/check-traceability` and `tools/agent/generate-indexes`; treat their failures as findings.
4. Disposition per finding, citing the record ID it violates: mechanical well-bounded fixes → a new WO via `/wo-author`; process or harness friction → a feedback record from `.factory/templates/feedback.yaml` under `.factory/feedback/<YYYY-MM>/`.
5. Report the findings table (severity, area, violated record, disposition). Product code stays untouched.
