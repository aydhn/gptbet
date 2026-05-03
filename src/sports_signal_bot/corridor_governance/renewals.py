from datetime import datetime
from sports_signal_bot.corridor_governance.contracts import TreatyRenewalRecord

def build_treaty_renewal_proposal(treaty_ref: str, renewal_time: datetime) -> TreatyRenewalRecord:
    return TreatyRenewalRecord(
        treaty_ref=treaty_ref,
        renewal_time=renewal_time
    )

def validate_treaty_renewal_scope(old_scope: str, new_scope: str) -> bool:
    # Simplified validation: new scope should not be broader than old scope
    return old_scope == new_scope
