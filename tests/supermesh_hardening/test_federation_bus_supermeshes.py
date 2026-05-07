from src.sports_signal_bot.supermesh_hardening.bus_supermeshes import build_federation_bus_supermesh, add_supermesh_node, add_supermesh_edge, verify_federation_bus_supermesh
from src.sports_signal_bot.supermesh_hardening.contracts import SupermeshNodeRecord, SupermeshEdgeRecord

def test_build_federation_bus_supermesh():
    sm = build_federation_bus_supermesh("sm1", "bounded_federation_bus_supermesh")
    assert sm.federation_bus_supermesh_id == "sm1"
    assert sm.supermesh_status == "supermesh_verified"

def test_stale_edge_blocks_supermesh():
    sm = build_federation_bus_supermesh("sm1", "bounded_federation_bus_supermesh")
    add_supermesh_edge(sm, SupermeshEdgeRecord(edge_id="e1", edge_status="edge_current", from_node="n1", to_node="n2", is_stale=True))
    assert sm.supermesh_status == "supermesh_blocked"
    assert verify_federation_bus_supermesh(sm) == "supermesh_blocked"

def test_critical_ownerless_node_blocks_supermesh():
    sm = build_federation_bus_supermesh("sm1", "bounded_federation_bus_supermesh")
    add_supermesh_node(sm, SupermeshNodeRecord(node_id="n1", node_family="planetary_transport_node", is_critical=True, is_ownerless=True))
    assert sm.supermesh_status == "supermesh_blocked"
