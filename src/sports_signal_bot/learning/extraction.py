import uuid
from typing import List, Dict, Any, Optional
from .contracts import (
    PatternCandidateRecord,
    RuleExtractionRecord
)

class RuleExtractor:
    @staticmethod
    def extract_structured_rule(candidate: PatternCandidateRecord) -> RuleExtractionRecord:
        conditions = RuleExtractor.normalize_condition_block(candidate.condition_summary)
        action = RuleExtractor.normalize_action_block(candidate.candidate_action, candidate.condition_summary)
        constraints = RuleExtractor.attach_safety_constraints(candidate)

        return RuleExtractionRecord(
            extraction_id=str(uuid.uuid4()),
            pattern_id=candidate.pattern_id,
            condition_block=conditions,
            action_block=action,
            exclusions=[],
            safety_constraints=constraints,
            expiry_or_review_window="30_days",
            target_config_family=candidate.component_family
        )

    @staticmethod
    def normalize_condition_block(raw_conditions: Dict[str, Any]) -> Dict[str, Any]:
        normalized = {}
        for k, v in raw_conditions.items():
            if k == "action":
                continue
            normalized[k] = v
        return normalized

    @staticmethod
    def normalize_action_block(raw_action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": raw_action,
            "target": context.get("provider_id", "unknown_target"),
            "adjustment": context.get("reputation_adjustment", 0)
        }

    @staticmethod
    def attach_safety_constraints(candidate: PatternCandidateRecord) -> Dict[str, Any]:
        return {
            "requires_review": True if candidate.support.contradiction_burden > 0.1 else False,
            "max_impact": "bounded",
            "ops_mode_stable_required": True
        }

    @staticmethod
    def render_rule_preview(extraction: RuleExtractionRecord) -> str:
        cond_str = ", ".join(f"{k}={v}" for k, v in extraction.condition_block.items())
        act_str = f"{extraction.action_block['type']} -> {extraction.action_block['target']} ({extraction.action_block.get('adjustment', '')})"
        return f"IF {cond_str} THEN {act_str}"
