from typing import Any, Dict, List, Optional

from sports_signal_bot.providers.requests import ProviderRequestRecord


class RoutingStrategy:
    def select_providers(
        self, request: ProviderRequestRecord, available_providers: List[Dict[str, Any]]
    ) -> List[str]:
        raise NotImplementedError


class PrimaryThenFallbackStrategy(RoutingStrategy):
    def select_providers(
        self, request: ProviderRequestRecord, available_providers: List[Dict[str, Any]]
    ) -> List[str]:
        sorted_providers = sorted(
            available_providers, key=lambda x: x.get("default_priority", 99)
        )
        return [
            p["provider_name"]
            for p in sorted_providers
            if p.get("data_family") == request.data_family
        ]


class QualityWeightedRoutingStrategy(RoutingStrategy):
    def select_providers(
        self, request: ProviderRequestRecord, available_providers: List[Dict[str, Any]]
    ) -> List[str]:
        # Placeholder: assume available_providers have a historical 'average_quality'
        sorted_providers = sorted(
            available_providers,
            key=lambda x: x.get("average_quality", 0.0),
            reverse=True,
        )
        return [
            p["provider_name"]
            for p in sorted_providers
            if p.get("data_family") == request.data_family
        ]


class StableProviderPreferredStrategy(RoutingStrategy):
    def select_providers(
        self, request: ProviderRequestRecord, available_providers: List[Dict[str, Any]]
    ) -> List[str]:
        # Exclude UNSTABLE/QUARANTINED
        stable = [
            p
            for p in available_providers
            if p.get("health_status", "healthy") in ["healthy", "degraded"]
        ]
        sorted_providers = sorted(stable, key=lambda x: x.get("default_priority", 99))
        return [
            p["provider_name"]
            for p in sorted_providers
            if p.get("data_family") == request.data_family
        ]


class CachedFirstForPreviewStrategy(RoutingStrategy):
    def select_providers(
        self, request: ProviderRequestRecord, available_providers: List[Dict[str, Any]]
    ) -> List[str]:
        # Prefer cache
        sorted_providers = sorted(
            available_providers,
            key=lambda x: 0 if x.get("provider_kind") == "cached_proxy" else 1,
        )
        return [
            p["provider_name"]
            for p in sorted_providers
            if p.get("data_family") == request.data_family
        ]


class ConservativeOpsProviderStrategy(RoutingStrategy):
    def select_providers(
        self, request: ProviderRequestRecord, available_providers: List[Dict[str, Any]]
    ) -> List[str]:
        stable = [
            p
            for p in available_providers
            if p.get("health_status", "healthy") == "healthy"
        ]
        sorted_providers = sorted(stable, key=lambda x: x.get("default_priority", 99))
        return [
            p["provider_name"]
            for p in sorted_providers
            if p.get("data_family") == request.data_family
        ]
