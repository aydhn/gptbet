#!/bin/bash
mkdir -p sports_signal_bot/src/sports_signal_bot/backtest
cat << 'PY' > sports_signal_bot/src/sports_signal_bot/backtest/contracts.py
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from sports_signal_bot.policy.contracts import ActionClass, PolicySignalStatus


class SettlementStatus(str, Enum):
    SETTLED_WIN = "settled_win"
    SETTLED_LOSS = "settled_loss"
    SETTLED_VOID = "settled_void"
    SETTLED_PUSH = "settled_push"
    UNSETTLED_PENDING = "unsettled_pending"
    UNSUPPORTED_SETTLEMENT = "unsupported_settlement"
    INVALID_RESULT = "invalid_result"


class ExecutionEligibility(str, Enum):
    EXECUTABLE = "executable"
    SKIPPED_POLICY = "skipped_policy"
    SKIPPED_WATCHLIST = "skipped_watchlist"
    INVALID_CLASS = "invalid_class"
    BLOCKED = "blocked"


class ExecutionEligibilityRecord(BaseModel):
    eligibility: ExecutionEligibility
    reason: str


class SettlementRecord(BaseModel):
    status: SettlementStatus
    realized_outcome: Optional[str] = None
    hit_flag: Optional[bool] = None
    probabilistic_loss: Optional[float] = None
    notes: Optional[str] = None
    processed_at_utc: datetime = Field(default_factory=datetime.utcnow)


class BacktestDecisionRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    event_datetime_utc: datetime
    decision_timestamp_utc: datetime

    selection: str
    signal_status: PolicySignalStatus
    action_class: ActionClass

    final_probability: Optional[float] = None
    market_implied_probability: Optional[float] = None
    signal_score: Optional[float] = None

    threshold_policy_name: str
    policy_name: str

    edge_snapshot: Optional[float] = None
    warnings: List[str] = Field(default_factory=list)


class BacktestLedgerRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    event_datetime_utc: datetime
    decision_timestamp_utc: datetime

    signal_status: PolicySignalStatus
    action_class: ActionClass

    executed_flag: bool
    execution_reason: str

    selection: str
    final_probability: Optional[float] = None
    market_implied_probability: Optional[float] = None
    signal_score: Optional[float] = None

    threshold_policy_name: str
    policy_name: str

    result_status: SettlementStatus
    realized_outcome: Optional[str] = None
    hit_flag: Optional[bool] = None
    probabilistic_loss: Optional[float] = None

    edge_snapshot: Optional[float] = None
    warnings: List[str] = Field(default_factory=list)
    run_id: str

    stake_units: Optional[float] = None
    payout_multiplier: Optional[float] = None
    pnl_units: Optional[float] = None


class BacktestReplayRecord(BaseModel):
    decision: BacktestDecisionRecord
    eligibility: ExecutionEligibilityRecord
    settlement: SettlementRecord


class ActionSubsetSummary(BaseModel):
    subset_name: str
    total_decisions: int = 0
    executed_decisions: int = 0
    skipped_decisions: int = 0
    win_count: int = 0
    loss_count: int = 0
    void_count: int = 0
    hit_rate: Optional[float] = None
    average_signal_score: Optional[float] = None
    average_edge_snapshot: Optional[float] = None


class BacktestPeriodSummary(BaseModel):
    period_label: str
    start_date: datetime
    end_date: datetime

    executed_count: int = 0
    hit_rate: Optional[float] = None
    avg_score: Optional[float] = None
    avg_edge: Optional[float] = None
    void_count: int = 0
    warnings: List[str] = Field(default_factory=list)


