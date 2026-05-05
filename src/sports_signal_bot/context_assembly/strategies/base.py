class BaseContextAssemblyStrategy:
    def __init__(self, config: dict):
        self.config = config

    def apply_trace_rules(self, route):
        pass

    def apply_freshness_rules(self, case):
        pass

    def apply_exchange_rules(self, case):
        pass

    def apply_context_rules(self, bundle):
        pass
