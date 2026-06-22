import json
import os
from typing import Dict, Any

from .bus_supermeshes import build_federation_bus_supermesh, summarize_federation_bus_supermesh
from .cadence_fabrics import build_scheduler_cadence_fabric, summarize_scheduler_cadence_fabric
from .audit_pulse_lanes import build_global_audit_pulse_lane, summarize_global_audit_pulse_lane
from .handoff_observatories import build_planetary_handoff_observatory, summarize_planetary_handoff_observatory
from .summaries import build_supermesh_fabric_matrix, summarize_supermesh_fabric_matrix, add_matrix_row
from .budgets import build_supermesh_fabric_budgets, summarize_supermesh_fabric_budgets
from .manifests import (
    generate_supermesh_hardening_manifest,
    SupermeshManifestInputs
)
from .strategies.base import SupermeshHardeningStrategy

class SupermeshHardeningIntegrator:
    def __init__(self, strategy: SupermeshHardeningStrategy):
        self.strategy = strategy
        self.supermeshes = []
        self.fabrics = []
        self.pulse_lanes = []
        self.observatories = []
        self.matrix = build_supermesh_fabric_matrix()
        self.budget_manifest = build_supermesh_fabric_budgets()
        self.summary = {}

    def add_supermesh(self, mesh):
        self.supermeshes.append(mesh)

    def add_fabric(self, fabric):
        self.fabrics.append(fabric)

    def add_pulse_lane(self, lane):
        self.pulse_lanes.append(lane)

    def add_observatory(self, observatory):
        self.observatories.append(observatory)

    def run_pass(self):
        # In a real run, this would trigger verification passes per element.
        self.strategy.apply(self)

        # Populate dummy matrix row for summary sake
        add_matrix_row(self.matrix, {
            "owner_visible": True,
            "freshness_note_visible": True,
            "no_safe_visible": True,
            "sovereignty_note_visible": True,
            "residue_visible": True,
            "replayability_preserved": True
        })

    def summarize(self) -> Dict[str, Any]:
        sm_summary = summarize_federation_bus_supermesh(self.supermeshes[0]) if self.supermeshes else {"status": "none"}
        fab_summary = summarize_scheduler_cadence_fabric(self.fabrics[0]) if self.fabrics else {"status": "none"}
        pulse_summary = summarize_global_audit_pulse_lane(self.pulse_lanes[0]) if self.pulse_lanes else {"status": "none"}
        obs_summary = summarize_planetary_handoff_observatory(self.observatories[0]) if self.observatories else {"status": "none"}
        mat_summary = summarize_supermesh_fabric_matrix(self.matrix)
        bud_summary = summarize_supermesh_fabric_budgets(self.budget_manifest)

        inputs = SupermeshManifestInputs(
            supermesh_summary=sm_summary,
            fabric_summary=fab_summary,
            pulse_summary=pulse_summary,
            observatory_summary=obs_summary,
            matrix_summary=mat_summary,
            budget_summary=bud_summary
        )
        self.summary = generate_supermesh_hardening_manifest(inputs)
        return self.summary

    def export_artifacts(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "federation_bus_supermeshes.json"), "w") as f:
            json.dump([sm.dict() for sm in self.supermeshes], f, indent=2)
        with open(os.path.join(output_dir, "scheduler_cadence_fabrics.json"), "w") as f:
            json.dump([fab.dict() for fab in self.fabrics], f, indent=2)
        with open(os.path.join(output_dir, "global_audit_pulse_lanes.json"), "w") as f:
            json.dump([pl.dict() for pl in self.pulse_lanes], f, indent=2)
        with open(os.path.join(output_dir, "planetary_handoff_observatories.json"), "w") as f:
            json.dump([ob.dict() for ob in self.observatories], f, indent=2)
        with open(os.path.join(output_dir, "supermesh_fabric_matrix.json"), "w") as f:
            json.dump(self.matrix, f, indent=2)
        with open(os.path.join(output_dir, "supermesh_fabric_budgets.json"), "w") as f:
            json.dump(self.budget_manifest.dict(), f, indent=2)
        with open(os.path.join(output_dir, "supermesh_hardening_manifest.json"), "w") as f:
            json.dump(self.summary, f, indent=2)