class ReplayWindowDefinition(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    window_type: str = "full-history"


class ReplayWindowRecord(BaseModel):
    definition: ReplayWindowDefinition
    total_evaluated: int = 0
    execution_rate: float = 0.0


class BacktestSummaryRecord(BaseModel):
    run_id: str
    sport: str
    market: str
    total_decisions: int = 0
    executed_decisions: int = 0
    skipped_decisions: int = 0
    win_count: int = 0
    loss_count: int = 0
    void_count: int = 0
    hit_rate: Optional[float] = None
    average_signal_score: Optional[float] = None
    average_edge_snapshot: Optional[float] = None

    action_class_distribution: Dict[str, int] = Field(default_factory=dict)
    market_distribution: Dict[str, int] = Field(default_factory=dict)
    policy_distribution: Dict[str, int] = Field(default_factory=dict)

    replay_log_loss: Optional[float] = None
    replay_brier: Optional[float] = None
    average_final_probability: Optional[float] = None


class BacktestRunManifest(BaseModel):
    run_id: str
    generated_at_utc: datetime = Field(default_factory=datetime.utcnow)
    sport: str
    market_type: str
    execution_policy_name: str
    window: ReplayWindowDefinition

    summary: BacktestSummaryRecord
    action_subsets: List[ActionSubsetSummary] = Field(default_factory=list)
    period_summaries: List[BacktestPeriodSummary] = Field(default_factory=list)

    ledger_artifact_path: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)
PY

cat << 'PY' > sports_signal_bot/src/sports_signal_bot/backtest/execution.py
from abc import ABC, abstractmethod
from typing import List

from sports_signal_bot.policy.contracts import ActionClass
from sports_signal_bot.backtest.contracts import ExecutionEligibility, ExecutionEligibilityRecord, BacktestDecisionRecord


class ExecutionPolicy(ABC):

    @abstractmethod
    def resolve_execution_subset(self, decision: BacktestDecisionRecord) -> ExecutionEligibilityRecord:
        pass

    def is_executable_decision(self, decision: BacktestDecisionRecord) -> bool:
        record = self.resolve_execution_subset(decision)
        return record.eligibility == ExecutionEligibility.EXECUTABLE

    def explain_execution_exclusion(self, decision: BacktestDecisionRecord) -> str:
        record = self.resolve_execution_subset(decision)
        return record.reason


class ApprovedOnlyExecution(ExecutionPolicy):
    def resolve_execution_subset(self, decision: BacktestDecisionRecord) -> ExecutionEligibilityRecord:
        if decision.action_class == ActionClass.APPROVED_CANDIDATE:
            return ExecutionEligibilityRecord(eligibility=ExecutionEligibility.EXECUTABLE, reason="Approved candidate")
        elif decision.action_class == ActionClass.CANDIDATE:
            return ExecutionEligibilityRecord(eligibility=ExecutionEligibility.SKIPPED_POLICY, reason="Only approved candidates are executed")
        elif decision.action_class == ActionClass.WATCHLIST:
            return ExecutionEligibilityRecord(eligibility=ExecutionEligibility.SKIPPED_WATCHLIST, reason="Watchlist shadow execution not enabled")
        elif decision.action_class == ActionClass.BLOCKED_CANDIDATE:
            return ExecutionEligibilityRecord(eligibility=ExecutionEligibility.BLOCKED, reason="Blocked candidate")
        return ExecutionEligibilityRecord(eligibility=ExecutionEligibility.INVALID_CLASS, reason=f"Invalid action class: {decision.action_class}")


class CandidateAndApprovedExecution(ExecutionPolicy):
    def resolve_execution_subset(self, decision: BacktestDecisionRecord) -> ExecutionEligibilityRecord:
        if decision.action_class in [ActionClass.APPROVED_CANDIDATE, ActionClass.CANDIDATE]:
            return ExecutionEligibilityRecord(eligibility=ExecutionEligibility.EXECUTABLE, reason=f"Valid candidate: {decision.action_class}")
        elif decision.action_class == ActionClass.WATCHLIST:
            return ExecutionEligibilityRecord(eligibility=ExecutionEligibility.SKIPPED_WATCHLIST, reason="Watchlist shadow execution not enabled")
        elif decision.action_class == ActionClass.BLOCKED_CANDIDATE:
            return ExecutionEligibilityRecord(eligibility=ExecutionEligibility.BLOCKED, reason="Blocked candidate")
        return ExecutionEligibilityRecord(eligibility=ExecutionEligibility.INVALID_CLASS, reason=f"Invalid action class: {decision.action_class}")


