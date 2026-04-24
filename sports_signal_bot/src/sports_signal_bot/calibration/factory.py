from typing import Dict, Any, Optional
from sports_signal_bot.calibration.registry import CalibrationRegistry
from sports_signal_bot.calibration.base import BaseCalibrator

class CalibrationFactory:
    """Factory to instantiate calibrators."""

    @staticmethod
    def create(method_name: str, config: Optional[Dict[str, Any]] = None) -> BaseCalibrator:
        calibrator_cls = CalibrationRegistry.get(method_name)
        return calibrator_cls(config=config)
