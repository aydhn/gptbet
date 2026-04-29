from sports_signal_bot.providers.identities import EntityAliasRecord, resolve_team_alias


def test_identity_alias_resolution():
    aliases = [
        EntityAliasRecord(
            internal_id="int_1",
            entity_type="team",
            canonical_name="Arsenal",
            aliases=["Arsenal FC", "Gunners"],
        )
    ]
    res = resolve_team_alias("Arsenal FC", aliases)
    assert res.resolved_id == "int_1"

    res2 = resolve_team_alias("Unknown", aliases)
    assert res2.resolved_id is None
