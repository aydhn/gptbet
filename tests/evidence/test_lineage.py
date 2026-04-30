from sports_signal_bot.evidence.lineage import build_evidence_graph, add_lineage_node, add_lineage_edge, trace_decision_backwards

def test_evidence_graph():
    graph = build_evidence_graph("g1")
    add_lineage_node(graph, "n1", "feature", {})
    add_lineage_node(graph, "n2", "decision", {})
    add_lineage_edge(graph, "n1", "n2", "derived_from")

    assert len(graph.nodes) == 2
    assert len(graph.edges) == 1

    trace = trace_decision_backwards(graph, "n2")
    assert len(trace) == 2
    assert trace[0].node_id == "n2"
    assert trace[1].node_id == "n1"
