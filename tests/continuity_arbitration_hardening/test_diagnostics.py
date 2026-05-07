from src.sports_signal_bot.continuity_arbitration_hardening.diagnostics import check_release_blockers

def test_check_release_blockers():
    report = {
        "archive_proof_meshes": [
            {"mesh_id": "1", "status": "mesh_broken"}
        ]
    }
    blockers = check_release_blockers(report)
    assert len(blockers) == 1
    assert "Mesh broken: 1" in blockers[0]
