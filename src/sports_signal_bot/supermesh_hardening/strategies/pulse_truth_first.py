from .base import SupermeshHardeningStrategy
from ..audit_pulse_lanes import build_global_audit_pulse_lane, emit_audit_pulse
from ..contracts import AuditPulseRecord

class PulseTruthFirstStrategy(SupermeshHardeningStrategy):
    name = "PulseTruthFirstStrategy"

    def apply(self, integrator):
        pulse_lane = build_global_audit_pulse_lane("pl-truth", "executive_visibility_pulse_lane")
        emit_audit_pulse(pulse_lane, AuditPulseRecord(pulse_id="p-truth-1", pulse_family="executive_visibility_pulse"))
        integrator.add_pulse_lane(pulse_lane)

        # Other elements bare minimum
        from ..bus_supermeshes import build_federation_bus_supermesh
        integrator.add_supermesh(build_federation_bus_supermesh("sm-truth", "composite_federation_bus_supermesh"))

        from ..cadence_fabrics import build_scheduler_cadence_fabric
        integrator.add_fabric(build_scheduler_cadence_fabric("fab-truth", "composite_scheduler_cadence_fabric"))

        from ..handoff_observatories import build_planetary_handoff_observatory
        integrator.add_observatory(build_planetary_handoff_observatory("obs-truth", "composite_planetary_handoff_observatory"))
