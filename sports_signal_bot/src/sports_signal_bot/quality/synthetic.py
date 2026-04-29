from typing import Dict, Any, List
import random
import hashlib

class SyntheticFixtureFactory:
    def __init__(self, seed: int = 42):
        self.seed = seed
        self._reset_random()

    def _reset_random(self):
        random.seed(self.seed)

    def create_event(self, event_id: str) -> Dict[str, Any]:
        self._reset_random() # Ensure determinism based on ID if needed, or just keep sequence
        # A simple hash-based determinism for properties
        h = int(hashlib.md5(event_id.encode()).hexdigest(), 16)
        return {
            "event_id": event_id,
            "sport": "soccer",
            "home_team": f"Home_{h % 100}",
            "away_team": f"Away_{h % 100}",
            "start_time": "2024-01-01T20:00:00Z"
        }

class ScenarioDataBuilder:
    def __init__(self, factory: SyntheticFixtureFactory):
        self.factory = factory

    def build_inference_scenario_data(self) -> Dict[str, Any]:
        return {
            "events": [self.factory.create_event("evt_1"), self.factory.create_event("evt_2")],
            "market": "match_odds",
            "signals": [{"event_id": "evt_1", "score": 0.8}, {"event_id": "evt_2", "score": 0.2}]
        }
