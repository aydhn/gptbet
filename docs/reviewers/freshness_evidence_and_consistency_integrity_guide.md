---
title: Freshness, Evidence, and Consistency Integrity Reviewers Guide
family: consistency_ledgers
owner_role: Principal Alignment Federation Engineer
freshness_window: 90d
---

# Reviewers Guide

When reviewing consistency ledger outputs:

1. **Check Contradictions First**: Look at the `preview-consistency-ledgers` output. Critical contradictions (like `no_safe_visibility_contradiction`) require immediate manual investigation.
2. **Trace the Lineage**: Every ledger entry has a `source_ref`. If a consistency shift degraded to `contradicted`, check the involved entry refs to understand which inputs conflicted (e.g., one was stale while another claimed high assurance).
3. **Validate No-Safe Visibility**: Ensure that if any underlying evidence or trace carried a `no_safe_recovery_hint`, it successfully propagated to the ledger entry's `caveat_state` or `warnings`.
