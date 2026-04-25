from typing import Any, Dict, List

from ..alignment import align_predictions_to_reference_classes
from ..contracts import (EnsembleDiagnosticsRecord, EnsembleInputRecord,
                         EnsembleOutputRecord, SourceContributionRecord)
from .base import BaseEnsembler


class BestSourceFallbackEnsembler(BaseEnsembler):

    def __init__(
        self, name: str = "best_source_fallback", config: Dict[str, Any] = None
    ):
        super().__init__(name, config)
        self.source_priority = self.config.get("source_priority", [])

    def combine(self, input_record: EnsembleInputRecord) -> EnsembleOutputRecord:
        if not input_record.predictions:
            return self._create_empty_output(input_record)

        reference_classes = input_record.predictions[0].class_labels
        aligned_preds = align_predictions_to_reference_classes(
            input_record.predictions, reference_classes
        )

        if not aligned_preds:
            return self._create_empty_output(
                input_record, warnings=["No compatible sources found after alignment."]
            )

        selected_pred = None
        used_source_name = ""

        # Try to find a prediction matching the priority list
        for priority_source in self.source_priority:
            for p in aligned_preds:
                if (
                    p.source_name == priority_source
                    or p.source_family == priority_source
                ):
                    selected_pred = p
                    used_source_name = p.source_name
                    break
            if selected_pred:
                break

        # Fallback to the first available if none matched priority
        if not selected_pred:
            selected_pred = aligned_preds[0]
            used_source_name = selected_pred.source_name

        final_probs = selected_pred.probabilities.copy()
        final_predicted_class = selected_pred.predicted_class

        components = [
            SourceContributionRecord(
                source_name=selected_pred.source_name,
                source_family=selected_pred.source_family,
                weight=1.0,
                is_calibrated=selected_pred.is_calibrated,
            )
        ]

        # the ones we didn't use
        excluded = [
            p.source_name for p in aligned_preds if p.source_name != used_source_name
        ]

        diagnostics = EnsembleDiagnosticsRecord(
            num_sources_eligible=len(input_record.predictions),
            num_sources_used=1,
            excluded_sources=excluded,
            top_class_confidence=final_probs.get(final_predicted_class, 0.0),
            entropy=0.0,  # Not very meaningful for single source here
            max_disagreement=0.0,
            source_variance=0.0,
        )

        return EnsembleOutputRecord(
            event_id=input_record.event_id,
            sport=input_record.sport,
            market_type=input_record.market_type,
            ensemble_name=self.name,
            final_probabilities=final_probs,
            final_predicted_class=final_predicted_class,
            component_sources=components,
            diagnostics=diagnostics,
        )

    def _create_empty_output(
        self, input_record: EnsembleInputRecord, warnings: List[str] = None
    ) -> EnsembleOutputRecord:
        diag = EnsembleDiagnosticsRecord(
            num_sources_eligible=len(input_record.predictions),
            num_sources_used=0,
            warnings=warnings or ["No valid input predictions."],
        )
        return EnsembleOutputRecord(
            event_id=input_record.event_id,
            sport=input_record.sport,
            market_type=input_record.market_type,
            ensemble_name=self.name,
            final_probabilities={},
            final_predicted_class="UNKNOWN",
            component_sources=[],
            diagnostics=diag,
            status="failed",
        )
