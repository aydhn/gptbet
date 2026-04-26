from abc import ABC, abstractmethod
from typing import List

from sports_signal_bot.backtest.contracts import (
    BacktestDecisionRecord,
    ExecutionEligibility,
    ExecutionEligibilityRecord,
)
from sports_signal_bot.policy.contracts import ActionClass


class ExecutionPolicy(ABC):

    @abstractmethod
    def resolve_execution_subset(
        self, decision: BacktestDecisionRecord
    ) -> ExecutionEligibilityRecord:
        pass

    def is_executable_decision(self, decision: BacktestDecisionRecord) -> bool:
        record = self.resolve_execution_subset(decision)
        return record.eligibility == ExecutionEligibility.EXECUTABLE

    def explain_execution_exclusion(self, decision: BacktestDecisionRecord) -> str:
        record = self.resolve_execution_subset(decision)
        return record.reason


class ApprovedOnlyExecution(ExecutionPolicy):
    def resolve_execution_subset(
        self, decision: BacktestDecisionRecord
    ) -> ExecutionEligibilityRecord:
        if decision.action_class == ActionClass.APPROVED_CANDIDATE:
            return ExecutionEligibilityRecord(
                eligibility=ExecutionEligibility.EXECUTABLE, reason="Approved candidate"
            )
        elif decision.action_class == ActionClass.CANDIDATE:
            return ExecutionEligibilityRecord(
                eligibility=ExecutionEligibility.SKIPPED_POLICY,
                reason="Only approved candidates are executed",
            )
        elif decision.action_class == ActionClass.WATCHLIST:
            return ExecutionEligibilityRecord(
                eligibility=ExecutionEligibility.SKIPPED_WATCHLIST,
                reason="Watchlist shadow execution not enabled",
            )
        elif decision.action_class == ActionClass.BLOCKED_CANDIDATE:
            return ExecutionEligibilityRecord(
                eligibility=ExecutionEligibility.BLOCKED, reason="Blocked candidate"
            )
        return ExecutionEligibilityRecord(
            eligibility=ExecutionEligibility.INVALID_CLASS,
            reason=f"Invalid action class: {decision.action_class}",
        )


class CandidateAndApprovedExecution(ExecutionPolicy):
    def resolve_execution_subset(
        self, decision: BacktestDecisionRecord
    ) -> ExecutionEligibilityRecord:
        if decision.action_class in [
            ActionClass.APPROVED_CANDIDATE,
            ActionClass.CANDIDATE,
        ]:
            return ExecutionEligibilityRecord(
                eligibility=ExecutionEligibility.EXECUTABLE,
                reason=f"Valid candidate: {decision.action_class}",
            )
        elif decision.action_class == ActionClass.WATCHLIST:
            return ExecutionEligibilityRecord(
                eligibility=ExecutionEligibility.SKIPPED_WATCHLIST,
                reason="Watchlist shadow execution not enabled",
            )
        elif decision.action_class == ActionClass.BLOCKED_CANDIDATE:
            return ExecutionEligibilityRecord(
                eligibility=ExecutionEligibility.BLOCKED, reason="Blocked candidate"
            )
        return ExecutionEligibilityRecord(
            eligibility=ExecutionEligibility.INVALID_CLASS,
            reason=f"Invalid action class: {decision.action_class}",
        )


class WatchlistShadowExecution(ExecutionPolicy):
    def resolve_execution_subset(
        self, decision: BacktestDecisionRecord
    ) -> ExecutionEligibilityRecord:
        if decision.action_class in [
            ActionClass.APPROVED_CANDIDATE,
            ActionClass.CANDIDATE,
            ActionClass.WATCHLIST,
        ]:
            return ExecutionEligibilityRecord(
                eligibility=ExecutionEligibility.EXECUTABLE,
                reason=f"Shadow execution: {decision.action_class}",
            )
        elif decision.action_class == ActionClass.BLOCKED_CANDIDATE:
            return ExecutionEligibilityRecord(
                eligibility=ExecutionEligibility.BLOCKED, reason="Blocked candidate"
            )
        return ExecutionEligibilityRecord(
            eligibility=ExecutionEligibility.INVALID_CLASS,
            reason=f"Invalid action class: {decision.action_class}",
        )


class CustomActionClassExecutionPolicy(ExecutionPolicy):
    def __init__(self, allowed_classes: List[ActionClass]):
        self.allowed_classes = allowed_classes

    def resolve_execution_subset(
        self, decision: BacktestDecisionRecord
    ) -> ExecutionEligibilityRecord:
        if not self.allowed_classes:
            return ExecutionEligibilityRecord(
                eligibility=ExecutionEligibility.INVALID_CLASS,
                reason="Empty allowed execution subset",
            )

        if decision.action_class in self.allowed_classes:
            return ExecutionEligibilityRecord(
                eligibility=ExecutionEligibility.EXECUTABLE,
                reason=f"Custom execution: {decision.action_class}",
            )
        elif decision.action_class == ActionClass.BLOCKED_CANDIDATE:
            return ExecutionEligibilityRecord(
                eligibility=ExecutionEligibility.BLOCKED, reason="Blocked candidate"
            )
        return ExecutionEligibilityRecord(
            eligibility=ExecutionEligibility.SKIPPED_POLICY,
            reason=f"Action class not in allowed list: {decision.action_class}",
        )
