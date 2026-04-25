import datetime
import json
import uuid

from sports_signal_bot.research.artifacts import ResearchArtifactManager
from sports_signal_bot.research.contracts import ResearchScenario
from sports_signal_bot.research.manifests import build_research_manifest
from sports_signal_bot.research.period_runner import PeriodRunner
from sports_signal_bot.research.planner import WalkForwardPlanner
from sports_signal_bot.research.reporting import TimeSliceReporter


class ResearchRunner:
    """Orchestrates the entire research run."""

    def __init__(self, scenario: ResearchScenario):
        self.scenario = scenario
        self.run_id = f"research_{datetime.datetime.now().strftime('%Y%md%H%M%S')}_{uuid.uuid4().hex[:6]}"

    def run(self) -> str:
        """Executes the research scenario."""

        planner = WalkForwardPlanner(self.scenario)
        plan = planner.generate_plan()

        period_runner = PeriodRunner(self.scenario)
        artifact_manager = ResearchArtifactManager(self.run_id)
        reporter = TimeSliceReporter()

        period_records = []

        for window in plan.periods:
            # 1. Run period
            record = period_runner.run_period(window)
            period_records.append(record)

            # 2. Save period artifact
            artifact_manager.save_period_artifact(
                window.period_id, "period_record", json.loads(record.model_dump_json())
            )

        # 3. Generate summary report
        summary = reporter.generate_report(self.scenario.scenario_id, period_records)
        summary_path = artifact_manager.save_time_slice_summary(summary)

        # 4. Generate manifest
        paths = {"time_slice_summary": summary_path}
        manifest = build_research_manifest(
            self.run_id,
            self.scenario,
            period_records,
            paths,
            self.scenario.model_dump(),  # Config snapshot
        )

        manifest_path = artifact_manager.save_manifest(manifest)

        return manifest_path
