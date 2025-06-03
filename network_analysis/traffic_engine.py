"""Network Traffic Analysis Engine with DPI and Ollama integration."""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass, field
from typing import Dict, Iterable, List

import numpy as np
import requests
from scapy.all import IP, TCP, Raw, sniff


@dataclass(frozen=True)
class FlowKey:
    """Five-tuple identifying a TCP flow."""

    src: str
    src_port: int
    dst: str
    dst_port: int
    proto: str = "TCP"


@dataclass
class FlowState:
    packets: List
    bytes: int = 0
    start_time: float = 0.0
    last_seen: float = 0.0
    payload: bytes = field(default_factory=bytes)


class MachineLearningAnalyzer:
    """Client for Ollama-hosted models."""

    def __init__(self, url: str):
        self.url = url.rstrip("/")

    def analyze(self, features: Dict) -> Dict:
        payload = {"model": "transformer-seq", "prompt": json.dumps(features)}
        try:
            resp = requests.post(self.url, json=payload, timeout=5)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException:
            return {"error": "Ollama request failed"}


class BaselineModel:
    """Simple statistical baseline of flow features."""

    def __init__(self):
        self.samples: List[np.ndarray] = []

    def update(self, vector: Iterable[float]) -> None:
        self.samples.append(np.fromiter(vector, dtype=float))

    def score(self, vector: Iterable[float]) -> float:
        if not self.samples:
            return 0.0
        mat = np.vstack(self.samples)
        mean = mat.mean(axis=0)
        return float(np.linalg.norm(np.fromiter(vector, dtype=float) - mean))


class ThreatIntelCorrelator:
    """Placeholder for STIX/TAXII threat intelligence lookups."""

    def __init__(self):
        self.indicators = set()

    def check(self, flow: FlowState) -> List[str]:
        matches = []
        for ip in [pkt[IP].src for pkt in flow.packets if IP in pkt]:
            if ip in self.indicators:
                matches.append(ip)
        return matches


class TrafficEngine:
    def __init__(self, iface: str, ollama_url: str) -> None:
        self.iface = iface
        self.capture_filter = "tcp"
        self.flows: Dict[FlowKey, FlowState] = {}
        self.ml = MachineLearningAnalyzer(ollama_url)
        self.baseline = BaselineModel()
        self.threatintel = ThreatIntelCorrelator()

    def start(self) -> None:
        sniff(
            iface=self.iface,
            filter=self.capture_filter,
            prn=self._process_packet,
            store=False,
        )

    def _process_packet(self, pkt):
        if not (IP in pkt and TCP in pkt):
            return
        ip = pkt[IP]
        tcp = pkt[TCP]
        key = FlowKey(ip.src, tcp.sport, ip.dst, tcp.dport)
        state = self.flows.setdefault(key, FlowState([], start_time=time.time()))
        state.packets.append(pkt)
        state.bytes += len(pkt)
        state.last_seen = time.time()
        if Raw in pkt:
            state.payload += bytes(pkt[Raw].load)
        if tcp.flags.F or tcp.flags.R:
            self._finalize_flow(key)

    def _finalize_flow(self, key: FlowKey) -> None:
        state = self.flows.pop(key, None)
        if not state:
            return
        features = self._extract_features(state)
        ml_result = self.ml.analyze(features)
        deviation = self.baseline.score(features.values())
        self.baseline.update(features.values())
        threats = self.threatintel.check(state)
        report = {
            "flow": key.__dict__,
            "features": features,
            "ml_result": ml_result,
            "baseline_deviation": deviation,
            "threat_matches": threats,
        }
        print(json.dumps(report))

    @staticmethod
    def _extract_features(state: FlowState) -> Dict:
        duration = state.last_seen - state.start_time
        return {
            "packet_count": len(state.packets),
            "total_bytes": state.bytes,
            "duration": duration,
            "payload_size": len(state.payload),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Network traffic analysis engine")
    parser.add_argument("--iface", default="eth0", help="Network interface to sniff")
    parser.add_argument(
        "--ollama-url",
        default="http://localhost:11434/api/generate",
        help="Ollama inference API URL",
    )
    args = parser.parse_args()
    engine = TrafficEngine(args.iface, args.ollama_url)
    engine.start()


if __name__ == "__main__":
    main()
