from abc import ABC, abstractmethod

from sports_signal_bot.release_management.contracts import PromotionRequestRecord


class ReleaseStrategy(ABC):
    @abstractmethod
    def handle_request(self, request: PromotionRequestRecord, registry_or_runner: any) -> any:
        pass
