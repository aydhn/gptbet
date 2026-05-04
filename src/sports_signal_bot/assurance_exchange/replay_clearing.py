import uuid
from typing import List, Dict
from .contracts import (
    ReplayMarketClearingLayerRecord,
    ReplayClearingBookRecord,
    ReplayClearingOfferRecord,
    ReplayClearingRequestRecord,
    WarningRecord
)

def build_replay_market_clearing_layer(clearing_family: str) -> ReplayMarketClearingLayerRecord:
    return ReplayMarketClearingLayerRecord(
        replay_clearing_layer_id=f"rmcl_{uuid.uuid4()}",
        clearing_family=clearing_family,
        marketplace_refs=[],
        clearing_book_refs=[],
        active_offer_refs=[],
        active_request_refs=[],
        active_decision_refs=[],
        fairness_policy_ref="default_fairness",
        health_status="healthy",
        warnings=[]
    )

def build_replay_clearing_book(replay_family: str, scope_class: str) -> ReplayClearingBookRecord:
    return ReplayClearingBookRecord(
        clearing_book_id=f"rcb_{uuid.uuid4()}",
        replay_family=replay_family,
        scope_class=scope_class,
        compatible_offer_refs=[],
        compatible_request_refs=[],
        backlog_refs=[],
        pressure_state="normal",
        clearing_status="clearing_ready",
        warnings=[]
    )

def ingest_clearing_offer_and_request(book: ReplayClearingBookRecord, offer: ReplayClearingOfferRecord, request: ReplayClearingRequestRecord) -> ReplayClearingBookRecord:
    book.compatible_offer_refs.append(offer.offer_id)
    book.compatible_request_refs.append(request.request_id)
    return book

def compute_replay_clearing_decision(book: ReplayClearingBookRecord) -> str:
    if not book.compatible_offer_refs or not book.compatible_request_refs:
        book.clearing_status = "clearing_blocked"
        return "no_safe_clearing_path"

    book.clearing_status = "clearing_caveated"
    return "cleared_caveated_replay"

def summarize_replay_clearing(layer: ReplayMarketClearingLayerRecord) -> Dict:
    return {
        "id": layer.replay_clearing_layer_id,
        "health": layer.health_status,
        "active_offers": len(layer.active_offer_refs),
        "active_requests": len(layer.active_request_refs)
    }
