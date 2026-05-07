from .base import SupermeshHardeningStrategy
from ..handoff_observatories import build_planetary_handoff_observatory, register_observatory_window
from ..contracts import HandoffObservatoryWindowRecord

class ObservatoryIntegrityFirstStrategy(SupermeshHardeningStrategy):
    name = "ObservatoryIntegrityFirstStrategy"

    def apply(self, integrator):
        obs = build_planetary_handoff_observatory("obs-integrity", "sovereignty_visibility_handoff_observatory")
        register_observatory_window(obs, HandoffObservatoryWindowRecord(window_id="w-integrity-1", window_family="sovereignty_owner_window"))
        integrator.add_observatory(obs)

        # Other elements bare minimum
        from ..bus_supermeshes import build_federation_bus_supermesh
        integrator.add_supermesh(build_federation_bus_supermesh("sm-integrity", "composite_federation_bus_supermesh"))

        from ..cadence_fabrics import build_scheduler_cadence_fabric
        integrator.add_fabric(build_scheduler_cadence_fabric("fab-integrity", "composite_scheduler_cadence_fabric"))

        from ..audit_pulse_lanes import build_global_audit_pulse_lane
        integrator.add_pulse_lane(build_global_audit_pulse_lane("pl-integrity", "composite_global_audit_pulse_lane"))
