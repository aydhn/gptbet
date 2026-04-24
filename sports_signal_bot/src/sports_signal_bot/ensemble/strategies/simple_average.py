from typing import Dict, Any, List
from .base import BaseEnsembler
from ..contracts import EnsembleInputRecord, EnsembleOutputRecord, SourceContributionRecord, EnsembleDiagnosticsRecord
from ..alignment import align_predictions_to_reference_classes
from ..diagnostics import calculate_entropy, probability_dispersion, top_class_disagreement, source_count_summary

class SimpleAverageEnsembler(BaseEnsembler):

    def __init__(self, name: str = "simple_average", config: Dict[str, Any] = None):
        super().__init__(name, config)

    def combine(self, input_record: EnsembleInputRecord) -> EnsembleOutputRecord:
        if not input_record.predictions:
            return self._create_empty_output(input_record)

        # 1. Determine reference classes (use the first prediction's classes as reference for simplicity)
        reference_classes = input_record.predictions[0].class_labels

        # 2. Align predictions
        aligned_preds = align_predictions_to_reference_classes(input_record.predictions, reference_classes)

        if not aligned_preds:
            return self._create_empty_output(input_record, warnings=["No compatible sources found after alignment."])

        # 3. Calculate average
        n_sources = len(aligned_preds)
        weight = 1.0 / n_sources

        final_probs = {cls: 0.0 for cls in reference_classes}
        for p in aligned_preds:
            for cls, prob in p.probabilities.items():
                final_probs[cls] += prob * weight

        # 4. Determine final class
        final_predicted_class = max(final_probs.items(), key=lambda x: x[1])[0]

        # 5. Build components
        components = [
            SourceContributionRecord(
                source_name=p.source_name,
                source_family=p.source_family,
                weight=weight,
                is_calibrated=p.is_calibrated
            ) for p in aligned_preds
        ]

        # 6. Build diagnostics
        probs_list = [p.probabilities for p in aligned_preds]
        diagnostics = EnsembleDiagnosticsRecord(
            num_sources_eligible=len(input_record.predictions),
            num_sources_used=n_sources,
            top_class_confidence=final_probs[final_predicted_class],
            entropy=calculate_entropy(final_probs),
            max_disagreement=top_class_disagreement(probs_list, reference_classes),
            source_variance=probability_dispersion(probs_list, reference_classes)
        )

        return EnsembleOutputRecord(
            event_id=input_record.event_id,
            sport=input_record.sport,
            market_type=input_record.market_type,
            ensemble_name=self.name,
            final_probabilities=final_probs,
            final_predicted_class=final_predicted_class,
            component_sources=components,
            diagnostics=diagnostics
        )

    def _create_empty_output(self, input_record: EnsembleInputRecord, warnings: List[str] = None) -> EnsembleOutputRecord:
        diag = EnsembleDiagnosticsRecord(
            num_sources_eligible=len(input_record.predictions),
            num_sources_used=0,
            warnings=warnings or ["No valid input predictions."]
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
            status="failed"
        )
