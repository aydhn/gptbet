import json
from src.sports_signal_bot.planetary_hardening.contracts import (
    PlanetaryCoverageCalendarManifestRecord,
    IntercontinentalRecoveryManifestRecord,
    GlobalQuorumFederationManifestRecord,
    FollowTheSunAuditManifestRecord
)

def build_planetary_continuity_matrix(calendars: PlanetaryCoverageCalendarManifestRecord, lanes: IntercontinentalRecoveryManifestRecord, federations: GlobalQuorumFederationManifestRecord, audits: FollowTheSunAuditManifestRecord) -> dict:
    return {
        "planetary_coverage_calendars": [c.calendar_family for c in calendars.calendars],
        "intercontinental_recovery_lanes": [l.lane_family for l in lanes.lanes],
        "global_quorum_federations": [f.federation_family for f in federations.federations],
        "follow_the_sun_audits": [a.audit_family for a in audits.audits]
    }

def validate_planetary_continuity_row(row: dict) -> bool:
    return True

def summarize_planetary_continuity_matrix(matrix: dict) -> dict:
    return {
        "total_calendars": len(matrix.get("planetary_coverage_calendars", [])),
        "total_lanes": len(matrix.get("intercontinental_recovery_lanes", [])),
        "total_federations": len(matrix.get("global_quorum_federations", [])),
        "total_audits": len(matrix.get("follow_the_sun_audits", []))
    }
