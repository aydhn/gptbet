from sports_signal_bot.source_selection.catalog import SourceCatalog, SourceCatalogEntry
from sports_signal_bot.source_selection.metadata import SourceMetadataLoader, SourceMetadataRecord
from sports_signal_bot.source_selection.scoring import SourceTrustScorer
from sports_signal_bot.source_selection.chain import SourcePolicyChain
from sports_signal_bot.source_selection.contracts import SourcePolicyDefinition
from sports_signal_bot.source_selection.runner import SourceSelectionRunner

class MockLoader(SourceMetadataLoader):
    def load_metadata(self, source_name: str, event_id: str, sport: str, market_type: str) -> SourceMetadataRecord:
        meta = super().load_metadata(source_name, event_id, sport, market_type)
        if source_name == "bad":
            meta.refresh_info.is_stale_flag = True
            # To trigger QualityThresholdPolicy max_model_age_days
            meta.refresh_info.last_model_refresh_timestamp = None
        return meta

def test_source_selection_runner(tmp_path):
    catalog = SourceCatalog([
        SourceCatalogEntry(source_name="good", source_family="f", supported_sports=["s"], supported_markets=["m"]),
        SourceCatalogEntry(source_name="bad", source_family="f", supported_sports=["s"], supported_markets=["m"]),
    ])

    loader = MockLoader()
    scorer = SourceTrustScorer()

    defs = [
        SourcePolicyDefinition(policy_name="BasicAvailabilityPolicy"),
        SourcePolicyDefinition(policy_name="QualityThresholdPolicy", parameters={"min_trust_score": 0.3, "max_model_age_days": 30})
    ]
    chain = SourcePolicyChain(defs)

    runner = SourceSelectionRunner(
        catalog=catalog,
        metadata_loader=loader,
        scorer=scorer,
        policy_chain=chain,
        manifest_dir=tmp_path / "manifests",
        report_dir=tmp_path / "reports"
    )

    manifest = runner.run_selection("e", "s", "m")

    assert manifest.summary.total_candidates == 2
    # 'bad' has missing refresh_timestamp -> age 999 -> drops it
    assert manifest.summary.eligible_count == 1
    assert "good" in manifest.selected_sources
    assert "bad" not in manifest.selected_sources
