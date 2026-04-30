import json

def summarize_staged_channel_state(active_records: list) -> dict:
    summary = {
        "active_candidates": len(active_records),
        "by_channel": {},
        "stage_distribution": {}
    }
    for record in active_records:
        ch = record.get("channel", "unknown")
        st = record.get("stage", "unknown")
        summary["by_channel"][ch] = summary["by_channel"].get(ch, 0) + 1
        summary["stage_distribution"][st] = summary["stage_distribution"].get(st, 0) + 1
    return summary

def generate_manifest(records: list, output_path: str):
    with open(output_path, "w") as f:
        json.dump(records, f, indent=2)
