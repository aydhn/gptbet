from .base import SupermeshHardeningStrategy
from ..bus_supermeshes import build_federation_bus_supermesh, add_supermesh_node, add_supermesh_edge
from ..contracts import SupermeshNodeRecord, SupermeshEdgeRecord

class BalancedSupermeshReadinessStrategy(SupermeshHardeningStrategy):
    name = "BalancedSupermeshReadinessStrategy"

    def apply(self, integrator):
        sm = build_federation_bus_supermesh("sm-balanced", "degraded_federation_bus_supermesh")
        add_supermesh_node(sm, SupermeshNodeRecord(node_id="n1", node_family="planetary_transport_node", is_critical=True))
        add_supermesh_edge(sm, SupermeshEdgeRecord(edge_id="e1", edge_status="edge_current", from_node="n1", to_node="n2"))
        integrator.add_supermesh(sm)

        # Cadence Fabric
        from ..cadence_fabrics import build_scheduler_cadence_fabric, add_cadence_fabric_lane
        from ..contracts import CadenceFabricLaneRecord
        fab = build_scheduler_cadence_fabric("fab-balanced", "continuity_owner_cadence_fabric")
        add_cadence_fabric_lane(fab, CadenceFabricLaneRecord(lane_id="l1", lane_family="continuity_owner_lane", is_critical=True))
        integrator.add_fabric(fab)

        # Pulse Lane
        from ..audit_pulse_lanes import build_global_audit_pulse_lane, emit_audit_pulse
        from ..contracts import AuditPulseRecord
        pulse_lane = build_global_audit_pulse_lane("pl-balanced", "continuity_owner_pulse_lane")
        emit_audit_pulse(pulse_lane, AuditPulseRecord(pulse_id="p1", pulse_family="continuity_owner_pulse"))
        integrator.add_pulse_lane(pulse_lane)

        # Observatory
        from ..handoff_observatories import build_planetary_handoff_observatory, register_observatory_window
        from ..contracts import HandoffObservatoryWindowRecord
        obs = build_planetary_handoff_observatory("obs-balanced", "continuity_owner_handoff_observatory")
        register_observatory_window(obs, HandoffObservatoryWindowRecord(window_id="w1", window_family="recovery_owner_window"))
        integrator.add_observatory(obs)
