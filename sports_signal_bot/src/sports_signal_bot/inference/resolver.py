from typing import Any, Dict, List, Optional

from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.inference.contracts import (ArtifactChainRecord,
                                                   ArtifactResolutionRecord)

logger = get_logger("ArtifactResolver")


class ArtifactResolver:
    def __init__(self, catalog_adapter=None):
        self.catalog_adapter = catalog_adapter

    def resolve_chain(
        self, sport: str, market_type: str, policy: str = "latest_compatible"
    ) -> ArtifactChainRecord:
        logger.info(
            f"Resolving artifact chain for {sport} - {market_type} using {policy} policy"
        )

        chain = ArtifactChainRecord(sport=sport, market_type=market_type)

        try:
            # 1. Feature Config
            feat_res = self._resolve_component(
                "feature_config", sport, market_type, policy
            )
            chain.feature_config_id = feat_res.resolved_id

            # 2. Base Model
            model_res = self._resolve_component("model", sport, market_type, policy)
            if not model_res.resolved_id:
                chain.is_valid = False
                chain.warnings.append("No valid base model found.")
            chain.model_artifact_id = model_res.resolved_id

            # 3. Calibrator
            calib_res = self._resolve_component(
                "calibrator", sport, market_type, policy
            )
            chain.calibrator_artifact_id = calib_res.resolved_id
            if not calib_res.resolved_id:
                chain.warnings.append(
                    "No calibrator found. Will degrade to raw base model probabilities."
                )

            # 4. Ensemble
            ens_res = self._resolve_component("ensemble", sport, market_type, policy)
            chain.ensemble_artifact_id = ens_res.resolved_id

            # 5. Stacker (Optional)
            stacker_res = self._resolve_component("stacker", sport, market_type, policy)
            chain.stacker_artifact_id = stacker_res.resolved_id

            # 6. Threshold Policy
            thresh_res = self._resolve_component(
                "threshold_policy", sport, market_type, policy
            )
            chain.threshold_policy_id = thresh_res.resolved_id
            if not thresh_res.resolved_id:
                chain.warnings.append("No threshold policy found.")

            # 7. Execution Policy
            exec_pol_res = self._resolve_component(
                "execution_policy", sport, market_type, policy
            )
            chain.policy_artifact_id = exec_pol_res.resolved_id

            # 8. Sizing
            sizing_res = self._resolve_component(
                "sizing_strategy", sport, market_type, policy
            )
            chain.sizing_strategy_id = sizing_res.resolved_id

            # 9. Portfolio
            port_res = self._resolve_component(
                "portfolio_strategy", sport, market_type, policy
            )
            chain.portfolio_strategy_id = port_res.resolved_id

        except Exception as e:
            logger.error(f"Error resolving artifact chain: {str(e)}")
            chain.is_valid = False
            chain.warnings.append(str(e))

        return chain

    def _resolve_component(
        self, component_type: str, sport: str, market_type: str, policy: str
    ) -> ArtifactResolutionRecord:
        # In a real implementation, this queries an Artifact Catalog or File System
        # We mock the resolution logic here for the 'live-like' structure

        res = ArtifactResolutionRecord(artifact_type=component_type)

        if policy == "latest_compatible" or policy == "latest_stable":
            # Mock IDs based on component
            prefix_map = {
                "feature_config": "feat",
                "model": "mod",
                "calibrator": "calib",
                "ensemble": "ens",
                "stacker": "stack",
                "threshold_policy": "thresh",
                "execution_policy": "exec",
                "sizing_strategy": "size",
                "portfolio_strategy": "port",
            }

            # Simulate stacker not being available for some markets to test fallback
            if component_type == "stacker" and market_type == "moneyline":
                res.resolved_id = None
                res.fallback_used = True
                res.fallback_reason = "No stacker trained for moneyline."
            elif (
                component_type == "calibrator"
                and policy == "latest_stable"
                and market_type == "spread"
            ):
                res.resolved_id = None
                res.fallback_used = True
                res.fallback_reason = "Stable calibrator not found, fallback to raw."
            else:
                res.resolved_id = f"{prefix_map.get(component_type, 'art')}_{sport}_{market_type}_v1.0"
                res.version = "1.0"
                res.resolved_path = (
                    f"artifacts/{sport}/{market_type}/{component_type}/v1.0.pkl"
                )

        return res

    def validate_artifact_chain(self, chain: ArtifactChainRecord) -> bool:
        if not chain.model_artifact_id:
            logger.error("Chain invalid: Missing base model")
            return False
        return True
