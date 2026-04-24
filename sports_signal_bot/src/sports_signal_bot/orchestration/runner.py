import logging
from datetime import datetime
import pandas as pd
import numpy as np
from typing import Dict, Any

from sports_signal_bot.data.mock_providers import MockScheduleProvider, MockOddsProvider
from sports_signal_bot.features.registry import FeatureRegistry
from sports_signal_bot.models.dummy_predictor import DummyPredictor
from sports_signal_bot.notifications.telegram_stub import TelegramNotifierStub
from sports_signal_bot.utils.evaluation import EvaluationHelper
from sports_signal_bot.core.logger import get_logger

logger = get_logger("SmokeRunner")

class SmokeRunner:
    def __init__(self):
        self.schedule_provider = MockScheduleProvider()
        self.odds_provider = MockOddsProvider()
        self.feature_registry = FeatureRegistry()
        self.model = DummyPredictor()
        self.notifier = TelegramNotifierStub()
        self.evaluator = EvaluationHelper()

    def run(self) -> Dict[str, Any]:
        logger.info("Starting Smoke Pipeline...")

        # 1. Get schedule
        events = self.schedule_provider.get_events(datetime.now(), datetime.now())
        logger.info(f"Fetched {len(events)} events.")

        # 2. Get odds
        event_ids = [e.event_id for e in events]
        odds = self.odds_provider.get_odds(event_ids)
        logger.info(f"Fetched odds for {len(odds)} events.")

        # 3. Build features
        event_dicts = [{"event_id": e.event_id, "home_team": e.home_team, "away_team": e.away_team} for e in events]
        features = pd.DataFrame(event_dicts)
        features["mock_f1"] = 1.0
        features["mock_f2"] = 0.5
        logger.info(f"Built feature matrix of shape {features.shape}.")

        # 4. Mock Training
        X_train = pd.DataFrame({"mock_f1": [1.0, 0.5, 0.8, 0.2], "mock_f2": [0.2, 0.8, 0.5, 0.9]})
        y_train = pd.Series([0, 1, 0, 1])
        logger.info("Training dummy model...")
        self.model.fit(X_train, y_train)

        # 5. Predict
        X_pred = features[["mock_f1", "mock_f2"]]
        predictions = self.model.predict_proba(X_pred)
        logger.info(f"Generated predictions: {predictions}")

        # 6. Evaluate
        # In smoke test, let's assume y_true is [1]
        y_true = np.array([1])
        metrics = self.evaluator.evaluate_predictions(y_true, predictions)
        logger.info(f"Evaluation Metrics: {metrics}")

        # 7. Notify
        summary = f"Smoke run completed. Events: {len(events)}\nMetrics: {metrics}"
        self.notifier.send_message(summary)

        logger.info("Smoke Pipeline completed successfully.")
        return {"status": "success", "metrics": metrics, "predictions": predictions.tolist()}
