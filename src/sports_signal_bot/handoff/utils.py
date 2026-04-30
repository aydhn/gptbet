import uuid

def generate_handoff_id() -> str:
    return f"handoff_{uuid.uuid4().hex[:8]}"
