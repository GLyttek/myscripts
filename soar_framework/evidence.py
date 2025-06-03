"""Evidence collection and preservation utilities."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Dict, List


def blockchain_hash(data: bytes) -> str:
    """Return a simple blockchain-style hash for the provided data."""
    return hashlib.sha256(data).hexdigest()


@dataclass
class EvidenceItem:
    """Represents a collected piece of evidence."""

    identifier: str
    path: str
    timestamp: str
    handler: str
    integrity_hash: str


class EvidenceLedger:
    """Maintains an immutable audit trail using hash chaining."""

    def __init__(self) -> None:
        self.records: List[Dict[str, str]] = []

    def add_record(self, item: EvidenceItem) -> None:
        previous_hash = self.records[-1]["ledger_hash"] if self.records else ""
        data = json.dumps(
            {
                "id": item.identifier,
                "path": item.path,
                "time": item.timestamp,
                "handler": item.handler,
                "hash": item.integrity_hash,
                "prev": previous_hash,
            },
            sort_keys=True,
        ).encode()
        ledger_hash = blockchain_hash(data)
        self.records.append({"ledger_hash": ledger_hash, **json.loads(data)})
