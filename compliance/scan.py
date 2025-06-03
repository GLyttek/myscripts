#!/usr/bin/env python3
"""Simplified compliance baseline scanner.

This script compares system configuration file hashes against a baseline
configuration defined in JSON. It outputs a compliance score and logs
detailed results to `compliance_logs/`.
"""

import hashlib
import json
import os
from datetime import datetime

BASELINE_FILE = os.path.join(os.path.dirname(__file__), "baseline", "os_baseline.json")
LOG_DIR = os.path.join(os.path.dirname(__file__), "compliance_logs")


def sha256_file(path: str) -> str:
    """Return SHA256 hex digest of file contents."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_baseline(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def check_compliance() -> dict:
    baseline = load_baseline(BASELINE_FILE)
    results = []
    for entry in baseline.get("files", []):
        file_path = entry["path"]
        expected_hash = entry.get("sha256")
        if not os.path.exists(file_path):
            results.append({"path": file_path, "status": "missing"})
            continue
        actual_hash = sha256_file(file_path)
        status = "match" if actual_hash == expected_hash else "mismatch"
        results.append({
            "path": file_path,
            "status": status,
            "expected": expected_hash,
            "actual": actual_hash,
        })
    matched = sum(1 for r in results if r["status"] == "match")
    total = len(results)
    score = (matched / total) * 100 if total else 0
    return {"score": score, "results": results}


def log_results(data: dict) -> None:
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    log_file = os.path.join(LOG_DIR, f"scan_{timestamp}.json")
    with open(log_file, "w") as f:
        json.dump(data, f, indent=2)


def main():
    report = check_compliance()
    print(f"Compliance score: {report['score']:.2f}%")
    for r in report["results"]:
        print(f"{r['path']}: {r['status']}")
    log_results(report)


if __name__ == "__main__":
    main()
