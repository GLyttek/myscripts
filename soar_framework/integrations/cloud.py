"""Cloud provider security integration stubs."""

from __future__ import annotations

from typing import Any, Dict
import requests


class CloudSecurityClient:
    """Example client for a cloud service provider security API."""

    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def quarantine_resource(self, resource_id: str) -> None:
        url = f"{self.base_url}/resources/{resource_id}/quarantine"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        requests.post(url, headers=headers, timeout=10)

    def fetch_events(self) -> Dict[str, Any]:
        url = f"{self.base_url}/events"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
