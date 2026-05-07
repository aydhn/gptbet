from typing import List
from .contracts import ArchiveCorridorChainRecord, ChainStatus

def build_archive_corridor_chain(chain_id: str, family: str) -> ArchiveCorridorChainRecord:
    return ArchiveCorridorChainRecord(
        archive_corridor_chain_id=chain_id,
        chain_family=family,
        node_refs=[],
        edge_refs=[],
        segment_refs=[],
        hash_refs=[],
        lineage_refs=[],
        replay_refs=[],
        residue_refs=[],
        chain_status=ChainStatus.CHAIN_REVIEW_ONLY,
        warnings=[]
    )

def add_corridor_chain_segment(chain: ArchiveCorridorChainRecord, segment_id: str):
    chain.segment_refs.append(segment_id)

def verify_archive_corridor_chain(chain: ArchiveCorridorChainRecord):
    if "no_replay" in chain.replay_refs:
        chain.chain_status = ChainStatus.CHAIN_GAPPED
        chain.warnings.append("Replay support missing")
    else:
        chain.chain_status = ChainStatus.CHAIN_VERIFIED

def replay_archive_corridor_chain(chain: ArchiveCorridorChainRecord):
    pass

def summarize_archive_corridor_chain(chain: ArchiveCorridorChainRecord) -> dict:
    return {
        "chain_id": chain.archive_corridor_chain_id,
        "status": chain.chain_status.value
    }
