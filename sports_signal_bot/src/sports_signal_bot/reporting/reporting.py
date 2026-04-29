import json
from pathlib import Path

from sports_signal_bot.reporting.contracts import (ReportBundleRecord,
                                                   ReportingManifest)


class ReportingReporter:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write_json_bundle(self, bundle: ReportBundleRecord):
        path = self.output_dir / "report_bundle.json"
        with open(path, "w") as f:
            f.write(bundle.model_dump_json(indent=2))
        return path

    def write_markdown_summary(self, bundle: ReportBundleRecord):
        path = self.output_dir / "report_bundle.md"
        with open(path, "w") as f:
            f.write(
                f"# Report Bundle: {bundle.reporting_period.upper()} ({bundle.audience_profile})\n\n"
            )
            f.write(f"**Start**: {bundle.time_range_start}\n")
            f.write(f"**End**: {bundle.time_range_end}\n\n")

            f.write("## KPIs\n")
            for kpi in bundle.kpi_bundle.kpis:
                f.write(f"- {kpi.kpi_id}: {kpi.value} {kpi.unit}\n")

            f.write("\n## Sections\n")
            for sec in bundle.sections:
                f.write(f"### {sec.section_name}\n")
                f.write(f"{sec.narrative_summary}\n\n")

            if bundle.warnings_caveats:
                f.write("## Warnings\n")
                for w in bundle.warnings_caveats:
                    f.write(f"- {w}\n")
        return path

    def write_manifest(self, manifest: ReportingManifest):
        path = self.output_dir / "reporting_manifest.json"
        with open(path, "w") as f:
            f.write(manifest.model_dump_json(indent=2))
        return path

    def write_csv_extracts(self, bundle: ReportBundleRecord):
        # Basic implementation for CSV
        kpi_path = self.output_dir / "kpi_values.csv"
        with open(kpi_path, "w") as f:
            f.write("kpi_id,value,unit\n")
            for kpi in bundle.kpi_bundle.kpis:
                f.write(f"{kpi.kpi_id},{kpi.value},{kpi.unit}\n")
        return kpi_path
