from sports_signal_bot.multi_region_fabric.contracts import RegionFailoverRecord

FAILOVER_OUTCOMES = [
    "failover_not_permitted",
    "failover_review_only",
    "failover_assistance_only",
    "failover_prepared",
    "failover_executed_cautious",
    "failover_blocked_revalidation",
    "failover_reverted"
]

def evaluate_region_failover(src: str, tgt: str, revalidated: bool) -> RegionFailoverRecord:
    return RegionFailoverRecord(
        failover_id=f"fo_{src}_{tgt}",
        source_region=src,
        target_region=tgt,
        status="failover_prepared" if revalidated else "failover_blocked_revalidation",
        reason="Revalidation check"
    )

def prepare_failover_bundle(fo_id: str) -> dict:
    return {"ready": True}

def revalidate_after_failover(fo_id: str) -> bool:
    return True

def summarize_failover_readiness(fo: RegionFailoverRecord) -> str:
    return f"Failover status: {fo.status}"
