from .contracts import *

def build_successor_federation_council(council_id: str, family: SuccessorCouncilFamily) -> SuccessorFederationCouncilRecord:
    return SuccessorFederationCouncilRecord(
        successor_federation_council_id=council_id,
        council_family=family
    )

def open_successor_federation_case(council: SuccessorFederationCouncilRecord, case_id: str, family: SuccessorCaseFamily):
    case = SuccessorFederationCaseRecord(
        successor_case_id=case_id,
        case_family=family
    )
    council.cases.append(case)
    return case

def resolve_successor_federation_case(case: SuccessorFederationCaseRecord, convergence: SuccessorConvergenceBand, decision: SuccessorCouncilDecision):
    case.convergence_state = convergence
    case.decision = decision
    if convergence == SuccessorConvergenceBand.stable_convergence:
        case.case_status = SuccessorCaseStatus.case_decided
    else:
        case.case_status = SuccessorCaseStatus.case_decided_with_caveats
        case.warnings.append("Case resolved with weak or bounded convergence. Strong hints capped.")
