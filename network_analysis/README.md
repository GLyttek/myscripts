# Network Traffic Analysis Engine

This module provides a starting point for building a network traffic analysis platform with deep packet inspection (DPI) and machine-learning based anomaly detection. Packets are captured using `scapy` and organized into stateful TCP flows. Feature vectors are extracted from each reconstructed flow and sent to an Ollama API endpoint for classification. Basic baseline modelling and threat intelligence correlation hooks are included.

## Features

- Bidirectional packet capture using libpcap via **scapy**.
- Session state tracking for TCP flow reassembly.
- Application layer payload inspection with customizable parsers.
- Integration with Ollama-hosted models for anomaly detection and threat pattern recognition.
- Baseline communication profiling using simple statistical learning.
- Threat intelligence lookups through STIX/TAXII feeds (placeholder implementation).

## Usage

Install dependencies and run the engine with root privileges to access network interfaces:

```bash
cd network_analysis
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
sudo python traffic_engine.py --iface eth0
```

The script prints inference results and baseline deviation scores for each completed TCP flow. Modify the code to adapt model endpoints, feature extraction, or threat intelligence sources.

This is a minimal proof of concept and not intended for production without further optimization and security review.
