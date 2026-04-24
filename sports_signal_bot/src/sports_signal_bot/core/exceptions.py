class BaseBotError(Exception):
    """Base exception for all sports signal bot errors."""
    pass

class ConfigError(BaseBotError):
    """Raised when there is an issue with configuration."""
    pass

class DataError(BaseBotError):
    """Raised when there is an issue with data loading or processing."""
    pass

class PipelineError(BaseBotError):
    """Raised when there is an issue in the execution pipeline."""
    pass
