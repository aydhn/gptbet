import uuid
from datetime import datetime
from pathlib import Path
from typing import List

from sports_signal_bot.backtest.contracts import (
    BacktestDecisionRecord,
    BacktestRunManifest,
    ReplayWindowDefinition,
)
from sports_signal_bot.backtest.execution import ExecutionPolicy
from sports_signal_bot.backtest.inputs import BacktestInputBuilder
from sports_signal_bot.backtest.ledger import LedgerWriter
from sports_signal_bot.backtest.periods import PeriodSummarizer
from sports_signal_bot.backtest.replay import ChronologicalReplayEngine, ReplayPlanner
from sports_signal_bot.backtest.reporting import BacktestReporter
from sports_signal_bot.backtest.settlement import SettlementEngine
from sports_signal_bot.backtest.summaries import SummaryGenerator
from sports_signal_bot.labels.contracts import LabelRecord


class BacktestRunner:
    def __init__(
        self,
        sport: str,
        market: str,
        execution_policy: ExecutionPolicy,
        output_dir: str = "results/backtest",
    ):
        self.sport = sport
        self.market = market
        self.execution_policy = execution_policy
        self.output_dir = Path(output_dir) / self.sport / self.market
        self.run_id = str(uuid.uuid4())

        self.input_builder = BacktestInputBuilder()
        self.planner = ReplayPlanner()
        self.replay_engine = ChronologicalReplayEngine()
        self.settlement_engine = SettlementEngine()
        self.ledger_writer = LedgerWriter(self.output_dir)
        self.summary_generator = SummaryGenerator()
        self.period_summarizer = PeriodSummarizer()
        self.reporter = BacktestReporter(self.output_dir)

    def run(
        self, decisions: List[BacktestDecisionRecord], labels: List[LabelRecord]
    ) -> BacktestRunManifest:
        aligned_dataset = self.input_builder.align_decisions_with_results(
            decisions, labels
        )
        warnings = self.input_builder.validate_replay_dataset(aligned_dataset)

        sequence = self.planner.build_replay_sequence(aligned_dataset)

        replay_records = self.replay_engine.process_sequence(
            sequence=sequence,
            execution_engine=self.execution_policy,
            settlement_engine=self.settlement_engine,
        )

        ledger = self.ledger_writer.generate_ledger_records(self.run_id, replay_records)
        csv_path = self.ledger_writer.save_to_csv(ledger)
        self.ledger_writer.save_to_json(ledger)

        overall_summary = self.reporter.generate_summary(
            self.run_id, self.sport, self.market, ledger
        )
        action_summaries = self.summary_generator.summarize_by_action_class(ledger)
        period_summaries = self.period_summarizer.summarize_by_period(
            ledger, period="daily"
        )

        manifest = BacktestRunManifest(
            run_id=self.run_id,
            sport=self.sport,
            market_type=self.market,
            execution_policy_name=self.execution_policy.__class__.__name__,
            window=ReplayWindowDefinition(),
            summary=overall_summary,
            action_subsets=action_summaries,
            period_summaries=period_summaries,
            ledger_artifact_path=str(csv_path),
            warnings=warnings,
        )

        self.reporter.save_manifest(manifest)
        self.reporter.save_summary(overall_summary)

        return manifest
