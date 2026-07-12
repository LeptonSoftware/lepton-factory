---
name: factory-learn
description: Synthesize accumulated feedback records into concrete harness improvements. Run as /factory-learn.
disable-model-invocation: true
---

# Factory Learn

1. Read every `.factory/feedback/*/WO-*.yaml` whose `absorbed_by` is null. Cluster by recurrence: the same friction across 2+ WOs is a pattern; one-offs stay recorded, unactioned.
2. For each pattern, choose the cheapest structural fix, preferring the most mechanical: deterministic check (`tools/agent/` script or CI gate) > template change (`.factory/templates/`) > policy update (`.factory/policies/`) > skill edit (`.claude/skills/`) > doc update. A prose exhortation is never the fix — prose-only gates get skipped under pressure; that is measured, not hypothetical.
3. Each improvement becomes a Work Order via `/wo-author` (harness paths are owned by BP-COMP-FACTORY-HARNESS; several are high tier by `.factory/config.yaml`).
4. Skill edits follow `writing-factory-skills`, including a planted-defect eval for any reviewer skill.
5. Close the loop: set `absorbed_by: WO-NNNN` in each absorbed feedback record (lifecycle: `.factory/feedback/README.md`). Feedback that implies a requirement change is routed to `docs/product/` as a proposal — never absorbed silently into the harness.
6. Report: patterns found, WOs created, feedback items absorbed vs deferred.
