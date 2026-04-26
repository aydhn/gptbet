import datetime
from typing import List, Dict
from sports_signal_bot.portfolio.contracts import PortfolioCandidateRecord, ExposureBucketRecord

def assign_time_buckets(candidates: List[PortfolioCandidateRecord], bucket_minutes: int = 60) -> List[ExposureBucketRecord]:
    if not candidates:
        return []

    # Sort chronologically
    sorted_candidates = sorted(candidates, key=lambda c: c.event_datetime_utc)

    buckets = []
    current_bucket_start = None
    current_bucket_candidates = []

    for candidate in sorted_candidates:
        if current_bucket_start is None:
            # Align to nice boundary (e.g., hour) if needed, but for simplicity, just use the first event's time
            # Round down to nearest bucket_minutes
            dt = candidate.event_datetime_utc
            minutes = (dt.hour * 60 + dt.minute) // bucket_minutes * bucket_minutes
            h, m = divmod(minutes, 60)
            current_bucket_start = dt.replace(hour=h, minute=m, second=0, microsecond=0)

        bucket_end = current_bucket_start + datetime.timedelta(minutes=bucket_minutes)

        if candidate.event_datetime_utc < bucket_end:
            current_bucket_candidates.append(candidate)
        else:
            # Finalize current bucket
            if current_bucket_candidates:
                buckets.append(
                    ExposureBucketRecord(
                        bucket_id=current_bucket_start.isoformat(),
                        start_time=current_bucket_start,
                        end_time=bucket_end,
                        candidates=current_bucket_candidates,
                        total_proposed_fraction=sum(c.proposed_stake_fraction for c in current_bucket_candidates),
                        total_allocated_fraction=0.0
                    )
                )

            # Start new bucket
            dt = candidate.event_datetime_utc
            minutes = (dt.hour * 60 + dt.minute) // bucket_minutes * bucket_minutes
            h, m = divmod(minutes, 60)
            current_bucket_start = dt.replace(hour=h, minute=m, second=0, microsecond=0)
            bucket_end = current_bucket_start + datetime.timedelta(minutes=bucket_minutes)
            current_bucket_candidates = [candidate]

    # Finalize last bucket
    if current_bucket_candidates:
        bucket_end = current_bucket_start + datetime.timedelta(minutes=bucket_minutes)
        buckets.append(
            ExposureBucketRecord(
                bucket_id=current_bucket_start.isoformat(),
                start_time=current_bucket_start,
                end_time=bucket_end,
                candidates=current_bucket_candidates,
                total_proposed_fraction=sum(c.proposed_stake_fraction for c in current_bucket_candidates),
                total_allocated_fraction=0.0
            )
        )

    return buckets
