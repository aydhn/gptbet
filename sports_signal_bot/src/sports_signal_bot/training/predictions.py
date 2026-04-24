import pandas as pd
import numpy as np
from typing import List, Dict, Any
from datetime import datetime, timezone
from sports_signal_bot.training.contracts import ValidationPredictionRecord

def format_validation_predictions(
    df: pd.DataFrame,
    valid_indices: np.ndarray,
    y_pred_proba: np.ndarray,
    classes: np.ndarray,
    sport: str,
    market_type: str,
    label_name: str,
    target_column: str,
    model_name: str,
    fold_id: str,
    split_metadata: Dict[str, Any]
) -> List[ValidationPredictionRecord]:
    """
    Format predictions on the validation set into strongly typed ValidationPredictionRecords,
    ready for calibration or ensembling.
    """
    records = []

    valid_df = df.iloc[valid_indices]

    # We assume valid_df has 'event_id' and the target column
    for i, (_, row) in enumerate(valid_df.iterrows()):
        true_class_val = row.get(target_column)

        # Determine the true class index if possible
        true_class_index = None
        if pd.notna(true_class_val) and true_class_val in classes:
            true_class_index = np.where(classes == true_class_val)[0][0]

        # Get probabilities for this row
        probs = y_pred_proba[i]

        # Predicted class (argmax)
        pred_class_idx = int(np.argmax(probs))

        # Map probabilities to class names/values
        prob_dict = {str(c): float(p) for c, p in zip(classes, probs)}

        record = ValidationPredictionRecord(
            event_id=str(row['event_id']),
            sport=sport,
            market_type=market_type,
            label_name=label_name,
            true_class_index=int(true_class_index) if true_class_index is not None else None,
            predicted_class=pred_class_idx,
            predicted_probabilities=prob_dict,
            model_name=model_name,
            fold_id=fold_id,
            split_metadata=split_metadata,
            timestamp_utc=datetime.now(timezone.utc).isoformat()
        )
        records.append(record)

    return records
