from pathlib import Path
import json
from typing import Dict, Any, List
from .contracts import TelegramDispatchManifest

class DispatchReporter:
    def __init__(self, manifest: TelegramDispatchManifest):
        self.manifest = manifest

    def build_summary_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.manifest.run_id,
            "timestamp": self.manifest.timestamp.isoformat(),
            "metrics": {
                "total_rendered": self.manifest.total_messages_rendered,
                "total_sent": self.manifest.total_messages_sent,
                "suppressed": self.manifest.suppressed_count,
                "retries": self.manifest.retry_count,
                "final_failures": self.manifest.final_failures_count
            },
            "channel_breakdown": self.manifest.channel_breakdown,
            "severity_breakdown": self.manifest.severity_breakdown
        }

    def write_summary(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.build_summary_dict(), f, indent=2)

    def get_cli_output(self) -> str:
        s = self.build_summary_dict()
        m = s["metrics"]
        lines = [
            f"=== Dispatch Summary for {s['run_id']} ===",
            f"Messages Rendered: {m['total_rendered']}",
            f"Messages Sent:     {m['total_sent']}",
            f"Suppressed:        {m['suppressed']}",
            f"Failures:          {m['final_failures']}",
            f"Retries:           {m['retries']}",
            "",
            "Channels:"
        ]
        for c, count in s["channel_breakdown"].items():
            lines.append(f"  - {c}: {count}")

        return "\n".join(lines)
