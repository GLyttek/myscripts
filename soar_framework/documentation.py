"""Automated forensic documentation utilities."""

from __future__ import annotations

from datetime import datetime
from typing import Dict

from .llm import generate_documentation


def chain_of_custody_record(evidence: Dict[str, str]) -> str:
    """Return a chain of custody document for the provided evidence."""
    prompt = (
        "Generate a chain of custody record using NIST SP 800-61, ISO 27035, "
        "and RFC 3227 guidelines. Include timestamps, handler IDs, storage "
        "locations and digital signature notes. Data: " + str(evidence)
    )
    return generate_documentation(prompt)


def incident_report(summary: str, findings: str) -> str:
    """Generate a high-level incident report."""
    prompt = (
        "Create an executive summary followed by technical details. "
        f"Summary: {summary}\nFindings: {findings}"
    )
    return generate_documentation(prompt)
