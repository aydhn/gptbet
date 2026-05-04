from sports_signal_bot.capability_negotiation.portable_specs import build_portable_spec_bundle, verify_portable_spec_bundle
from sports_signal_bot.capability_negotiation.contracts import SpecPortabilityClass

def test_portable_spec_bundle():
    specs = [
        {"spec_id": "spec1", "internal_only": False},
        {"spec_id": "spec2", "internal_only": True},
        {"spec_id": "spec3", "internal_only": False, "requires_review": True}
    ]
    assertions = [{"id": "a1", "semantics": "test"}]

    bundle = build_portable_spec_bundle("test_family", specs, assertions, "redacted")

    assert "spec2" not in bundle.included_specs
    assert bundle.portable_profile == SpecPortabilityClass.review_only_portable
    assert verify_portable_spec_bundle(bundle) is True
