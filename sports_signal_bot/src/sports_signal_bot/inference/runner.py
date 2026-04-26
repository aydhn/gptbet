import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional

from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.inference.contracts import (InferenceDecisionPacket,
                                                   InferenceMode,
                                                   InferenceReviewPacket,
                                                   InferenceRunContext,
                                                   InferenceSnapshotManifest,
                                                   PipelineStepResult)
from sports_signal_bot.inference.pipeline import InferencePipelineExecutor
from sports_signal_bot.inference.resolver import ArtifactResolver
from sports_signal_bot.inference.slots import SlotResolver
from sports_signal_bot.inference.universe import EventUniverseBuilder

logger = get_logger("InferenceRunner")


class InferenceRunner:
    def __init__(self, schedule_provider=None):
        self.universe_builder = EventUniverseBuilder(schedule_provider)
        self.slot_resolver = SlotResolver()
        self.artifact_resolver = ArtifactResolver()
        self.pipeline_executor = InferencePipelineExecutor()

    def run(
        self,
        sport: str,
        market: str,
        slot_name: Optional[str] = None,
        mode: str = "research_live_like_mode",
    ):
        run_timestamp = datetime.now(timezone.utc)
        run_id = f"inf_{run_timestamp.strftime('%Y%m%d%H%M%S')}"

        logger.info(
            f"Starting Inference Run: {run_id} | Sport: {sport} | Market: {market} | Slot: {slot_name} | Mode: {mode}"
        )

        # 1. Resolve Slot
        slot_def = None
        if slot_name:
            slot_def = self.slot_resolver.resolve_slot_definition(slot_name)
            logger.info(
                f"Resolved slot: {slot_def.name} (horizon: {slot_def.event_inclusion_horizon_hours}h)"
            )

        # 2. Setup Context
        context = InferenceRunContext(
            run_id=run_id,
            run_timestamp_utc=run_timestamp,
            slot_id=slot_name or "ad_hoc",
            target_date=run_timestamp.date().isoformat(),
            inference_mode=InferenceMode(mode),
            artifact_snapshot_policy=(
                slot_def.artifact_resolution_policy if slot_def else "latest_compatible"
            ),
            event_selection_policy="slot_window" if slot_def else "immediate",
        )

        # 3. Build Universe
        target_dt = run_timestamp
        lookahead = slot_def.lookahead_window_hours if slot_def else 12
        raw_universe = self.universe_builder.build_event_universe(
            target_dt, sport, lookahead
        )
        events = self.universe_builder.filter_pre_match_events(raw_universe, target_dt)
        events = self.universe_builder.filter_supported_markets(events, market)
        events = self.universe_builder.exclude_closed_or_invalid_events(events)

        if not events:
            logger.warning("Empty event universe after filtering. Aborting inference.")
            return None

        logger.info(f"Final event universe size: {len(events)}")

        # 4. Resolve Artifact Chain
        chain = self.artifact_resolver.resolve_chain(
            sport, market, policy=context.artifact_snapshot_policy
        )
        if not self.artifact_resolver.validate_artifact_chain(chain):
            logger.error("Invalid artifact chain. Aborting.")
            return None

        # 5. Execute Pipeline
        base_preds = self.pipeline_executor.run_base_inference(events, chain)
        final_preds = self.pipeline_executor.resolve_prediction_fallback(
            base_preds, chain
        )
        scores = self.pipeline_executor.generate_signal_scores(final_preds, chain)

        # 6. Build Packets
        decision_packets = []
        review_packets = []
        action_dist = {}

        for evt in events:
            probs = final_preds["predictions"].get(evt.event_id, {})
            score = scores.get(evt.event_id, 0.0)

            # Mock policy logic
            selected_side = max(probs, key=probs.get) if probs else None
            is_approved = score > 0.55
            action_class = "approved_candidate" if is_approved else "rejected_candidate"
            action_dist[action_class] = action_dist.get(action_class, 0) + 1

            d_packet = InferenceDecisionPacket(
                event_id=evt.event_id,
                sport=sport,
                market_type=market,
                teams=f"{evt.home_team} vs {evt.away_team}",
                final_probabilities=probs,
                selected_side=selected_side,
                signal_score=score,
                threshold_status="passed" if is_approved else "failed",
                policy_action_class=action_class,
                final_allocated_stake=1.0 if is_approved else 0.0,
                rationale_summary=f"Score {score:.2f} {'meets' if is_approved else 'below'} threshold",
                artifact_chain_summary={"source": final_preds["source"]},
            )
            decision_packets.append(d_packet)

            r_packet = InferenceReviewPacket(
                event_id=evt.event_id,
                sport=sport,
                market_type=market,
                threshold_rationale=f"Score {score:.2f} evaluated against dynamic regime thresholds.",
                portfolio_budget_notes="Unconstrained dummy portfolio",
            )
            review_packets.append(r_packet)

        # 7. Write Manifest
        manifest = InferenceSnapshotManifest(
            run_context=context,
            universe_size=len(events),
            resolved_artifact_chains={"primary": chain},
            fallback_counts={
                "calibrator_fallback": 1 if "calibrator" in str(chain.warnings) else 0
            },
            final_action_class_distribution=action_dist,
            warnings=chain.warnings,
        )

        # 8. Output
        out_dir = f"results/inference/{run_id}"
        os.makedirs(out_dir, exist_ok=True)

        with open(f"{out_dir}/decisions.json", "w") as f:
            json.dump([p.model_dump() for p in decision_packets], f, indent=2)

        with open(f"{out_dir}/manifest.json", "w") as f:
            # Need default=str for datetime serialization
            json.dump(manifest.model_dump(), f, indent=2, default=str)

        logger.info(f"Inference complete. Packets saved to {out_dir}")
        return manifest, decision_packets, review_packets
