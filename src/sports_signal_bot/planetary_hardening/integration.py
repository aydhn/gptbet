import json
from pathlib import Path

from src.sports_signal_bot.planetary_hardening.contracts import (
    PlanetaryCoverageCalendarManifestRecord,
    IntercontinentalRecoveryManifestRecord,
    GlobalQuorumFederationManifestRecord,
    FollowTheSunAuditManifestRecord,
    PlanetaryCoverageCalendarRecord,
    CoverageCalendarZoneRecord,
    IntercontinentalRecoveryLaneRecord,
    RecoveryLaneSourceRecord,
    RecoveryLaneTargetRecord,
    GlobalQuorumFederationRecord,
    FederatedQuorumNodeRecord,
    FollowTheSunAuditPackRecord,
    AuditPackEvidenceRecord,
    AuditPackHandoffRecord
)
from src.sports_signal_bot.planetary_hardening.coverage_calendars import build_planetary_coverage_calendar, verify_planetary_coverage_calendar, summarize_planetary_coverage_calendar
from src.sports_signal_bot.planetary_hardening.recovery_lanes import build_intercontinental_recovery_lane, verify_recovery_lane_source_and_target, summarize_intercontinental_recovery_lane
from src.sports_signal_bot.planetary_hardening.quorum_federations import build_global_quorum_federation, verify_global_quorum_federation, summarize_global_quorum_federation
from src.sports_signal_bot.planetary_hardening.follow_the_sun_audits import build_follow_the_sun_audit_pack, verify_follow_the_sun_audit_pack, verify_follow_the_sun_handoff, summarize_follow_the_sun_audit_pack
from src.sports_signal_bot.planetary_hardening.budgets import build_planetary_resilience_budgets, summarize_planetary_resilience_budgets
from src.sports_signal_bot.planetary_hardening.summaries import build_planetary_continuity_matrix, summarize_planetary_continuity_matrix
from src.sports_signal_bot.planetary_hardening.diagnostics import generate_health_report

class PlanetaryHardeningIntegrator:
    def __init__(self, strategy_name: str = "conservative"):
        self.strategy_name = strategy_name
        self.calendar_manifest = PlanetaryCoverageCalendarManifestRecord(manifest_id="cm_1")
        self.lane_manifest = IntercontinentalRecoveryManifestRecord(manifest_id="lm_1")
        self.federation_manifest = GlobalQuorumFederationManifestRecord(manifest_id="fm_1")
        self.audit_manifest = FollowTheSunAuditManifestRecord(manifest_id="am_1")
        self.budget_manifest = build_planetary_resilience_budgets()

    def run_pass(self):
        reject_stale = self.strategy_name != "balanced"

        # Calendars
        cal = build_planetary_coverage_calendar("composite_planetary_coverage_calendar", [CoverageCalendarZoneRecord(zone_id="z1", owner="o1")])
        cal = verify_planetary_coverage_calendar(cal, reject_stale=reject_stale)
        self.calendar_manifest.calendars.append(cal)

        # Lanes
        lane = build_intercontinental_recovery_lane("americas_to_europe_recovery_lane", RecoveryLaneSourceRecord(source_id="s1", is_fresh=True), RecoveryLaneTargetRecord(target_id="t1", is_ready=True))
        lane = verify_recovery_lane_source_and_target(lane, reject_stale=reject_stale)
        self.lane_manifest.lanes.append(lane)

        # Federations
        fed = build_global_quorum_federation("bounded_global_quorum_federation", [FederatedQuorumNodeRecord(node_id="n1", is_stale=False)])
        fed = verify_global_quorum_federation(fed, cap_on_stale=reject_stale)
        self.federation_manifest.federations.append(fed)

        # Audits
        audit = build_follow_the_sun_audit_pack("follow_the_sun_handoff_audit", [AuditPackEvidenceRecord(evidence_id="e1", is_stale=False)])
        audit = verify_follow_the_sun_handoff(audit, AuditPackHandoffRecord(handoff_id="h1", is_replayable=True))
        audit = verify_follow_the_sun_audit_pack(audit, reject_stale=reject_stale)
        self.audit_manifest.audits.append(audit)

    def summarize(self) -> dict:
        matrix = build_planetary_continuity_matrix(self.calendar_manifest, self.lane_manifest, self.federation_manifest, self.audit_manifest)
        matrix_summary = summarize_planetary_continuity_matrix(matrix)
        budget_summary = summarize_planetary_resilience_budgets(self.budget_manifest)

        return {
            "calendars": [summarize_planetary_coverage_calendar(c) for c in self.calendar_manifest.calendars],
            "lanes": [summarize_intercontinental_recovery_lane(l) for l in self.lane_manifest.lanes],
            "federations": [summarize_global_quorum_federation(f) for f in self.federation_manifest.federations],
            "audits": [summarize_follow_the_sun_audit_pack(a) for a in self.audit_manifest.audits],
            "health": generate_health_report(matrix_summary, budget_summary)
        }

    def export_artifacts(self, output_dir: str):
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)

        with open(path / "planetary_coverage_calendars.json", "w") as f:
            json.dump(self.calendar_manifest.model_dump(), f, indent=2)

        with open(path / "intercontinental_recovery_lanes.json", "w") as f:
            json.dump(self.lane_manifest.model_dump(), f, indent=2)

        with open(path / "global_quorum_federations.json", "w") as f:
            json.dump(self.federation_manifest.model_dump(), f, indent=2)

        with open(path / "follow_the_sun_audit_packs.json", "w") as f:
            json.dump(self.audit_manifest.model_dump(), f, indent=2)

        with open(path / "planetary_resilience_budgets.json", "w") as f:
            json.dump(self.budget_manifest.model_dump(), f, indent=2)

        matrix = build_planetary_continuity_matrix(self.calendar_manifest, self.lane_manifest, self.federation_manifest, self.audit_manifest)
        with open(path / "planetary_continuity_matrix.json", "w") as f:
            json.dump(matrix, f, indent=2)

        summary = self.summarize()
        with open(path / "planetary_hardening_health_report.json", "w") as f:
            json.dump(summary["health"], f, indent=2)
