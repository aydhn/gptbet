class SmokeRunnerV2:
    def __init__(self, test_runner):
        self.test_runner = test_runner

    def run_smoke_suite(self):
        # Maps to running pytest with smoke tag
        return self.test_runner.run_by_tags(["smoke"])
