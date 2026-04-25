from typing import Dict, Type

from sports_signal_bot.regimes.definitions import (
    RuleBasedEventRegimeClassifier, RuleBasedPeriodRegimeClassifier)


class RegimeRegistry:
    _event_classifiers: Dict[str, Type[RuleBasedEventRegimeClassifier]] = {}
    _period_classifiers: Dict[str, Type[RuleBasedPeriodRegimeClassifier]] = {}

    @classmethod
    def register_event_classifier(cls, family: str):
        def decorator(classifier_cls: Type[RuleBasedEventRegimeClassifier]):
            cls._event_classifiers[family] = classifier_cls
            return classifier_cls

        return decorator

    @classmethod
    def register_period_classifier(cls, family: str):
        def decorator(classifier_cls: Type[RuleBasedPeriodRegimeClassifier]):
            cls._period_classifiers[family] = classifier_cls
            return classifier_cls

        return decorator

    @classmethod
    def get_event_classifiers(cls) -> Dict[str, Type[RuleBasedEventRegimeClassifier]]:
        return cls._event_classifiers

    @classmethod
    def get_period_classifiers(cls) -> Dict[str, Type[RuleBasedPeriodRegimeClassifier]]:
        return cls._period_classifiers
