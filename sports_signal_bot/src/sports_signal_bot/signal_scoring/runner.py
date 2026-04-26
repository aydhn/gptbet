import datetime
import os
import uuid
from typing import Any, Dict, List, Optional

from sports_signal_bot.signal_scoring.contracts import (SignalCandidateRecord,
                                                        SignalManifest,
                                                        SignalRankingRecord,
                                                        SignalScoreRecord)
from sports_signal_bot.signal_scoring.factory import SignalScorerFactory
from sports_signal_bot.signal_scoring.ranking import rank_signals
from sports_signal_bot.signal_scoring.reporting import (
    export_signal_manifest, export_signal_scores_csv)


class SignalScoringRunner:

    def __init__(self, config: Dict[str, Any], output_dir: str):
        self.config = config
        self.output_dir = output_dir
        self.run_id = f"sig_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"

    def run(
        self,
        candidates: List[SignalCandidateRecord],
        sport: str,
        market_type: str,
        strategy_name: Optional[str] = None,
    ) -> SignalManifest:
        """Executes the scoring pipeline for a set of candidates."""

        # Determine strategy
        if not strategy_name:
            strategy_name = self.config.get("default_signal_strategy", "balanced")

        scorer = SignalScorerFactory.create(strategy_name, self.config)

        # 1. Score
        scored_signals = scorer.score_signals(candidates)

        # Handle fallback for those with NO_MARKET_REFERENCE if needed
        # We could route them to the fallback scorer here, but for now we let the main scorer handle it

        # 2. Rank
        ranked_signals = rank_signals(scored_signals)

        # 3. Generate Manifest
        manifest = self._build_manifest(
            sport, market_type, strategy_name, scored_signals, ranked_signals
        )

        # 4. Export Artifacts
        self._export_artifacts(
            sport, market_type, scored_signals, ranked_signals, manifest
        )

        return manifest

    def _build_manifest(
        self,
        sport: str,
        market_type: str,
        strategy_name: str,
        scored: List[SignalScoreRecord],
        ranked: List[SignalRankingRecord],
    ) -> SignalManifest:

        from sports_signal_bot.signal_scoring.manifests import \
            generate_signal_manifest

        return generate_signal_manifest(
            self.run_id, sport, market_type, strategy_name, scored, ranked
        )

    def _export_artifacts(
        self,
        sport: str,
        market_type: str,
        scored: List[SignalScoreRecord],
        ranked: List[SignalRankingRecord],
        manifest: SignalManifest,
    ) -> None:

        base_path = os.path.join(self.output_dir, sport, market_type, self.run_id)
        os.makedirs(base_path, exist_ok=True)

        export_signal_scores_csv(scored, os.path.join(base_path, "signal_scores.csv"))
        export_signal_manifest(
            manifest, os.path.join(base_path, "signal_manifest.json")
        )

        # Optionally export rankings CSV
        if ranked:
            import csv

            rank_path = os.path.join(base_path, "signal_ranking.csv")
            with open(rank_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "rank",
                        "tier",
                        "event_id",
                        "selection",
                        "final_signal_score",
                        "status",
                        "edge_estimate",
                        "confidence_score",
                    ]
                )
                for r in ranked:
                    writer.writerow(
                        [
                            r.rank,
                            r.tier,
                            r.event_id,
                            r.selection,
                            f"{r.final_signal_score:.4f}",
                            r.status.value,
                            f"{r.edge_estimate:.4f}",
                            f"{r.confidence_score:.4f}",
                        ]
                    )
