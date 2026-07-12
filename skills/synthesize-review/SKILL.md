---
name: synthesize-review
description: Use when Gate C and Gate D reports are in hand and need merging — after audit-verification and adversarial-qa (high tier; at medium tier Gate D folds into the final review round and this skill is not on the path), before repair work begins.
---

# Synthesize Review Findings

Merge the round's independent reports into one durable record and one repair queue.

1. Collect every Gate C and Gate D report for this round.
2. Dedupe: findings describing the same defect merge into one, keeping the strongest evidence and crediting each source gate/lens.
3. Classify each finding Blocking or Advisory. Blocking = the WO cannot be trusted merged until fixed: a broken AC, a violated invariant, a test that cannot fail, a security or data risk.
4. Map each finding to its files/areas and to the AC, invariant, or policy it violates.
5. Write a FRESH Round into review-log.md per the round template in `.factory/templates/review-log.md` — append-only, never edit prior rounds; one findings-register row per finding; verdict CHANGES_REQUESTED iff at least one Blocking finding survives, APPROVED otherwise.
6. Emit each Blocking finding as a repair item in checklist.md, referencing its findings-register row.
7. Decide which gates re-run after repair and write them into next_action: a repair changing what a test proves → re-run `audit-verification`; a repair changing behavior → re-run the affected adversarial lens; every repair diff → a fresh `review-slice`. **Review-loop cap:** if a gate has already gone through 2 repair→fresh-review cycles, do not queue a third — write `update-state --wo WO-XXXX --status blocked --blocked "review loop exceeded on <gate> — human decision required"` and stop.
8. Record the gate — the synthesizer is the SOLE writer of `adversarial_qa` (lenses and `adversarial-qa` only collect): `tools/agent/update-state --wo WO-XXXX --status in_review --phase adversarial --gate adversarial_qa=<approved|changes_requested> --next "<repair items and gates to re-run, or 'converge'>"`. Synthesis and repair are part of the `adversarial` phase; `converge-work-order` moves the phase forward.

The synthesizer merges reports. It never softens a verdict, never drops a finding because the plan mandated it, and never repairs code itself — repairs belong to the implementer.

## Receiving the findings (for the implementer)

<!-- adapted from obra/superpowers receiving-code-review (MIT) -->

A finding is a claim to evaluate, not an order to obey. Before repairing:

- **Evaluate each finding critically.** Reviewers are sometimes wrong — a "bug" may be
  intended behavior, a "violation" may misread the contract. Judge on the merits.
- **Push back with evidence, on the record.** Disagree by *appending* a response under
  the finding's register row in review-log.md (append-only — never edit or delete the
  finding). State the evidence; let the record hold both views.
- **Repair what is real.** A correct finding gets fixed, not argued.
- **Escalate, never silently resolve.** A Blocking finding you believe is wrong goes to
  a human — do not silently comply (repairing something that wasn't broken) and do not
  silently ignore (dropping a finding you dislike). Both corrupt the record.
