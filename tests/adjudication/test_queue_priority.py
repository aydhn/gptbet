import pytest

from sports_signal_bot.adjudication.cases import AdjudicationCaseBuilder
from sports_signal_bot.adjudication.contracts import (
    AdjudicationQueuePriority, AdjudicationSeverity)


def test_assign_case_priority():
    assert (
        AdjudicationCaseBuilder.assign_case_priority(AdjudicationSeverity.critical)
        == AdjudicationQueuePriority.urgent
    )
    assert (
        AdjudicationCaseBuilder.assign_case_priority(AdjudicationSeverity.high)
        == AdjudicationQueuePriority.high
    )
    assert (
        AdjudicationCaseBuilder.assign_case_priority(AdjudicationSeverity.medium)
        == AdjudicationQueuePriority.normal
    )
    assert (
        AdjudicationCaseBuilder.assign_case_priority(AdjudicationSeverity.low)
        == AdjudicationQueuePriority.low
    )
