from .base import BaseRemediationStrategy

class ConservativeApprovalGatedCopilotStrategy(BaseRemediationStrategy):
    def __init__(self):
        super().__init__()
        self.name = "ConservativeApprovalGatedCopilotStrategy"

class BalancedRecoveryPreparationStrategy(BaseRemediationStrategy):
    def __init__(self):
        super().__init__()
        self.name = "BalancedRecoveryPreparationStrategy"

class FederationAwarePlaybookStrategy(BaseRemediationStrategy):
    def __init__(self):
        super().__init__()
        self.name = "FederationAwarePlaybookStrategy"

class RehearsalFirstStrategy(BaseRemediationStrategy):
    def __init__(self):
        super().__init__()
        self.name = "RehearsalFirstStrategy"

class GuardStrictSelfHealingPrepStrategy(BaseRemediationStrategy):
    def __init__(self):
        super().__init__()
        self.name = "GuardStrictSelfHealingPrepStrategy"
