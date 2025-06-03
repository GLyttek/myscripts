"""Ollama integration utilities.

This module provides helper functions for interacting with an Ollama
server that hosts incident-response specific models. The LLM is used to
produce forensically sound reports that meet legal admissibility
requirements.
"""

from __future__ import annotations

import json
from typing import Dict, Any
import requests


class OllamaClient:
    """Simple wrapper around the Ollama REST API."""

    def __init__(self, base_url: str = "http://localhost:11434") -> None:
        self.base_url = base_url.rstrip("/")

    def generate(self, prompt: str, model: str = "incident-model") -> str:
        """Generate text using the given model."""
        url = f"{self.base_url}/api/generate"
        payload = {"model": model, "prompt": prompt}
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")


def generate_documentation(prompt: str) -> str:
    """Generate documentation text for the given prompt."""
    client = OllamaClient()
    return client.generate(prompt)
