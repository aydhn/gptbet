import csv
import json
import os
from typing import List

from .contracts import SignalManifest, SignalRankingRecord, SignalScoreRecord


def export_signal_scores_csv(
    signals: List[SignalScoreRecord], output_path: str
) -> None:
    if not signals:
        return

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "event_id",
                "sport",
                "market_type",
                "selection",
                "status",
                "final_signal_score",
                "normalized_score",
                "final_probability",
                "market_implied_probability",
                "edge_estimate",
                "confidence_score",
                "uncertainty_penalty",
                "disagreement_penalty",
                "data_quality_penalty",
                "source_health_penalty",
                "regime_adjustment",
            ]
        )

        for s in signals:
            c = s.components
            writer.writerow(
                [
                    s.event_id,
                    s.sport,
                    s.market_type,
                    s.selection,
                    s.status.value,
                    f"{s.final_signal_score:.4f}",
                    (
                        f"{s.normalized_score:.4f}"
                        if s.normalized_score is not None
                        else ""
                    ),
                    f"{s.final_probability:.4f}",
                    (
                        f"{s.market_implied_probability:.4f}"
                        if s.market_implied_probability is not None
                        else ""
                    ),
                    f"{c.edge_estimate:.4f}",
                    f"{c.confidence_score:.4f}",
                    f"{c.uncertainty_penalty:.4f}",
                    f"{c.disagreement_penalty:.4f}",
                    f"{c.data_quality_penalty:.4f}",
                    f"{c.source_health_penalty:.4f}",
                    f"{c.regime_adjustment:.4f}",
                ]
            )


def export_signal_manifest(manifest: SignalManifest, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        # Pydantic v2 compatible
        json.dump(manifest.model_dump(mode="json"), f, indent=2)
