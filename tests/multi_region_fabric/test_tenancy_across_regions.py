from sports_signal_bot.multi_region_fabric.tenancy import validate_tenant_region_boundary

def test_validate_tenant_region_boundary():
    assert validate_tenant_region_boundary("tenant1", "us-east")
