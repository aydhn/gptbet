from sports_signal_bot.federated_governance.contracts import CrossPlaneConflictRecord, MeshPolicyBindingRecord
from sports_signal_bot.federated_governance.mesh import detect_policy_collision, resolve_policy_precedence

def test_detect_policy_collision():
    b1 = MeshPolicyBindingRecord(binding_id="b1", policy_family="risk", owner_plane="p1", consumer_planes=["target"], override_rules={}, precedence_rank=1, violation_action="escalate")
    b2 = MeshPolicyBindingRecord(binding_id="b2", policy_family="quality", owner_plane="p2", consumer_planes=["target"], override_rules={}, precedence_rank=2, violation_action="escalate")

    collision = detect_policy_collision([b1, b2], "target")
    assert collision is not None
    assert "b1" in collision.policies_involved

def test_resolve_policy_precedence():
    b1 = MeshPolicyBindingRecord(binding_id="b1", policy_family="risk", owner_plane="p1", consumer_planes=["target"], override_rules={}, precedence_rank=1, violation_action="escalate")
    b2 = MeshPolicyBindingRecord(binding_id="b2", policy_family="quality", owner_plane="p2", consumer_planes=["target"], override_rules={}, precedence_rank=2, violation_action="escalate")

    winner = resolve_policy_precedence([b1, b2])
    assert winner.binding_id == "b2"
