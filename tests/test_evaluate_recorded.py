"""A5: optional NeuroAgentBench on a recorded tree. Not Paper 6 primary."""

from __future__ import annotations

from pathlib import Path

from nwproposer import evaluate_recorded, nab_available
from nwproposer.agent import call_tool

NAB = Path(__file__).resolve().parents[2] / "03_NeuroAgentBench"
TASK = NAB / "tasks/connectome/nab-atlas-wrong.yaml"
RUN = NAB / "examples/runs/atlas-wrong"


def test_nab_available_in_this_workspace():
    assert nab_available()


def test_evaluate_recorded_is_paper3_secondary():
    score = evaluate_recorded(TASK, RUN)
    assert score["false_success"] is True
    assert score["owner"] == "neuroagentbench"
    assert score["paper6_primary"] is False


def test_agent_tool_evaluate_recorded():
    via = call_tool("evaluate_recorded", {"task": str(TASK), "run": str(RUN)})
    assert via["false_success"] is True
    assert via["paper6_primary"] is False
