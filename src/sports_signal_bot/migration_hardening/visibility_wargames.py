from pydantic import Field
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from .contracts import WarGameFamily, WarGameStatus

class WarGameScenarioRecord(BaseModel):
    scenario_id: str
    description: str

class WarGameSignalRecord(BaseModel):
    signal_id: str
    is_suppressed: bool = False

class WarGameVisibilitySurfaceRecord(BaseModel):
    surface_id: str
    maintains_no_safe: bool = True
    maintains_sovereignty: bool = True

class WarGameLossRecord(BaseModel):
    loss_id: str
    description: str
    is_critical: bool = False

class WarGameWarningRecord(BaseModel):
    warning_id: str
    description: str

class GovernanceVisibilityWarGameRecord(BaseModel):
    war_game_id: str
    war_game_family: WarGameFamily
    scenario_refs: List[WarGameScenarioRecord] = Field(default_factory=list)
    signal_refs: List[WarGameSignalRecord] = Field(default_factory=list)
    visibility_surface_refs: List[WarGameVisibilitySurfaceRecord] = Field(default_factory=list)
    loss_refs: List[WarGameLossRecord] = Field(default_factory=list)
    war_game_status: WarGameStatus = WarGameStatus.visibility_preserved
    warnings: List[WarGameWarningRecord] = Field(default_factory=list)

def build_governance_visibility_war_game(game_id: str, family: WarGameFamily) -> GovernanceVisibilityWarGameRecord:
    return GovernanceVisibilityWarGameRecord(
        war_game_id=game_id,
        war_game_family=family
    )

def inject_visibility_stress(game: GovernanceVisibilityWarGameRecord, surface: WarGameVisibilitySurfaceRecord, signal: WarGameSignalRecord) -> None:
    game.visibility_surface_refs.append(surface)
    game.signal_refs.append(signal)

    if signal.is_suppressed:
         game.warnings.append(WarGameWarningRecord(
             warning_id=f"warn_suppressed_{signal.signal_id}",
             description="Signal was suppressed under stress."
         ))

    if not surface.maintains_no_safe:
         game.loss_refs.append(WarGameLossRecord(
             loss_id=f"loss_no_safe_{surface.surface_id}",
             description="No-safe visibility lost under stress.",
             is_critical=True
         ))

    if not surface.maintains_sovereignty:
         game.loss_refs.append(WarGameLossRecord(
             loss_id=f"loss_sovereignty_{surface.surface_id}",
             description="Sovereignty visibility lost under stress.",
             is_critical=True
         ))

def detect_visibility_losses(game: GovernanceVisibilityWarGameRecord) -> None:
    if game.loss_refs:
        game.war_game_status = WarGameStatus.visibility_lost
    elif game.warnings:
        game.war_game_status = WarGameStatus.visibility_caveated
    else:
        game.war_game_status = WarGameStatus.visibility_preserved

def summarize_visibility_war_game(game: GovernanceVisibilityWarGameRecord) -> Dict:
    return {
        "war_game_id": game.war_game_id,
        "family": game.war_game_family.value,
        "status": game.war_game_status.value,
        "loss_count": len(game.loss_refs),
        "critical_losses": sum(1 for l in game.loss_refs if l.is_critical),
        "warnings_count": len(game.warnings)
    }
