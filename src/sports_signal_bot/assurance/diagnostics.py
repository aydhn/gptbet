from typing import Dict

def diagnose_envelope_blocker(envelope: Dict) -> str:
    if envelope.get("blocked_claims"):
        return f"Blocked claims: {', '.join(envelope['blocked_claims'])}"
    return "No obvious blockers."
