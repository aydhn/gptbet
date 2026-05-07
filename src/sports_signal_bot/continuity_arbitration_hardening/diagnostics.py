def check_release_blockers(report: dict) -> list:
    blockers = []

    # Check rails
    for rail in report.get("continuity_arbitration_rails", []):
        if rail["status"] not in ["rail_verified", "rail_caveated"]:
            blockers.append(f"Rail blocked: {rail['rail_id']}")

    # Check fabrics
    for fabric in report.get("scheduler_recovery_fabrics", []):
        if fabric["status"] not in ["fabric_verified", "fabric_caveated"]:
            blockers.append(f"Fabric blocked: {fabric['fabric_id']}")

    # Check meshes
    for mesh in report.get("archive_proof_meshes", []):
        if mesh["status"] not in ["mesh_verified", "mesh_caveated"]:
            blockers.append(f"Mesh broken: {mesh['mesh_id']}")

    # Check ledgers
    for ledger in report.get("worldwide_visibility_ledgers", []):
        if ledger["status"] not in ["ledger_verified", "ledger_caveated"]:
            blockers.append(f"Ledger blocked: {ledger['ledger_id']}")

    return blockers
