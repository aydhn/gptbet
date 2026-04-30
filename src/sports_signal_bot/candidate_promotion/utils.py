def generate_id(prefix: str = "id") -> str:
    import uuid
    return f"{prefix}_{str(uuid.uuid4())[:8]}"
