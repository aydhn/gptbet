from datetime import datetime, timedelta

from sports_signal_bot.providers.contracts import DataFamily
from sports_signal_bot.providers.requests import (
    ProviderRequestRecord,
    validate_provider_request,
)


def test_provider_request_validation():
    now = datetime.utcnow()
    req = ProviderRequestRecord(
        sport="football",
        data_family=DataFamily.FIXTURES,
        start_date=now,
        end_date=now + timedelta(days=1),
    )
    assert validate_provider_request(req) == True

    req_invalid = ProviderRequestRecord(
        sport="football",
        data_family=DataFamily.FIXTURES,
        start_date=now + timedelta(days=1),
        end_date=now,
    )
    assert validate_provider_request(req_invalid) == False
