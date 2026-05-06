class BaseRegionalHardeningStrategy:
    def __init__(self, config: dict):
        self.config = config

    def apply(self, context):
        raise NotImplementedError