class WatchlistShadowExecution(ExecutionPolicy):
    def resolve_execution_subset(self, decision: BacktestDecisionRecord) -> ExecutionEligibilityRecord:
        if decision.action_class in [ActionClass.APPROVED_CANDIDATE, ActionClass.CANDIDATE, ActionClass.WATCHLIST]:
            return ExecutionEligibilityRecord(eligibility=ExecutionEligibility.EXECUTABLE, reason=f"Shadow execution: {decision.action_class}")
        elif decision.action_class == ActionClass.BLOCKED_CANDIDATE:
            return ExecutionEligibilityRecord(eligibility=ExecutionEligibility.BLOCKED, reason="Blocked candidate")
        return ExecutionEligibilityRecord(eligibility=ExecutionEligibility.INVALID_CLASS, reason=f"Invalid action class: {decision.action_class}")


class CustomActionClassExecutionPolicy(ExecutionPolicy):
    def __init__(self, allowed_classes: List[ActionClass]):
        self.allowed_classes = allowed_classes

    def resolve_execution_subset(self, decision: BacktestDecisionRecord) -> ExecutionEligibilityRecord:
        if not self.allowed_classes:
            return ExecutionEligibilityRecord(eligibility=ExecutionEligibility.INVALID_CLASS, reason="Empty allowed execution subset")

        if decision.action_class in self.allowed_classes:
            return ExecutionEligibilityRecord(eligibility=ExecutionEligibility.EXECUTABLE, reason=f"Custom execution: {decision.action_class}")
        elif decision.action_class == ActionClass.BLOCKED_CANDIDATE:
            return ExecutionEligibilityRecord(eligibility=ExecutionEligibility.BLOCKED, reason="Blocked candidate")
        return ExecutionEligibilityRecord(eligibility=ExecutionEligibility.SKIPPED_POLICY, reason=f"Action class not in allowed list: {decision.action_class}")
PY

cat << 'PY' > sports_signal_bot/src/sports_signal_bot/backtest/settlement.py
from typing import Any, Dict, Optional, Tuple

from sports_signal_bot.backtest.contracts import SettlementStatus, SettlementRecord, BacktestDecisionRecord
from sports_signal_bot.markets.enums import LabelValidityStatus
from sports_signal_bot.labels.contracts import LabelRecord


class SettlementEngine:

    def __init__(self, supported_markets: list[str] = None):
        self.supported_markets = supported_markets or [
            "football_1x2", "football_over_under", "football_btts",
            "basketball_match_winner", "basketball_total_points"
        ]

    def resolve_realized_selection(self, label: LabelRecord) -> Optional[str]:
        if label.validity_status in [LabelValidityStatus.VOID, LabelValidityStatus.INVALID, LabelValidityStatus.UNSUPPORTED]:
            return None
        return label.target_text

    def compare_decision_vs_result(self, decision: BacktestDecisionRecord, label: LabelRecord) -> SettlementRecord:
        if decision.market_type not in self.supported_markets:
            return SettlementRecord(
                status=SettlementStatus.UNSUPPORTED_SETTLEMENT,
                notes=f"Market {decision.market_type} not supported for settlement"
            )

        realized_outcome = self.resolve_realized_selection(label)

        is_void = self.handle_void_or_cancelled(label)
        if is_void:
            return SettlementRecord(
                status=SettlementStatus.SETTLED_VOID,
                notes="Event or label was void/cancelled"
            )

        if label.validity_status == LabelValidityStatus.PENDING:
            return SettlementRecord(
                status=SettlementStatus.UNSETTLED_PENDING,
                notes="Label result is pending"
            )

        if decision.market_type in ["football_1x2", "football_btts", "basketball_match_winner"]:
            return self.settle_multiclass_decision(decision, realized_outcome)
        elif decision.market_type in ["football_over_under", "basketball_total_points"]:
            return self.settle_line_based_market(decision, label)

        return SettlementRecord(
            status=SettlementStatus.UNSUPPORTED_SETTLEMENT,
            notes=f"Fallback unsupported market logic hit for {decision.market_type}"
        )

    def settle_binary_decision(self, decision: BacktestDecisionRecord, realized_outcome: Optional[str]) -> SettlementRecord:
        if not realized_outcome:
            return SettlementRecord(status=SettlementStatus.INVALID_RESULT, notes="Realized outcome is missing")

        hit = decision.selection.lower() == realized_outcome.lower()
        status = SettlementStatus.SETTLED_WIN if hit else SettlementStatus.SETTLED_LOSS
        return SettlementRecord(
            status=status,
            realized_outcome=realized_outcome,
            hit_flag=hit
        )

    def settle_multiclass_decision(self, decision: BacktestDecisionRecord, realized_outcome: Optional[str]) -> SettlementRecord:
        if not realized_outcome:
            return SettlementRecord(status=SettlementStatus.INVALID_RESULT, notes="Realized outcome is missing")

        hit = decision.selection.lower() == realized_outcome.lower()
        status = SettlementStatus.SETTLED_WIN if hit else SettlementStatus.SETTLED_LOSS
        return SettlementRecord(
            status=status,
            realized_outcome=realized_outcome,
            hit_flag=hit
        )

    def settle_line_based_market(self, decision: BacktestDecisionRecord, label: LabelRecord) -> SettlementRecord:
        realized_outcome = label.target_text
        if not realized_outcome:
            return SettlementRecord(status=SettlementStatus.INVALID_RESULT, notes="Realized outcome is missing")

        if label.line_value is not None and label.target_value is not None:
             if label.line_value == label.target_value:
                 return SettlementRecord(
                    status=SettlementStatus.SETTLED_PUSH,
                    realized_outcome=realized_outcome,
                    hit_flag=None,
                    notes="Push due to matching line exactly"
                 )

        hit = decision.selection.lower() == realized_outcome.lower()
        status = SettlementStatus.SETTLED_WIN if hit else SettlementStatus.SETTLED_LOSS
        return SettlementRecord(
            status=status,
            realized_outcome=realized_outcome,
            hit_flag=hit
        )

    def handle_void_or_cancelled(self, label: LabelRecord) -> bool:
        if label.validity_status in [LabelValidityStatus.VOID, LabelValidityStatus.INVALID]:
            return True
        return False
