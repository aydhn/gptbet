from typing import Dict, Any, List
from datetime import datetime
from .base import BaseEcosystemSyncStrategy
from ..contracts import (
    EcosystemSyncRunRecord,
    DiscoverySubscriptionRecord,
    SubscriptionFamily,
    SubscriptionStatus,
    SyncMode,
    CatalogOverlayRecord,
    OverlayFamily,
    EcosystemRoutingRecord,
    RoutingCandidateRecord,
    RoutingStatus,
    RoutingScoreBreakdownRecord
)
from ..subscriptions import SubscriptionRegistry
from ..sync import EcosystemSyncPlanner, SyncExecutor
from ..overlays import OverlayRebuilder
from ..routing import EcosystemRoutingEngine
from ..cache import RoutingCacheBuilder

class ConservativeSyncRoutingStrategy(BaseEcosystemSyncStrategy):
    """Conservative strategy: heavy trust and quarantine discipline."""

    def get_strategy_name(self) -> str:
        return "ConservativeSyncRoutingStrategy"

    def execute_pass(self, config: Dict[str, Any]) -> Dict[str, Any]:
        # Initialize components
        registry = SubscriptionRegistry()
        planner = EcosystemSyncPlanner(registry)
        executor = SyncExecutor(registry)
        overlay_rebuilder = OverlayRebuilder(config.get("overlay_merge_rules", {}))
        routing_engine = EcosystemRoutingEngine(config)
        cache_builder = RoutingCacheBuilder({})

        # 1. Setup mock subscription
        sub = DiscoverySubscriptionRecord(
            subscription_id="sub_trusted_registry_1",
            subscription_family=SubscriptionFamily.REGISTRY_CATALOG,
            target_catalog_ref="target_catalog_a",
            target_scope={},
            subscribed_families=[SubscriptionFamily.REGISTRY_CATALOG],
            refresh_policy={"refresh_interval_hints": {"interval_seconds": 3600}, "freshness_thresholds": {}, "allowed_target_families": [], "trust_downgrade_triggers": [], "stale_source_suppression_rules": {"threshold_seconds": 86400, "suppress": True}, "sync_retry_policy": {"max_attempts": 3, "backoff_factor": 2.0}, "supersession_required_families": [], "quarantine_on_mismatch_rules": {}, "source_visibility_restrictions": [], "overlay_merge_allowances": {"allow_downgrade": True}},
            trust_policy_ref="strict_trust",
            sync_mode=SyncMode.SCHEDULED,
            current_status=SubscriptionStatus.AWAITING_FIRST_SYNC,
            last_success_at=None,
            warnings=[]
        )
        registry.register(sub)

        # 2. Plan and Execute Sync
        plan = planner.build_sync_plan(SyncMode.SCHEDULED)

        run_record = EcosystemSyncRunRecord(
            run_id=f"run_{datetime.utcnow().timestamp()}",
            plan_id=plan.plan_id,
            status="running",
            start_time=datetime.utcnow()
        )

        results = []
        for sub_id in plan.subscriptions_to_sync:
            res = executor.execute_sync_step(sub_id)
            results.append(res)
            if res.get("lag_record"):
                run_record.lag_records.append(res["lag_record"])

        run_record.status = "success" if executor.validate_sync_results(results) else "failed"
        run_record.end_time = datetime.utcnow()

        # 3. Rebuild Overlays
        overlay = overlay_rebuilder.build_catalog_overlay("base_catalog", OverlayFamily.TRUST, ["target_catalog_a"])
        decision = overlay_rebuilder.merge_overlay_entries(overlay, [{"ref": "entry_1"}], "target_catalog_a")

        # 4. Routing
        candidate = RoutingCandidateRecord(
            candidate_ref="target_catalog_a",
            score_breakdown=RoutingScoreBreakdownRecord(base_score=0, components=[], total_score=85.0),
            penalties=[]
        )

        routing_record = EcosystemRoutingRecord(
            routing_id=f"route_{datetime.utcnow().timestamp()}",
            query_ref="query_registries",
            candidate_refs=[candidate],
            selected_route_refs=["target_catalog_a"],
            weighting_profile="conservative",
            trust_weight_summary=85.0,
            freshness_weight_summary=10.0,
            compatibility_weight_summary=5.0,
            routing_status=RoutingStatus.SELECTED,
            warnings=[]
        )

        # 5. Cache
        cache_builder.build_routing_cache("query_registries", routing_record)

        return {
            "strategy": self.get_strategy_name(),
            "run": run_record.model_dump(),
            "overlays_built": 1,
            "routing_status": routing_record.routing_status.value,
            "cache_state": cache_builder.summarize_cache_state()
        }
