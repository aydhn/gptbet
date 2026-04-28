import pytest
import datetime
from sports_signal_bot.scheduler.contracts import ScheduledJobDefinition, JobState, SlotType
from sports_signal_bot.scheduler.dependencies import DependencyGraph

def test_dependency_graph_valid():
    jobs = [
        ScheduledJobDefinition(job_name="A", job_family="fam", job_runner_entrypoint="A", output_contract_name="outA"),
        ScheduledJobDefinition(job_name="B", job_family="fam", dependency_names=["A"], job_runner_entrypoint="B", output_contract_name="outB"),
        ScheduledJobDefinition(job_name="C", job_family="fam", dependency_names=["A", "B"], job_runner_entrypoint="C", output_contract_name="outC")
    ]
    graph = DependencyGraph(jobs)
    assert graph.validate_graph() == True
    order = graph.topologically_order_jobs()
    assert order == ["A", "B", "C"]

def test_dependency_graph_cycle():
    jobs = [
        ScheduledJobDefinition(job_name="A", job_family="fam", dependency_names=["B"], job_runner_entrypoint="A", output_contract_name="outA"),
        ScheduledJobDefinition(job_name="B", job_family="fam", dependency_names=["A"], job_runner_entrypoint="B", output_contract_name="outB")
    ]
    graph = DependencyGraph(jobs)
    assert graph.validate_graph() == False
    with pytest.raises(ValueError):
        graph.topologically_order_jobs()

def test_resolve_dependency_readiness():
    jobs = [
        ScheduledJobDefinition(job_name="A", job_family="fam", job_runner_entrypoint="A", output_contract_name="outA"),
        ScheduledJobDefinition(job_name="B", job_family="fam", dependency_names=["A"], job_runner_entrypoint="B", output_contract_name="outB")
    ]
    graph = DependencyGraph(jobs)

    # Not ready if A is planned
    states = {"A": JobState.planned}
    assert graph.resolve_dependency_readiness("B", states) == False

    # Ready if A is succeeded
    states = {"A": JobState.succeeded}
    assert graph.resolve_dependency_readiness("B", states) == True
