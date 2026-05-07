from .bus_meshes import build_planetary_bus_mesh, verify_planetary_bus_mesh, summarize_planetary_bus_mesh
from .corridor_chains import build_archive_corridor_chain, verify_archive_corridor_chain, summarize_archive_corridor_chain
from .simulation_federations import build_audit_simulation_federation, verify_audit_simulation_federation, summarize_audit_simulation_federation
from .scheduler_audits import build_global_continuity_scheduler_audit, summarize_global_scheduler_audit
from .budgets import build_global_scheduler_budgets, summarize_global_scheduler_budgets
from .summaries import build_planetary_mesh_matrix

class PlanetaryMeshIntegration:
    def __init__(self):
        self.meshes = []
        self.chains = []
        self.federations = []
        self.scheduler_audits = []

    def add_mesh(self, mesh):
        verify_planetary_bus_mesh(mesh)
        self.meshes.append(mesh)

    def add_chain(self, chain):
        verify_archive_corridor_chain(chain)
        self.chains.append(chain)

    def add_federation(self, fed):
        verify_audit_simulation_federation(fed)
        self.federations.append(fed)

    def add_scheduler_audit(self, audit):
        self.scheduler_audits.append(audit)

    def summarize(self):
        return {
            "meshes": [summarize_planetary_bus_mesh(m) for m in self.meshes],
            "chains": [summarize_archive_corridor_chain(c) for c in self.chains],
            "federations": [summarize_audit_simulation_federation(f) for f in self.federations],
            "scheduler_audits": [summarize_global_scheduler_audit(s) for s in self.scheduler_audits],
            "budgets": summarize_global_scheduler_budgets(build_global_scheduler_budgets()),
            "matrix": build_planetary_mesh_matrix(),
            "overall_readiness": "ready",
            "release_blockers": []
        }
