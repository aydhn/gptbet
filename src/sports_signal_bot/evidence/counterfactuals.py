from typing import Dict, Any
from sports_signal_bot.evidence.contracts import CounterfactualHintRecord

def build_counterfactual_hints(
    hint_id: str,
    hint_text: str,
    status: str,
    parameters_changed: Dict[str, Any],
    expected_outcome: str
) -> CounterfactualHintRecord:
    return CounterfactualHintRecord(
        hint_id=hint_id,
        hint_text=hint_text,
        status=status,
        parameters_changed=parameters_changed,
        expected_outcome=expected_outcome
    )

def generate_threshold_counterfactual(current_score: float, required_threshold: float) -> CounterfactualHintRecord:
    if current_score >= required_threshold:
        return build_counterfactual_hints(
            hint_id="cf_thresh_high",
            hint_text=f"If threshold was higher than {current_score:.2f}, this would be rejected.",
            status="informative_only",
            parameters_changed={"threshold": current_score + 0.01},
            expected_outcome="rejected"
        )
    else:
        return build_counterfactual_hints(
            hint_id="cf_thresh_low",
            hint_text=f"If threshold was lower than {current_score:.2f}, this would be accepted.",
            status="informative_only",
            parameters_changed={"threshold": current_score - 0.01},
            expected_outcome="accepted"
        )
