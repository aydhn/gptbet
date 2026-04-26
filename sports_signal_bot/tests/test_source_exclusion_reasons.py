from sports_signal_bot.source_selection.contracts import (
    SourceEligibilityRecord, SourceExclusionReasonRecord)


def test_exclusion_reason_record():
    ex = SourceExclusionReasonRecord(reason_code="test_reason", details="Some details")
    assert ex.reason_code == "test_reason"
    assert ex.details == "Some details"

    rec = SourceEligibilityRecord(
        event_id="e", sport="s", market_type="m", source_name="s", source_family="f"
    )
    rec.exclusion_reasons.append(ex)
    assert len(rec.exclusion_reasons) == 1
