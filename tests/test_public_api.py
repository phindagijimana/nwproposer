"""Public import and agent tool schema. No execute tool. No MCP. No model API."""

from __future__ import annotations

import os

import pytest

from nwproposer import propose
from nwproposer.agent import TOOLS, call_tool

INTENT = {
    "plugin_id": "fastsurfer",
    "plugin_version": "2.4.2",
    "image_digest": "sha256:PENDING",
    "inputs": {"T1w": "bids:sub-01/anat/sub-01_T1w.nii.gz"},
    "backend": "local_docker",
    "network": "off",
}


def test_public_propose() -> None:
    os.environ.pop("OPENAI_API_KEY", None)
    request = propose(INTENT)
    assert request["notes"]["agent_may_not_execute"] is True


def test_agent_tool_has_no_execute() -> None:
    via = call_tool("propose", INTENT)
    assert via["notes"]["agent_may_not_execute"] is True
    assert {tool["name"] for tool in TOOLS} == {"propose", "submit", "evaluate_recorded"}
    with pytest.raises(ValueError, match="execute"):
        call_tool("execute", {})
