from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.release_management.contracts import PromotionRequestRecord, RequestType
from sports_signal_bot.release_management.strategies.base import ReleaseStrategy

logger = get_logger("StableFirstRecoveryStrategy")


class StableFirstRecoveryStrategy(ReleaseStrategy):
    def handle_request(self, request: PromotionRequestRecord, runner: any) -> any:
        logger.info(f"Running stable first recovery for {request.request_id}")

        if request.request_type == RequestType.rollback_to_previous_stable:
            return runner._run_rollback(request)

        if request.request_type == RequestType.promote_stable_fallback_chain:
            return runner._run_standard_promotion(request)

        logger.warning(f"Request type {request.request_type} discouraged in recovery mode.")
        return runner._run_standard_promotion(request)
