# utility functions for policy as code
def format_policy_decision(decision):
    return f"Status: {decision.decision_status.value}, Blockers: {decision.blockers}"
