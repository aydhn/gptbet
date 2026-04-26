from typing import Dict, List, Optional

from .contracts import SourceTrustScoreRecord
from .metadata import SourceMetadataRecord


class SourceTrustScorer:
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        # Default weighting policy
        self.weights = weights or {
            "performance": 0.3,
            "recency": 0.2,
            "coverage": 0.2,
            "regime_fit": 0.2,
            "data_quality": 0.1,
        }
        # Normalize weights
        total = sum(self.weights.values())
        if total > 0:
            self.weights = {k: v / total for k, v in self.weights.items()}

    def compute_performance_component(self, metadata: SourceMetadataRecord) -> float:
        """Score based on historical log loss/brier and benchmark relative perf."""
        score = 0.5  # Default safe middle
        if metadata.eval_info.recent_log_loss is not None:
            # Assume log_loss of 0.69 is random, 0.5 is good.
            ll = metadata.eval_info.recent_log_loss
            if ll < 0.5:
                score = 1.0
            elif ll > 0.7:
                score = 0.0
            else:
                score = 1.0 - ((ll - 0.5) / 0.2)

        # Adjust with benchmark relative
        score += metadata.eval_info.benchmark_relative_performance * 0.1
        return max(0.0, min(1.0, score))

    def compute_recency_component(self, metadata: SourceMetadataRecord) -> float:
        """Score based on model and calibration age."""
        if metadata.refresh_info.is_stale_flag:
            return 0.0

        m_age = metadata.model_age_days
        c_age = metadata.calibration_age_days

        m_score = max(0.0, 1.0 - (m_age / 30.0))  # Decays over 30 days
        if metadata.is_calibrated:
            c_score = max(0.0, 1.0 - (c_age / 14.0))  # Calibrator decays faster
            return (m_score * 0.4) + (c_score * 0.6)

        return m_score

    def compute_coverage_component(self, metadata: SourceMetadataRecord) -> float:
        """Score based on historical coverage rate."""
        return max(0.0, min(1.0, metadata.recent_coverage_rate))

    def compute_regime_fit_component(
        self, metadata: SourceMetadataRecord, active_regimes: List[str]
    ) -> float:
        """Score based on performance in currently active regimes."""
        if not active_regimes or not metadata.regime_profile.regime_scores:
            return 0.5  # Neutral fallback

        total_score = 0.0
        valid_regimes = 0
        for r in active_regimes:
            if r in metadata.regime_profile.regime_scores:
                score = metadata.regime_profile.regime_scores[r]
                sample_size = metadata.regime_profile.regime_sample_sizes.get(r, 0)

                # Dampen low sample sizes
                damping_factor = min(1.0, sample_size / 50.0)

                # Assuming score is 0-1, blend with neutral prior
                damped_score = (score * damping_factor) + (0.5 * (1.0 - damping_factor))

                total_score += damped_score
                valid_regimes += 1

        if valid_regimes == 0:
            return 0.5

        return total_score / valid_regimes

    def combine_trust_components(
        self, metadata: SourceMetadataRecord, active_regimes: Optional[List[str]] = None
    ) -> SourceTrustScoreRecord:
        """Combines all components into a final trust score."""
        perf = self.compute_performance_component(metadata)
        rec = self.compute_recency_component(metadata)
        cov = self.compute_coverage_component(metadata)
        reg = self.compute_regime_fit_component(metadata, active_regimes or [])
        dq = 1.0 if not metadata.has_invalid_probabilities else 0.0

        breakdown = {
            "performance": perf,
            "recency": rec,
            "coverage": cov,
            "regime_fit": reg,
            "data_quality": dq,
        }

        total = sum(breakdown[k] * self.weights.get(k, 0.0) for k in breakdown)

        warnings = []
        if rec < 0.2:
            warnings.append("Low recency score.")
        if cov < 0.5:
            warnings.append("Low coverage rate.")
        if dq == 0.0:
            warnings.append("Invalid probabilities detected.")

        return SourceTrustScoreRecord(
            performance_score=perf,
            recency_score=rec,
            coverage_score=cov,
            regime_fit_score=reg,
            data_quality_score=dq,
            disagreement_penalty=0.0,
            total_trust_score=max(0.0, min(1.0, total)),
            component_breakdown=breakdown,
            warnings=warnings,
        )

    def explain_trust_score(self, score: SourceTrustScoreRecord) -> str:
        """Provides a human readable explanation of the trust score."""
        explanation = f"Total Trust Score: {score.total_trust_score:.2f}\n"
        explanation += "Breakdown:\n"
        for k, v in score.component_breakdown.items():
            explanation += (
                f"  - {k}: {v:.2f} (weight: {self.weights.get(k, 0.0):.2f})\n"
            )
        if score.warnings:
            explanation += "Warnings:\n"
            for w in score.warnings:
                explanation += f"  - {w}\n"
        return explanation
