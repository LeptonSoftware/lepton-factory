# Execution Checklist — WO-XXXX

<!-- Live document: check items DURING execution, not retrospectively. Every item ends
[x] or [SKIP] with `Skip reason:` on the next line. Unchecked items at handoff are
execution failures. Phase headings mirror upstream 8090; our gates live inside them.
Add repo-specific items; never delete standard ones. -->

## Phase 1: Start / Context Gathering

- [ ] Work order read; In/Out of Scope understood
- [ ] Every linked Requirement read; ACs extracted verbatim
- [ ] Every linked Blueprint read; references traversed recursively to completion
- [ ] Analogous code inspected; reusable components identified in context.md
- [ ] Local conventions (errors, logging, tests, naming) recorded in context.md
- [ ] Baseline verified: clean worktree/branch, existing tests pass
- [ ] **Certification: context gathering complete and recorded in context.md**

## Phase 2: Planning And Implementation

- [ ] contract.md compiled (Gate 0); known unknowns and HITL decisions listed
- [ ] Unresolved HITL decisions escalated before planning proceeded
- [ ] implementation-plan.md written; no placeholders
- [ ] Plan challenge (Gate A) verdict recorded [medium/high tier]
- [ ] Plan revised and re-challenged if verdict was REVISE
- [ ] Each slice implemented per plan; state.yaml updated at each slice boundary
- [ ] TDD applied at meaningful seams; violations repaired by revert-and-verify
- [ ] Slice review (Gate B) passed for each slice; findings repaired
- [ ] Plan revisions recorded when reality diverged (plan_revision bumped)
- [ ] Out-of-scope findings filed as new WOs or feedback, not implemented
- [ ] **Certification: implementation matches the approved plan as revised**

## Phase 3: Review And Verification

- [ ] All targeted suites pass; full validation run for the affected area
- [ ] The software was RUN and observed (app/API/CLI/worker/migration as applicable);
      evidence recorded in evidence/ or below
- [ ] Verification audit (Gate C) passed: tests proven able to fail [medium/high tier]
- [ ] Adversarial QA (Gate D) executed; findings synthesized to review-log.md [high tier; folded into the final review round at medium]
- [ ] Blocking adversarial findings repaired; affected gates re-run
- [ ] Convergence check done; gaps filed (missing/partial/contradicts/unrequested) [separate gate at high tier; inside the final review round at medium]
- [ ] Full independent review round in review-log.md ends APPROVED [medium/high tier]
- [ ] Documentation impact evaluated; descriptive docs updated; architectural changes proposed
- [ ] factory feedback recorded if meaningful friction occurred
- [ ] **Certification: verification evidence is genuine, current, and covers every AC**

## Final Completion Check

- [ ] Every checklist item above is [x] or [SKIP] with a reason
- [ ] context.md links complete; implementation-plan.md reflects what actually landed
- [ ] state.yaml status is in_review or beyond; gates recorded per risk tier
- [ ] validate-work-order passes locally
- [ ] PR created with template; WO referenced
- [ ] **Certification: this work order is complete and resumable by another agent**
