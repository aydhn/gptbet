import uuid
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional

from .contracts import (
    SourceEligibilityRecord,
    SourceSelectionDecision,
    SourceSelectionManifest,
    SourceSelectionDiagnostics
)
from .catalog import SourceCatalog
from .metadata import SourceMetadataLoader
from .scoring import SourceTrustScorer
from .chain import SourcePolicyChain
from .manifests import ManifestWriter
from .diagnostics import DiagnosticsBuilder
from .reporting import SelectionReporter

class SourceSelectionRunner:
    def __init__(self,
                 catalog: SourceCatalog,
                 metadata_loader: SourceMetadataLoader,
                 scorer: SourceTrustScorer,
                 policy_chain: SourcePolicyChain,
                 manifest_dir: Path,
                 report_dir: Path):
        self.catalog = catalog
        self.metadata_loader = metadata_loader
        self.scorer = scorer
        self.policy_chain = policy_chain
        self.manifest_writer = ManifestWriter(manifest_dir)
        self.reporter = SelectionReporter(report_dir)
        self.diagnostics_builder = DiagnosticsBuilder()

    def run_selection(self,
                      event_id: str,
                      sport: str,
                      market_type: str,
                      active_regimes: Optional[List[str]] = None) -> SourceSelectionManifest:

        start_time = time.time()
        run_id = f"sel_{uuid.uuid4().hex[:8]}"

        # 1. Identify candidates
        candidates = self.catalog.get_candidates(sport, market_type)

        # 2. Load metadata and init records
        metadata_map = {}
        eligibility_records = []

        for cand in candidates:
            meta = self.metadata_loader.load_metadata(cand.source_name, event_id, sport, market_type)
            metadata_map[cand.source_name] = meta

            record = SourceEligibilityRecord(
                event_id=event_id,
                sport=sport,
                market_type=market_type,
                source_name=cand.source_name,
                source_family=cand.source_family,
                is_available=True, # Start optimistic
                is_eligible=True
            )

            # 3. Score
            trust_score = self.scorer.combine_trust_components(meta, active_regimes)
            record.trust_score = trust_score
            record.eligibility_score = trust_score.total_trust_score

            eligibility_records.append(record)

        # 4. Apply Policy Chain
        context = {'fallback_used': False, 'active_regimes': active_regimes}
        self.policy_chain.run_chain(metadata_map, eligibility_records, context)

        # 5. Build Decisions
        decisions = []
        selected_sources = []
        for r in eligibility_records:
            d = SourceSelectionDecision(
                source_name=r.source_name,
                is_selected=r.is_eligible,
                reasoning="Eligible" if r.is_eligible else f"Excluded: {', '.join([ex.reason_code for ex in r.exclusion_reasons])}",
                eligibility_record=r
            )
            decisions.append(d)
            if r.is_eligible:
                selected_sources.append(r.source_name)

        # 6. Diagnostics & Summary
        summary = self.diagnostics_builder.build_summary(decisions, context)
        diag = SourceSelectionDiagnostics(
            execution_time_ms=(time.time() - start_time) * 1000.0,
            fallback_decisions=["Fallback was triggered."] if context.get('fallback_used') else []
        )

        # 7. Manifest
        manifest = SourceSelectionManifest(
            run_id=run_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_id=event_id,
            sport=sport,
            market_type=market_type,
            selected_sources=selected_sources,
            decisions=decisions,
            summary=summary,
            diagnostics=diag
        )

        self.manifest_writer.write_manifest(manifest)
        self.reporter.export_reports(manifest)

        return manifest
