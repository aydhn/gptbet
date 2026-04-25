from typing import Any, Dict, List

from sports_signal_bot.regimes.contracts import (EventRegimeRecord,
                                                 PeriodRegimeRecord,
                                                 RegimeAssignmentResult,
                                                 RegimeWarningRecord)
from sports_signal_bot.regimes.factory import RegimeFactory
from sports_signal_bot.regimes.inputs import (EventRegimeInputs,
                                              PeriodRegimeInputs)


class RegimeRunner:
    def __init__(self, factory: RegimeFactory):
        self.event_classifiers = factory.create_event_classifiers()
        self.period_classifiers = factory.create_period_classifiers()

    def assign_event_regimes(self, inputs: EventRegimeInputs) -> RegimeAssignmentResult:
        records: List[EventRegimeRecord] = []
        warnings: List[RegimeWarningRecord] = []

        for classifier in self.event_classifiers:
            try:
                assigned = classifier.assign_event_regimes(inputs)
                records.extend(assigned)
            except Exception as e:
                warnings.append(
                    RegimeWarningRecord(
                        warning_type="event_classification_error",
                        message=str(e),
                        context={"classifier": classifier.__class__.__name__},
                    )
                )

        return RegimeAssignmentResult(event_regimes=records, warnings=warnings)

    def assign_period_regimes(
        self, inputs: PeriodRegimeInputs
    ) -> RegimeAssignmentResult:
        records: List[PeriodRegimeRecord] = []
        warnings: List[RegimeWarningRecord] = []

        for classifier in self.period_classifiers:
            try:
                assigned = classifier.assign_period_regimes(inputs)
                records.extend(assigned)
            except Exception as e:
                warnings.append(
                    RegimeWarningRecord(
                        warning_type="period_classification_error",
                        message=str(e),
                        context={"classifier": classifier.__class__.__name__},
                    )
                )

        return RegimeAssignmentResult(period_regimes=records, warnings=warnings)
