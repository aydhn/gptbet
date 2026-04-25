from typing import Any, Dict, List, Optional

import pandas as pd
from pydantic import BaseModel, Field


class EventRegimeInputs(BaseModel):
    event_id: str
    sport: str
    market_type: str
    features: Dict[str, Any] = Field(default_factory=dict)
    source_probabilities: Dict[str, Dict[str, float]] = Field(default_factory=dict)
    ensemble_probabilities: Dict[str, float] = Field(default_factory=dict)
    data_completeness: float = 1.0
    missing_sources: int = 0
    total_sources: int = 1

    model_config = {"arbitrary_types_allowed": True}


class PeriodRegimeInputs(BaseModel):
    period_id: int
    sport: str
    market_type: str
    evaluation_summary: Dict[str, Any] = Field(default_factory=dict)
    historical_metrics: List[Dict[str, Any]] = Field(default_factory=list)

    model_config = {"arbitrary_types_allowed": True}


def build_event_regime_inputs(
    event_id: str,
    sport: str,
    market_type: str,
    features: Optional[Dict[str, Any]] = None,
    source_probabilities: Optional[Dict[str, Dict[str, float]]] = None,
    ensemble_probabilities: Optional[Dict[str, float]] = None,
    data_completeness: float = 1.0,
    missing_sources: int = 0,
    total_sources: int = 1,
) -> EventRegimeInputs:
    return EventRegimeInputs(
        event_id=event_id,
        sport=sport,
        market_type=market_type,
        features=features or {},
        source_probabilities=source_probabilities or {},
        ensemble_probabilities=ensemble_probabilities or {},
        data_completeness=data_completeness,
        missing_sources=missing_sources,
        total_sources=total_sources,
    )


def build_period_regime_inputs(
    period_id: int,
    sport: str,
    market_type: str,
    evaluation_summary: Optional[Dict[str, Any]] = None,
    historical_metrics: Optional[List[Dict[str, Any]]] = None,
) -> PeriodRegimeInputs:
    return PeriodRegimeInputs(
        period_id=period_id,
        sport=sport,
        market_type=market_type,
        evaluation_summary=evaluation_summary or {},
        historical_metrics=historical_metrics or [],
    )


def merge_regime_supporting_features(
    base_features: Dict[str, Any], additional_features: Dict[str, Any]
) -> Dict[str, Any]:
    merged = base_features.copy()
    merged.update(additional_features)
    return merged


def validate_regime_input_coverage(
    inputs: EventRegimeInputs, required_fields: List[str]
) -> List[str]:
    warnings = []
    for field in required_fields:
        if field not in inputs.features:
            warnings.append(f"Missing required feature: {field}")
    return warnings
