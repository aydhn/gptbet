from .contracts import ExecutionTokenRenewalRecord, RenewalStatus
import datetime

def request_renewal(lane_ref: str, prior_token: str) -> ExecutionTokenRenewalRecord:
    return ExecutionTokenRenewalRecord(
        renewal_id=f"ren_{lane_ref}_{datetime.datetime.now().timestamp()}",
        prior_token_ref=prior_token,
        lane_ref=lane_ref,
        renewal_request_ref="req_1",
        renewal_decision_ref="dec_pending",
        renewal_status=RenewalStatus.REQUESTED
    )

def decide_renewal(renewal: ExecutionTokenRenewalRecord, approve: bool, tighter_scope: bool = False) -> ExecutionTokenRenewalRecord:
    if approve:
        if tighter_scope:
            renewal.renewal_status = RenewalStatus.APPROVED_TIGHTER
        else:
            renewal.renewal_status = RenewalStatus.APPROVED
        renewal.new_token_ref = f"token_new_{renewal.prior_token_ref}"
    else:
        renewal.renewal_status = RenewalStatus.DENIED
    return renewal
