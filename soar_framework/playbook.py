"""Dynamic playbook execution engine."""

from __future__ import annotations

import yaml
from typing import Callable, Dict, Any


class Playbook:
    """Loads and executes playbooks defined in YAML."""

    def __init__(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as f:
            self.definition = yaml.safe_load(f)
        self.actions: Dict[str, Callable[[Dict[str, Any]], None]] = {}

    def register_action(self, name: str, func: Callable[[Dict[str, Any]], None]) -> None:
        self.actions[name] = func

    def run(self) -> None:
        for step in self.definition.get("steps", []):
            action = step.get("action")
            params = step.get("params", {})
            handler = self.actions.get(action)
            if handler:
                handler(params)
            else:
                raise ValueError(f"Unknown action: {action}")
