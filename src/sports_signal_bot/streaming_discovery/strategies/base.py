from abc import ABC, abstractmethod
from typing import List
from ..contracts import AdaptiveRoutingProfileRecord

class BaseStreamingRoutingStrategy(ABC):
    @abstractmethod
    def get_profile(self) -> AdaptiveRoutingProfileRecord:
        pass
