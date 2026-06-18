import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from .contracts import (
    PolicyEvaluationRecord,
    PolicyDecisionRecordV2,
    PolicyDecisionStatus,
    PolicyBundleRecord,
    PolicyRuleRecord,
    PolicyOverlayRecord,
)
from .precedence import PrecedenceResolver


class PolicyRegistry:
    def __init__(self):
        self.bundles: Dict[str, PolicyBundleRecord] = {}
        self.rules: Dict[str, PolicyRuleRecord] = {}
        self.overlays: Dict[str, PolicyOverlayRecord] = {}

    def register_bundle(self, bundle: PolicyBundleRecord):
        self.bundles[bundle.policy_bundle_id] = bundle

    def register_rule(self, rule: PolicyRuleRecord):
        self.rules[rule.rule_id] = rule

    def register_overlay(self, overlay: PolicyOverlayRecord):
        self.overlays[overlay.overlay_id] = overlay


class PolicyResolver:
    def __init__(self, registry: PolicyRegistry):
        self.registry = registry

    def resolve_relevant_policies(
        self, context: Dict[str, Any], target_bundle_ids: List[str]
    ) -> List[PolicyRuleRecord]:
        relevant_rules = []
        for bundle_id in target_bundle_ids:
            bundle = self.registry.bundles.get(bundle_id)
            if bundle:
                for rule_id in bundle.rules:
                    rule = self.registry.rules.get(rule_id)
                    if rule and rule.enabled:
                        relevant_rules.append(rule)
        return relevant_rules


class PolicyEvaluator:
    def evaluate_condition(
        self, condition: Dict[str, Any], context: Dict[str, Any]
    ) -> bool:
        namespace = condition.get("namespace", "")
        field = condition.get("field", "")
        operator = condition.get("operator", "==")
        expected_value = condition.get("value")

        # Basic dot notation resolution
        context_val = context
        if namespace:
            for part in namespace.split("."):
                if isinstance(context_val, dict):
                    context_val = context_val.get(part, {})
                else:
                    context_val = None
                    break

        if isinstance(context_val, dict):
            actual_value = context_val.get(field)
        else:
            actual_value = None

        if actual_value is None:
            return False

        if operator == "==":
            return actual_value == expected_value
        elif operator == "!=":
            return actual_value != expected_value
        elif operator == ">=":
            try:
                return actual_value >= expected_value
            except TypeError:
                return False
        elif operator == "<=":
            try:
                return actual_value <= expected_value
            except TypeError:
                return False
        elif operator == ">":
            try:
                return actual_value > expected_value
            except TypeError:
                return False
        elif operator == "<":
            try:
                return actual_value < expected_value
            except TypeError:
                return False
        elif operator == "in":
            try:
                return actual_value in expected_value
            except TypeError:
                return False
        return False

    def evaluate_policy_conditions(
        self, rules: List[PolicyRuleRecord], context: Dict[str, Any]
    ) -> List[PolicyRuleRecord]:
        matched_rules = []
        for rule in rules:
            all_match = True
            for condition in rule.conditions:
                if not self.evaluate_condition(condition, context):
                    all_match = False
                    break
            if (
                all_match or not rule.conditions
            ):  # Empty conditions means it always applies if scoped correctly
                matched_rules.append(rule)
        return matched_rules


class PolicyDecisionBuilder:
    def __init__(self, precedence_resolver: PrecedenceResolver):
        self.precedence_resolver = precedence_resolver

    def execute_policy_actions(self, rules: List[PolicyRuleRecord]) -> Dict[str, Any]:
        if not rules:
            return {
                "status": PolicyDecisionStatus.PERMIT,
                "blockers": [],
                "followups": [],
                "warnings": [],
                "escalations": [],
            }

        status = PolicyDecisionStatus.PERMIT
        blockers = None
        followups = None
        warnings = None
        escalations = None

        # Determine highest precedence rule families
        rule_families = list({r.rule_family for r in rules})
        ordered_families = self.precedence_resolver.resolve_precedence(rule_families)

        from collections import defaultdict

        rules_by_family = defaultdict(list)
        for rule in rules:
            rules_by_family[rule.rule_family].append(rule)

        # Sort rules by precedence (lower index = higher precedence)
        sorted_rules = []
        for family in ordered_families:
            sorted_rules.extend(rules_by_family[family])

        for rule in sorted_rules:
            for action in rule.actions:
                action_type = action.get("action_type")
                if action_type == "deny":
                    status = PolicyDecisionStatus.DENY
                    if blockers is None:
                        blockers = []
                    blockers.append(f"Blocked by {rule.rule_id}: {rule.title}")
                elif (
                    action_type == "require_approval"
                    and status != PolicyDecisionStatus.DENY
                ):
                    status = PolicyDecisionStatus.REQUIRE_APPROVAL
                    if followups is None:
                        followups = []
                    followups.append(f"Approval required by {rule.rule_id}")
                elif action_type == "escalate":
                    status = PolicyDecisionStatus.ESCALATE
                    if escalations is None:
                        escalations = []
                    escalations.append(f"Escalated by {rule.rule_id}")
                elif action_type == "hold" and status not in [
                    PolicyDecisionStatus.DENY,
                    PolicyDecisionStatus.ESCALATE,
                ]:
                    status = PolicyDecisionStatus.HOLD
                    if blockers is None:
                        blockers = []
                    blockers.append(f"Held by {rule.rule_id}: {rule.title}")

        return {
            "status": status,
            "blockers": blockers if blockers is not None else [],
            "followups": followups if followups is not None else [],
            "warnings": warnings if warnings is not None else [],
            "escalations": escalations if escalations is not None else [],
        }

    def build_policy_decision(
        self,
        matched_rules: List[PolicyRuleRecord],
        target_bundle_ids: List[str],
        context_id: str,
    ) -> PolicyDecisionRecordV2:
        action_results = self.execute_policy_actions(matched_rules)

        return PolicyDecisionRecordV2(
            decision_id=f"dec_{uuid.uuid4().hex[:8]}",
            context_id=context_id,
            decision_status=action_results["status"],
            blockers=action_results["blockers"],
            required_followups=action_results["followups"],
            triggered_rules=[r.rule_id for r in matched_rules],
            applied_bundle_refs=target_bundle_ids,
            policy_explanation=f"Evaluated {len(matched_rules)} matching rules.",
        )


class PolicyEngine:
    def __init__(self):
        self.registry = PolicyRegistry()
        self.resolver = PolicyResolver(self.registry)
        self.evaluator = PolicyEvaluator()
        self.precedence_resolver = PrecedenceResolver()
        self.decision_builder = PolicyDecisionBuilder(self.precedence_resolver)

    def evaluate(
        self, context: Dict[str, Any], target_bundle_ids: List[str]
    ) -> PolicyEvaluationRecord:
        relevant_rules = self.resolver.resolve_relevant_policies(
            context, target_bundle_ids
        )
        matched_rules = self.evaluator.evaluate_policy_conditions(
            relevant_rules, context
        )
        context_id = context.get("context_id", f"ctx_{uuid.uuid4().hex[:8]}")
        decision = self.decision_builder.build_policy_decision(
            matched_rules, target_bundle_ids, context_id
        )

        return PolicyEvaluationRecord(
            evaluation_id=f"eval_{uuid.uuid4().hex[:8]}",
            context_data=context,
            target_bundle_ids=target_bundle_ids,
            decision=decision,
        )
