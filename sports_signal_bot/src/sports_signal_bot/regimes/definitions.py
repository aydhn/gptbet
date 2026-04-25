from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from sports_signal_bot.regimes.contracts import (EventRegimeRecord,
                                                 PeriodRegimeRecord,
                                                 RegimeDefinition)
from sports_signal_bot.regimes.inputs import (EventRegimeInputs,
                                              PeriodRegimeInputs)
from sports_signal_bot.regimes.thresholds import RegimeThresholdsConfig


class BaseRegimeClassifier(ABC):
    def __init__(self, config: RegimeThresholdsConfig):
        self.config = config

    @abstractmethod
    def describe(self) -> RegimeDefinition:
        pass

    def validate_event_inputs(self, inputs: EventRegimeInputs) -> List[str]:
        req_inputs = self.describe().required_inputs
        warnings = []
        for req in req_inputs:
            if req not in inputs.features and not hasattr(inputs, req):
                warnings.append(f"Missing required input: {req}")
        return warnings

    def validate_period_inputs(self, inputs: PeriodRegimeInputs) -> List[str]:
        return []


class RuleBasedEventRegimeClassifier(BaseRegimeClassifier):
    @abstractmethod
    def assign_event_regimes(
        self, inputs: EventRegimeInputs
    ) -> List[EventRegimeRecord]:
        pass


class RuleBasedPeriodRegimeClassifier(BaseRegimeClassifier):
    @abstractmethod
    def assign_period_regimes(
        self, inputs: PeriodRegimeInputs
    ) -> List[PeriodRegimeRecord]:
        pass
