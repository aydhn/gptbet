from typing import Dict, List, Any
from datetime import datetime
from .contracts import (
    DisclosureBundleRecord,
    PublicationDecisionRecord,
    PublicationProfileRecord
)
from .redaction import scan_publication_for_leaks

def collect_publication_blockers(
    bundle: DisclosureBundleRecord,
    payload: Dict[str, Any],
    profile: PublicationProfileRecord
) -> List[str]:
    blockers = []

    # 1. Scope policy blocker
    if bundle.bundle_family not in profile.allowed_item_families:
        blockers.append(f"blocked_by_scope_policy: Family {bundle.bundle_family} not allowed in profile {profile.profile_id}")

    # 2. Redaction failure blocker
    leak_check = scan_publication_for_leaks(payload, profile.forbidden_field_families, bundle.disclosure_bundle_id)
    if not leak_check.passed:
        blockers.append(f"blocked_by_redaction_failure: Leaks detected: {leak_check.detected_leaks}")

    # 3. Integrity gap
    if not bundle.verification_refs:
        blockers.append("blocked_by_integrity_gap: Missing verification_refs")

    return blockers

def classify_publication_decision(blockers: List[str], has_warnings: bool) -> str:
    if blockers:
        # Give specific priority to what blocker is the main reason
        if any("redaction_failure" in b for b in blockers):
            return "blocked_by_redaction_failure"
        if any("scope_policy" in b for b in blockers):
            return "blocked_by_scope_policy"
        if any("integrity_gap" in b for b in blockers):
            return "blocked_by_integrity_gap"
        return "quarantine_not_publishable"

    if has_warnings:
        return "publish_ready_with_caveats"

    return "publish_ready"

def evaluate_publishability(
    bundle: DisclosureBundleRecord,
    payload: Dict[str, Any],
    profile: PublicationProfileRecord
) -> PublicationDecisionRecord:
    blockers = collect_publication_blockers(bundle, payload, profile)
    has_warnings = len(bundle.warnings) > 0
    decision_str = classify_publication_decision(blockers, has_warnings)

    return PublicationDecisionRecord(
        decision_id=f"pub_dec_{bundle.disclosure_bundle_id}",
        bundle_id=bundle.disclosure_bundle_id,
        decision=decision_str,
        blockers=blockers,
        caveats=[w.description for w in bundle.warnings],
        evaluated_at=datetime.utcnow()
    )

def explain_publication_outcome(decision: PublicationDecisionRecord) -> str:
    if decision.decision in ["publish_ready", "publish_ready_with_caveats"]:
        return f"Bundle {decision.bundle_id} is approved for publication. Status: {decision.decision}. Caveats: {decision.caveats}"
    else:
        return f"Bundle {decision.bundle_id} is blocked from publication. Status: {decision.decision}. Blockers: {decision.blockers}"
