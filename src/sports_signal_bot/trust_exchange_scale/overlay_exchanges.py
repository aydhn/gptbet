from datetime import datetime, timedelta, timezone
import uuid
from typing import List, Dict, Any
from .contracts import (
    OverlayExchangePacketRecord, TrustOverlayExchangeRecord, OverlayExchangeScopeRecord
)

def build_overlay_exchange_packet(source_overlay: Dict[str, Any], target_scope: str) -> OverlayExchangePacketRecord:
    # Caveat preservation
    caveats = source_overlay.get("caveats", ["default_caveat"])

    status = "prepared"
    warnings = []

    # Freshness check
    last_updated = source_overlay.get("last_updated", datetime.now(timezone.utc) - timedelta(days=1))
    if (datetime.now(timezone.utc) - last_updated).total_seconds() > 3600:
        warnings.append("source_overlay_stale")
        status = "exchanged_degraded"
    else:
        status = "validated"

    return OverlayExchangePacketRecord(
        overlay_exchange_packet_id=f"oep-{uuid.uuid4().hex[:8]}",
        source_overlay_ref=source_overlay.get("id", "unknown"),
        source_registry_refs=["reg-1"],
        source_hub_refs=["hub-1"],
        exchange_scope=OverlayExchangeScopeRecord(
            scope_id=target_scope,
            allowed_dimensions=["currentness_projection", "caveat_preservation"],
            max_projection_strength="bounded",
            caveat_requirements=["must_preserve_all"]
        ),
        projected_dimensions={"mesh_route_projection": 0.8},
        preserved_caveat_refs=caveats,
        currentness_refs=["curr-1"],
        validity_window={"start": datetime.now(timezone.utc), "end": datetime.now(timezone.utc) + timedelta(hours=1)},
        replay_support_refs=["rep-1"],
        exchange_status=status,
        warnings=warnings
    )

def summarize_overlay_exchange(record: TrustOverlayExchangeRecord) -> Dict[str, Any]:
    return {
        "id": record.overlay_exchange_id,
        "health": record.health_state,
        "packets": len(record.packet_refs),
        "warnings": len(record.warnings)
    }
