from typing import List
from .contracts import (
    PlanetaryCoverageSynthesisRecord,
    CoverageZoneRecord,
    CoverageWindowRecord,
    CoverageOwnerRecord,
    PlanetaryCoverageWarningRecord,
    CoverageSeamRecord,
    CoverageGapRecord
)

def build_planetary_coverage_synthesis(synthesis_id: str, family: str) -> PlanetaryCoverageSynthesisRecord:
    return PlanetaryCoverageSynthesisRecord(
        planetary_coverage_synthesis_id=synthesis_id,
        synthesis_family=family,
        synthesis_status="coverage_verified"
    )

def synthesize_planetary_coverage_windows(synthesis: PlanetaryCoverageSynthesisRecord, windows: List[CoverageWindowRecord]) -> None:
    synthesis.window_refs.extend(windows)

def detect_planetary_coverage_seams(synthesis: PlanetaryCoverageSynthesisRecord, seams: List[CoverageSeamRecord]) -> None:
    for seam in seams:
        if seam.status == "missing_ack":
            synthesis.warnings.append(PlanetaryCoverageWarningRecord(
                warning_id=f"warn_{seam.seam_id}",
                message="seam missing ack"
            ))
            if synthesis.synthesis_status == "coverage_verified":
                synthesis.synthesis_status = "coverage_caveated"
    synthesis.seam_refs.extend(seams)

def summarize_planetary_coverage(synthesis: PlanetaryCoverageSynthesisRecord) -> dict:
    return {
        "id": synthesis.planetary_coverage_synthesis_id,
        "status": synthesis.synthesis_status,
        "windows_count": len(synthesis.window_refs),
        "seams_count": len(synthesis.seam_refs),
        "warnings": len(synthesis.warnings)
    }

def verify_planetary_coverage_handoff(synthesis: PlanetaryCoverageSynthesisRecord, gap: CoverageGapRecord) -> None:
    if gap.duration_minutes > 0:
         synthesis.gap_refs.append(gap)
         synthesis.synthesis_status = "coverage_gapped"
         synthesis.warnings.append(PlanetaryCoverageWarningRecord(warning_id=f"gap_{gap.gap_id}", message="planetary coverage gap hidden by synthesis summary"))
