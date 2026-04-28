from typing import List, Dict, Set
from .contracts import JobDependencyRecord, JobState, ScheduledJobDefinition

class DependencyGraph:
    def __init__(self, jobs: List[ScheduledJobDefinition]):
        self.jobs = {j.job_name: j for j in jobs}
        self.adj_list: Dict[str, List[str]] = {j.job_name: list(j.dependency_names) for j in jobs}

    def validate_graph(self) -> bool:
        visited = set()
        path = set()

        def has_cycle(node: str) -> bool:
            if node in path: return True
            if node in visited: return False
            visited.add(node)
            path.add(node)
            for neighbor in self.adj_list.get(node, []):
                if has_cycle(neighbor): return True
            path.remove(node)
            return False

        for node in self.adj_list:
            if has_cycle(node):
                return False
        return True

    def topologically_order_jobs(self) -> List[str]:
        if not self.validate_graph():
            raise ValueError("Graph contains a cycle")

        visited = set()
        order = []

        def dfs(node: str):
            if node in visited: return
            visited.add(node)
            for neighbor in self.adj_list.get(node, []):
                dfs(neighbor)
            order.append(node)

        for node in self.adj_list:
            dfs(node)

        return order

    def resolve_dependency_readiness(self, job_name: str, execution_states: Dict[str, JobState]) -> bool:
        job = self.jobs.get(job_name)
        if not job: return False

        for dep_name in job.dependency_names:
            dep_state = execution_states.get(dep_name, JobState.planned)
            if dep_state not in [JobState.succeeded, JobState.succeeded_with_warnings, JobState.skipped]:
                return False
        return True

    def explain_dependency_block(self, job_name: str, execution_states: Dict[str, JobState]) -> str:
        job = self.jobs.get(job_name)
        if not job: return "Job not found"

        reasons = []
        for dep_name in job.dependency_names:
            dep_state = execution_states.get(dep_name, JobState.planned)
            if dep_state not in [JobState.succeeded, JobState.succeeded_with_warnings, JobState.skipped]:
                reasons.append(f"Requires {dep_name} (current: {dep_state.value})")
        return ", ".join(reasons)