PY

cat << 'PY' > sports_signal_bot/src/sports_signal_bot/backtest/inputs.py
from typing import Dict, List, Tuple

from sports_signal_bot.backtest.contracts import BacktestDecisionRecord
from sports_signal_bot.labels.contracts import LabelRecord


class BacktestInputBuilder:
    def __init__(self):
        pass

    def load_backtest_inputs(self, decisions: List[BacktestDecisionRecord], labels: List[LabelRecord]) -> Tuple[List[BacktestDecisionRecord], List[LabelRecord]]:
        return decisions, labels

    def align_decisions_with_results(
        self, decisions: List[BacktestDecisionRecord], labels: List[LabelRecord]
    ) -> List[Tuple[BacktestDecisionRecord, LabelRecord]]:
        aligned = []
        label_map = {f"{l.event_id}_{l.market_type}": l for l in labels}

        for d in decisions:
            key = f"{d.event_id}_{d.market_type}"
            if key in label_map:
                aligned.append((d, label_map[key]))

        return aligned

    def validate_replay_dataset(self, dataset: List[Tuple[BacktestDecisionRecord, LabelRecord]]) -> List[str]:
        warnings = []
        event_decision_combos = set()
        for d, l in dataset:
            key = f"{d.event_id}_{d.market_type}_{d.selection}"
            if key in event_decision_combos:
                warnings.append(f"Duplicate decision found for {key}")
            event_decision_combos.add(key)

            if d.event_id != l.event_id:
                 warnings.append(f"Mismatch event ids in aligned dataset: {d.event_id} vs {l.event_id}")

        return warnings

    def enrich_with_signal_context(self, decision: BacktestDecisionRecord, signal_score: float, edge: float) -> BacktestDecisionRecord:
        decision.signal_score = signal_score
        decision.edge_snapshot = edge
        return decision
PY

cat << 'PY' > sports_signal_bot/src/sports_signal_bot/backtest/replay.py
from typing import List, Tuple

from sports_signal_bot.backtest.contracts import BacktestDecisionRecord, BacktestReplayRecord, SettlementRecord, ExecutionEligibilityRecord, ExecutionEligibility
from sports_signal_bot.labels.contracts import LabelRecord


