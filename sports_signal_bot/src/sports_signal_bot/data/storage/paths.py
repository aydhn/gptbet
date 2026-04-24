from pathlib import Path
from datetime import datetime
from sports_signal_bot.core.paths import get_data_dir
from sports_signal_bot.core.constants import SportType

def get_raw_storage_path(provider_name: str, sport: SportType, dataset_type: str, dt: datetime = None) -> Path:
    """e.g., data/raw/pinnacle/football/odds/2023-10-24/data.json"""
    base = get_data_dir() / "raw"
    date_str = (dt or datetime.now()).strftime("%Y-%m-%d")
    return base / provider_name / sport.value / dataset_type / date_str

def get_processed_storage_path(dataset_type: str, sport: SportType, ingest_id: str) -> Path:
    """e.g., data/processed/fixtures/football/ingest_123.json"""
    base = get_data_dir() / "processed"
    return base / dataset_type / sport.value

def get_manifest_storage_path() -> Path:
    return get_data_dir() / "processed" / "manifests"
