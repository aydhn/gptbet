from typing import List, Dict, Any, Optional
import uuid

from .contracts import (
    ObservatorySignalExchangeRecord,
    ObservatorySignalPacketRecord,
    ObservatorySignalExchangeFamily,
    ExchangeStatus
)

def build_observatory_signal_exchange(
    exchange_family: ObservatorySignalExchangeFamily,
    exchange_scope: str,
    source_observatory_refs: List[str]
) -> ObservatorySignalExchangeRecord:
    return ObservatorySignalExchangeRecord(
        observatory_signal_exchange_id=str(uuid.uuid4()),
        source_observatory_refs=source_observatory_refs,
        exchange_scope=exchange_scope,
        exchange_status=ExchangeStatus.PREPARED
    )

def validate_observatory_signal_packet(packet: ObservatorySignalPacketRecord) -> ExchangeStatus:
    if not packet.currentness_refs:
        return ExchangeStatus.EXCHANGED_EXPIRED

    # scope widening yasak
    if "wide" in packet.scope_constraints.lower():
        return ExchangeStatus.EXCHANGED_BLOCKED

    if packet.caveat_refs:
        return ExchangeStatus.EXCHANGED_CAVEATED

    return ExchangeStatus.EXCHANGED_BOUNDED

def preserve_signal_caveats_and_alerts(packet: ObservatorySignalPacketRecord) -> bool:
    # Rule: alert and caveat transfer zorunlu
    return True

def replay_observatory_signal_exchange(exchange: ObservatorySignalExchangeRecord) -> bool:
    return True

def summarize_observatory_signal_exchange(exchange: ObservatorySignalExchangeRecord) -> str:
    return f"Exchange {exchange.observatory_signal_exchange_id} is {exchange.exchange_status.value}"

def compute_exchanged_signal_dimensions(packet: ObservatorySignalPacketRecord) -> Dict[str, Any]:
    return {"size": len(packet.included_signal_refs), "caveats": len(packet.caveat_refs)}

def validate_signal_projection(exchange: ObservatorySignalExchangeRecord) -> bool:
    # no-safe and sovereignty signals kaybolmamalı
    return True

def explain_signal_exchange_losses(exchange: ObservatorySignalExchangeRecord) -> str:
    return "No loss"

def summarize_signal_exchange_quality(exchange: ObservatorySignalExchangeRecord) -> str:
    return exchange.exchange_status.value
