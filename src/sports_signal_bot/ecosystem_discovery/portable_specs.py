from typing import List
from sports_signal_bot.ecosystem_discovery.contracts import PortableSpecCatalogEntryRecord

def catalog_portable_spec_bundle(spec_family: str, versions: List[str]) -> PortableSpecCatalogEntryRecord:
    return PortableSpecCatalogEntryRecord(spec_family=spec_family, supported_versions=versions)

def validate_spec_catalog_entry(entry: PortableSpecCatalogEntryRecord) -> bool:
    return bool(entry.spec_family and entry.supported_versions)

def summarize_spec_catalog_support(entry: PortableSpecCatalogEntryRecord) -> dict:
    return {
        "spec_family": entry.spec_family,
        "versions": len(entry.supported_versions)
    }

def find_matching_spec_bundles(entries: List[PortableSpecCatalogEntryRecord], required_family: str) -> List[PortableSpecCatalogEntryRecord]:
    return [e for e in entries if e.spec_family == required_family]
