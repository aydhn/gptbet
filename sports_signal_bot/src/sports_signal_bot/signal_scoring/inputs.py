from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from sports_signal_bot.ensemble.contracts import EnsembleOutputRecord
from sports_signal_bot.stacker.contracts import MetaPredictionRecord


class SignalInputBuilderContext(BaseModel):
    """Context required to build signal candidates."""
    # From phase 10/11
    ensemble_output: Optional[EnsembleOutputRecord] = None
    stacker_output: Optional[MetaPredictionRecord] = None

    # Optional diagnostics from earlier phases
    source_disagreement_diagnostics: Dict[str, Any] = Field(default_factory=dict)
    data_quality_summaries: Dict[str, Any] = Field(default_factory=dict)
    source_selection_diagnostics: Dict[str, Any] = Field(default_factory=dict)

    # From phase 14
    regime_assignments: List[Dict[str, Any]] = Field(default_factory=list)

    # Market lines / odds
    market_implied_probabilities: Dict[str, float] = Field(default_factory=dict)
    market_lines: Dict[str, Any] = Field(default_factory=dict)

    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SignalInputBuilder:
    """Helper to construct SignalCandidateRecord from various phase outputs."""

    @staticmethod
    def extract_final_probabilities(context: SignalInputBuilderContext) -> Dict[str, float]:
        if context.stacker_output:
            return context.stacker_output.final_probabilities
        elif context.ensemble_output:
            return context.ensemble_output.final_probabilities
        return {}

    @staticmethod
    def extract_predicted_class(context: SignalInputBuilderContext) -> Optional[str]:
        if context.stacker_output:
            return context.stacker_output.predicted_class
        elif context.ensemble_output:
            return context.ensemble_output.final_predicted_class
        return None

    @staticmethod
    def extract_event_info(context: SignalInputBuilderContext) -> Dict[str, str]:
        if context.stacker_output:
            return {
                "event_id": context.stacker_output.event_id,
                "sport": context.stacker_output.sport,
                "market_type": context.stacker_output.market_type
            }
        elif context.ensemble_output:
            return {
                "event_id": context.ensemble_output.event_id,
                "sport": context.ensemble_output.sport,
                "market_type": context.ensemble_output.market_type
            }
        return {"event_id": "unknown", "sport": "unknown", "market_type": "unknown"}
