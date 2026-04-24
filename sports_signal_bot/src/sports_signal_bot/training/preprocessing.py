import pandas as pd
import numpy as np
from typing import List, Optional
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def build_preprocessing_pipeline(
    numeric_features: List[str],
    categorical_features: Optional[List[str]] = None,
    scale_numeric: bool = False
) -> ColumnTransformer:
    """
    Builds a robust, basic preprocessing pipeline for tabular data.

    Numeric features:
    - Impute missing values with the median.
    - Optionally scale with StandardScaler.

    Categorical features:
    - Impute missing values with 'missing' constant.
    - OneHotEncode with handle_unknown='ignore'.
    """
    if categorical_features is None:
        categorical_features = []

    numeric_steps = [('imputer', SimpleImputer(strategy='median'))]
    if scale_numeric:
        numeric_steps.append(('scaler', StandardScaler()))

    numeric_transformer = Pipeline(steps=numeric_steps)

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    transformers = []
    if numeric_features:
        transformers.append(('num', numeric_transformer, numeric_features))
    if categorical_features:
        transformers.append(('cat', categorical_transformer, categorical_features))

    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder='drop'  # Drop any columns not explicitly handled
    )

    return preprocessor
