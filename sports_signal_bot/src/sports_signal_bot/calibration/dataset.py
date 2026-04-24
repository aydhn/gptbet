import pandas as pd
from typing import List
from datetime import datetime, timezone
from sports_signal_bot.training.contracts import ValidationPredictionRecord

def build_calibration_dataset_from_validation_predictions(
    validation_records: List[ValidationPredictionRecord],
    class_labels: List[str]
) -> pd.DataFrame:
    """
    Converts a list of ValidationPredictionRecords into a standardized DataFrame for calibration.
    """
    data = []
    for record in validation_records:
        row = {
            "event_id": record.event_id,
            "fold_id": record.fold_id,
            "true_class_index": record.true_class_index,
            "predicted_class": record.predicted_class,
            "model_name": record.model_name,
            "market_type": record.market_type,
            "label_name": record.label_name,
            "sport": record.sport,
            "timestamp_utc": record.timestamp_utc,
        }

        # Add probability for each class label to ensure ordering
        for i, class_label in enumerate(class_labels):
            row[f"prob_{class_label}"] = record.predicted_probabilities.get(class_label, 0.0)

        if record.true_class_index is not None and 0 <= record.true_class_index < len(class_labels):
            row["true_label"] = class_labels[record.true_class_index]
        else:
            row["true_label"] = None

        data.append(row)

    df = pd.DataFrame(data)
    # Ensure all probability columns are float
    for label in class_labels:
         df[f"prob_{label}"] = df[f"prob_{label}"].astype(float)
    return df

def extract_calibration_features_and_targets(df: pd.DataFrame, class_labels: List[str]):
    """
    Extracts the features (raw probabilities) and targets (true class indices) from a calibration DataFrame.
    Returns X (N, n_classes), y (N,)
    """
    prob_cols = [f"prob_{label}" for label in class_labels]
    X = df[prob_cols].values.astype(float)
    # Convert series to int, handling NaNs
    y = df["true_class_index"].fillna(-1).astype(int).values
    return X, y
