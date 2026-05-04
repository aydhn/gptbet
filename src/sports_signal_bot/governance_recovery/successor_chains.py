from typing import List, Optional
from .contracts import (
    SuccessorChainRecord,
    SuccessorRegistryEntryRecord
)

def build_successor_chain(source_baseline_ref: str, successors: List[str]) -> SuccessorChainRecord:
    return SuccessorChainRecord(
        chain_id=f"chain_{source_baseline_ref}",
        source_baseline_ref=source_baseline_ref,
        successor_sequence=successors
    )

def compare_successor_candidates(candidates: List[str]) -> Optional[str]:
    if candidates:
        return candidates[-1]
    return None

def preserve_successor_lineage(chain: SuccessorChainRecord) -> SuccessorChainRecord:
    return chain

def summarize_successor_chain(chain: SuccessorChainRecord) -> dict:
    return {"chain_id": chain.chain_id, "length": len(chain.successor_sequence)}
