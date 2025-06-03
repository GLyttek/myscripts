"""Endpoint Detection and Response integration stubs."""

from __future__ import annotations

from typing import Any, Dict
import requests


class EdrClient:
    """Example client for an EDR platform."""

    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def isolate_host(self, host_id: str) -> None:
        url = f"{self.base_url}/hosts/{host_id}/isolate"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        requests.post(url, headers=headers, timeout=10)

    def fetch_incidents(self) -> Dict[str, Any]:
        url = f"{self.base_url}/incidents"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
