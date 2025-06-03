"""Example entry point for the SOAR framework."""

from __future__ import annotations

from .playbook import Playbook
from .documentation import incident_report
from .integrations.siem import SiemClient
from .integrations.edr import EdrClient
from .integrations.cloud import CloudSecurityClient


def load_default_actions(pb: Playbook, siem: SiemClient, edr: EdrClient, cloud: CloudSecurityClient) -> None:
    def fetch_alerts(_: dict) -> None:
        alerts = siem.fetch_alerts()
        print("Fetched alerts", alerts)

    def isolate(params: dict) -> None:
        host = params.get("host")
        edr.isolate_host(host)
        print(f"Host {host} isolated")

    def quarantine(params: dict) -> None:
        resource = params.get("resource")
        cloud.quarantine_resource(resource)
        print(f"Resource {resource} quarantined")

    pb.register_action("fetch_alerts", fetch_alerts)
    pb.register_action("isolate_host", isolate)
    pb.register_action("quarantine_resource", quarantine)


def run_playbook(path: str) -> None:
    siem = SiemClient("https://siem.example.com/api", "token")
    edr = EdrClient("https://edr.example.com/api", "token")
    cloud = CloudSecurityClient("https://cloud.example.com/api", "token")

    pb = Playbook(path)
    load_default_actions(pb, siem, edr, cloud)
    pb.run()

    report = incident_report("Sample incident", "No findings yet")
    print(report)


if __name__ == "__main__":
    run_playbook("playbooks/sample_playbook.yaml")
