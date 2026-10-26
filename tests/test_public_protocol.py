"""Public protocol tools: NeuroPilot approval list + CyberNeuro Planner≠Dispatcher."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

from baselines.cyberneuro_split import SHELL_KEYS, dispatch, is_propose_request, plan
from baselines.neuropilot_approval import CONSEQUENTIAL_FIELDS, review_approval
from proposer.canonicalize import load_document
from proposer.forbidden import imported_module_names


def test_network_on_requires_approve(network_on_request):
    review = review_approval(network_on_request)
    assert review["requires_approve"] is True
    assert "network_on" in review["triggers"]
    assert review["citation"] == "arXiv:2608.07541"
    assert "unrelated" in review["unrelated_vscode"].lower()


def test_human_fastsurfer_no_extra_approve_when_already_approved(human_fastsurfer_job):
    human = load_document(human_fastsurfer_job)
    review = review_approval(human, already_approved=True)
    assert review["requires_approve"] is False
    assert review["extra_approve"] is False
    assert review["triggers"] == []


def test_consequential_list_covers_locked_fields():
    assert CONSEQUENTIAL_FIELDS == (
        "overwrite",
        "delete",
        "slurm_array",
        "backend_switch",
        "network_on",
        "fallback_plugin",
    )
    base = {
        "plugin_id": "fastsurfer",
        "image_digest": "sha256:PENDING",
        "inputs": {"T1w": "bids:sub-01/anat/sub-01_T1w.nii.gz"},
        "backend": "local_docker",
        "network": "off",
    }
    cases = {
        "overwrite": {**base, "overwrite": True},
        "delete": {**base, "delete": True},
        "slurm_array": {**base, "slurm_array": True},
        "backend_switch": {**base, "previous_backend": "local_docker", "backend": "slurm"},
        "network_on": {**base, "network": "on"},
        "fallback_plugin": {**base, "fallback_plugin": "freesurfer"},
    }
    for field, request in cases.items():
        review = review_approval(request)
        assert review["requires_approve"] is True, field
        assert field in review["triggers"], field


def test_planner_output_is_propose_request_not_shell(human_fastsurfer_job):
    human = load_document(human_fastsurfer_job)
    planned = plan(
        {
            "plugin_id": human["plugin_id"],
            "plugin_version": human["plugin_version"],
            "image_digest": human["image_digest"],
            "inputs": human["inputs"],
            "parameters": human["parameters"],
            "backend": human["backend"],
            "network": human["network"],
            "approval": {"execution": True},
        }
    )
    assert planned["kind"] == "propose_request"
    assert is_propose_request(planned)
    assert planned["plugin_id"] == "fastsurfer"
    assert planned["notes"]["not_a_shell_command"] is True
    for key in SHELL_KEYS:
        assert key not in planned
    with pytest.raises(ValueError, match="not a shell command"):
        plan({**human, "command": "fastsurfer --t1 /tmp/t1.nii.gz"})


def test_dispatcher_does_not_execute_or_load_backend_execution(human_fastsurfer_job):
    human = load_document(human_fastsurfer_job)
    planned = plan(
        {
            "plugin_id": human["plugin_id"],
            "plugin_version": human["plugin_version"],
            "image_digest": human["image_digest"],
            "inputs": human["inputs"],
            "parameters": human["parameters"],
            "backend": human["backend"],
            "network": human["network"],
        }
    )
    result = dispatch(planned)
    assert result["executed"] is False
    assert result["posted"] is False
    assert result["implemented_as"] == "existing_submit_stub"
    assert result["imported_backend_execution"] is False
    assert result["backend_execution_loaded"] is False
    assert "backend.execution" not in sys.modules
    names = imported_module_names(Path(importlib.import_module("baselines.cyberneuro_split").__file__ or ""))
    assert "backend.execution" not in names
    with pytest.raises(ImportError):
        importlib.import_module("backend.execution")
    with pytest.raises(ValueError, match="not a shell command"):
        dispatch({"command": "echo pwn", "plugin_id": "fastsurfer"})
