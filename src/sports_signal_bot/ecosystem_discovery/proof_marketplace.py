from typing import List
from sports_signal_bot.ecosystem_discovery.contracts import (
    PortableProofCatalogRecord,
    ProofAvailabilityRecord,
    RetrievalHintRecord,
    ProofMarketplaceStyleRecord,
    CatalogEntryRecord
)

def build_portable_proof_catalog(proof_family: str) -> PortableProofCatalogRecord:
    return PortableProofCatalogRecord(proof_family=proof_family)

def register_proof_availability(state: str, proof_ref: str) -> ProofAvailabilityRecord:
    return ProofAvailabilityRecord(state=state, proof_ref=proof_ref)

def validate_proof_catalog_entry(record: PortableProofCatalogRecord) -> bool:
    return bool(record.proof_family)

def summarize_proof_catalog(catalog: PortableProofCatalogRecord) -> dict:
    return {
        "proof_family": catalog.proof_family,
        "carried_claims": len(catalog.carried_claim_families),
        "notarization_available": catalog.notarization_availability
    }

def build_retrieval_hint(hint_type: str, instructions: str) -> RetrievalHintRecord:
    return RetrievalHintRecord(hint_type=hint_type, instructions=instructions)

def validate_retrieval_path(hint: RetrievalHintRecord) -> bool:
    return hint.hint_type in ["fetch_via_registry", "fetch_via_envelope", "local_replay"]

def classify_availability_state(state: str) -> str:
    valid_states = ["available_local", "available_federated", "stale_available"]
    return state if state in valid_states else "unavailable"

def summarize_retrieval_constraints(hints: List[RetrievalHintRecord]) -> dict:
    return {"hints": len(hints), "types": [h.hint_type for h in hints]}

def build_marketplace_style_listing(entry: CatalogEntryRecord) -> ProofMarketplaceStyleRecord:
    import uuid
    return ProofMarketplaceStyleRecord(listing_id=f"list_{uuid.uuid4().hex[:8]}")
