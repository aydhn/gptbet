import pandas as pd
from sports_signal_bot.features.contracts import NullPolicy

def apply_null_policy(df: pd.DataFrame, policy: NullPolicy) -> pd.DataFrame:
    """
    Applies the specified null handling policy to the feature matrix.
    """
    df = df.copy()
    if policy == NullPolicy.KEEP_NULLS:
        return df

    elif policy == NullPolicy.FILL_DEFAULTS:
        # Fill numeric with 0, keep object cols intact for now or fill with empty string
        for col in df.columns:
            if col == 'event_id': continue
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(0.0)

    elif policy == NullPolicy.ADD_MISSING_INDICATORS:
        for col in df.columns:
            if col == 'event_id': continue
            if df[col].isnull().any():
                df[f"{col}_is_missing"] = df[col].isnull().astype(int)
                # Then we usually fill defaults
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(0.0)

    return df
