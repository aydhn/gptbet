import pytest

def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: mark test as a smoke test")
    config.addinivalue_line("markers", "contract: mark test as a contract test")
    config.addinivalue_line("markers", "scenario: mark test as a scenario test")
    config.addinivalue_line("markers", "regression: mark test as a regression test")
    config.addinivalue_line("markers", "golden: mark test as a golden dataset test")
