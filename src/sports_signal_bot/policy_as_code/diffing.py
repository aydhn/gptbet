import uuid
from typing import Dict, Any, List
from .contracts import PolicyBundleRecord, PolicyDiffRecord, PolicyRuleRecord

class PolicyDiffEngine:
    def __init__(self, rules_registry: Dict[str, PolicyRuleRecord]):
        self.rules_registry = rules_registry

    def diff_policy_bundles(self, base: PolicyBundleRecord, target: PolicyBundleRecord) -> PolicyDiffRecord:
        added = list(set(target.rules) - set(base.rules))
        removed = list(set(base.rules) - set(target.rules))
        common = list(set(target.rules).intersection(set(base.rules)))

        changed = {}
        for rule_id in common:
            base_rule = self.rules_registry.get(rule_id)
            # In a real system, target rules might be in a proposed registry
            # We mock detection by assuming same rule_id means no change for this simple implementation
            pass

        risk_hints = []
        if removed:
            risk_hints.append(f"Removed {len(removed)} rules. This might relax safety boundaries.")
        if added:
            risk_hints.append(f"Added {len(added)} new rules.")

        summary = f"Diff: +{len(added)} rules, -{len(removed)} rules, ~{len(changed)} changed."

        return PolicyDiffRecord(
            diff_id=f"diff_{uuid.uuid4().hex[:8]}",
            base_bundle_id=base.policy_bundle_id,
            target_bundle_id=target.policy_bundle_id,
            added_rules=added,
            removed_rules=removed,
            changed_rules=changed,
            risk_hints=risk_hints,
            human_readable_summary=summary
        )

    def summarize_rule_changes(self, changed_rules: Dict[str, Any]) -> str:
        return f"{len(changed_rules)} rules changed."

    def highlight_dangerous_policy_deltas(self, diff: PolicyDiffRecord) -> List[str]:
        return diff.risk_hints