class ReplayPlanner:
    def __init__(self):
        pass

    def build_replay_sequence(
        self, dataset: List[Tuple[BacktestDecisionRecord, LabelRecord]]
    ) -> List[Tuple[BacktestDecisionRecord, LabelRecord]]:

        def sort_key(item: Tuple[BacktestDecisionRecord, LabelRecord]):
            d, _ = item
            return (d.decision_timestamp_utc, d.event_datetime_utc, d.event_id)

        return sorted(dataset, key=sort_key)


class ChronologicalReplayEngine:

    def process_sequence(
        self,
        sequence: List[Tuple[BacktestDecisionRecord, LabelRecord]],
        execution_engine,
        settlement_engine
    ) -> List[BacktestReplayRecord]:

        replay_records = []
        for decision, label in sequence:
            eligibility_record = execution_engine.resolve_execution_subset(decision)
            settlement_record = settlement_engine.compare_decision_vs_result(decision, label)

            replay_records.append(
                BacktestReplayRecord(
                    decision=decision,
                    eligibility=eligibility_record,
                    settlement=settlement_record
                )
            )

        return replay_records
PY

cat << 'PY' > sports_signal_bot/src/sports_signal_bot/backtest/ledger.py
import csv
import json
from pathlib import Path
from typing import List

from sports_signal_bot.backtest.contracts import BacktestReplayRecord, BacktestLedgerRecord, ExecutionEligibility


class LedgerWriter:
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_ledger_records(self, run_id: str, replay_records: List[BacktestReplayRecord]) -> List[BacktestLedgerRecord]:
        ledger_records = []
        for r in replay_records:
            d = r.decision
            s = r.settlement
            e = r.eligibility

            executed = e.eligibility == ExecutionEligibility.EXECUTABLE

            lr = BacktestLedgerRecord(
                event_id=d.event_id,
                sport=d.sport,
                market_type=d.market_type,
                event_datetime_utc=d.event_datetime_utc,
                decision_timestamp_utc=d.decision_timestamp_utc,
                signal_status=d.signal_status,
                action_class=d.action_class,
                executed_flag=executed,
                execution_reason=e.reason,
                selection=d.selection,
                final_probability=d.final_probability,
                market_implied_probability=d.market_implied_probability,
                signal_score=d.signal_score,
                threshold_policy_name=d.threshold_policy_name,
                policy_name=d.policy_name,
                result_status=s.status,
                realized_outcome=s.realized_outcome,
                hit_flag=s.hit_flag,
                probabilistic_loss=s.probabilistic_loss,
                edge_snapshot=d.edge_snapshot,
                warnings=d.warnings,
                run_id=run_id
            )
            ledger_records.append(lr)

        return ledger_records

    def save_to_csv(self, records: List[BacktestLedgerRecord], filename: str = "backtest_ledger.csv") -> Path:
        if not records:
            return self.output_dir / filename

        filepath = self.output_dir / filename
        fieldnames = list(records[0].model_dump().keys())

        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in records:
                row = r.model_dump()
                row['event_datetime_utc'] = row['event_datetime_utc'].isoformat()
                row['decision_timestamp_utc'] = row['decision_timestamp_utc'].isoformat()
                writer.writerow(row)

        return filepath

    def save_to_json(self, records: List[BacktestLedgerRecord], filename: str = "backtest_ledger.json") -> Path:
        filepath = self.output_dir / filename
        data = [r.model_dump(mode="json") for r in records]

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        return filepath
PY

cat << 'PY' > sports_signal_bot/src/sports_signal_bot/backtest/summaries.py
from typing import List, Dict

from sports_signal_bot.backtest.contracts import BacktestLedgerRecord, ActionSubsetSummary, SettlementStatus
from sports_signal_bot.policy.contracts import ActionClass

