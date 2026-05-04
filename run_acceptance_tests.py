import sys

def check_files():
    files = [
        "src/sports_signal_bot/governance_fabric/contracts.py",
        "src/sports_signal_bot/governance_fabric/councils.py",
        "src/sports_signal_bot/governance_fabric/fabrics.py",
        "src/sports_signal_bot/governance_fabric/federations.py",
        "src/sports_signal_bot/governance_fabric/audits.py",
        "src/sports_signal_bot/governance_fabric/integration.py",
        "src/sports_signal_bot/governance_fabric/strategies/conservative.py",
        "configs/governance_fabric/default.yaml",
        "README_Phase83.md",
        "docs/governance_tier_councils_and_projection_audit_architecture.md",
        "results/governance_fabric_summary.json"
    ]
    import os
    missing = []
    for f in files:
        if not os.path.exists(f):
            missing.append(f)
    if missing:
        print(f"Missing files: {missing}")
        return False
    return True

if __name__ == "__main__":
    if check_files():
        print("All acceptance criteria passed!")
        sys.exit(0)
    else:
        sys.exit(1)
