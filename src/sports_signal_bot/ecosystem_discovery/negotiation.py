from sports_signal_bot.ecosystem_discovery.contracts import VerifierProtocolProfileRecord

def enforce_protocol_negotiation_safety(profile: VerifierProtocolProfileRecord) -> bool:
    if "public_discovery_protocol" in profile.profile_name and "verifier" in profile.supported_request_families:
        return False
    return True

def downgrade_to_common_protocol_subset(offered: VerifierProtocolProfileRecord, local_policy: dict) -> VerifierProtocolProfileRecord:
    if not local_policy.get("allow_unverified_extensions", False):
        offered.supported_request_families = [f for f in offered.supported_request_families if f in local_policy.get("allowed_requests", [])]
    return offered

def prevent_profile_escalation(offered: VerifierProtocolProfileRecord, base: VerifierProtocolProfileRecord) -> bool:
    return set(offered.supported_request_families).issubset(set(base.supported_request_families))

def explain_auto_negotiation_restrictions(profile: VerifierProtocolProfileRecord) -> str:
    if profile.warnings:
        return f"Restricted due to: {', '.join(profile.warnings)}"
    return "Negotiated safely."
