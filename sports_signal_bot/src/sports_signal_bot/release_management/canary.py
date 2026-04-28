import uuid
from typing import Dict, Optional

from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.release_management.contracts import (
    CanaryComparisonRecord,
    CanaryHealthSnapshot,
    CanaryPromotionGateRecord,
    CanaryResult,
    CanaryValidationRecord,
)

logger = get_logger("CanaryValidator")


class CanaryValidator:
    def __init__(self):
        pass

    def evaluate_canary(
        self,
        run_id: str,
        canary_chain_id: str,
        stable_chain_id: str,
        canary_metrics: Dict[str, float],
        stable_metrics: Dict[str, float],
        health_snapshot: CanaryHealthSnapshot,
    ) -> CanaryValidationRecord:
        logger.info(f"Evaluating canary run {run_id} for chain {canary_chain_id}")

        comparisons = []
        gates = []
        passed_all_gates = True
        warnings = False

        # Mock comparisons based on inputs
        for metric, stable_val in stable_metrics.items():
            if metric in canary_metrics:
                canary_val = canary_metrics[metric]
                delta = canary_val - stable_val

                # simple logic: lower logloss is better, higher edge is better
                if metric == "logloss":
                    passed = delta <= 0.05  # allow slight deterioration
                    threshold = 0.05
                else:
                    passed = delta >= -0.05
                    threshold = -0.05

                comp = CanaryComparisonRecord(
                    metric_name=metric,
                    canary_value=canary_val,
                    stable_value=stable_val,
                    delta=delta,
                    threshold=threshold,
                    passed=passed,
                )
                comparisons.append(comp)

                if not passed:
                    passed_all_gates = False
                    warnings = True
                    gates.append(
                        CanaryPromotionGateRecord(
                            gate_name=f"metric_check_{metric}",
                            passed=False,
                            reason=f"{metric} deteriorated beyond threshold",
                        )
                    )

        # Check health
        if health_snapshot.health_score < 80.0:
            passed_all_gates = False
            gates.append(
                CanaryPromotionGateRecord(
                    gate_name="health_check",
                    passed=False,
                    reason=f"Health score {health_snapshot.health_score} below 80",
                )
            )
        else:
            gates.append(
                CanaryPromotionGateRecord(
                    gate_name="health_check", passed=True, reason="Health score ok"
                )
            )

        if health_snapshot.anomalies > 0:
            warnings = True

        result = CanaryResult.inconclusive
        if passed_all_gates and not warnings:
            result = CanaryResult.pass_
        elif passed_all_gates and warnings:
            result = CanaryResult.pass_with_warnings
        else:
            result = CanaryResult.fail

        return CanaryValidationRecord(
            validation_id=str(uuid.uuid4()),
            run_id=run_id,
            canary_chain_id=canary_chain_id,
            stable_chain_id=stable_chain_id,
            comparisons=comparisons,
            health=health_snapshot,
            gates=gates,
            result=result,
        )
