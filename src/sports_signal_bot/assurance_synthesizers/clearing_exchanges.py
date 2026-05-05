from typing import List, Optional, Dict
import uuid

from src.sports_signal_bot.assurance_synthesizers.contracts import (
    EvidenceClearingExchangeRecord,
    ClearingExchangePacketRecord,
    ExchangeStatus
)

def build_evidence_clearing_exchange(
    exchange_scope: str,
    validity_window: str
) -> EvidenceClearingExchangeRecord:
    return EvidenceClearingExchangeRecord(
        evidence_clearing_exchange_id=f"exch_{uuid.uuid4().hex[:8]}",
        exchange_scope=exchange_scope,
        validity_window=validity_window
    )

def validate_clearing_exchange_packet(
    packet: ClearingExchangePacketRecord,
    sovereignty_allowed: bool
) -> ExchangeStatus:
    if not sovereignty_allowed:
        packet.warnings.append("blocked by sovereignty boundaries")
        return ExchangeStatus.exchanged_blocked

    if "partial" in packet.evidence_completeness or "weak" in packet.evidence_completeness:
        packet.warnings.append("evidence completeness partial, downgrading to caveated")
        return ExchangeStatus.exchanged_caveated

    return ExchangeStatus.exchanged_bounded

def summarize_clearing_exchange(exchange: EvidenceClearingExchangeRecord) -> Dict[str, str]:
    return {
        "id": exchange.evidence_clearing_exchange_id,
        "scope": exchange.exchange_scope,
        "status": exchange.exchange_status.value,
        "warning_count": str(len(exchange.warnings))
    }
