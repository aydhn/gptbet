from sports_signal_bot.ecosystem_discovery.contracts import (
    CatalogTrustScoreRecord,
    AssuranceRegistryCatalogRecord
)

def compute_catalog_trust_score(catalog: AssuranceRegistryCatalogRecord, is_notarized: bool = False, is_signed: bool = False, freshness_days: int = 0) -> CatalogTrustScoreRecord:
    score = 50.0  # Baseline
    components = {"baseline": score}

    if is_notarized:
        score += 20.0
        components["notarization"] = 20.0
    if is_signed:
        score += 15.0
        components["signature"] = 15.0

    if freshness_days < 1:
        score += 15.0
        components["freshness"] = 15.0
    elif freshness_days > 7:
        score -= 20.0
        components["staleness_penalty"] = -20.0

    # Cap at 100
    score = min(max(score, 0.0), 100.0)
    return CatalogTrustScoreRecord(catalog_id=catalog.catalog_id, score=score, components=components)

def classify_catalog_trust(score: float) -> str:
    if score >= 90:
        return "trusted"
    elif score >= 70:
        return "trusted_with_caveats"
    elif score >= 50:
        return "review_only"
    elif score >= 30:
        return "quarantine_default"
    else:
        return "untrusted"

def downgrade_catalog_for_staleness(catalog: AssuranceRegistryCatalogRecord) -> AssuranceRegistryCatalogRecord:
    catalog.trust_profile = "review_only"
    catalog.warnings.append("Downgraded due to staleness.")
    return catalog

def summarize_trust_drivers(trust_record: CatalogTrustScoreRecord) -> dict:
    return trust_record.components
