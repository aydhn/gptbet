def generate_resilience_synthesis_summary() -> dict:
    return {
        "compiler_federation_counts": {"healthy": 1, "stale": 0},
        "replay_exchange_counts": {"bounded": 1, "review_only": 0},
        "debt_distribution": {"open": 1, "aging": 0},
        "synthesis_band_distribution": {"stabilized_resilience_with_caps": 1},
        "overall_health": "healthy"
    }
