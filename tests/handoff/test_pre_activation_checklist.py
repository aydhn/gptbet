from sports_signal_bot.handoff.checklists import build_pre_activation_checklist, validate_pre_activation_items

def test_build_pre_activation_checklist():
    context = {"gates_fresh": True, "approval_complete": True, "rollback_target_known": True, "docs_linked": True}
    checklist = build_pre_activation_checklist("h1", context)
    assert checklist.is_complete
    assert validate_pre_activation_items(checklist)

def test_build_pre_activation_checklist_incomplete():
    context = {"gates_fresh": True, "approval_complete": False, "rollback_target_known": True, "docs_linked": True}
    checklist = build_pre_activation_checklist("h1", context)
    assert not checklist.is_complete
    assert not validate_pre_activation_items(checklist)
