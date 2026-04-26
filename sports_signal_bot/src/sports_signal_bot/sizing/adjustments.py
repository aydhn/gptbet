from sports_signal_bot.sizing.contracts import (
    SizingConfig,
    SizingComponentRecord,
    StakeSizingInputRecord,
)


def apply_edge_adjustment(input_record: StakeSizingInputRecord) -> float:
    """Calculates an edge multiplier. Could be 1.0 or scale up slightly for massive edges."""
    edge = input_record.edge_estimate
    if edge <= 0:
        return 0.0  # No positive edge, sizing should be 0

    # Baseline 1.0
    multiplier = 1.0

    # Slight bump for high edges, but conservative
    if edge > 0.05:
        multiplier = 1.1
    if edge > 0.10:
        multiplier = 1.2

    return multiplier


def apply_confidence_adjustment(
    input_record: StakeSizingInputRecord, config: SizingConfig
) -> float:
    """Calculates a confidence multiplier."""
    confidence = input_record.confidence_score
    min_b, max_b = config.confidence_multiplier_bounds

    # Simple linear map: confidence 0.0 -> min_b, 1.0 -> 1.0, >1.0 -> up to max_b
    if confidence < 1.0:
        multiplier = min_b + (1.0 - min_b) * confidence
    else:
        multiplier = 1.0 + (max_b - 1.0) * min(confidence - 1.0, 1.0)  # Clamp

    return max(min_b, min(multiplier, max_b))


def apply_uncertainty_disagreement_adjustment(
    input_record: StakeSizingInputRecord, config: SizingConfig
) -> float:
    """Calculates an uncertainty/disagreement dampening multiplier."""
    u_pen = input_record.uncertainty_penalty
    d_pen = input_record.disagreement_penalty

    u_min, u_max = config.uncertainty_penalty_bounds
    d_min, d_max = config.disagreement_penalty_bounds

    u_damp = 1.0 - max(u_min, min(u_pen, u_max))
    d_damp = 1.0 - max(d_min, min(d_pen, d_max))

    # Multiplicative penalty
    return u_damp * d_damp


def apply_data_quality_adjustment(input_record: StakeSizingInputRecord) -> float:
    """Calculates a data quality/source health dampening multiplier."""
    dq_pen = input_record.data_quality_penalty
    sh_pen = input_record.source_health_penalty

    # Severe penalties can drop multiplier to 0
    multiplier = 1.0 - dq_pen - sh_pen
    return max(0.0, multiplier)


def apply_regime_risk_adjustment(input_record: StakeSizingInputRecord) -> float:
    """Calculates a regime risk multiplier."""
    # From input record, regime adjustment acts as a direct multiplier
    # e.g. 0.8 for high volatility regime
    return max(0.0, input_record.regime_adjustment)


def compute_sizing_adjustments(
    input_record: StakeSizingInputRecord, config: SizingConfig
) -> SizingComponentRecord:
    edge_mult = apply_edge_adjustment(input_record)
    conf_mult = apply_confidence_adjustment(input_record, config)
    uncert_mult = apply_uncertainty_disagreement_adjustment(input_record, config)
    qual_mult = apply_data_quality_adjustment(input_record)
    reg_mult = apply_regime_risk_adjustment(input_record)

    combined = edge_mult * conf_mult * uncert_mult * qual_mult * reg_mult

    return SizingComponentRecord(
        edge_multiplier=edge_mult,
        confidence_multiplier=conf_mult,
        uncertainty_multiplier=uncert_mult,
        data_quality_multiplier=qual_mult,
        regime_multiplier=reg_mult,
        combined_multiplier=combined,
    )
