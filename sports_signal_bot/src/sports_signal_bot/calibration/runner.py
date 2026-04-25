import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from sports_signal_bot.calibration.comparison import create_comparison_record
from sports_signal_bot.calibration.contracts import (
    CalibratedPredictionRecord, CalibrationComparisonRecord,
    CalibrationRunManifest, CalibrationSummary, ReliabilityBinRecord)
from sports_signal_bot.calibration.dataset import (
    build_calibration_dataset_from_validation_predictions,
    extract_calibration_features_and_targets)
from sports_signal_bot.calibration.factory import CalibrationFactory
from sports_signal_bot.calibration.manifests import save_calibration_manifest
from sports_signal_bot.calibration.metrics import (calculate_brier_score,
                                                   calculate_ece_mce,
                                                   calculate_log_loss)
from sports_signal_bot.calibration.reliability import generate_reliability_bins
from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.core.paths import get_project_root
from sports_signal_bot.training.contracts import ValidationPredictionRecord

logger = get_logger("CalibrationRunner")


class CalibrationRunner:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.run_id = f"calib_{uuid.uuid4().hex[:8]}"
        self.sport = config.get("sport", "unknown")
        self.market_type = config.get("market_type", "unknown")
        self.label_name = config.get("label_name", "unknown")
        self.method_name = config.get("method", "binary_identity")
        self.class_labels = config.get("class_labels", ["0", "1"])
        self.source_model_run_id = config.get("source_model_run_id")

        # Path setup
        self.output_dir = (
            get_project_root()
            / "data"
            / "processed"
            / "calibration"
            / self.sport
            / self.market_type
            / self.run_id
        )
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _evaluate(
        self, X: np.ndarray, y: np.ndarray, method: str
    ) -> CalibrationSummary:
        """Evaluates metrics and reliability bins for a probability matrix."""

        is_binary = len(self.class_labels) == 2
        positive_class_index = (
            1 if is_binary else -1
        )  # Unused in multiclass ECE fallback generally

        log_loss_val = calculate_log_loss(
            y, X, labels=np.arange(len(self.class_labels))
        )
        brier_val = calculate_brier_score(
            y, X, positive_class_index=positive_class_index
        )
        ece, mce = calculate_ece_mce(
            y,
            X,
            n_bins=self.config.get("n_bins", 10),
            positive_class_index=positive_class_index,
        )

        bins = generate_reliability_bins(
            y,
            X,
            n_bins=self.config.get("n_bins", 10),
            positive_class_index=positive_class_index,
        )

        if is_binary:
            mean_conf = float(np.mean(X[:, positive_class_index]))
        else:
            mean_conf = float(np.mean(np.max(X, axis=1)))

        return CalibrationSummary(
            method=method,
            log_loss=log_loss_val,
            brier_score=brier_val,
            ece=ece,
            mce=mce,
            reliability_bins=bins,
            mean_confidence=mean_conf,
            calibration_coverage=1.0,  # Placeholder
        )

    def run(
        self, validation_records: List[ValidationPredictionRecord]
    ) -> Dict[str, Any]:
        logger.info(
            f"Starting calibration run {self.run_id} using method {self.method_name}"
        )
        started_at = datetime.now(timezone.utc).isoformat()
        warnings = []

        if not validation_records:
            logger.error("No validation records provided for calibration.")
            return {"status": "error", "reason": "empty_input"}

        # 1. Build Dataset
        df = build_calibration_dataset_from_validation_predictions(
            validation_records, self.class_labels
        )

        # Filter out rows with missing true labels
        df = df.dropna(subset=["true_label"])
        if df.empty:
            logger.error("No valid validation records with true labels.")
            return {"status": "error", "reason": "no_true_labels"}

        X_raw, y = extract_calibration_features_and_targets(df, self.class_labels)

        # 2. Evaluate Raw
        raw_summary = self._evaluate(X_raw, y, "raw")

        # 3. Fit Calibrator
        calibrator_config = self.config.get("calibrator_config", {})
        calibrator = CalibrationFactory.create(self.method_name, calibrator_config)

        logger.info(f"Fitting {self.method_name} on {len(X_raw)} samples.")
        calibrator.fit(X_raw, y)

        # 4. Transform
        X_calibrated = calibrator.transform(X_raw)

        # 5. Evaluate Calibrated
        calibrated_summary = self._evaluate(X_calibrated, y, self.method_name)

        # 6. Compare
        comparison = create_comparison_record(
            run_id=self.run_id,
            raw_summary=raw_summary,
            calibrated_summary=calibrated_summary,
            overfit_ece_threshold=self.config.get("overfit_ece_threshold", 0.01),
        )

        if comparison.possible_overfit_warning:
            warnings.append(
                "Possible overfit detected: ECE is extremely low compared to raw."
            )
        if not comparison.calibration_improvement:
            warnings.append(
                "Calibration did not improve log loss or ECE significantly."
            )

        # 7. Generate Output Records
        calibrated_records = []
        for i, row in df.iterrows():
            event_id = str(row["event_id"])
            raw_probs = {
                label: X_raw[i, j] for j, label in enumerate(self.class_labels)
            }
            cal_probs = {
                label: X_calibrated[i, j] for j, label in enumerate(self.class_labels)
            }
            cal_class = int(np.argmax(X_calibrated[i]))

            # Match back to original record model name and fold if possible
            orig_rec = next(
                (r for r in validation_records if r.event_id == event_id), None
            )
            model_name = orig_rec.model_name if orig_rec else "unknown"
            fold_id = orig_rec.fold_id if orig_rec else "unknown"

            record = CalibratedPredictionRecord(
                event_id=event_id,
                sport=self.sport,
                market_type=self.market_type,
                label_name=self.label_name,
                true_class_index=int(y[i]),
                raw_predicted_probabilities=raw_probs,
                calibrated_predicted_probabilities=cal_probs,
                calibrated_predicted_class=cal_class,
                model_name=model_name,
                calibration_method=self.method_name,
                calibration_run_id=self.run_id,
                fold_id=fold_id,
                timestamp_utc=started_at,
            )
            calibrated_records.append(record)

        # 8. Save Artifacts
        artifact_path = str(self.output_dir / "calibrator.joblib")
        calibrator.save_artifact(artifact_path)

        preds_path = self.output_dir / "calibrated_predictions.jsonl"
        with open(preds_path, "w") as f:
            for p in calibrated_records:
                f.write(p.model_dump_json() + "\n")

        comparison_path = self.output_dir / "comparison.json"
        with open(comparison_path, "w") as f:
            f.write(comparison.model_dump_json(indent=2))

        bins_path = self.output_dir / "reliability_bins.json"
        with open(bins_path, "w") as f:
            json.dump(
                [b.model_dump() for b in calibrated_summary.reliability_bins],
                f,
                indent=2,
            )

        manifest = CalibrationRunManifest(
            run_id=self.run_id,
            source_model_run_id=self.source_model_run_id,
            sport=self.sport,
            market_type=self.market_type,
            label_name=self.label_name,
            calibration_method=self.method_name,
            class_labels=self.class_labels,
            calibration_dataset_size=len(X_raw),
            raw_metrics={
                "log_loss": raw_summary.log_loss,
                "brier_score": raw_summary.brier_score,
                "ece": raw_summary.ece,
            },
            calibrated_metrics={
                "log_loss": calibrated_summary.log_loss,
                "brier_score": calibrated_summary.brier_score,
                "ece": calibrated_summary.ece,
            },
            delta_metrics={
                "log_loss": comparison.delta_log_loss,
                "brier_score": comparison.delta_brier_score,
                "ece": comparison.delta_ece,
            },
            calibrator_artifact_path=artifact_path,
            reliability_summary_path=str(bins_path),
            warnings=warnings,
            config_snapshot=self.config,
            timestamp_utc=started_at,
        )

        manifest_path = self.output_dir / "manifest.json"
        save_calibration_manifest(manifest, str(manifest_path))

        logger.info(f"Calibration run complete. Saved to {self.output_dir}")

        return {
            "status": "success",
            "run_id": self.run_id,
            "manifest": manifest,
            "comparison": comparison,
            "output_dir": str(self.output_dir),
        }
