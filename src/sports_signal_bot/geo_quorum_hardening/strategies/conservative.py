from src.sports_signal_bot.geo_quorum_hardening.strategies.base import BaseGeoQuorumHardeningStrategy
from src.sports_signal_bot.geo_quorum_hardening.contracts import GeoQuorumHardeningManifestRecord
from datetime import datetime, timezone
import uuid

class ConservativeGeoQuorumHardeningStrategy(BaseGeoQuorumHardeningStrategy):
    def evaluate(self, inputs: dict) -> GeoQuorumHardeningManifestRecord:
        warnings = []
        status = "healthy"
        if not inputs.get("quorum_sufficient", True):
            warnings.append("ConservativeStrategy: Quorum erosion detected.")
            status = "blocked"
        return GeoQuorumHardeningManifestRecord(
            manifest_id=f"cgeoqhm-{uuid.uuid4().hex[:8]}",
            regional_quorum_drill_refs=inputs.get("quorum_drill_refs", []),
            active_passive_rehearsal_refs=inputs.get("rehearsal_refs", []),
            global_coverage_synthesis_refs=inputs.get("coverage_refs", []),
            rolling_evacuation_chain_refs=inputs.get("evacuation_refs", []),
            overall_status=status,
            warnings=warnings,
            created_at=datetime.now(timezone.utc)
        )
