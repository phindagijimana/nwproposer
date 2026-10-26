"""A1: proposer-only adapter. Importing the executor fails the paper."""

from __future__ import annotations

import importlib
import sys

import pytest

from proposer.forbidden import (
    FORBIDDEN_MODULES,
    assert_execution_not_loaded,
    assert_no_forbidden_imports,
    forbidden_imports_found,
    imported_module_names,
)
from proposer.propose import propose
from proposer.submit import PostRecorder, submit


def test_arms_h_g_u_are_declared(arms):
    assert set(arms) == {"H", "G", "U"}
    assert "scicap_invoke" in arms["G"]["gates"]
    assert arms["U"]["gates"] == []
    assert arms["U"]["tools_and_shell"] == "allowed"


def test_proposer_source_has_no_forbidden_imports():
    assert_no_forbidden_imports()
    assert forbidden_imports_found() == []


def test_a1_scan_baselines_and_adapters(paper_root):
    """Wave 3/4: proposer, dispatcher, and public package cannot import backend.execution."""
    roots = (
        paper_root / "baselines",
        paper_root / "adapters",
        paper_root / "proposer",
        paper_root / "nwproposer",
    )
    assert forbidden_imports_found(roots) == []
    assert "backend.execution" not in sys.modules
    with pytest.raises(ImportError):
        importlib.import_module("backend.execution")
    assert_execution_not_loaded()


def test_g_is_not_a_neuroclaw_wrap(arms):
    hits = forbidden_imports_found()
    claw = [hit for hit in hits if any(name in hit[1] for name in ("neuroclaw", "claw_shell", "neurodiscovery"))]
    assert claw == []
    source = (importlib.import_module("proposer.submit").__file__ or "")
    text = open(source, encoding="utf-8").read()
    assert "NeuroClaw" not in text or "not a NeuroClaw wrap" in text
    assert arms["G"]["neuroclaw_wrap"] is False
    assert arms["U"]["neuroclaw_wrap"] is False
    assert arms["U"]["writer"] == "unconstrained_agent"
    assert arms["U"]["gates"] == []


def test_backend_execution_is_not_vendored():
    assert "backend.execution" not in sys.modules
    with pytest.raises(ImportError):
        importlib.import_module("backend.execution")
    assert_execution_not_loaded()


def test_importing_proposer_does_not_load_executor():
    importlib.reload(importlib.import_module("proposer"))
    importlib.reload(importlib.import_module("proposer.submit"))
    for name in FORBIDDEN_MODULES:
        assert name not in sys.modules


def test_proposer_init_does_not_import_submit(paper_root):
    init = paper_root / "proposer" / "__init__.py"
    names = imported_module_names(init)
    assert "proposer.submit" not in names
    assert "submit" not in names
    import proposer

    assert "submit" not in proposer.__all__


def test_propose_and_submit_do_not_open_a_network_or_container():
    intent = {
        "plugin_id": "fastsurfer",
        "plugin_version": "2.4.2",
        "image_digest": "sha256:PENDING",
        "inputs": {"T1w": "bids:sub-01/anat/sub-01_T1w.nii.gz"},
        "backend": "local_docker",
        "network": "off",
        "approval": {"execution": True},
    }
    request = propose(intent)
    assert request["notes"]["agent_may_not_execute"] is True
    poster = PostRecorder()
    result = submit(request, arm="G", approve=True, poster=poster)
    assert result.posted is True
    assert result.reason == "dry_run_existing_submit"
    assert len(poster.posts) == 1
