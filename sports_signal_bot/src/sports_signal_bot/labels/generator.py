from datetime import datetime
from typing import Dict, List, Optional

from sports_signal_bot.labels.contracts import LabelRecord, LabelValidityStatus
from sports_signal_bot.labels.naming import generate_label_name
from sports_signal_bot.markets.definitions import MarketDefinition
from sports_signal_bot.results.contracts import EventResultRecord
from sports_signal_bot.results.resolvers import resolve_market


class LabelGenerator:
    def __init__(
        self,
        market_definitions: List[MarketDefinition],
        line_sets: Optional[Dict[str, List[float]]] = None,
    ):
        self.markets = {m.market_type: m for m in market_definitions}
        self.line_sets = line_sets or {}

    def generate(self, result: EventResultRecord) -> List[LabelRecord]:
        labels = []
        for m_type, market_def in self.markets.items():
            if market_def.sport != result.sport:
                continue

            lines = self.line_sets.get(m_type, [None])
            if not lines:
                lines = [None]  # Ensure at least one attempt if no lines defined

            for line in lines:
                label_name = generate_label_name(m_type, line)

                try:
                    target_text, status, reason = resolve_market(
                        market_def.settlement_rule_name, result, line
                    )
                    class_idx = None
                    if (
                        target_text
                        and market_def.selection_schema
                        and target_text in market_def.selection_schema
                    ):
                        class_idx = market_def.selection_schema.index(target_text)

                    rec = LabelRecord(
                        event_id=result.event_id,
                        market_type=m_type,
                        label_name=label_name,
                        target_text=target_text,
                        class_index=class_idx,
                        line_value=line,
                        validity_status=status,
                        invalid_reason=reason,
                        generated_at_utc=datetime.utcnow(),
                    )
                    labels.append(rec)
                except Exception as e:
                    labels.append(
                        LabelRecord(
                            event_id=result.event_id,
                            market_type=m_type,
                            label_name=label_name,
                            validity_status=LabelValidityStatus.INVALID,
                            invalid_reason=str(e),
                            generated_at_utc=datetime.utcnow(),
                        )
                    )
        return labels
