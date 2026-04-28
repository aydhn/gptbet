from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.release_management.contracts import PromotionRequestRecord, RequestType
from sports_signal_bot.release_management.history import ReleaseLedger
from sports_signal_bot.release_management.planning import PromotionPlanner
from sports_signal_bot.release_management.promotion import PromotionDecisionEngine, PromotionExecutor
from sports_signal_bot.release_management.registry import StrategyRegistry
from sports_signal_bot.release_management.rollback import RollbackExecutor, RollbackPlanner
from sports_signal_bot.release_management.state import ChannelStateManager

logger = get_logger("ReleaseRunner")


class ReleaseRunner:
    def __init__(self, data_dir: str = "data/release"):
        self.state_manager = ChannelStateManager(data_dir=data_dir)
        self.decision_engine = PromotionDecisionEngine(self.state_manager)
        self.planner = PromotionPlanner()
        self.executor = PromotionExecutor(self.state_manager)
        self.rollback_planner = RollbackPlanner(self.state_manager)
        self.rollback_executor = RollbackExecutor(self.state_manager)
        self.ledger = ReleaseLedger(data_dir=data_dir)

    def process_request(self, request: PromotionRequestRecord, strategy_name: str = "conservative_promotion") -> any:
        strategy = StrategyRegistry.get_strategy(strategy_name)
        return strategy.handle_request(request, self)

    def _run_standard_promotion(self, request: PromotionRequestRecord) -> any:
        decision = self.decision_engine.evaluate_request(request)
        if decision.decision != "approved":
            logger.warning(f"Promotion request {request.request_id} denied: {decision.rationale}")
            self.ledger.append_ledger(request, decision, None)
            return decision

        plan = self.planner.create_plan(request, decision)
        if plan:
            self.executor.execute_plan(plan, request)

        self.ledger.append_ledger(request, decision, plan)
        return decision

    def _run_rollback(self, request: PromotionRequestRecord) -> any:
        plan = self.rollback_planner.create_rollback_plan(
            sport=request.sport, market_type=request.market_type, reason=request.rationale
        )
        if not plan:
            return None

        execution = self.rollback_executor.execute_rollback(plan)
        plan.execution = execution

        self.ledger.append_rollback(request, plan)
        return plan
