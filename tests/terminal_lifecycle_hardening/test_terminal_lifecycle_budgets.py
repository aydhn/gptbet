import unittest
from src.sports_signal_bot.terminal_lifecycle_hardening.budgets import (
    build_terminal_lifecycle_budgets, measure_terminal_lifecycle_budget_consumption,
    summarize_terminal_lifecycle_budgets
)

class TestTerminalLifecycleBudgets(unittest.TestCase):
    def test_build_budgets(self):
        budgets = build_terminal_lifecycle_budgets()
        self.assertIn("closure_bundle_budgets", budgets)
        self.assertIn("deprecation_budgets", budgets)
        self.assertIn("maintenance_mode_budgets", budgets)
        self.assertIn("stewardship_budgets", budgets)

    def test_measure_consumption(self):
        consumptions = measure_terminal_lifecycle_budget_consumption()
        self.assertEqual(len(consumptions), 1)

    def test_summarize_budgets(self):
        summary = summarize_terminal_lifecycle_budgets()
        self.assertEqual(summary["total_budgets"], 4)
        self.assertEqual(summary["breaches"], 0)
        self.assertEqual(summary["status"], "healthy")
