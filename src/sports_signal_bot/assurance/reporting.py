from typing import List, Dict

def generate_assurance_summary(claims: List[Dict], envelopes: List[Dict]) -> Dict:
    return {
        "total_claims": len(claims),
        "total_envelopes": len(envelopes),
        "blocked_envelopes": len([e for e in envelopes if e.get('final_assurance_decision') == 'assurance_blocked'])
    }
