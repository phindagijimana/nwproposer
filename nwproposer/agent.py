"""Agent call contract. Propose / dry-run submit only. No execute tool."""

from __future__ import annotations

from typing import Any

from nwproposer import propose, submit
from proposer.submit import PostRecorder

TOOLS: list[dict[str, Any]] = [
    {
        "name": "propose",
        "description": (
            "Write the same job a human would submit. Does not execute. "
            "Not a NeuroClaw wrap."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "plugin_id": {"type": "string"},
                "plugin_version": {"type": "string"},
                "image_digest": {"type": "string"},
                "inputs": {"type": "object"},
                "backend": {"type": "string"},
                "network": {"type": "string", "default": "off"},
                "parameters": {"type": "object"},
                "approval": {"type": "object"},
            },
            "required": [
                "plugin_id",
                "plugin_version",
                "image_digest",
                "inputs",
                "backend",
            ],
        },
    },
    {
        "name": "submit",
        "description": (
            "Dry-run post of a proposed job through gates. "
            "Does not execute. Arm G is fail-closed."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "request": {"type": "object", "description": "Output of propose"},
                "arm": {"type": "string", "enum": ["H", "G", "U"], "default": "G"},
                "approve": {"type": "boolean", "default": False},
            },
            "required": ["request"],
        },
    },
]


def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "execute":
        raise ValueError("execute is not a tool; nwproposer does not execute")
    if name == "propose":
        return propose(arguments)
    if name == "submit":
        result = submit(
            arguments["request"],
            arm=str(arguments.get("arm", "G")),
            approve=bool(arguments.get("approve", False)),
            poster=PostRecorder(),
        )
        return {
            "arm": result.arm,
            "posted": result.posted,
            "reason": result.reason,
            "scicap_decision": result.scicap_decision,
            "sciguard_status": result.sciguard_status,
            "incorrect_submission": result.incorrect_submission,
        }
    raise ValueError(f"unknown tool: {name}")
