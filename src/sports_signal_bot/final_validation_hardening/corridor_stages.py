from pydantic import BaseModel

class ValidationStageFreshnessRecord(BaseModel):
    pass

class ValidationStageOwnerRecord(BaseModel):
    pass

class ValidationStageMismatchRecord(BaseModel):
    pass

class ValidationStageDriftRecord(BaseModel):
    pass

class ValidationStageFallbackRecord(BaseModel):
    pass

class ValidationStageHealthMarkerRecord(BaseModel):
    pass

def create_validation_checkpoint(checkpoint_id: str, family: str):
    pass

def detect_validation_stage_gaps(stage_id: str):
    pass

def diff_validation_stage_replay(stage_id: str):
    pass

def summarize_validation_stages(stages: list):
    pass
