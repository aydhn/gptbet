from .claims import create_claim
from .attestations import build_assurance_attestation
from .bundles import build_proof_carrying_bundle
from .envelopes import build_promotion_envelope
from .strategies.balanced_proof_carrying import BalancedProofCarryingStrategy
from .contracts import ClaimFamily, SupportStrength, AttestationIssuerFamily

def run_assurance_pipeline_for_target(target_ref: str):
    strategy = BalancedProofCarryingStrategy()
    required_families = strategy.get_required_claim_families()

    claims = [
        create_claim(f"clm_{target_ref}_pol", ClaimFamily.policy_conformance_claim, target_ref, "Policy conforms", SupportStrength.high),
        create_claim(f"clm_{target_ref}_int", ClaimFamily.integrity_chain_claim, target_ref, "Integrity verified", SupportStrength.high),
        create_claim(f"clm_{target_ref}_tr", ClaimFamily.transparency_publication_claim, target_ref, "Inclusion proofs", SupportStrength.medium),
        create_claim(f"clm_{target_ref}_e2e", ClaimFamily.e2e_promotion_claim, target_ref, "E2E gates passed", SupportStrength.high, dependencies=[f"clm_{target_ref}_pol"])
    ]

    attestations = [
        build_assurance_attestation(AttestationIssuerFamily.conformance_runner_attester, target_ref, [claims[0].claim_id]),
        build_assurance_attestation(AttestationIssuerFamily.integrity_verifier_attester, target_ref, [claims[1].claim_id]),
    ]

    bundle = build_proof_carrying_bundle(target_ref, claims, [a.attestation_id for a in attestations])
    envelope = build_promotion_envelope(target_ref, bundle, claims, [f.value for f in required_families])

    passed, reason = strategy.evaluate_envelope(envelope, claims)

    return {
        "target": target_ref,
        "claims": [c.model_dump() for c in claims],
        "attestations": [a.model_dump() for a in attestations],
        "bundle": bundle.model_dump(),
        "envelope": envelope.model_dump(),
        "evaluation_passed": passed,
        "evaluation_reason": reason
    }
