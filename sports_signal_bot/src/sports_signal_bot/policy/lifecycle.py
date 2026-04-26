from typing import Dict, Any, List
from sports_signal_bot.policy.contracts import PolicySignalStatus, PolicyLifecycleRecord

class LifecycleManager:
    @staticmethod
    def get_allowed_transitions() -> Dict[PolicySignalStatus, List[PolicySignalStatus]]:
        return {
            PolicySignalStatus.PENDING: [PolicySignalStatus.SCORED, PolicySignalStatus.INVALID],
            PolicySignalStatus.SCORED: [
                PolicySignalStatus.BELOW_THRESHOLD,
                PolicySignalStatus.NO_BET_ZONE,
                PolicySignalStatus.WEAK_SIGNAL,
                PolicySignalStatus.CANDIDATE,
                PolicySignalStatus.BLOCKED,
                PolicySignalStatus.REJECTED
            ],
            PolicySignalStatus.CANDIDATE: [
                PolicySignalStatus.APPROVED,
                PolicySignalStatus.BLOCKED,
                PolicySignalStatus.NO_BET_ZONE, # E.g., due to late news
                PolicySignalStatus.EXPIRED,
                PolicySignalStatus.OVERRIDDEN
            ],
            PolicySignalStatus.APPROVED: [
                PolicySignalStatus.BLOCKED,
                PolicySignalStatus.EXPIRED,
                PolicySignalStatus.OVERRIDDEN
            ],
            PolicySignalStatus.WEAK_SIGNAL: [
                PolicySignalStatus.REJECTED,
                PolicySignalStatus.EXPIRED
            ],
            PolicySignalStatus.BELOW_THRESHOLD: [
                PolicySignalStatus.EXPIRED
            ],
            PolicySignalStatus.NO_BET_ZONE: [
                PolicySignalStatus.EXPIRED,
                PolicySignalStatus.OVERRIDDEN
            ],
            PolicySignalStatus.BLOCKED: [
                PolicySignalStatus.OVERRIDDEN
            ],
            PolicySignalStatus.REJECTED: [],
            PolicySignalStatus.INVALID: [],
            PolicySignalStatus.EXPIRED: [],
            PolicySignalStatus.OVERRIDDEN: []
        }

    @staticmethod
    def is_transition_valid(current: PolicySignalStatus, target: PolicySignalStatus) -> bool:
        allowed = LifecycleManager.get_allowed_transitions().get(current, [])
        return target in allowed
