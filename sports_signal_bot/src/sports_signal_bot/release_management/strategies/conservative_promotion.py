from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.release_management.contracts import PromotionRequestRecord, RequestType
from sports_signal_bot.release_management.strategies.base import ReleaseStrategy

logger = get_logger("ConservativePromotionStrategy")


class ConservativePromotionStrategy(ReleaseStrategy):
    def handle_request(self, request: PromotionRequestRecord, runner: any) -> any:
        logger.info(f"Running conservative promotion strategy for {request.request_id}")

        if request.request_type == RequestType.promote_candidate_to_stable_direct:
            logger.error("Direct promotion to stable not allowed in conservative strategy.")
            return None

        if request.request_type == RequestType.promote_candidate_to_canary:
            return runner._run_standard_promotion(request)

        if request.request_type == RequestType.promote_canary_to_stable:
            # Here we would normally check if canary validation has passed.
            return runner._run_standard_promotion(request)

        return runner._run_standard_promotion(request)
