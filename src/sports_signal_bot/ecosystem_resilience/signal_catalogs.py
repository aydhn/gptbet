from typing import List
from sports_signal_bot.ecosystem_resilience.contracts import (
    MarketplaceSignalCatalogRecord,
    BaselineMarketplaceSignalRecord
)

def build_marketplace_signal_catalog(catalog_id: str, entries: List[str]) -> MarketplaceSignalCatalogRecord:
    return MarketplaceSignalCatalogRecord(
        catalog_id=catalog_id,
        entries=entries
    )

def register_signal_catalog_entry(catalog: MarketplaceSignalCatalogRecord, entry_id: str) -> MarketplaceSignalCatalogRecord:
    if entry_id not in catalog.entries:
        catalog.entries.append(entry_id)
    return catalog

def suppress_marketplace_signal(signal: BaselineMarketplaceSignalRecord, reason: str) -> BaselineMarketplaceSignalRecord:
    signal.relevance_band = "suppressed_signal"
    signal.warnings.append(f"Suppressed: {reason}")
    return signal

def summarize_signal_catalog_health(catalog: MarketplaceSignalCatalogRecord) -> str:
    return f"Catalog {catalog.catalog_id} has {len(catalog.entries)} entries."
