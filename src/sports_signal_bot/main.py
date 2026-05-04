from sports_signal_bot.cli.execution_coordination import app as execution_coordination_app
from sports_signal_bot.cli.live_execution_cli import app as live_execution_app
from sports_signal_bot.remediation_lanes.cli import remediation_lanes_app
import typer
from sports_signal_bot.cli.resilience_advisor import app as resilience_advisor_app
from sports_signal_bot.cli.remediation_copilot import app as copilot_app
from sports_signal_bot.cli.distributed_coordination import app as distributed_coordination_app

from sports_signal_bot.registry_conformance.cli import app as registry_conformance_app
app = typer.Typer()

from sports_signal_bot.cli.sovereign_corridors_cli import app as sovereign_corridors_app
multi_region_fabric_app = typer.Typer()
app.add_typer(multi_region_fabric_app, name="multi-region", help="Multi-Region Execution Fabric operations")

import json
from datetime import datetime
from sports_signal_bot.multi_region_fabric.regions import build_region
from sports_signal_bot.multi_region_fabric.shards import build_broker_shards
from sports_signal_bot.multi_region_fabric.treaties import build_recovery_treaty
from sports_signal_bot.multi_region_fabric.sovereignty import resolve_sovereignty_policy
from sports_signal_bot.multi_region_fabric.failover import evaluate_region_failover
from sports_signal_bot.multi_region_fabric.strategies.conservative import ConservativeMultiRegionFabricStrategy
from sports_signal_bot.multi_region_fabric.strategies.balanced_treaty_aware import BalancedTreatyAwareFabricStrategy
from sports_signal_bot.multi_region_fabric.strategies.sovereignty_first import SovereigntyFirstRemediationStrategy

@multi_region_fabric_app.command("run-multi-region-fabric-pass")
def run_multi_region_fabric_pass():
    typer.echo("Running multi-region execution fabric pass...")
    r1 = build_region("us-east", "primary_execution_region", "US East Primary")
    r2 = build_region("eu-west", "secondary_execution_region", "EU West Secondary")
    s1 = build_broker_shards("shard-1", "execution_token_shard", "us-east", "cluster-A")
    t1 = build_recovery_treaty("treaty-1", "review_delegation_treaty", ["us-east", "eu-west"], datetime(2030,1,1))
    p1 = resolve_sovereignty_policy("sov-1", "domain-A")
    f1 = evaluate_region_failover("us-east", "eu-west", True)

    summary = {
        "regions": [r1.model_dump(), r2.model_dump()],
        "shards": [s1.model_dump()],
        "treaties": [t1.model_dump()],
        "sovereignty": [p1.model_dump()],
        "failover_readiness": [f1.model_dump()],
        "status": "healthy"
    }

    import os
    os.makedirs("results", exist_ok=True)
    with open("results/multi_region_fabric_summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)

    typer.echo("Multi-region fabric pass complete. Summary written to results/multi_region_fabric_summary.json.")

@multi_region_fabric_app.command("preview-multi-region-fabrics")
def preview_multi_region_fabrics():
    typer.echo("Previewing multi-region fabrics...")
    typer.echo("Fabric us-east-primary is ACTIVE with 3 clusters.")

@multi_region_fabric_app.command("preview-broker-shards")
def preview_broker_shards():
    typer.echo("Previewing broker shards...")
    typer.echo("Shard shard-1 owned by us-east / cluster-A")

@multi_region_fabric_app.command("preview-recovery-treaties")
def preview_recovery_treaties():
    typer.echo("Previewing recovery treaties...")
    typer.echo("Treaty treaty-1: review_delegation_treaty between us-east, eu-west")

@multi_region_fabric_app.command("preview-sovereignty-decisions")
def preview_sovereignty_decisions():
    typer.echo("Previewing sovereignty decisions...")
    typer.echo("Domain domain-A: strict local token nonportability")

@multi_region_fabric_app.command("preview-region-failovers")
def preview_region_failovers():
    typer.echo("Previewing region failovers...")
    typer.echo("us-east to eu-west: failover_prepared")

@multi_region_fabric_app.command("list-multi-region-fabric-strategies")
def list_multi_region_fabric_strategies():
    typer.echo("Available strategies:")
    typer.echo(" - ConservativeMultiRegionFabricStrategy")
    typer.echo(" - BalancedTreatyAwareFabricStrategy")
    typer.echo(" - SovereigntyFirstRemediationStrategy")
    typer.echo(" - BrokerShardStrictStrategy")
    typer.echo(" - FailoverGuardedStrategy")

app.add_typer(resilience_advisor_app, name="resilience-advisor")
app.add_typer(sovereign_corridors_app, name="sovereign-corridors", help="Phase 76: Sovereign Runtime Corridors")
app.add_typer(copilot_app, name="remediation-copilot")

app.add_typer(remediation_lanes_app, name="remediation-lanes", help="Phase 71: Remediation Lane Architecture")
app.add_typer(live_execution_app, name="live-execution", help="Live execution operations")
app.add_typer(execution_coordination_app, name="execution-coordination")
app.add_typer(distributed_coordination_app, name="distributed-coordination", help="Phase 74: Distributed Execution Coordination Fabric")
app.add_typer(registry_conformance_app, name="registry-conformance", help="Phase 78: Registry Conformance")


from sports_signal_bot.cli.federation_ecosystem import app as federation_ecosystem_app
app.add_typer(federation_ecosystem_app, name="federation-ecosystem", help="Phase 79: Federation Ecosystem")

from sports_signal_bot.cli.corridor_governance_cli import app as corridor_governance_app
app.add_typer(corridor_governance_app, name="corridor-governance", help="Corridor Governance operations")

from sports_signal_bot.deployment.cli import app as deploy_app
app.add_typer(deploy_app, name="deploy", help="Platform packaging and local deployment operations")

if __name__ == "__main__":
    app()
