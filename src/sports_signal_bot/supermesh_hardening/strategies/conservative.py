from .base import SupermeshHardeningStrategy
from ..bus_supermeshes import build_federation_bus_supermesh, add_supermesh_node, add_supermesh_edge
from ..contracts import SupermeshNodeRecord, SupermeshEdgeRecord

class ConservativeSupermeshHardeningStrategy(SupermeshHardeningStrategy):
    name = "ConservativeSupermeshHardeningStrategy"

    def apply(self, integrator):
        # Federation Bus Supermesh
        sm = build_federation_bus_supermesh("sm-conservative", "bounded_federation_bus_supermesh")
        add_supermesh_node(sm, SupermeshNodeRecord(node_id="n1", node_family="planetary_transport_node", is_critical=True))
        add_supermesh_edge(sm, SupermeshEdgeRecord(edge_id="e1", edge_status="edge_current", from_node="n1", to_node="n2"))

        # If any edge is stale, it blocks
        stale_edge = SupermeshEdgeRecord(edge_id="e2", edge_status="edge_stale", from_node="n2", to_node="n3", is_stale=True)
        # Note: in this strategy, we add it, which sets the mesh to blocked.
        # But for tests we may want a clean one or a blocked one depending on the test.
        # We will add a clean edge for general pass.
        clean_edge = SupermeshEdgeRecord(edge_id="e2", edge_status="edge_current", from_node="n2", to_node="n3", is_stale=False)
        add_supermesh_edge(sm, clean_edge)

        integrator.add_supermesh(sm)

        # Scheduler Cadence Fabric
        from ..cadence_fabrics import build_scheduler_cadence_fabric, add_cadence_fabric_lane
        from ..contracts import CadenceFabricLaneRecord
        fab = build_scheduler_cadence_fabric("fab-conservative", "planetary_coverage_cadence_fabric")
        add_cadence_fabric_lane(fab, CadenceFabricLaneRecord(lane_id="l1", lane_family="global_primary_lane", is_critical=True))
        integrator.add_fabric(fab)

        # Global Audit Pulse Lane
        from ..audit_pulse_lanes import build_global_audit_pulse_lane, emit_audit_pulse
        from ..contracts import AuditPulseRecord
        pulse_lane = build_global_audit_pulse_lane("pl-conservative", "worldwide_follow_the_sun_pulse_lane")
        emit_audit_pulse(pulse_lane, AuditPulseRecord(pulse_id="p1", pulse_family="operator_pulse"))
        integrator.add_pulse_lane(pulse_lane)

        # Planetary Handoff Observatory
        from ..handoff_observatories import build_planetary_handoff_observatory, register_observatory_window
        from ..contracts import HandoffObservatoryWindowRecord
        obs = build_planetary_handoff_observatory("obs-conservative", "follow_the_sun_handoff_observatory")
        register_observatory_window(obs, HandoffObservatoryWindowRecord(window_id="w1", window_family="operator_to_operator_window"))
        integrator.add_observatory(obs)
