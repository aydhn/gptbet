from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
from .contracts import (
    ExceptionRegistryFederationRecord,
    FederatedExceptionRegistryNodeRecord,
    ExceptionFederationLinkRecord,
    ExceptionFederationCurrentnessRecord,
    ExceptionFederationExpiryRecord,
    ExceptionFederationSupersessionRecord,
    ExceptionFederationVisibilityRecord,
    ExceptionFederationHealthRecord,
    ExceptionFederationManifestRecord,
    ExceptionFederationWarningRecord,
    ExceptionEntryProjectionStatus
)

def build_exception_registry_federation(federation_id: str, family: str) -> ExceptionRegistryFederationRecord:
    health = ExceptionFederationHealthRecord(is_healthy=True)
    return ExceptionRegistryFederationRecord(
        exception_federation_id=federation_id,
        federation_family=family,
        currentness_policy_ref="default_currentness_policy",
        expiry_policy_ref="default_expiry_policy",
        supersession_policy_ref="default_supersession_policy",
        health_status=health
    )

def add_exception_federation_link(federation: ExceptionRegistryFederationRecord, link: ExceptionFederationLinkRecord) -> ExceptionRegistryFederationRecord:
    federation.active_link_refs.append(link.link_id)
    return federation

def project_exception_currentness(federation: ExceptionRegistryFederationRecord, exception_ref: str) -> ExceptionEntryProjectionStatus:
    # Dummy implementation for now
    return ExceptionEntryProjectionStatus.PROJECTED_CURRENT_EXCEPTION

def validate_exception_expiry_across_federation(federation: ExceptionRegistryFederationRecord, exception_ref: str) -> bool:
    return True

def summarize_exception_federation_health(federation: ExceptionRegistryFederationRecord) -> ExceptionFederationHealthRecord:
    return federation.health_status
