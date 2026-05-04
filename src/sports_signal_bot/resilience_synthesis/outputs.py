from .contracts import SynthesisOutputRecord

def compute_synthesis_band(score: float, penalties: list, ceilings: list, sovereignty_passed: bool) -> str:
    if not sovereignty_passed:
        return "critically_fragile"
    if ceilings:
        return ceilings[0].max_band # simplified
    if score > 0.8:
        return "strong_bounded_resilience"
    if score > 0.5:
        return "stabilized_resilience_with_caps"
    return "review_only_resilience"

def explain_synthesized_resilience_score(output: SynthesisOutputRecord) -> str:
    return f"Band: {output.band}. Caveats: {len(output.preserved_caveat_refs)}. No Safe Hint: {output.no_safe_recovery_hint_preserved}"

def enforce_sovereignty_across_phase89(band: str, local_deny: bool) -> str:
    if local_deny:
        return "critically_fragile"
    return band

def preserve_local_deny_in_synthesized_outputs(band: str, local_deny: bool) -> str:
    if local_deny:
        return "critically_fragile"
    return band

def explain_sovereignty_phase89_effects(local_deny: bool) -> str:
    if local_deny:
         return "Local sovereignty DENIED the action. Score synthesis is heavily bounded."
    return "Local sovereignty PERMITTED the action."
