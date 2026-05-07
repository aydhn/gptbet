from .contracts import EndToEndValidationCorridorRecord, ValidationCorridorStageRecord

def build_end_to_end_validation_corridor(corridor_id: str, family: str) -> EndToEndValidationCorridorRecord:
    return EndToEndValidationCorridorRecord(
        validation_corridor_id=corridor_id,
        corridor_family=family,
        corridor_status="corridor_verified"
    )

def add_validation_corridor_stage(corridor: EndToEndValidationCorridorRecord, stage: ValidationCorridorStageRecord):
    corridor.stage_refs.append(stage.stage_id)

def verify_validation_corridor(corridor: EndToEndValidationCorridorRecord) -> bool:
    if "stale" in corridor.warnings:
        corridor.corridor_status = "corridor_blocked"
        return False
    return True

def replay_validation_corridor(corridor: EndToEndValidationCorridorRecord):
    pass

def summarize_validation_corridor(corridor: EndToEndValidationCorridorRecord) -> dict:
    return {"id": corridor.validation_corridor_id, "status": corridor.corridor_status}