class SummaryGenerator:
    def _calculate_subset(self, name: str, records: List[BacktestLedgerRecord]) -> ActionSubsetSummary:
        total = len(records)
        executed = sum(1 for r in records if r.executed_flag)
        skipped = total - executed

        wins = sum(1 for r in records if r.executed_flag and r.result_status == SettlementStatus.SETTLED_WIN)
        losses = sum(1 for r in records if r.executed_flag and r.result_status == SettlementStatus.SETTLED_LOSS)
        voids = sum(1 for r in records if r.executed_flag and r.result_status == SettlementStatus.SETTLED_VOID)

        resolved_count = wins + losses
        hit_rate = (wins / resolved_count) if resolved_count > 0 else None

        avg_score = None
        valid_scores = [r.signal_score for r in records if r.signal_score is not None]
        if valid_scores:
            avg_score = sum(valid_scores) / len(valid_scores)

        avg_edge = None
        valid_edges = [r.edge_snapshot for r in records if r.edge_snapshot is not None]
        if valid_edges:
            avg_edge = sum(valid_edges) / len(valid_edges)

        return ActionSubsetSummary(
            subset_name=name,
            total_decisions=total,
            executed_decisions=executed,
            skipped_decisions=skipped,
            win_count=wins,
            loss_count=losses,
            void_count=voids,
            hit_rate=hit_rate,
            average_signal_score=avg_score,
            average_edge_snapshot=avg_edge
        )

    def summarize_by_action_class(self, ledger: List[BacktestLedgerRecord]) -> List[ActionSubsetSummary]:
        class_map: Dict[ActionClass, List[BacktestLedgerRecord]] = {}
        for r in ledger:
            class_map.setdefault(r.action_class, []).append(r)

        summaries = []
        for ac, records in class_map.items():
            summaries.append(self._calculate_subset(ac.value, records))
        return summaries

    def summarize_by_market(self, ledger: List[BacktestLedgerRecord]) -> List[ActionSubsetSummary]:
        market_map: Dict[str, List[BacktestLedgerRecord]] = {}
        for r in ledger:
            market_map.setdefault(r.market_type, []).append(r)

        summaries = []
        for mt, records in market_map.items():
            summaries.append(self._calculate_subset(mt, records))
        return summaries
PY

cat << 'PY' > sports_signal_bot/src/sports_signal_bot/backtest/periods.py
from datetime import datetime, timedelta
from typing import List, Dict

from sports_signal_bot.backtest.contracts import BacktestLedgerRecord, BacktestPeriodSummary, SettlementStatus


class PeriodSummarizer:
    def summarize_by_period(self, ledger: List[BacktestLedgerRecord], period: str = "daily") -> List[BacktestPeriodSummary]:
        if not ledger:
            return []

        period_map: Dict[str, List[BacktestLedgerRecord]] = {}

        for r in ledger:
            dt = r.decision_timestamp_utc
            if period == "daily":
                label = dt.strftime("%Y-%m-%d")
            elif period == "weekly":
                year, week, _ = dt.isocalendar()
                label = f"{year}-W{week:02d}"
            elif period == "monthly":
                label = dt.strftime("%Y-%m")
            else:
                label = "all_time"

            period_map.setdefault(label, []).append(r)

        summaries = []
        for label, records in sorted(period_map.items()):
            start_date = min(r.decision_timestamp_utc for r in records)
            end_date = max(r.decision_timestamp_utc for r in records)

            executed_count = sum(1 for r in records if r.executed_flag)
            wins = sum(1 for r in records if r.executed_flag and r.result_status == SettlementStatus.SETTLED_WIN)
            losses = sum(1 for r in records if r.executed_flag and r.result_status == SettlementStatus.SETTLED_LOSS)
            voids = sum(1 for r in records if r.executed_flag and r.result_status == SettlementStatus.SETTLED_VOID)

            resolved_count = wins + losses
            hit_rate = (wins / resolved_count) if resolved_count > 0 else None

            valid_scores = [r.signal_score for r in records if r.signal_score is not None]
            avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else None

            valid_edges = [r.edge_snapshot for r in records if r.edge_snapshot is not None]
            avg_edge = sum(valid_edges) / len(valid_edges) if valid_edges else None

            warnings = []
            for r in records:
                if r.warnings:
                    warnings.extend(r.warnings)

            summaries.append(
                BacktestPeriodSummary(
                    period_label=label,
                    start_date=start_date,
                    end_date=end_date,
                    executed_count=executed_count,
                    hit_rate=hit_rate,
                    avg_score=avg_score,
                    avg_edge=avg_edge,
                    void_count=voids,
                    warnings=list(set(warnings))[:5]
                )
            )

        return summaries
PY

cat << 'PY' > sports_signal_bot/src/sports_signal_bot/backtest/reporting.py
import json
from pathlib import Path
from typing import List

