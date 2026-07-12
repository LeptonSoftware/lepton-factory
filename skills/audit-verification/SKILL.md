---
name: audit-verification
description: Use when implementation and slice reviews are complete and the risk tier requires Gate C — audit the proof that tests actually verify the contract, not the code itself.
---
<!-- break-the-behavior audit and evidence discipline adapted from obra/superpowers verification-before-completion (MIT) -->

# Audit the Verification (Gate C)

Auditor tier: per `.factory/policies/model-routing.md` — never lighter than the implementer.

Audit the PROOF, not the code. "All tests pass" is not evidence — it is the claim under audit. Distrust summaries: the implementer's report, checklist prose, and green CI are inputs to verify, never verdicts to accept. Independence (`.factory/README.md` §4, restated): the auditor is never the implementer and never modifies product code — the disposable worktree below is the sanctioned exception, and it is discarded.

For EACH row of the verification contract table in `.factory/work-orders/WO-XXXX/contract.md`:

1. **The test exists.** Locate the automated test the row names and confirm it actually runs in the invoked suite — a test that exists but is skipped or filtered out fails the row.
2. **The test can fail.** In a disposable worktree (`git worktree add /tmp/audit-WO-XXXX-<n> HEAD`), deliberately break the behavior the AC describes — invert the condition, corrupt the value, remove the write — run the test, and confirm it FAILS for the stated reason. Remove the worktree afterward. A test that stays green while the behavior is broken proves nothing: Blocking.
3. **Assertions are meaningful.** The test asserts real behavior, not mock call counts; expected values come from an independent source of truth, not recomputed the way the production code computes them.
4. **Production paths execute.** The test exercises the real code path, not a test-only shim or a mock of the module under test.
5. **Negative case present.** The row's negative case has its own test or recorded runtime evidence.
6. **Evidence is current.** The row's runtime action was performed against the current build; the evidence in `evidence/` or the checklist carries the command and its output. "Should", "probably", and stale screenshots fail the row.

## Output

A verification audit table appended to review-log.md — one row per COV:

| COV | Test located | Fails when broken | Assertions meaningful | Negative case | Runtime evidence | Pass/Fail |
|---|---|---|---|---|---|---|

— plus findings (Blocking/Advisory, with the command + output that demonstrates each) and verdict, exactly: APPROVED | CHANGES_REQUESTED. Then
`tools/agent/update-state --wo WO-XXXX --phase verify --gate verification_audit=<approved|changes_requested>`.
