import uuid
from sports_signal_bot.ecosystem_discovery.contracts import VerifierProtocolProfileRecord

def build_verifier_protocol_profile(profile_name: str) -> VerifierProtocolProfileRecord:
    return VerifierProtocolProfileRecord(
        protocol_profile_id=f"prof_{uuid.uuid4().hex[:8]}",
        profile_name=profile_name,
        supported_request_families=["base_request"],
        supported_response_families=["base_response"],
        supported_negotiation_modes=["strict"],
        supported_proof_formats=["json"],
        supported_redaction_profiles=["minimal"],
        supported_replay_modes=["local"]
    )

def negotiate_protocol_profile(offered: VerifierProtocolProfileRecord, required: VerifierProtocolProfileRecord) -> VerifierProtocolProfileRecord:
    # Build a common subset
    common_req = list(set(offered.supported_request_families) & set(required.supported_request_families))
    common_resp = list(set(offered.supported_response_families) & set(required.supported_response_families))
    common_proof = list(set(offered.supported_proof_formats) & set(required.supported_proof_formats))

    negotiated = build_verifier_protocol_profile(f"negotiated_{offered.profile_name}_{required.profile_name}")
    negotiated.supported_request_families = common_req
    negotiated.supported_response_families = common_resp
    negotiated.supported_proof_formats = common_proof

    if not common_req or not common_resp:
        negotiated.warnings.append("Negotiation resulted in empty required capabilities. Safe subset failed.")

    return negotiated

def restrict_protocol_to_safe_subset(profile: VerifierProtocolProfileRecord) -> VerifierProtocolProfileRecord:
    profile.supported_request_families = [req for req in profile.supported_request_families if req != "unsafe_extension"]
    return profile

def summarize_protocol_negotiation(profile: VerifierProtocolProfileRecord) -> dict:
    return {
        "profile_id": profile.protocol_profile_id,
        "valid": len(profile.supported_request_families) > 0,
        "warnings": profile.warnings
    }
