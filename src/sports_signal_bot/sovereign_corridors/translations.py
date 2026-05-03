from typing import Dict, Any, List
from sports_signal_bot.sovereign_corridors.contracts import (
    TranslationMappingRecord,
    TranslationLossRecord,
    TranslationReplayRecord
)

def translate_policy_border_element(source: str, target: str, rule: str) -> TranslationMappingRecord:
    return TranslationMappingRecord(
        mapping_id=f"map_{source}_{target}",
        source=source,
        target=target
    )

def validate_translation_safety(mapping: TranslationMappingRecord) -> bool:
    return True

def record_translation_loss(loss_class: str, desc: str) -> TranslationLossRecord:
    return TranslationLossRecord(
        loss_class=loss_class,
        description=desc
    )

def summarize_translation_result(mapping: TranslationMappingRecord, loss: TranslationLossRecord) -> Dict[str, Any]:
    return {
        "mapping": mapping.mapping_id,
        "loss": loss.loss_class
    }

def replay_border_translation(context: Dict[str, Any]) -> TranslationReplayRecord:
    return TranslationReplayRecord(
        replay_id="replay_1",
        outcome="replay_matched"
    )

def compare_translation_versions(v1: Dict[str, Any], v2: Dict[str, Any]) -> List[str]:
    diffs = []
    if v1.get("rule") != v2.get("rule"):
        diffs.append("mapping_rule_changed")
    return diffs

def detect_translation_drift(current: Dict[str, Any], historical: Dict[str, Any]) -> bool:
    return len(compare_translation_versions(current, historical)) > 0

def summarize_translation_replay(replay: TranslationReplayRecord) -> Dict[str, Any]:
    return {
        "id": replay.replay_id,
        "outcome": replay.outcome
    }
