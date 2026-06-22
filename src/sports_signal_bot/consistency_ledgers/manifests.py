import json
from typing import Any, Dict, List

from sports_signal_bot.consistency_ledgers.contracts import (
    AlignmentCompilerFederationManifestRecord,
    DisputeTribunalMeshManifestRecord,
    EvidenceExchangeClearerManifestRecord,
    GovernanceConsistencyLedgerManifestRecord,
)


class ConsistencyLedgersManifest:
    def __init__(self):
        self.federations: List[Dict[str, Any]] = []
        self.meshes: List[Dict[str, Any]] = []
        self.clearers: List[Dict[str, Any]] = []
        self.ledgers: List[Dict[str, Any]] = []

    def add_federation(self, record: Any):
        if hasattr(record, "model_dump"):
            self.federations.append(record.model_dump())
        else:
            self.federations.append(record)

    def add_mesh(self, record: Any):
        if hasattr(record, "model_dump"):
            self.meshes.append(record.model_dump())
        else:
            self.meshes.append(record)

    def add_clearer(self, record: Any):
        if hasattr(record, "model_dump"):
            self.clearers.append(record.model_dump())
        else:
            self.clearers.append(record)

    def add_ledger(self, record: Any):
        if hasattr(record, "model_dump"):
            self.ledgers.append(record.model_dump())
        else:
            self.ledgers.append(record)

    def to_json(self) -> str:
        return json.dumps(
            {
                "federations": self.federations,
                "meshes": self.meshes,
                "clearers": self.clearers,
                "ledgers": self.ledgers,
            },
            indent=2,
        )
