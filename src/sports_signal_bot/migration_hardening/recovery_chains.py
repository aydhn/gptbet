from pydantic import Field
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from .contracts import ChainFamily, ChainStatus

class RecoveryChainNodeRecord(BaseModel):
    node_id: str
    description: str
    is_stale: bool = False

class RecoveryChainEdgeRecord(BaseModel):
    edge_id: str
    from_node: str
    to_node: str
    has_lineage: bool = False

class RecoveryChainDependencyRecord(BaseModel):
    dependency_id: str
    is_broken: bool = False

class RecoveryChainGapRecord(BaseModel):
    gap_id: str
    description: str

class RecoveryChainWarningRecord(BaseModel):
    warning_id: str
    description: str

class ArchivalRecoveryChainRecord(BaseModel):
    recovery_chain_id: str
    chain_family: ChainFamily
    node_refs: List[RecoveryChainNodeRecord] = Field(default_factory=list)
    edge_refs: List[RecoveryChainEdgeRecord] = Field(default_factory=list)
    dependency_refs: List[RecoveryChainDependencyRecord] = Field(default_factory=list)
    gap_refs: List[RecoveryChainGapRecord] = Field(default_factory=list)
    chain_status: ChainStatus = ChainStatus.chain_gapped
    warnings: List[RecoveryChainWarningRecord] = Field(default_factory=list)

def build_archival_recovery_chain(chain_id: str, family: ChainFamily) -> ArchivalRecoveryChainRecord:
    return ArchivalRecoveryChainRecord(
        recovery_chain_id=chain_id,
        chain_family=family
    )

def add_recovery_chain_node(chain: ArchivalRecoveryChainRecord, node: RecoveryChainNodeRecord) -> None:
    chain.node_refs.append(node)
    if node.is_stale:
        chain.gap_refs.append(RecoveryChainGapRecord(
            gap_id=f"gap_stale_node_{node.node_id}",
            description=f"Node {node.node_id} is stale."
        ))

def add_recovery_chain_edge(chain: ArchivalRecoveryChainRecord, edge: RecoveryChainEdgeRecord) -> None:
    chain.edge_refs.append(edge)
    if not edge.has_lineage:
        chain.gap_refs.append(RecoveryChainGapRecord(
            gap_id=f"gap_missing_lineage_{edge.edge_id}",
            description=f"Edge {edge.edge_id} missing lineage."
        ))

def verify_recovery_chain_integrity(chain: ArchivalRecoveryChainRecord) -> None:
    broken_deps = [d for d in chain.dependency_refs if d.is_broken]
    if broken_deps:
        for bd in broken_deps:
             chain.gap_refs.append(RecoveryChainGapRecord(
                 gap_id=f"gap_broken_dep_{bd.dependency_id}",
                 description=f"Dependency {bd.dependency_id} is broken."
             ))

    if chain.gap_refs:
        if any("broken_dep" in g.gap_id for g in chain.gap_refs):
            chain.chain_status = ChainStatus.chain_broken
        else:
            chain.chain_status = ChainStatus.chain_gapped
    elif chain.warnings:
        chain.chain_status = ChainStatus.chain_caveated
    else:
        chain.chain_status = ChainStatus.chain_verified

def summarize_archival_recovery_chain(chain: ArchivalRecoveryChainRecord) -> Dict:
    return {
        "chain_id": chain.recovery_chain_id,
        "family": chain.chain_family.value,
        "status": chain.chain_status.value,
        "nodes_count": len(chain.node_refs),
        "edges_count": len(chain.edge_refs),
        "gaps_count": len(chain.gap_refs)
    }
