"""Structured intent → propose_request. No model API. Does not execute."""

from __future__ import annotations

from typing import Any, Mapping

from proposer.canonicalize import normalize_network
from proposer.forbidden import assert_execution_not_loaded

REQUIRED_INTENT_FIELDS = (
    "plugin_id",
    "plugin_version",
    "image_digest",
    "inputs",
    "backend",
)


def propose(intent: Mapping[str, Any]) -> dict[str, Any]:
    """Emit a propose_request the existing NeuroInsight submit already understands."""
    assert_execution_not_loaded()
    missing = [field for field in REQUIRED_INTENT_FIELDS if field not in intent]
    if missing:
        raise ValueError(f"intent missing required fields: {missing}")

    workflow = bool(intent.get("workflow") or intent.get("workflow_id"))
    request: dict[str, Any] = {
        "proposer": "agent",
        "plugin_id": intent["plugin_id"],
        "plugin_version": str(intent["plugin_version"]),
        "image_digest": intent["image_digest"],
        "inputs": dict(intent["inputs"]),
        "parameters": dict(intent.get("parameters") or {}),
        "backend": intent["backend"],
        "network": normalize_network(intent.get("network", "off")),
        "approval": {
            "execution": bool((intent.get("approval") or {}).get("execution", False)),
        },
        "guards": {
            "scicap_invoke": "pending",
            "sciguard_validate": "pending" if workflow else "not_applicable",
        },
        "notes": {
            "agent_may_not_execute": True,
        },
    }
    if workflow:
        request["workflow"] = True
        request["workflow_id"] = intent.get("workflow_id") or intent["plugin_id"]
    if "atlas_declared" in (intent.get("parameters") or {}):
        request["parameters"]["atlas_declared"] = intent["parameters"]["atlas_declared"]
    if "atlas_actual" in (intent.get("parameters") or {}):
        request["parameters"]["atlas_actual"] = intent["parameters"]["atlas_actual"]
    return request
