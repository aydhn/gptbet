import uuid
from typing import List, Tuple

from .contracts import (
    CandidateComparisonRecord,
    DominanceRelationRecord,
    ObjectiveDirection,
    ParetoFrontRecord,
)


def dominates(
    candidate_a: CandidateComparisonRecord,
    candidate_b: CandidateComparisonRecord,
    required_metrics: List[str],
) -> Tuple[bool, List[str]]:
    """Checks if candidate_a dominates candidate_b."""
    map_a = {m.metric_name: m for m in candidate_a.metrics}
    map_b = {m.metric_name: m for m in candidate_b.metrics}

    better_in_at_least_one = False
    dominating_metrics = []

    for metric_name in required_metrics:
        # If a metric is missing in A, A cannot dominate B
        if metric_name not in map_a:
            return False, []

        val_a = map_a[metric_name].value
        dir_a = map_a[metric_name].direction

        # If B is missing the metric, A is better by default for this metric
        val_b = (
            map_b.get(metric_name).value
            if metric_name in map_b
            else (
                float("-inf")
                if dir_a == ObjectiveDirection.MAXIMIZE
                else float("inf")
            )
        )

        if dir_a == ObjectiveDirection.MAXIMIZE:
            if val_a < val_b:
                return False, []
            if val_a > val_b:
                better_in_at_least_one = True
                dominating_metrics.append(metric_name)
        else:  # MINIMIZE
            if val_a > val_b:
                return False, []
            if val_a < val_b:
                better_in_at_least_one = True
                dominating_metrics.append(metric_name)

    return better_in_at_least_one, dominating_metrics


def explain_why_candidate_is_dominated(
    dominating_id: str, dominated_id: str, metrics: List[str]
) -> str:
    """Generates an explanation for dominance."""
    return (
        f"Candidate {dominated_id} is dominated by {dominating_id} "
        f"on metrics: {', '.join(metrics)} while being no better "
        f"on others."
    )


def compute_dominance_relations(
    candidates: List[CandidateComparisonRecord], required_metrics: List[str]
) -> List[DominanceRelationRecord]:
    """Computes all pairwise dominance relations."""
    relations = []

    for i, cand_a in enumerate(candidates):
        for j, cand_b in enumerate(candidates):
            if i == j:
                continue

            is_dominating, metrics = dominates(
                cand_a, cand_b, required_metrics
            )
            if is_dominating:
                relations.append(
                    DominanceRelationRecord(
                        relation_id=str(uuid.uuid4()),
                        dominating_candidate_id=cand_a.candidate_id,
                        dominated_candidate_id=cand_b.candidate_id,
                        dominating_metrics=metrics,
                        explanation=explain_why_candidate_is_dominated(
                            cand_a.candidate_id,
                            cand_b.candidate_id,
                            metrics,
                        ),
                    )
                )

    return relations


def _find_source_sccs(
    candidate_ids: List[str],
    relations: List[DominanceRelationRecord],
) -> List[str]:
    import collections

    graph = collections.defaultdict(list)
    for rel in relations:
        graph[rel.dominating_candidate_id].append(
            rel.dominated_candidate_id
        )

    index = 0
    indices = {}
    lowlinks = {}
    on_stack = set()
    stack = []
    sccs = []

    def strongconnect(v):
        nonlocal index
        indices[v] = index
        lowlinks[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)

        for w in graph[v]:
            if w not in indices:
                strongconnect(w)
                lowlinks[v] = min(lowlinks[v], lowlinks[w])
            elif w in on_stack:
                lowlinks[v] = min(lowlinks[v], indices[w])

        if lowlinks[v] == indices[v]:
            scc = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                scc.append(w)
                if w == v:
                    break
            sccs.append(scc)

    for v in candidate_ids:
        if v not in indices:
            strongconnect(v)

    scc_of = {}
    for i, scc in enumerate(sccs):
        for v in scc:
            scc_of[v] = i

    in_degree = {i: 0 for i in range(len(sccs))}
    for rel in relations:
        scc_u = scc_of[rel.dominating_candidate_id]
        scc_v = scc_of[rel.dominated_candidate_id]
        if scc_u != scc_v:
            in_degree[scc_v] += 1

    source_scc_nodes = []
    for i, scc in enumerate(sccs):
        if in_degree[i] == 0:
            source_scc_nodes.extend(scc)

    return source_scc_nodes


def compute_pareto_fronts(
    candidates: List[CandidateComparisonRecord], required_metrics: List[str]
) -> List[ParetoFrontRecord]:
    """
    Computes Pareto fronts by iteratively removing non-dominated candidates.
    """
    fronts = []
    remaining_candidates = list(candidates)
    front_index = 1

    all_relations = compute_dominance_relations(candidates, required_metrics)

    while remaining_candidates:
        current_front_ids = []
        current_relations = compute_dominance_relations(
            remaining_candidates, required_metrics
        )

        # Candidate is in the current front if it is part of a source SCC
        # in the dominance graph
        # This handles cycles gracefully
        remaining_ids = [c.candidate_id for c in remaining_candidates]
        current_front_ids = _find_source_sccs(
            remaining_ids, current_relations
        )

        if not current_front_ids:
            # Fallback if something goes wrong, though SCC should always find
            # at least one source
            break

        # Collect relations involving the current front dominating others
        front_relations = [
            rel
            for rel in all_relations
            if rel.dominating_candidate_id in current_front_ids
            and rel.dominated_candidate_id not in current_front_ids
        ]

        fronts.append(
            ParetoFrontRecord(
                front_index=front_index,
                candidate_ids=current_front_ids,
                relations=front_relations,
            )
        )

        remaining_candidates = [
            c
            for c in remaining_candidates
            if c.candidate_id not in current_front_ids
        ]
        front_index += 1

    return fronts


def summarize_front_distribution(fronts: List[ParetoFrontRecord]) -> str:
    """Summarizes the size of each Pareto front."""
    summary = []
    for f in fronts:
        summary.append(
            f"Front {f.front_index}: {len(f.candidate_ids)} candidates"
        )
    return ", ".join(summary)
