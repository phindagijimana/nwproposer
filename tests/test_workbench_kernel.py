"""Finish A1–A3 against public neuroworkbench + SciCap + SciGuard.

Not neuroinsight_research. No confirmatory percentages.
"""

from __future__ import annotations

from pathlib import Path

from adapters.neuroworkbench.request import (
    to_workbench_request,
    workbench_available,
)
from proposer.canonicalize import load_document
from proposer.equality import jobs_equal
from proposer.forbidden import assert_execution_not_loaded
from proposer.propose import propose
from nwproposer.agent import call_tool
from proposer.submit import PostRecorder, submit

ROOT = Path(__file__).resolve().parents[1]
HUMAN = ROOT / "fixtures" / "workbench_human.yaml"


def _intent(document: dict) -> dict:
    return {
        "plugin_id": document["plugin_id"],
        "plugin_version": document["plugin_version"],
        "image_digest": document["image_digest"],
        "inputs": document["inputs"],
        "parameters": document.get("parameters") or {},
        "backend": document["backend"],
        "network": document.get("network", "off"),
        "approval": document.get("approval") or {"execution": True},
    }


def test_workbench_is_the_public_kernel():
    assert workbench_available()
    mapped = to_workbench_request(load_document(HUMAN))
    assert mapped["backend"] == "local_container"
    assert mapped["plugin_id"] == "fastsurfer_anatomical"


def test_g_equals_h_on_workbench_and_dry_runs(tmp_path: Path):
    human = load_document(HUMAN)
    proposed = propose(_intent(human))
    assert jobs_equal(human, proposed)
    assert proposed["notes"]["agent_may_not_execute"] is True

    h_result = submit(
        human, arm="H", approve=True, kernel="workbench", store=tmp_path / "h"
    )
    g_result = submit(
        proposed, arm="G", approve=True, kernel="workbench", store=tmp_path / "g"
    )
    assert h_result.posted is True
    assert g_result.posted is True
    assert jobs_equal(human, g_result.job)
    assert g_result.reason == "dry_run_neuroworkbench"
    assert g_result.workbench is not None
    assert g_result.workbench["status"] == "accepted"
    assert g_result.workbench["receipt"]["dry_run"] is True
    assert_execution_not_loaded()


def test_g_does_not_hand_illegal_job_to_workbench(illegal_dk_as_dkt, tmp_path: Path):
    poster = PostRecorder()
    result = submit(
        illegal_dk_as_dkt,
        arm="G",
        approve=True,
        poster=poster,
        kernel="workbench",
        store=tmp_path,
    )
    assert result.scicap_decision == "REJECT"
    assert result.posted is False
    assert result.workbench is None
    assert poster.posts == []
    assert_execution_not_loaded()


def test_agent_submit_uses_workbench_kernel(tmp_path: Path):
    human = load_document(HUMAN)
    proposed = propose(_intent(human))
    via = call_tool(
        "submit",
        {
            "request": proposed,
            "arm": "G",
            "approve": True,
            "kernel": "workbench",
            "store": str(tmp_path),
        },
    )
    assert via["posted"] is True
    assert via["reason"] == "dry_run_neuroworkbench"
    assert via["workbench_status"] == "accepted"
    assert via["dry_run"] is True
    assert_execution_not_loaded()


def test_u_does_not_use_the_workbench_kernel(illegal_dk_as_dkt):
    result = submit(illegal_dk_as_dkt, arm="U", approve=True, kernel="workbench")
    assert result.posted is True
    assert result.incorrect_submission is True
    assert result.workbench is None
    assert result.reason == "unconstrained"
