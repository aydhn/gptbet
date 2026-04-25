import uuid
from typing import Any, Dict, List

from .contracts import (EnsembleInputRecord, EnsembleOutputRecord)
from .factory import EnsembleFactory
from .manifests import EnsembleRunManifest
from .policies import apply_calibrated_preference_policy


class EnsembleRunner:

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.strategy_name = self.config.get("strategy", "simple_average")
        self.ensembler = EnsembleFactory.create(
            self.strategy_name, self.config.get("strategy_config", {})
        )
        self.preference_mode = self.config.get("preference_mode", "prefer_calibrated")

    def run(self, input_records: List[EnsembleInputRecord]) -> Dict[str, Any]:

        run_id = f"ens_run_{uuid.uuid4().hex[:8]}"
        results = []

        for record in input_records:
            # Apply policy
            filtered_preds = apply_calibrated_preference_policy(
                record.predictions, self.preference_mode
            )

            # Create a new input record with filtered predictions
            filtered_record = EnsembleInputRecord(
                event_id=record.event_id,
                sport=record.sport,
                market_type=record.market_type,
                predictions=filtered_preds,
            )

            output = self.ensembler.combine(filtered_record)
            results.append(output)

        manifest = self._build_manifest(run_id, results)

        return {
            "status": "success",
            "run_id": run_id,
            "outputs": results,
            "manifest": manifest,
        }

    def _build_manifest(
        self, run_id: str, results: List[EnsembleOutputRecord]
    ) -> EnsembleRunManifest:
        if not results:
            return EnsembleRunManifest(
                run_id=run_id,
                sport="unknown",
                market_type="unknown",
                ensemble_strategy=self.strategy_name,
                target_classes=[],
                config=self.config,
            )

        sport = results[0].sport
        market = results[0].market_type

        # Count source usage
        source_summary = {}
        for r in results:
            for src in r.component_sources:
                source_summary[src.source_name] = (
                    source_summary.get(src.source_name, 0) + 1
                )

        return EnsembleRunManifest(
            run_id=run_id,
            sport=sport,
            market_type=market,
            ensemble_strategy=self.strategy_name,
            target_classes=(
                list(results[0].final_probabilities.keys()) if results else []
            ),
            config=self.config,
            source_summary=source_summary,
        )
