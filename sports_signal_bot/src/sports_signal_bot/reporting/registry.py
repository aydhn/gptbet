from pathlib import Path
from typing import Dict, List, Optional

import yaml

from sports_signal_bot.reporting.contracts import (AudienceProfileRecord,
                                                   KPIDefinitionRecord)


class MetricRegistry:
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.kpis: Dict[str, KPIDefinitionRecord] = {}
        self.audiences: Dict[str, AudienceProfileRecord] = {}
        self.enabled_families: List[str] = []
        self._load_configs()

    def _load_configs(self):
        kpi_file = self.config_dir / "kpis.yaml"
        if kpi_file.exists():
            with open(kpi_file, "r") as f:
                data = yaml.safe_load(f)
                self.enabled_families = data.get("enabled_metric_families", [])
                for kpi_data in data.get("kpi_definitions", []):
                    # Map yaml 'id' to pydantic 'kpi_id'
                    kpi_data["kpi_id"] = kpi_data.pop("id")
                    kpi = KPIDefinitionRecord(**kpi_data)
                    self.kpis[kpi.kpi_id] = kpi

        audience_file = self.config_dir / "audiences.yaml"
        if audience_file.exists():
            with open(audience_file, "r") as f:
                data = yaml.safe_load(f)
                for audience_id, aud_data in data.get("profiles", {}).items():
                    aud = AudienceProfileRecord(**aud_data)
                    self.audiences[audience_id] = aud

    def get_kpi(self, kpi_id: str) -> Optional[KPIDefinitionRecord]:
        return self.kpis.get(kpi_id)

    def list_kpis(self) -> List[KPIDefinitionRecord]:
        return list(self.kpis.values())

    def get_audience(self, audience_id: str) -> Optional[AudienceProfileRecord]:
        return self.audiences.get(audience_id)
