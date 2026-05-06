from src.sports_signal_bot.geo_quorum_hardening.strategies.base import BaseGeoQuorumHardeningStrategy
from src.sports_signal_bot.geo_quorum_hardening.contracts import GeoQuorumHardeningManifestRecord
from datetime import datetime, timezone
import uuid

class BalancedGeoQuorumReadinessStrategy(BaseGeoQuorumHardeningStrategy):
    def evaluate(self, inputs: dict) -> GeoQuorumHardeningManifestRecord:
        warnings = []
        status = "healthy"
        if inputs.get("coverage_seam_gaps", 0) > 0:
            warnings.append("BalancedStrategy: Coverage seam gaps detected.")
            status = "degraded"
        return GeoQuorumHardeningManifestRecord(
            manifest_id=f"bgeoqhm-{uuid.uuid4().hex[:8]}",
            regional_quorum_drill_refs=inputs.get("quorum_drill_refs", []),
            active_passive_rehearsal_refs=inputs.get("rehearsal_refs", []),
            global_coverage_synthesis_refs=inputs.get("coverage_refs", []),
            rolling_evacuation_chain_refs=inputs.get("evacuation_refs", []),
            overall_status=status,
            warnings=warnings,
            created_at=datetime.now(timezone.utc)
        )
