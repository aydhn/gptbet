import pytest
from sports_signal_bot.assurance.dependencies import build_claim_dependency_graph

def test_dependency_graph():
    claims = [
        {"claim_id": "c1", "dependency_refs": []},
        {"claim_id": "c2", "dependency_refs": ["c1"]}
    ]
    graph = build_claim_dependency_graph(claims)
    assert graph["c2"] == ["c1"]
