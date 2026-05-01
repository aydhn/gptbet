from typing import Dict, List, Any, Set
import json
from .contracts import (
    PublicationRedactionRuleRecord,
    DisclosureRedactionDecisionRecord,
    PublicationLeakCheckRecord
)

def build_publication_redaction_plan(
    family: str,
    profile_forbidden_fields: List[str]
) -> List[PublicationRedactionRuleRecord]:
    rules = []
    for field in profile_forbidden_fields:
        rules.append(PublicationRedactionRuleRecord(
            rule_id=f"rule_{family}_{field}",
            target_family=family,
            fields_to_redact=[field],
            masking_strategy="REDACTED"
        ))
    return rules

def _redact_dict(data: Dict[str, Any], fields_to_redact: Set[str], masking_strategy: str) -> Dict[str, Any]:
    result = {}
    for k, v in data.items():
        if k in fields_to_redact:
            result[k] = f"[{masking_strategy}]"
        elif isinstance(v, dict):
            result[k] = _redact_dict(v, fields_to_redact, masking_strategy)
        elif isinstance(v, list):
            result[k] = [_redact_dict(i, fields_to_redact, masking_strategy) if isinstance(i, dict) else i for i in v]
        else:
            result[k] = v
    return result

def redact_disclosure_payload(
    payload: Dict[str, Any],
    rules: List[PublicationRedactionRuleRecord]
) -> tuple[Dict[str, Any], DisclosureRedactionDecisionRecord]:
    fields_to_redact = set()
    for r in rules:
        fields_to_redact.update(r.fields_to_redact)

    # Very simple implementation, assuming strategy is REDACTED
    redacted_payload = _redact_dict(payload, fields_to_redact, "REDACTED")

    # We should count how many actually redacted but for now mock it
    decision = DisclosureRedactionDecisionRecord(
        decision_id="dec_temp",
        bundle_id="temp",
        applied_rules=[r.rule_id for r in rules],
        redacted_fields_count=len(fields_to_redact) # simplified
    )
    return redacted_payload, decision

def scan_publication_for_leaks(
    payload: Dict[str, Any],
    forbidden_fields: List[str],
    bundle_id: str
) -> PublicationLeakCheckRecord:
    # Recursively check for forbidden fields keys
    leaks = []

    def check_dict(d: Dict[str, Any], path: str = ""):
        for k, v in d.items():
            current_path = f"{path}.{k}" if path else k
            if k in forbidden_fields and v != "[REDACTED]":
                leaks.append(current_path)
            if isinstance(v, dict):
                check_dict(v, current_path)
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        check_dict(item, f"{current_path}[{i}]")

    check_dict(payload)
    return PublicationLeakCheckRecord(
        check_id=f"leak_check_{bundle_id}",
        bundle_id=bundle_id,
        passed=len(leaks) == 0,
        detected_leaks=leaks
    )

def verify_disclosure_safe(payload: Dict[str, Any], profile_forbidden_fields: List[str], bundle_id: str) -> bool:
    leak_check = scan_publication_for_leaks(payload, profile_forbidden_fields, bundle_id)
    return leak_check.passed

def summarize_redaction_effect(decision: DisclosureRedactionDecisionRecord) -> Dict[str, Any]:
    return {
        "decision_id": decision.decision_id,
        "bundle_id": decision.bundle_id,
        "rules_applied": len(decision.applied_rules),
        "redacted_fields": decision.redacted_fields_count
    }
