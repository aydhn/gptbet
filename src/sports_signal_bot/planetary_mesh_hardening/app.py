import typer
import json
from .integration import PlanetaryMeshIntegration
from .bus_meshes import build_planetary_bus_mesh
from .corridor_chains import build_archive_corridor_chain
from .simulation_federations import build_audit_simulation_federation
from .scheduler_audits import build_global_continuity_scheduler_audit
from .manifests import generate_planetary_mesh_hardening_manifest

app = typer.Typer()

def run_all(strategy: str = "conservative"):
    integ = PlanetaryMeshIntegration()
    integ.add_mesh(build_planetary_bus_mesh("m1", "composite_planetary_bus_mesh"))
    integ.add_chain(build_archive_corridor_chain("c1", "intercontinental_archive_corridor_chain"))
    integ.add_federation(build_audit_simulation_federation("f1", "composite_audit_simulation_federation"))
    integ.add_scheduler_audit(build_global_continuity_scheduler_audit("s1", "planetary_coverage_scheduler_audit"))

    summary = integ.summarize()

    with open("planetary_bus_meshes.json", "w") as f:
        json.dump(summary["meshes"], f, indent=2)
    with open("archive_corridor_chains.json", "w") as f:
        json.dump(summary["chains"], f, indent=2)
    with open("audit_simulation_federations.json", "w") as f:
        json.dump(summary["federations"], f, indent=2)
    with open("global_continuity_scheduler_audits.json", "w") as f:
        json.dump(summary["scheduler_audits"], f, indent=2)
    with open("planetary_mesh_hardening_health_report.json", "w") as f:
        json.dump({"readiness": summary["overall_readiness"]}, f, indent=2)

    return summary

@app.command("run-hardening-pack-14")
def run_hardening_pack_14():
    print("Running planetary mesh hardening pack 14...")
    summary = run_all()
    print("Planetary mesh hardening complete. Report generated.")
    print(json.dumps(summary, indent=2))

@app.command("preview-planetary-bus-mesh-report")
def preview_mesh():
    print("Previewing planetary bus mesh report...")

@app.command("preview-archive-corridor-chain-report")
def preview_chain():
    print("Previewing archive corridor chain report...")

@app.command("preview-audit-simulation-federation-report")
def preview_fed():
    print("Previewing audit simulation federation report...")

@app.command("preview-global-scheduler-audit-report")
def preview_sched():
    print("Previewing global continuity scheduler audit report...")

@app.command("preview-planetary-mesh-hardening-health")
def preview_health():
    print("Previewing health...")

@app.command("list-planetary-mesh-hardening-strategies")
def list_strategies():
    print("Strategies: ConservativePlanetaryMeshHardeningStrategy, BalancedMeshReadinessStrategy, ChainIntegrityFirstStrategy, SchedulerAuditFirstStrategy")
