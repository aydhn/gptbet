from sports_signal_bot.multi_region_fabric.shards import build_broker_shards, validate_shard_single_owner

def test_build_broker_shards():
    shard = build_broker_shards("s1", "execution_token_shard", "us-east", "c1")
    assert validate_shard_single_owner(shard)
