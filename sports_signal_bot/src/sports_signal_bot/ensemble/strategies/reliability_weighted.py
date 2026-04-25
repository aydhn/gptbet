from typing import Any, Dict, List

from ..alignment import align_predictions_to_reference_classes
from ..contracts import (EnsembleDiagnosticsRecord, EnsembleInputRecord,
                         EnsembleOutputRecord, SourceContributionRecord)
from ..diagnostics import (calculate_entropy, probability_dispersion,
                           top_class_disagreement)
from ..weights import derive_source_weight, normalize_source_weights
from .base import BaseEnsembler


class ReliabilityWeightedEnsembler(BaseEnsembler):

    def __init__(
        self, name: str = "reliability_weighted", config: Dict[str, Any] = None
    ):
        super().__init__(name, config)
        self.reliability_table = self.config.get("reliability_table", {})

    def fit(self, metadata: Dict[str, Any] = None):
        if metadata:
            self.reliability_table.update(metadata)

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

        raw_weights = {}
        for p in aligned_preds:
            # Try to lookup reliability metrics
            metrics = self.reliability_table.get(p.source_name, {})
            log_loss = metrics.get("validation_log_loss")
            brier = metrics.get("brier_score")

            weight = derive_source_weight(
                validation_log_loss=log_loss,
                brier_score=brier,
                is_calibrated=p.is_calibrated,
            )
            raw_weights[p.source_name] = weight

        norm_weights = normalize_source_weights(raw_weights)

        final_probs = {cls: 0.0 for cls in reference_classes}
        components = []

        for p in aligned_preds:
            w = norm_weights.get(p.source_name, 0.0)
            for cls, prob in p.probabilities.items():
                final_probs[cls] += prob * w

            components.append(
                SourceContributionRecord(
                    source_name=p.source_name,
                    source_family=p.source_family,
                    weight=w,
                    is_calibrated=p.is_calibrated,
                )
            )

        final_predicted_class = max(final_probs.items(), key=lambda x: x[1])[0]

        probs_list = [p.probabilities for p in aligned_preds]
        diagnostics = EnsembleDiagnosticsRecord(
            num_sources_eligible=len(input_record.predictions),
            num_sources_used=len(aligned_preds),
            top_class_confidence=final_probs[final_predicted_class],
            entropy=calculate_entropy(final_probs),
            max_disagreement=top_class_disagreement(probs_list, reference_classes),
            source_variance=probability_dispersion(probs_list, reference_classes),
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
