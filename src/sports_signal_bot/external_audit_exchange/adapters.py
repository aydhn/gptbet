from abc import ABC, abstractmethod
from typing import Dict, Any
from .contracts import ExternalAuditRequestRecord, ExternalAuditResponseRecord

class BaseExchangeAdapter(ABC):
    @abstractmethod
    def export_request(self, request: ExternalAuditRequestRecord) -> Dict[str, Any]:
        pass

    @abstractmethod
    def import_response(self, raw_response: Dict[str, Any]) -> ExternalAuditResponseRecord:
        pass

    @abstractmethod
    def validate_packet(self, packet: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def canonicalize_packet(self, packet: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def verify_response_integrity(self, response: ExternalAuditResponseRecord) -> bool:
        pass

    @abstractmethod
    def summarize_exchange(self, request: ExternalAuditRequestRecord, response: ExternalAuditResponseRecord) -> Dict[str, Any]:
        pass

class FilePacketExchangeAdapter(BaseExchangeAdapter):
    def export_request(self, request: ExternalAuditRequestRecord) -> Dict[str, Any]:
        return {"type": "file_packet", "payload": request.model_dump(mode="json")}

    def import_response(self, raw_response: Dict[str, Any]) -> ExternalAuditResponseRecord:
        return ExternalAuditResponseRecord(**raw_response["payload"])

    def validate_packet(self, packet: Dict[str, Any]) -> bool:
        return "payload" in packet

    def canonicalize_packet(self, packet: Dict[str, Any]) -> str:
        return str(packet)

    def verify_response_integrity(self, response: ExternalAuditResponseRecord) -> bool:
        return True

    def summarize_exchange(self, request: ExternalAuditRequestRecord, response: ExternalAuditResponseRecord) -> Dict[str, Any]:
        return {"request_id": request.external_request_id, "status": response.response_status}

class SignedJsonExchangeAdapter(BaseExchangeAdapter):
    def export_request(self, request: ExternalAuditRequestRecord) -> Dict[str, Any]:
        return {"type": "signed_json", "payload": request.model_dump(mode="json")}

    def import_response(self, raw_response: Dict[str, Any]) -> ExternalAuditResponseRecord:
        return ExternalAuditResponseRecord(**raw_response["payload"])

    def validate_packet(self, packet: Dict[str, Any]) -> bool:
        return "payload" in packet

    def canonicalize_packet(self, packet: Dict[str, Any]) -> str:
        return str(packet)

    def verify_response_integrity(self, response: ExternalAuditResponseRecord) -> bool:
        return True

    def summarize_exchange(self, request: ExternalAuditRequestRecord, response: ExternalAuditResponseRecord) -> Dict[str, Any]:
        return {"request_id": request.external_request_id, "status": response.response_status}

class AuditSnapshotExchangeAdapter(BaseExchangeAdapter):
    def export_request(self, request: ExternalAuditRequestRecord) -> Dict[str, Any]:
        return {"type": "audit_snapshot", "payload": request.model_dump(mode="json")}

    def import_response(self, raw_response: Dict[str, Any]) -> ExternalAuditResponseRecord:
        return ExternalAuditResponseRecord(**raw_response["payload"])

    def validate_packet(self, packet: Dict[str, Any]) -> bool:
        return "payload" in packet

    def canonicalize_packet(self, packet: Dict[str, Any]) -> str:
        return str(packet)

    def verify_response_integrity(self, response: ExternalAuditResponseRecord) -> bool:
        return True

    def summarize_exchange(self, request: ExternalAuditRequestRecord, response: ExternalAuditResponseRecord) -> Dict[str, Any]:
        return {"request_id": request.external_request_id, "status": response.response_status}

class NotarizationHookAdapter(BaseExchangeAdapter):
    def export_request(self, request: ExternalAuditRequestRecord) -> Dict[str, Any]:
        return {"type": "notarization_hook", "payload": request.model_dump(mode="json")}

    def import_response(self, raw_response: Dict[str, Any]) -> ExternalAuditResponseRecord:
        return ExternalAuditResponseRecord(**raw_response["payload"])

    def validate_packet(self, packet: Dict[str, Any]) -> bool:
        return "payload" in packet

    def canonicalize_packet(self, packet: Dict[str, Any]) -> str:
        return str(packet)

    def verify_response_integrity(self, response: ExternalAuditResponseRecord) -> bool:
        return True

    def summarize_exchange(self, request: ExternalAuditRequestRecord, response: ExternalAuditResponseRecord) -> Dict[str, Any]:
        return {"request_id": request.external_request_id, "status": response.response_status}

class ExternalVerifierPlaceholderAdapter(BaseExchangeAdapter):
    def export_request(self, request: ExternalAuditRequestRecord) -> Dict[str, Any]:
        return {"type": "external_verifier_placeholder", "payload": request.model_dump(mode="json")}

    def import_response(self, raw_response: Dict[str, Any]) -> ExternalAuditResponseRecord:
        return ExternalAuditResponseRecord(**raw_response["payload"])

    def validate_packet(self, packet: Dict[str, Any]) -> bool:
        return "payload" in packet

    def canonicalize_packet(self, packet: Dict[str, Any]) -> str:
        return str(packet)

    def verify_response_integrity(self, response: ExternalAuditResponseRecord) -> bool:
        return True

    def summarize_exchange(self, request: ExternalAuditRequestRecord, response: ExternalAuditResponseRecord) -> Dict[str, Any]:
        return {"request_id": request.external_request_id, "status": response.response_status}

class WitnessStatementExchangeAdapter(BaseExchangeAdapter):
    def export_request(self, request: ExternalAuditRequestRecord) -> Dict[str, Any]:
        return {"type": "witness_statement_exchange", "payload": request.model_dump(mode="json")}

    def import_response(self, raw_response: Dict[str, Any]) -> ExternalAuditResponseRecord:
        return ExternalAuditResponseRecord(**raw_response["payload"])

    def validate_packet(self, packet: Dict[str, Any]) -> bool:
        return "payload" in packet

    def canonicalize_packet(self, packet: Dict[str, Any]) -> str:
        return str(packet)

    def verify_response_integrity(self, response: ExternalAuditResponseRecord) -> bool:
        return True

    def summarize_exchange(self, request: ExternalAuditRequestRecord, response: ExternalAuditResponseRecord) -> Dict[str, Any]:
        return {"request_id": request.external_request_id, "status": response.response_status}
