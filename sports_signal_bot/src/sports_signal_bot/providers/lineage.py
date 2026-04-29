from datetime import datetime
from typing import Any, Dict, List, Optional

from sports_signal_bot.providers.responses import ProviderLineageRecord


def generate_lineage_artifact(lineage: ProviderLineageRecord) -> Dict[str, Any]:
    return lineage.model_dump(mode="json")
