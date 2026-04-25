from typing import Any, Dict, List

from sports_signal_bot.research.contracts import (PeriodPerformanceRecord,
                                                  PeriodRunRecord,
                                                  TimeSliceSummaryRecord)
from sports_signal_bot.research.stability import flag_time_slice_instability


class TimeSliceReporter:
    """Generates time-sliced reports across periods."""

    def generate_report(
        self, scenario_id: str, records: List[PeriodRunRecord]
    ) -> TimeSliceSummaryRecord:

        perf_records = []
        log_loss_trend = {}
        accuracy_trend = {}

        cumulative_metrics = {}
        cumulative_counts = {}

        for r in records:
            if r.status != "success":
                continue

            metrics = r.evaluation_summary.get("metrics_by_source", {})
            num_events = r.evaluation_summary.get("num_events_evaluated", 0)

            # Find best source by log loss
            best_source = "none"
            best_ll = 999.0
            for src, m in metrics.items():
                if "log_loss" in m and m["log_loss"] < best_ll:
                    best_ll = m["log_loss"]
                    best_source = src

            p_rec = PeriodPerformanceRecord(
                period_id=r.period_id,
                metrics_by_source=metrics,
                best_source=best_source,
                num_events_evaluated=num_events,
            )
            perf_records.append(p_rec)

            # Build trends and cumulative
            for src, m in metrics.items():
                if src not in log_loss_trend:
                    log_loss_trend[src] = []
                    accuracy_trend[src] = []
                    cumulative_metrics[src] = {"log_loss": 0.0, "accuracy": 0.0}
                    cumulative_counts[src] = 0

                if "log_loss" in m:
                    log_loss_trend[src].append(m["log_loss"])
                    cumulative_metrics[src]["log_loss"] += m["log_loss"] * num_events
                if "accuracy" in m:
                    accuracy_trend[src].append(m["accuracy"])
                    cumulative_metrics[src]["accuracy"] += m["accuracy"] * num_events

                cumulative_counts[src] += num_events

        # Finalize cumulative
        leaderboard = {}
        for src in cumulative_metrics:
            if cumulative_counts[src] > 0:
                leaderboard[src] = {
                    "log_loss": cumulative_metrics[src]["log_loss"]
                    / cumulative_counts[src],
                    "accuracy": cumulative_metrics[src]["accuracy"]
                    / cumulative_counts[src],
                }

        warnings = flag_time_slice_instability(perf_records)

        return TimeSliceSummaryRecord(
            scenario_id=scenario_id,
            period_performances=perf_records,
            log_loss_trend=log_loss_trend,
            accuracy_trend=accuracy_trend,
            brier_trend={},  # Omitted for brevity
            coverage_trend={},
            cumulative_leaderboard=leaderboard,
            warnings=warnings,
        )
