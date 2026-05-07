import json
import os
from .mesh_federations import (
    build_planetary_mesh_federation, add_mesh_federation_link, verify_planetary_mesh_federation,
    FederationFamily, FederatedMeshNodeRecord, MeshFederationLinkRecord, MeshFederationContinuityRecord
)
from .corridor_superchains import (
    build_corridor_superchain, add_superchain_segment, verify_corridor_superchain,
    SuperchainFamily, SuperchainSegmentRecord, SuperchainReplayRecord, SuperchainLineageRecord
)
from .scheduler_buses import (
    build_scheduler_bus, add_scheduler_bus_lane, build_scheduler_bus_packet, verify_scheduler_bus,
    BusFamily, SchedulerBusLaneRecord, SchedulerBusPacketRecord, SchedulerBusCadenceRecord
)
from .audit_cadence import (
    build_global_audit_cadence_orchestration, simulate_audit_cadence, OrchestrationFamily, CadenceWindowRecord
)
from .budgets import (
    build_global_cadence_budgets, measure_global_cadence_budget_consumption,
    MeshFederationBudgetRecord, SuperchainBudgetRecord
)

def run_hardening_pack_15():
    # 1. Mesh Federation
    mesh_fed = build_planetary_mesh_federation("mf-01", FederationFamily.BOUNDED_PLANETARY_MESH_FEDERATION)
    mesh_fed.member_mesh_refs.append(FederatedMeshNodeRecord("node-01", "us-east"))
    add_mesh_federation_link(mesh_fed, MeshFederationLinkRecord("link-01", "node-01", "node-02"))
    mesh_fed.continuity_refs.append(MeshFederationContinuityRecord("cont-01"))
    mesh_health = verify_planetary_mesh_federation(mesh_fed)

    # 2. Corridor Superchain
    superchain = build_corridor_superchain("sc-01", SuperchainFamily.INTERCONTINENTAL_ARCHIVE_SUPERCHAIN)
    add_superchain_segment(superchain, SuperchainSegmentRecord("seg-01"))
    superchain.replay_refs.append(SuperchainReplayRecord("replay-01"))
    superchain.lineage_refs.append(SuperchainLineageRecord("lin-01"))
    sc_health = verify_corridor_superchain(superchain)

    # 3. Scheduler Bus
    bus = build_scheduler_bus("bus-01", BusFamily.PLANETARY_COVERAGE_SCHEDULER_BUS)
    add_scheduler_bus_lane(bus, SchedulerBusLaneRecord("lane-01"))
    bus.packet_refs.append(build_scheduler_bus_packet("pkt-01"))
    bus.cadence_refs.append(SchedulerBusCadenceRecord("cad-01", drift_ms=0))
    bus_health = verify_scheduler_bus(bus)

    # 4. Audit Cadence
    orch = build_global_audit_cadence_orchestration("orch-01", OrchestrationFamily.WORLDWIDE_FOLLOW_THE_SUN_CADENCE_ORCHESTRATION)
    orch.window_refs.append(CadenceWindowRecord("win-01", has_ack=True))
    orch_health = simulate_audit_cadence(orch)

    # Output generation
    output_dir = "artifacts"
    os.makedirs(output_dir, exist_ok=True)

    def dump(filename, data):
        with open(os.path.join(output_dir, filename), "w") as f:
            json.dump(data, f, indent=2)

    dump("planetary_mesh_federations.json", {"id": "mf-01", "status": mesh_health.status.value})
    dump("corridor_superchains.json", {"id": "sc-01", "status": sc_health.status.value})
    dump("scheduler_buses.json", {"id": "bus-01", "status": bus_health.status.value})
    dump("global_audit_cadence_orchestration.json", {"id": "orch-01", "status": orch_health.status.value})

    health_report = {
        "overall_status": "verified" if (
            mesh_health.is_healthy and sc_health.is_healthy and
            bus_health.is_healthy and orch_health.is_healthy
        ) else "caveated/blocked"
    }
    dump("planetary_federation_hardening_health_report.json", health_report)

    print("Planetary Federation Hardening Pack 15 execution completed.")
    print(f"Overall Status: {health_report['overall_status']}")
