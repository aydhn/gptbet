from typing import Dict, Type

from sports_signal_bot.calibration.base import BaseCalibrator


class CalibrationRegistry:
    """Registry for calibration methods."""

    _registry: Dict[str, Type[BaseCalibrator]] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(calibrator_cls: Type[BaseCalibrator]):
            cls._registry[name] = calibrator_cls
            return calibrator_cls

        return decorator

    @classmethod
    def get(cls, name: str) -> Type[BaseCalibrator]:
        if name not in cls._registry:
            raise ValueError(
                f"Calibrator '{name}' not found in registry. Available: {list(cls._registry.keys())}"
            )
        return cls._registry[name]

    @classmethod
    def list_available(cls) -> list[str]:
        return list(cls._registry.keys())
