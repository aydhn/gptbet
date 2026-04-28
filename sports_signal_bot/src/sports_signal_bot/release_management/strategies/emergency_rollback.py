from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.release_management.contracts import PromotionRequestRecord, RequestType
from sports_signal_bot.release_management.strategies.base import ReleaseStrategy

logger = get_logger("EmergencyRollbackStrategy")


class EmergencyRollbackStrategy(ReleaseStrategy):
    def handle_request(self, request: PromotionRequestRecord, runner: any) -> any:
        logger.info(f"Running emergency rollback for {request.request_id}")
        if request.request_type == RequestType.rollback_to_previous_stable:
            # Overrides approval requirement for speed
            return runner._run_rollback(request)
        return runner._run_standard_promotion(request)
