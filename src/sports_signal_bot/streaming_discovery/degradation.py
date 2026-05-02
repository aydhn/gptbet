from typing import List
from .contracts import DegradationModeRecord, SyncAnomalyClusterRecord

class DegradationMonitor:
    def __init__(self):
        self.active_modes: List[DegradationModeRecord] = [
            DegradationModeRecord(
                mode_family="normal_operation",
                triggers=["system_start"],
                impact_summary="System operating normally",
                is_active=True
            )
        ]

    def evaluate_health(self, clusters: List[SyncAnomalyClusterRecord]):
        high_severity_clusters = [c for c in clusters if c.severity == "high" and c.current_status == "open"]

        has_normal = any(m.mode_family == "normal_operation" and m.is_active for m in self.active_modes)
        has_degraded = any(m.mode_family == "routing_degraded_mode" and m.is_active for m in self.active_modes)

        if len(high_severity_clusters) > 0 and not has_degraded:
            # Enter degraded mode
            for m in self.active_modes:
                if m.mode_family == "normal_operation":
                    m.is_active = False

            self.active_modes.append(DegradationModeRecord(
                mode_family="routing_degraded_mode",
                triggers=[f"High severity clusters detected: {len(high_severity_clusters)}"],
                impact_summary="Routing is degraded, falling back to safe routes only",
                is_active=True
            ))

    def get_active_modes(self) -> List[DegradationModeRecord]:
        return [m for m in self.active_modes if m.is_active]
