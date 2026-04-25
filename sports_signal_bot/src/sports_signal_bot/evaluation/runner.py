import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from .alignment import (align_predictions_to_common_universe,
                        summarize_coverage_by_source)
from .comparison import generate_comparison_matrix
from .confidence import build_confidence_buckets
from .contracts import (EvaluationComparisonRecord, EvaluationDataset,
                        EvaluationRunManifest, EvaluationSummaryRecord,
                        LeaderboardRow)
from .leaderboard import build_leaderboard
from .loader import extract_probability_columns, load_evaluation_dataframe
from .manifests import save_evaluation_manifest
from .metrics import compute_all_metrics
from .registry import EvaluationRegistry
from .segments import evaluate_by_segment
from .validator import filter_valid_evaluation_data, validate_evaluation_data


class EvaluationRunner:
    """Central runner for the evaluation pipeline."""

    def __init__(
        self, registry: EvaluationRegistry, output_dir: Path, config: Dict[str, Any]
    ):
        self.registry = registry
        self.output_dir = output_dir
        self.config = config
        self.run_id = f"eval_{uuid.uuid4().hex[:8]}"

    def _create_dataset(
        self, sport: str, market_type: str, source_names: Optional[List[str]] = None
    ) -> EvaluationDataset:
        """Loads and aligns data for evaluation."""

        target_sources = source_names or self.registry.get_registered_sources()
        if not target_sources:
            raise ValueError("No sources registered for evaluation")

        file_paths = self.registry.get_source_paths(target_sources)

        required_cols = [
            "event_id",
            "sport",
            "market_type",
            "source_name",
            "true_label",
            "predicted_class",
        ]
        raw_df = load_evaluation_dataframe(file_paths, required_cols=required_cols)

        # Filter for sport/market
        df = raw_df[(raw_df["sport"] == sport) & (raw_df["market_type"] == market_type)]
        if df.empty:
            raise ValueError(f"No data found for sport={sport}, market={market_type}")

        # Basic validation and filtering
        warnings = validate_evaluation_data(df, required_cols)
        df = filter_valid_evaluation_data(df)

        # Same sample alignment
        same_sample = self.config.get("same_sample_only", True)
        aligned_df, orig_counts = align_predictions_to_common_universe(
            df,
            source_col="source_name",
            event_id_col="event_id",
            same_sample_only=same_sample,
        )

        if aligned_df.empty:
            raise ValueError("Common universe alignment resulted in an empty dataset.")

        # Ensure we still have the sources we wanted
        actual_sources = aligned_df["source_name"].unique().tolist()
        missing = set(target_sources) - set(actual_sources)
        if missing:
            warnings.append(f"Sources dropped completely during alignment: {missing}")

        return EvaluationDataset(
            aligned_predictions_frame=aligned_df,
            sources=actual_sources,
            target_metadata={"original_counts": orig_counts},
            comparison_universe_definition={
                "same_sample_only": same_sample,
                "common_event_count": len(aligned_df["event_id"].unique()),
            },
            warnings=warnings,
        )

    def run(
        self,
        sport: str,
        market_type: str,
        class_labels: List[str],
        source_names: Optional[List[str]] = None,
    ) -> EvaluationRunManifest:
        """Executes the full evaluation pipeline."""

        run_dir = self.output_dir / self.run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        dataset = self._create_dataset(sport, market_type, source_names)
        df = dataset.aligned_predictions_frame

        proba_cols = extract_probability_columns(df, class_labels)

        # 1. Generate Summaries per Source
        summaries = []
        coverage = summarize_coverage_by_source(
            df, dataset.target_metadata["original_counts"], source_col="source_name"
        )

        for source in dataset.sources:
            source_df = df[df["source_name"] == source]

            # Use source family from registry if available, else infer/default
            family = "unknown"
            if source in self.registry.sources:
                family = self.registry.sources[source].get("family", "unknown")
            elif "source_family" in source_df.columns:
                family = source_df["source_family"].iloc[0]

            metrics, class_metrics = compute_all_metrics(
                df=source_df,
                source_name=source,
                true_label_col="true_label",
                pred_class_col="predicted_class",
                proba_cols=proba_cols,
                labels=class_labels,
            )

            summary = EvaluationSummaryRecord(
                source_name=source,
                source_family=family,
                sport=sport,
                market_type=market_type,
                row_count=len(source_df),
                coverage_rate=coverage.get(source, 0.0),
                class_metrics=class_metrics,
                **metrics,
            )
            summaries.append(summary)

        # 2. Build Leaderboard
        primary_metric = self.config.get("primary_metric", "log_loss")
        secondary_metric = self.config.get("secondary_metrics", ["brier"])[0]

        leaderboard = build_leaderboard(
            summaries=summaries,
            primary_metric=primary_metric,
            secondary_metric=secondary_metric,
            min_rows=self.config.get("minimum_common_rows", 1),
        )

        # Save Leaderboard
        lb_df = pd.DataFrame([r.model_dump() for r in leaderboard])
        lb_path = run_dir / "leaderboard.csv"
        lb_df.to_csv(lb_path, index=False)

        # 3. Pairwise Comparisons
        comparisons = []
        if self.config.get("include_pairwise_comparisons", True):
            comparisons = generate_comparison_matrix(
                df=df,
                source_col="source_name",
                event_id_col="event_id",
                true_label_col="true_label",
                pred_class_col="predicted_class",
                proba_cols=proba_cols,
                labels=class_labels,
                base_source=None,  # All pairs
            )

            if comparisons:
                comp_data = []
                for c in comparisons:
                    row = c.pairwise_stats.model_dump()
                    comp_data.append(row)

                comp_df = pd.DataFrame(comp_data)
                comp_path = run_dir / "pairwise_comparisons.csv"
                comp_df.to_csv(comp_path, index=False)
            else:
                comp_path = run_dir / "pairwise_comparisons.csv"

        # 4. Confidence Buckets & Segments
        segment_paths = {}
        segment_dir = run_dir / "segments"
        segment_dir.mkdir(exist_ok=True)

        for source in dataset.sources:
            source_df = df[df["source_name"] == source]

            # Confidence buckets
            buckets = build_confidence_buckets(
                df=source_df,
                true_label_col="true_label",
                pred_class_col="predicted_class",
                proba_cols=proba_cols,
                bins=10,
                labels=class_labels,
            )

            if buckets:
                b_df = pd.DataFrame([b.model_dump() for b in buckets])
                b_path = segment_dir / f"{source}_confidence_buckets.csv"
                b_df.to_csv(b_path, index=False)
                segment_paths[f"{source}_confidence"] = str(b_path)

            # Configured segments
            for segment_col in self.config.get("enabled_segments", []):
                if segment_col in source_df.columns:
                    seg_records = evaluate_by_segment(
                        df=source_df,
                        segment_col=segment_col,
                        source_name=source,
                        true_label_col="true_label",
                        pred_class_col="predicted_class",
                        proba_cols=proba_cols,
                        labels=class_labels,
                    )

                    if seg_records:
                        s_df = pd.DataFrame([s.model_dump() for s in seg_records])
                        s_path = segment_dir / f"{source}_segment_{segment_col}.csv"
                        s_df.to_csv(s_path, index=False)
                        segment_paths[f"{source}_segment_{segment_col}"] = str(s_path)

        # 5. Build and Save Manifest
        manifest = EvaluationRunManifest(
            run_id=self.run_id,
            sport=sport,
            market_type=market_type,
            sources_evaluated=dataset.sources,
            same_sample_policy=dataset.comparison_universe_definition[
                "same_sample_only"
            ],
            common_universe_size=dataset.comparison_universe_definition[
                "common_event_count"
            ],
            ranking_metric=primary_metric,
            leaderboard_path=str(lb_path),
            comparison_table_path=str(comp_path) if comparisons else "",
            segment_report_paths=segment_paths,
            warnings=dataset.warnings,
            config_snapshot=self.config,
        )

        manifest_path = run_dir / "evaluation_manifest.json"
        save_evaluation_manifest(manifest, manifest_path)

        return manifest
