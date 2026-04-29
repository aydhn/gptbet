class RegressionRunner:
    def __init__(self, test_runner):
        self.test_runner = test_runner

    def run_regression_suite(self):
        # Maps to running pytest with regression tag
        return self.test_runner.run_by_tags(["regression"])
