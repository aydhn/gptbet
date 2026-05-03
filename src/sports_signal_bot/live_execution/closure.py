from .contracts import SupervisedClosureControllerRecord, ClosureStatus, CompletionClass

def start_closure_verification_session(lane_ref: str, req_signals: list) -> SupervisedClosureControllerRecord:
    return SupervisedClosureControllerRecord(
        controller_id=f"clos_{lane_ref}",
        lane_ref=lane_ref,
        closure_session_ref="sess_1",
        required_closure_signals=req_signals,
        closure_status=ClosureStatus.PENDING
    )

def verify_runtime_closure(controller: SupervisedClosureControllerRecord, signals_found: list) -> CompletionClass:
    missing = [s for s in controller.required_closure_signals if s not in signals_found]
    if missing:
        controller.closure_status = ClosureStatus.FAILED
        controller.warnings.append(f"Missing signals: {missing}")
        return CompletionClass.NOT_VERIFIED

    controller.closure_status = ClosureStatus.CLEAN
    return CompletionClass.VERIFIED
