def format_endurance_output(data: dict) -> str:
    import json
    return json.dumps(data, indent=2)
