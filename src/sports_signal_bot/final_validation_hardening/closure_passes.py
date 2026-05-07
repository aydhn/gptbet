from pydantic import BaseModel

class ReplayClosureFreshnessRecord(BaseModel):
    pass

class ReplayClosureLineageRecord(BaseModel):
    pass

class ReplayClosureMismatchRecord(BaseModel):
    pass

class ReplayClosureHealthMarkerRecord(BaseModel):
    pass

class ReplayClosureContinuityRecord(BaseModel):
    pass

class ReplayClosurePrecedenceRecord(BaseModel):
    pass

def validate_replay_closure_passes(compiler_id: str):
    pass

def classify_replay_closure_decision(decision_id: str):
    pass

def detect_replay_closure_gaps(compiler_id: str):
    pass

def summarize_replay_closure_passes(passes: list):
    pass
