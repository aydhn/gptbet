from typing import Any, Dict, List

import numpy as np
from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.inference.contracts import (ArtifactChainRecord,
                                                   EventUniverseRecord,
                                                   PipelineStepResult)

logger = get_logger("InferencePipelineExecutor")


class InferencePipelineExecutor:
    def __init__(self):
        pass

    def run_base_inference(
        self, events: List[EventUniverseRecord], chain: ArtifactChainRecord
    ) -> Dict[str, Any]:
        logger.info(f"Running base inference using model: {chain.model_artifact_id}")

        predictions = {}
        for evt in events:
            # Mock generating probabilities
            if chain.market_type == "1x2":
                probs = {"home": 0.5, "draw": 0.25, "away": 0.25}
            elif chain.market_type == "ou_2_5":
                probs = {"over": 0.45, "under": 0.55}
            else:
                probs = {"home": 0.6, "away": 0.4}
            predictions[evt.event_id] = probs

        return {"predictions": predictions, "source": "base_model"}

    def apply_inference_calibration(
        self, base_preds: Dict[str, Any], chain: ArtifactChainRecord
    ) -> Dict[str, Any]:
        if not chain.calibrator_artifact_id:
            logger.info("No calibrator found in chain. Skipping calibration.")
            return base_preds

        logger.info(f"Applying calibration using {chain.calibrator_artifact_id}")
        calibrated_preds = {}
        for evt_id, probs in base_preds["predictions"].items():
            # Mock calibration: slightly soften probabilities
            calib_probs = {
                k: v * 0.9 + 0.1 * (1 / len(probs)) for k, v in probs.items()
            }
            # Normalize
            total = sum(calib_probs.values())
            calibrated_preds[evt_id] = {k: v / total for k, v in calib_probs.items()}

        return {"predictions": calibrated_preds, "source": "calibrated_model"}

    def resolve_prediction_fallback(
        self, base_preds: Dict[str, Any], chain: ArtifactChainRecord
    ) -> Dict[str, Any]:
        # Stacker > Ensemble > Calibrated Base > Raw Base
        current_preds = base_preds
        current_preds = self.apply_inference_calibration(current_preds, chain)

        if chain.ensemble_artifact_id:
            logger.info(f"Applying ensemble: {chain.ensemble_artifact_id}")
            # Mock ensemble logic
            ens_preds = {}
            for evt_id, probs in current_preds["predictions"].items():
                # Tweak probabilities slightly to simulate ensemble
                ens_probs = {k: min(1.0, v * 1.05) for k, v in probs.items()}
                total = sum(ens_probs.values())
                ens_preds[evt_id] = {k: v / total for k, v in ens_probs.items()}
            current_preds = {"predictions": ens_preds, "source": "ensemble"}

        if chain.stacker_artifact_id:
            logger.info(f"Applying stacker: {chain.stacker_artifact_id}")
            # Mock stacker logic
            stack_preds = {}
            for evt_id, probs in current_preds["predictions"].items():
                stack_probs = {k: v * 0.95 + 0.05 for k, v in probs.items()}
                total = sum(stack_probs.values())
                stack_preds[evt_id] = {k: v / total for k, v in stack_probs.items()}
            current_preds = {"predictions": stack_preds, "source": "stacker"}

        logger.info(f"Final prediction source resolved to: {current_preds['source']}")
        return current_preds

    def generate_signal_scores(
        self, preds: Dict[str, Any], chain: ArtifactChainRecord
    ) -> Dict[str, float]:
        scores = {}
        for evt_id, probs in preds["predictions"].items():
            # Mock score logic: take max probability
            scores[evt_id] = max(probs.values())
        return scores
