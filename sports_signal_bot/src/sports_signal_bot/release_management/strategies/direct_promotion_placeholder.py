from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.release_management.contracts import PromotionRequestRecord
from sports_signal_bot.release_management.strategies.base import ReleaseStrategy

logger = get_logger("DirectPromotionStrategy")


class DirectPromotionStrategy(ReleaseStrategy):
    def handle_request(self, request: PromotionRequestRecord, runner: any) -> any:
        logger.info(f"Running direct promotion for {request.request_id}")
        return runner._run_standard_promotion(request)
