import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional

from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.release_management.contracts import ChannelStateRecord

logger = get_logger("ChannelStateManager")


class ChannelStateManager:
    def __init__(self, data_dir: str = "data/release"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.state_file_path = os.path.join(self.data_dir, "channel_states.json")
        self.states: Dict[str, ChannelStateRecord] = self._load_states()

    def _get_key(self, sport: str, market_type: str) -> str:
        return f"{sport}_{market_type}"

    def _load_states(self) -> Dict[str, ChannelStateRecord]:
        if not os.path.exists(self.state_file_path):
            return {}
        try:
            with open(self.state_file_path, "r") as f:
                data = json.load(f)
                return {k: ChannelStateRecord(**v) for k, v in data.items()}
        except Exception as e:
            logger.error(f"Error loading channel states: {e}")
            return {}

    def _save_states(self) -> None:
        try:
            with open(self.state_file_path, "w") as f:
                data = {
                    k: v.model_dump(mode="json")
                    for k, v in self.states.items()
                }
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving channel states: {e}")

    def get_active_channel_state(self, sport: str, market_type: str) -> ChannelStateRecord:
        key = self._get_key(sport, market_type)
        if key not in self.states:
            state = ChannelStateRecord(sport=sport, market_type=market_type)
            self.states[key] = state
            self._save_states()
        return self.states[key]

    def set_channel_state(self, state: ChannelStateRecord) -> None:
        key = self._get_key(state.sport, state.market_type)
        state.updated_at = datetime.now(timezone.utc)
        self.states[key] = state
        self._save_states()

    def promote_channel_pointer(
        self, sport: str, market_type: str, channel: str, chain_group_id: str
    ) -> None:
        state = self.get_active_channel_state(sport, market_type)
        if channel == "stable":
            state.previous_stable_chain_id = state.active_stable_chain_id
            state.active_stable_chain_id = chain_group_id
            state.last_known_good_chain_id = chain_group_id
        elif channel == "canary":
            state.active_canary_chain_id = chain_group_id
        elif channel == "candidate":
            if chain_group_id not in state.active_candidate_chains:
                state.active_candidate_chains.append(chain_group_id)
        self.set_channel_state(state)

    def freeze_channel(self, sport: str, market_type: str, reason: str) -> None:
        state = self.get_active_channel_state(sport, market_type)
        state.frozen_channel_flags["system"] = True
        self.set_channel_state(state)
        logger.warning(f"Froze channel for {sport} {market_type}: {reason}")

    def unfreeze_channel(self, sport: str, market_type: str) -> None:
        state = self.get_active_channel_state(sport, market_type)
        state.frozen_channel_flags.pop("system", None)
        self.set_channel_state(state)
        logger.info(f"Unfroze channel for {sport} {market_type}")

    def mark_artifact_quarantined(self, sport: str, market_type: str, artifact_id: str) -> None:
        state = self.get_active_channel_state(sport, market_type)
        if artifact_id not in state.quarantined_artifacts:
            state.quarantined_artifacts.append(artifact_id)
            self.set_channel_state(state)
            logger.warning(f"Quarantined artifact {artifact_id} for {sport} {market_type}")

    def is_quarantined(self, sport: str, market_type: str, artifact_id: str) -> bool:
        state = self.get_active_channel_state(sport, market_type)
        return artifact_id in state.quarantined_artifacts
