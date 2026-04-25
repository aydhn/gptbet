import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd

from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.core.paths import get_project_root
from sports_signal_bot.training.contracts import (DatasetBuildConfig,
                                                  FoldManifest,
                                                  TrainingDataset,
                                                  ValidationPredictionRecord)
from sports_signal_bot.training.dataset import TrainingDatasetBuilder
from sports_signal_bot.training.factory import TrainerFactory
from sports_signal_bot.training.manifests import generate_manifest
from sports_signal_bot.training.metrics import evaluate_classification_metrics
from sports_signal_bot.training.predictions import \
    format_validation_predictions
from sports_signal_bot.training.splits import (BaseSplitStrategy,
                                               ExpandingWindowSplit,
                                               HoldoutTimeSplit,
                                               RollingWindowSplit,
                                               WalkForwardSplit)

logger = get_logger("TrainingRunner")


class TrainingRunManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.run_id = f"train_{uuid.uuid4().hex[:8]}"
        self.sport = config.get("sport", "unknown")
        self.market_type = config.get("market_type", "unknown")
        self.label_name = config.get("label_name", "unknown")
        self.model_name = config.get("model_name", "logistic_regression")
        self.seed = config.get("seed", 42)

        # Determine paths
        self.output_dir = (
            get_project_root()
            / "data"
            / "processed"
            / "models"
            / self.sport
            / self.model_name
            / self.run_id
        )
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _create_split_strategy(self) -> BaseSplitStrategy:
        strategy_name = self.config.get("split_strategy", "holdout")
        split_kwargs = self.config.get("split_kwargs", {})

        if strategy_name == "holdout":
            return HoldoutTimeSplit(**split_kwargs)
        elif strategy_name == "expanding":
            return ExpandingWindowSplit(**split_kwargs)
        elif strategy_name == "rolling":
            return RollingWindowSplit(**split_kwargs)
        elif strategy_name == "walk_forward":
            return WalkForwardSplit(**split_kwargs)
        else:
            raise ValueError(f"Unknown split strategy: {strategy_name}")

    def run(self, features_df: pd.DataFrame, labels_df: pd.DataFrame) -> Dict[str, Any]:
        started_at = datetime.now(timezone.utc).isoformat()
        logger.info(f"Starting training run {self.run_id} for {self.model_name}")

        # 1. Build Dataset
        build_config = DatasetBuildConfig(
            sport=self.sport,
            market_type=self.market_type,
            label_name=self.label_name,
            **self.config.get("dataset_kwargs", {}),
        )
        builder = TrainingDatasetBuilder(build_config)
        df, dataset = builder.build(features_df, labels_df)

        if df.empty:
            logger.error("Empty dataset after build! Aborting.")
            return {"status": "error", "reason": "empty_dataset"}

        # 2. Split Strategy
        splitter = self._create_split_strategy()

        # 3. Model
        trainer_config = self.config.get("trainer_kwargs", {})
        trainer_config["random_state"] = self.seed
        # Pass seed to model kwargs if possible
        if "model_kwargs" not in trainer_config:
            trainer_config["model_kwargs"] = {}
        trainer_config["model_kwargs"]["random_state"] = self.seed

        fold_manifests: List[FoldManifest] = []
        all_validation_predictions: List[ValidationPredictionRecord] = []

        # Global metrics accumulator for walk-forward, or just the last fold for holdout
        final_metrics = {}

        for fold_id, train_idx, valid_idx, _ in splitter.split(df):
            logger.info(
                f"Processing fold {fold_id} (Train: {len(train_idx)}, Valid: {len(valid_idx)})"
            )

            # Re-instantiate trainer for each fold to avoid leakage across folds
            trainer = TrainerFactory.create(self.model_name, trainer_config)

            # Train
            fold_metrics = trainer.fit(dataset, df, train_idx, valid_idx)

            # Predict on valid (we do this manually here to get the full formatted records)
            if len(valid_idx) > 0:
                valid_df = df.iloc[valid_idx]
                X_valid = valid_df[dataset.feature_columns]
                y_pred_proba = trainer.predict_proba(valid_df)
                y_pred = trainer.predict(valid_df)
                y_true = valid_df[dataset.target_column].values

                # Recalculate metrics formally just to be sure we have everything
                metrics = evaluate_classification_metrics(
                    y_true, y_pred_proba, y_pred, trainer.classes_
                )

                fold_manifest = FoldManifest(
                    fold_id=fold_id,
                    train_start=str(df.iloc[train_idx]["event_datetime_utc"].min()),
                    train_end=str(df.iloc[train_idx]["event_datetime_utc"].max()),
                    valid_start=str(valid_df["event_datetime_utc"].min()),
                    valid_end=str(valid_df["event_datetime_utc"].max()),
                    train_rows=len(train_idx),
                    valid_rows=len(valid_idx),
                    class_distribution={
                        str(k): v
                        for k, v in valid_df[dataset.target_column]
                        .value_counts()
                        .to_dict()
                        .items()
                    },
                    metrics=metrics,
                )
                fold_manifests.append(fold_manifest)
                final_metrics = (
                    metrics  # Keep updating, last one wins, or we average later
                )

                # Format predictions
                preds = format_validation_predictions(
                    df,
                    valid_idx,
                    y_pred_proba,
                    trainer.classes_,
                    self.sport,
                    self.market_type,
                    self.label_name,
                    dataset.target_column,
                    self.model_name,
                    fold_id,
                    split_metadata={
                        "strategy": self.config.get("split_strategy", "holdout")
                    },
                )
                all_validation_predictions.extend(preds)

            # For this phase, we save the artifact of the LAST fold as the primary model.
            # In a true walk-forward, you'd save all or only the final retraining on ALL data.
            # Here we just save the current trainer's state
            trainer.save_artifact(str(self.output_dir / "artifact"))

        # Save all predictions
        preds_path = self.output_dir / "validation_predictions.jsonl"
        with open(preds_path, "w") as f:
            for p in all_validation_predictions:
                f.write(p.model_dump_json() + "\n")

        # Generate final manifest
        manifest = generate_manifest(
            run_id=self.run_id,
            sport=self.sport,
            market_type=self.market_type,
            label_name=self.label_name,
            model_name=self.model_name,
            split_strategy=self.config.get("split_strategy", "holdout"),
            total_train_rows=len(df),  # Approximation for total involved
            total_valid_rows=len(all_validation_predictions),
            feature_count=len(dataset.feature_columns),
            feature_list_path=str(self.output_dir / "artifact" / "metadata.joblib"),
            model_artifact_path=str(self.output_dir / "artifact"),
            metrics_summary=final_metrics,
            fold_manifests=fold_manifests,
            warnings=builder.warnings,
            seed=self.seed,
            config_snapshot=self.config,
            started_at_utc=started_at,
            output_path=str(self.output_dir / "manifest.json"),
        )

        logger.info(
            f"Training run completed. Manifest saved to {self.output_dir / 'manifest.json'}"
        )

        return {
            "status": "success",
            "run_id": self.run_id,
            "manifest": manifest,
            "output_dir": str(self.output_dir),
        }
