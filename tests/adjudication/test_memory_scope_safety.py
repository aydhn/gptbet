import pytest
from sports_signal_bot.adjudication.contracts import KnowledgeScopeRecord, KnowledgeScopeType
from sports_signal_bot.adjudication.scopes import ScopeManager
from sports_signal_bot.adjudication.validators import AdjudicationGuardrails

def test_scope_safety():
    valid_scope = ScopeManager.build_knowledge_scope(
        scope_type=KnowledgeScopeType.single_entity,
        target_value="m1"
    )
    assert ScopeManager.validate_scope_safety(valid_scope)

    invalid_scope = ScopeManager.build_knowledge_scope(
        scope_type=KnowledgeScopeType.single_entity,
        target_value=""
    )
    assert not ScopeManager.validate_scope_safety(invalid_scope)

    global_advisory = ScopeManager.build_knowledge_scope(
        scope_type=KnowledgeScopeType.global_advisory_only,
        target_value=""
    )
    assert AdjudicationGuardrails.check_memory_scope_not_overbroad(global_advisory)

    global_auto_apply = ScopeManager.build_knowledge_scope(
        scope_type=KnowledgeScopeType.global_advisory_only,
        target_value="",
        constraints={"auto_apply": True}
    )
    assert not AdjudicationGuardrails.check_memory_scope_not_overbroad(global_auto_apply)
