from typing import List, Optional

from .contracts import (
    ReplayWorkloadExchangeRecord,
    ReplayExchangePacketRecord,
    ReplayExchangeScopeRecord
)

def build_replay_workload_exchange(exchange_id: str) -> ReplayWorkloadExchangeRecord:
    return ReplayWorkloadExchangeRecord(
        replay_exchange_id=exchange_id,
        exchange_scope=ReplayExchangeScopeRecord(scope_id=f"scope_{exchange_id}"),
        validity_window="24h",
        exchange_status="prepared"
    )

def validate_replay_exchange_packet(packet: ReplayExchangePacketRecord) -> bool:
    if not packet.required_evidence_refs:
        return False
    return True

def summarize_replay_exchange(exchange: ReplayWorkloadExchangeRecord) -> dict:
    return {
        "id": exchange.replay_exchange_id,
        "status": exchange.exchange_status,
        "workloads": len(exchange.workload_packet_refs)
    }
