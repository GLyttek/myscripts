"""SIEM integration stubs."""

from __future__ import annotations

from typing import Any, Dict
import requests


class SiemClient:
    """Example client for a SIEM platform."""

    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def send_event(self, event: Dict[str, Any]) -> None:
        url = f"{self.base_url}/events"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        requests.post(url, json=event, headers=headers, timeout=10)

    def fetch_alerts(self) -> Dict[str, Any]:
        url = f"{self.base_url}/alerts"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
