from sports_signal_bot.adjudication.contracts import HumanCorrectionInput
from sports_signal_bot.adjudication.resolutions import HumanCorrectionBuilder


def test_correction_validation():
    input_req = HumanCorrectionInput(
        case_id="c1",
        corrected_field="start_time",
        old_value="2023-01-01T10:00:00Z",
        new_value="2023-01-01T12:00:00Z",
        resolution_basis="official source",
        scope="single_entity",
        confidence=0.9,
        propagate_to_memory=True,
        evidence_refs=["evidence_1"],
    )
    correction = HumanCorrectionBuilder.build_human_correction(input_req)

    assert HumanCorrectionBuilder.validate_correction_payload(correction)
    assert HumanCorrectionBuilder.classify_correction_risk(correction) == "low"

    # Missing evidence for memory propagation
    correction.evidence_refs = []
    assert not HumanCorrectionBuilder.validate_correction_payload(correction)
