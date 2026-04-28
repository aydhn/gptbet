from sports_signal_bot.approvals.contracts import RequestType, OperatorIdentityRecord

# Simple permission mapping
ROLE_PERMISSIONS = {
    "admin": list(RequestType),  # Can do everything
    "senior_operator": [
        RequestType.approve_high_risk_decision,
        RequestType.approve_refresh_plan,
        RequestType.approve_freeze_release,
        RequestType.approve_dispatch_override,
        RequestType.approve_mode_switch,
        RequestType.acknowledge_alarm,
        RequestType.defer_manual_review,
        RequestType.create_manual_override,
        RequestType.revoke_override
    ],
    "operator": [
        RequestType.acknowledge_alarm,
        RequestType.defer_manual_review,
        # Typically can review but maybe not approve high-risk stuff natively
        # unless it's a low-risk decision, but we'll map high_risk to senior
    ],
    "reviewer": [
        RequestType.defer_manual_review
    ]
}

def check_permission(operator: OperatorIdentityRecord, action_type: RequestType) -> bool:
    """Check if the operator's role allows the requested action type."""
    if not operator.active:
        return False

    allowed_actions = ROLE_PERMISSIONS.get(operator.role, [])
    return action_type in allowed_actions

def assert_permission(operator: OperatorIdentityRecord, action_type: RequestType) -> None:
    """Raise an error if permission is denied."""
    if not check_permission(operator, action_type):
        raise PermissionError(f"Operator '{operator.operator_id}' with role '{operator.role}' is not allowed to perform '{action_type.value}'")
