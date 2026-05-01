from typing import Dict, Any, List

def compute_verifier_experience_readiness(components: Dict[str, bool]) -> str:
    ready_count = sum(1 for v in components.values() if v)
    total_count = len(components)
    if total_count == 0:
        return "internal_preview_only"

    ratio = ready_count / total_count

    if ratio == 1.0:
        return "public_style_verification_experience_ready"
    elif ratio >= 0.8:
        return "external_dashboard_ready"
    elif ratio >= 0.5:
        return "verifier_portal_ready"
    elif ratio >= 0.2:
        return "controlled_external_preview_ready"
    else:
        return "internal_preview_only"

def score_portal_maturity(components: Dict[str, bool]) -> int:
    return int(sum(1 for v in components.values() if v) / max(len(components), 1) * 100)

def collect_portal_blockers(components: Dict[str, bool]) -> List[str]:
    return [k for k, v in components.items() if not v]

def summarize_upgrade_requirements(components: Dict[str, bool]) -> Dict[str, Any]:
    return {
        "current_maturity": score_portal_maturity(components),
        "blockers": collect_portal_blockers(components)
    }