from sports_signal_bot.backtest.contracts import BacktestRunManifest, BacktestSummaryRecord, BacktestLedgerRecord, SettlementStatus


class BacktestReporter:
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_summary(self, run_id: str, sport: str, market: str, ledger: List[BacktestLedgerRecord]) -> BacktestSummaryRecord:
        total = len(ledger)
        executed = sum(1 for r in ledger if r.executed_flag)
        skipped = total - executed

        wins = sum(1 for r in ledger if r.executed_flag and r.result_status == SettlementStatus.SETTLED_WIN)
        losses = sum(1 for r in ledger if r.executed_flag and r.result_status == SettlementStatus.SETTLED_LOSS)
        voids = sum(1 for r in ledger if r.executed_flag and r.result_status == SettlementStatus.SETTLED_VOID)

        resolved_count = wins + losses
        hit_rate = (wins / resolved_count) if resolved_count > 0 else None

        valid_scores = [r.signal_score for r in ledger if r.signal_score is not None]
        avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else None

        valid_edges = [r.edge_snapshot for r in ledger if r.edge_snapshot is not None]
        avg_edge = sum(valid_edges) / len(valid_edges) if valid_edges else None

        ac_dist = {}
        for r in ledger:
            ac_dist[r.action_class.value] = ac_dist.get(r.action_class.value, 0) + 1

        return BacktestSummaryRecord(
            run_id=run_id,
            sport=sport,
            market=market,
            total_decisions=total,
            executed_decisions=executed,
            skipped_decisions=skipped,
            win_count=wins,
            loss_count=losses,
            void_count=voids,
            hit_rate=hit_rate,
            average_signal_score=avg_score,
            average_edge_snapshot=avg_edge,
            action_class_distribution=ac_dist
        )

    def save_manifest(self, manifest: BacktestRunManifest, filename: str = "replay_manifest.json") -> Path:
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(manifest.model_dump(mode="json"), f, indent=2)
        return filepath

    def save_summary(self, summary: BacktestSummaryRecord, filename: str = "backtest_summary.json") -> Path:
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(summary.model_dump(mode="json"), f, indent=2)
        return filepath
PY

cat << 'PY' > sports_signal_bot/src/sports_signal_bot/backtest/runner.py
from datetime import datetime
from pathlib import Path
from typing import List
import uuid

from sports_signal_bot.backtest.contracts import (
    BacktestDecisionRecord,
    BacktestRunManifest,
    ReplayWindowDefinition,
)
from sports_signal_bot.labels.contracts import LabelRecord
from sports_signal_bot.backtest.inputs import BacktestInputBuilder
from sports_signal_bot.backtest.execution import ExecutionPolicy
from sports_signal_bot.backtest.settlement import SettlementEngine
from sports_signal_bot.backtest.replay import ChronologicalReplayEngine, ReplayPlanner
from sports_signal_bot.backtest.ledger import LedgerWriter
from sports_signal_bot.backtest.summaries import SummaryGenerator
from sports_signal_bot.backtest.periods import PeriodSummarizer
from sports_signal_bot.backtest.reporting import BacktestReporter


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

    def run(self, decisions: List[BacktestDecisionRecord], labels: List[LabelRecord]) -> BacktestRunManifest:
        aligned_dataset = self.input_builder.align_decisions_with_results(decisions, labels)
        warnings = self.input_builder.validate_replay_dataset(aligned_dataset)

        sequence = self.planner.build_replay_sequence(aligned_dataset)

        replay_records = self.replay_engine.process_sequence(
            sequence=sequence,
            execution_engine=self.execution_policy,
            settlement_engine=self.settlement_engine
        )

        ledger = self.ledger_writer.generate_ledger_records(self.run_id, replay_records)
        csv_path = self.ledger_writer.save_to_csv(ledger)
        self.ledger_writer.save_to_json(ledger)

        overall_summary = self.reporter.generate_summary(self.run_id, self.sport, self.market, ledger)
        action_summaries = self.summary_generator.summarize_by_action_class(ledger)
        period_summaries = self.period_summarizer.summarize_by_period(ledger, period="daily")

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
            warnings=warnings
        )

        self.reporter.save_manifest(manifest)
        self.reporter.save_summary(overall_summary)

        return manifest
PY
