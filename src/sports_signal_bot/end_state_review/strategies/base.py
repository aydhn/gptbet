from abc import ABC, abstractmethod
from typing import Any

class BaseEndStateReviewStrategy(ABC):

    @abstractmethod
    def evaluate_assurance_federation(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def evaluate_closure_mesh(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def evaluate_assurance_exchange(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def evaluate_end_state_review(self, *args, **kwargs) -> Any:
        pass
