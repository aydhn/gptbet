import uuid
from typing import List, Dict, Optional
from .contracts import AssuranceDashboardExchangeRecord, DashboardExchangePacketRecord, WarningRecord

def build_assurance_dashboard_exchange(
    source_dashboard_refs: List[str],
    source_snapshot_refs: List[str],
    exchange_scope: str,
    audience_profile_refs: List[str]
) -> AssuranceDashboardExchangeRecord:
    warnings = []
    if not source_snapshot_refs:
        warnings.append(WarningRecord(warning_id=str(uuid.uuid4()), message="Stale or missing snapshots", severity="high"))

    return AssuranceDashboardExchangeRecord(
        dashboard_exchange_id=f"dex_{uuid.uuid4()}",
        source_dashboard_refs=source_dashboard_refs,
        source_snapshot_refs=source_snapshot_refs,
        source_panel_refs=[],
        target_scope_refs=[],
        exchange_scope=exchange_scope,
        audience_profile_refs=audience_profile_refs,
        preserved_caveat_refs=[],
        currentness_refs=[],
        exchange_status="prepared" if not warnings else "prepared_with_warnings",
        warnings=warnings
    )

def validate_dashboard_exchange_packet(packet: DashboardExchangePacketRecord) -> bool:
    if not packet.currentness_refs:
        return False
    return True

def preserve_dashboard_caveats_and_alerts(exchange: AssuranceDashboardExchangeRecord, caveats: List[str]) -> AssuranceDashboardExchangeRecord:
    exchange.preserved_caveat_refs.extend(caveats)
    return exchange

def route_dashboard_exchange(exchange: AssuranceDashboardExchangeRecord) -> AssuranceDashboardExchangeRecord:
    if any(w.severity == "high" for w in exchange.warnings):
        exchange.exchange_status = "exchanged_blocked"
    elif exchange.preserved_caveat_refs:
        exchange.exchange_status = "exchanged_caveated"
    else:
        exchange.exchange_status = "exchanged_bounded_assurance"
    return exchange

def summarize_dashboard_exchange(exchange: AssuranceDashboardExchangeRecord) -> Dict:
    return {
        "id": exchange.dashboard_exchange_id,
        "status": exchange.exchange_status,
        "warnings_count": len(exchange.warnings),
        "caveats_count": len(exchange.preserved_caveat_refs)
    }
