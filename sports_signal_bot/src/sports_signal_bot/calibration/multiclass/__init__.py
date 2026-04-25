from .identity import MulticlassIdentityCalibrator
from .temperature_placeholder import TemperatureScalingPlaceholder
from .wrapper import MulticlassWrapperCalibrator

__all__ = [
    "MulticlassWrapperCalibrator",
    "MulticlassIdentityCalibrator",
    "TemperatureScalingPlaceholder",
]
