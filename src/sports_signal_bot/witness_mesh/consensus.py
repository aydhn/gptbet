from typing import List, Dict
from .contracts import WitnessStatementRecord, WitnessConsensusRecord, WitnessConsensusType, WitnessStatementType
import datetime

class ConsensusEngine:
    def aggregate_witness_statements(self, statements: List[WitnessStatementRecord]) -> Dict[str, List[WitnessStatementRecord]]:
        grouped = {}
        for stmt in statements:
            if stmt.target_ref not in grouped:
                grouped[stmt.target_ref] = []
            grouped[stmt.target_ref].append(stmt)
        return grouped

    def compute_witness_consensus(self, statements: List[WitnessStatementRecord], target_ref: str) -> WitnessConsensusRecord:
        # Simplistic consensus: majority rules on CONFIRMED vs others
        confirmed_ids = []
        dissenting_ids = []

        for stmt in statements:
            if stmt.target_ref != target_ref:
                continue
            if "confirmed" in stmt.verification_result.lower():
                confirmed_ids.append(stmt.witness_id)
            else:
                dissenting_ids.append(stmt.witness_id)

        total = len(confirmed_ids) + len(dissenting_ids)
        if total == 0:
            ctype = WitnessConsensusType.INSUFFICIENT_WITNESSES
        elif len(confirmed_ids) == total and total >= 2:
            ctype = WitnessConsensusType.UNANIMOUS_CONFIRMED
        elif len(confirmed_ids) > total / 2:
            ctype = WitnessConsensusType.MAJORITY_CONFIRMED
        elif len(confirmed_ids) == len(dissenting_ids) and total > 0:
            ctype = WitnessConsensusType.SPLIT_OBSERVATION
        else:
            ctype = WitnessConsensusType.CONTESTED

        return WitnessConsensusRecord(
            consensus_id=f"cons_{target_ref}_{datetime.datetime.utcnow().timestamp()}",
            target_ref=target_ref,
            consensus_type=ctype,
            supporting_witness_ids=confirmed_ids,
            dissenting_witness_ids=dissenting_ids,
            created_at=datetime.datetime.utcnow()
        )
