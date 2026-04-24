from typing import Dict, List, Optional
import pandas as pd
from sports_signal_bot.features.registry import FeatureRegistry
from sports_signal_bot.features.contracts import FeatureBuildContext
from sports_signal_bot.features.assembler import FeatureSetAssembler
from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.features.availability import generate_availability_summary

logger = get_logger("FeatureFactory")

class FeatureFactory:
    """Orchestrates building feature matrices from a set of builders."""

    def __init__(self, registry: FeatureRegistry):
        self.registry = registry

    def build_feature_matrix(self, context: FeatureBuildContext, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Builds the feature matrix using the specified builders in the context.
        """
        active_builders = self._get_active_builders(context)

        if not active_builders:
            logger.warning(f"No builders selected for sport {context.sport}. Returning empty matrix.")
            return pd.DataFrame()

        assembler = FeatureSetAssembler()

        missing_sources_all = set()
        skipped_builders = []
        builder_outputs = {}

        for builder in active_builders:
            logger.info(f"Running builder: {builder.name}")
            try:
                # Check required inputs
                missing_inputs = [inp for inp in builder.required_inputs if inp not in data]
                if missing_inputs:
                    logger.warning(f"Builder {builder.name} skipped. Missing inputs: {missing_inputs}")
                    missing_sources_all.update(missing_inputs)
                    skipped_builders.append(builder.name)
                    continue

                builder_df = builder.build(context, data)
                assembler.add_feature_set(builder.name, builder_df)
                builder_outputs[builder.name] = builder_df

            except Exception as e:
                logger.error(f"Error running builder {builder.name}: {e}")

        # Optional: in a real runner this path would be injected, we use a default here for tracking
        generate_availability_summary(
            run_id=context.run_id,
            builder_outputs=builder_outputs,
            missing_sources=list(missing_sources_all),
            skipped_builders=skipped_builders,
            output_path=f"data/processed/manifests/features_{context.run_id}"
        )

        return assembler.assemble(context.null_policy)

    def _get_active_builders(self, context: FeatureBuildContext):
        """Resolves which builders to run based on context includes/excludes and sport."""
        all_builders = self.registry.list_builders(sport=context.sport)

        # Filter by includes/excludes if specified at the family level
        # For simplicity, we assume include/exclude refers to builder 'family'

        if context.include_feature_families:
            all_builders = [b for b in all_builders if b.family in context.include_feature_families]

        if context.exclude_feature_families:
            all_builders = [b for b in all_builders if b.family not in context.exclude_feature_families]

        return all_builders
