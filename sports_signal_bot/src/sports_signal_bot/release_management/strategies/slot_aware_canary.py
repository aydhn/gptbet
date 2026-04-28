from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.release_management.contracts import PromotionRequestRecord
from sports_signal_bot.release_management.strategies.base import ReleaseStrategy

logger = get_logger("SlotAwareCanaryStrategy")


class SlotAwareCanaryStrategy(ReleaseStrategy):
    def handle_request(self, request: PromotionRequestRecord, runner: any) -> any:
        logger.info(f"Running slot aware canary strategy for {request.request_id}")
        # Custom logic for checking slots could go here before handing off to runner
        return runner._run_standard_promotion(request)
