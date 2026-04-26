import csv
import json
from pathlib import Path

from .contracts import SourceSelectionManifest


class SelectionReporter:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_reports(self, manifest: SourceSelectionManifest):
        run_dir = self.output_dir / manifest.run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        # Eligibility CSV
        eligibility_path = run_dir / f"source_eligibility_{manifest.event_id}.csv"
        with open(eligibility_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "event_id",
                    "source_name",
                    "source_family",
                    "is_eligible",
                    "trust_score",
                    "policy",
                    "warnings",
                ]
            )
            for d in manifest.decisions:
                ts = (
                    d.eligibility_record.trust_score.total_trust_score
                    if d.eligibility_record.trust_score
                    else 0.0
                )
                writer.writerow(
                    [
                        manifest.event_id,
                        d.source_name,
                        d.eligibility_record.source_family,
                        d.is_selected,
                        f"{ts:.3f}",
                        d.eligibility_record.policy_name,
                        "|".join(d.eligibility_record.warnings),
                    ]
                )

        # Trust Scores JSON
        trust_scores_path = run_dir / f"source_trust_scores_{manifest.event_id}.json"
        scores = {}
        for d in manifest.decisions:
            if d.eligibility_record.trust_score:
                scores[d.source_name] = d.eligibility_record.trust_score.model_dump()
        with open(trust_scores_path, "w") as f:
            json.dump(scores, f, indent=2)

        # Exclusions CSV
        exclusions_path = run_dir / f"exclusion_reasons_{manifest.event_id}.csv"
        with open(exclusions_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["event_id", "source_name", "reason_code", "details"])
            for d in manifest.decisions:
                if not d.is_selected:
                    for ex in d.eligibility_record.exclusion_reasons:
                        writer.writerow(
                            [
                                manifest.event_id,
                                d.source_name,
                                ex.reason_code,
                                ex.details,
                            ]
                        )
