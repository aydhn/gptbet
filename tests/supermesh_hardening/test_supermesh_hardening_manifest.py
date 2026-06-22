from src.sports_signal_bot.supermesh_hardening.manifests import (
    generate_supermesh_hardening_manifest,
    SupermeshManifestInputs
)


def test_generate_ready_manifest():
    inputs = SupermeshManifestInputs(
        supermesh_summary={"status": "supermesh_verified"},
        fabric_summary={"status": "fabric_verified"},
        pulse_summary={"status": "lane_verified"},
        observatory_summary={"status": "observatory_verified"},
        matrix_summary={"fully_compliant": True},
        budget_summary={"blockers": 0}
    )
    manifest = generate_supermesh_hardening_manifest(inputs)
    assert manifest["overall_readiness"] == "ready"


def test_generate_blocked_manifest():
    inputs = SupermeshManifestInputs(
        supermesh_summary={"status": "supermesh_blocked"},
        fabric_summary={"status": "fabric_verified"},
        pulse_summary={"status": "lane_verified"},
        observatory_summary={"status": "observatory_verified"},
        matrix_summary={"fully_compliant": True},
        budget_summary={"blockers": 0}
    )
    manifest = generate_supermesh_hardening_manifest(inputs)
    assert manifest["overall_readiness"] == "blocked"
