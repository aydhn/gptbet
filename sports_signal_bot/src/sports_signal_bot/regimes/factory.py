from typing import List

from sports_signal_bot.regimes.definitions import (
    RuleBasedEventRegimeClassifier, RuleBasedPeriodRegimeClassifier)
from sports_signal_bot.regimes.registry import RegimeRegistry
from sports_signal_bot.regimes.thresholds import (RegimeConfig,
                                                  RegimeThresholdsConfig)


class RegimeFactory:
    def __init__(
        self, thresholds_config: RegimeThresholdsConfig, regime_config: RegimeConfig
    ):
        self.thresholds_config = thresholds_config
        self.regime_config = regime_config

    def create_event_classifiers(self) -> List[RuleBasedEventRegimeClassifier]:
        classifiers = []
        for family, cls in RegimeRegistry.get_event_classifiers().items():
            if family in self.regime_config.enabled_regime_families:
                classifiers.append(cls(self.thresholds_config))
        return classifiers

    def create_period_classifiers(self) -> List[RuleBasedPeriodRegimeClassifier]:
        classifiers = []
        for family, cls in RegimeRegistry.get_period_classifiers().items():
            if family in self.regime_config.enabled_regime_families:
                classifiers.append(cls(self.thresholds_config))
        return classifiers
