"""Agent call contract. Propose / dry-run submit only. No execute tool."""

from __future__ import annotations

from typing import Any

from pathlib import Path

from nwproposer import evaluate_recorded, propose, submit
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
                "kernel": {
                    "type": "string",
                    "enum": ["workbench", "recorder"],
                    "default": "workbench",
                    "description": "workbench = public neuroworkbench dry-run",
                },
                "store": {"type": "string", "description": "Receipt store for workbench kernel"},
            },
            "required": ["request"],
        },
    },
    {
        "name": "evaluate_recorded",
        "description": (
            "Optional NeuroAgentBench score on a recorded run tree. "
            "Paper 3 owns this number. Does not start an agent."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "task": {"type": "string"},
                "run": {"type": "string"},
                "seed": {"type": "integer"},
            },
            "required": ["task", "run"],
        },
    },
]


def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "execute":
        raise ValueError("execute is not a tool; nwproposer does not execute")
    if name == "propose":
        return propose(arguments)
    if name == "submit":
        kernel = str(arguments.get("kernel", "workbench"))
        store = Path(arguments["store"]) if arguments.get("store") else None
        poster = None if kernel == "workbench" else PostRecorder()
        result = submit(
            arguments["request"],
            arm=str(arguments.get("arm", "G")),
            approve=bool(arguments.get("approve", False)),
            poster=poster,
            kernel=kernel,
            store=store,
        )
        payload = {
            "arm": result.arm,
            "posted": result.posted,
            "reason": result.reason,
            "scicap_decision": result.scicap_decision,
            "sciguard_status": result.sciguard_status,
            "incorrect_submission": result.incorrect_submission,
            "execute_called": result.execute_called,
        }
        if result.workbench is not None:
            payload["workbench_status"] = result.workbench.get("status")
            payload["dry_run"] = (result.workbench.get("receipt") or {}).get("dry_run")
        return payload
    if name == "evaluate_recorded":
        seed = arguments.get("seed")
        return evaluate_recorded(
            arguments["task"],
            arguments["run"],
            seed=None if seed is None else int(seed),
        )
    raise ValueError(f"unknown tool: {name}")
