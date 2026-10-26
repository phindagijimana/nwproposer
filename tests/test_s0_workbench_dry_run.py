"""Wave 6: legal G/H job on S0 T1w, dry-run through neuroworkbench.

Annex / LFS pointers are absent. Pytest does not download. No U-vs-G
percentages. evaluate_recorded stays paper6_primary: false.
"""

from __future__ import annotations

import sys
from pathlib import Path

from nwproposer import evaluate_recorded
from proposer.equality import jobs_equal
from proposer.external import (
    find_public_t1w,
    is_real_nifti_bytes,
    legal_s0_job,
    t1w_blocker,
)
from proposer.forbidden import assert_execution_not_loaded
from proposer.propose import propose
from proposer.score import item_score
from proposer.submit import PostRecorder, submit

_SUBMIT_MOD = sys.modules["proposer.submit"]

ROOT = Path(__file__).resolve().parents[1]
METHODS_TRACE = ROOT / "docs" / "METHODS_TRACE.md"
NAB = ROOT.parent / "03_NeuroAgentBench"
NAB_TASK = NAB / "tasks/connectome/nab-atlas-wrong.yaml"
NAB_RUN = NAB / "examples/runs/atlas-wrong"


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


def test_annex_pointer_is_absent(tmp_path: Path) -> None:
    pointer = tmp_path / "sub-01_T1w.nii.gz"
    pointer.write_text("../.git/annex/objects/SHA256E-s140--deadbeef\n")
    assert is_real_nifti_bytes(pointer) is False
    tiny = tmp_path / "tiny.nii.gz"
    tiny.write_bytes(b"\x1f\x8b" + b"\x00" * 20)
    assert is_real_nifti_bytes(tiny) is False


def test_s0_gzip_magic_is_required_when_present() -> None:
    blocker = t1w_blocker()
    assert blocker["bytes_in_git"] is False
    assert blocker["download_in_pytest"] is False
    assert blocker["paper6_primary"] is False
    t1w = find_public_t1w()
    if t1w is None:
        assert blocker["present"] is False
        return
    assert blocker["present"] is True
    assert blocker["gzip_magic"] is True
    assert blocker["annex_pointer_rejected"] is False
    assert blocker["size_bytes"] > 1024
    assert is_real_nifti_bytes(t1w) is True
    assert t1w.name == "sub-01_T1w.nii.gz"
    assert "ds000003" in str(t1w)


def test_legal_gh_job_dry_runs_s0_through_workbench(tmp_path: Path) -> None:
    human = legal_s0_job(proposer="human")
    if human is None:
        blocker = t1w_blocker()
        assert blocker["present"] is False
        assert Path(ROOT / "fixtures" / "workbench_human.yaml").is_file()
        return

    t1w = Path(human["inputs"]["t1w"])
    assert t1w.is_file()
    assert is_real_nifti_bytes(t1w)
    assert human["notes"]["s0_used"] is True
    assert human["notes"]["bytes_in_git"] is False
    assert human["notes"]["paper6_primary"] is False
    assert human["plugin_id"] == "fastsurfer_anatomical"
    assert human["backend"] == "local_container"
    assert human["network"] == "off"

    proposed = propose(_intent(human))
    assert jobs_equal(human, proposed)

    h_result = submit(
        human, arm="H", approve=True, kernel="workbench", store=tmp_path / "h"
    )
    g_result = submit(
        proposed, arm="G", approve=True, kernel="workbench", store=tmp_path / "g"
    )
    assert h_result.posted is True
    assert g_result.posted is True
    assert h_result.reason == "dry_run_neuroworkbench"
    assert g_result.reason == "dry_run_neuroworkbench"
    assert jobs_equal(human, g_result.job)
    assert g_result.job["inputs"]["t1w"] == str(t1w.resolve())
    assert g_result.workbench is not None
    assert g_result.workbench["status"] == "accepted"
    assert g_result.workbench["receipt"]["dry_run"] is True
    assert h_result.workbench is not None
    assert h_result.workbench["receipt"]["dry_run"] is True
    score = item_score(
        item_id="s0_fastsurfer_gh",
        arm="G",
        posted=g_result.posted,
        scicap_decision=g_result.scicap_decision,
        sciguard_status=g_result.sciguard_status,
        job_equal_to_human=True,
        receipt=g_result.workbench.get("receipt") or {},
    )
    assert score["paper6_primary"] is False
    assert score["job_equal_to_human"] is True
    assert score["incorrect_submission"] is False
    assert "%" not in str(score)
    assert_execution_not_loaded()


def test_g_gate_blocks_illegal_before_workbench(
    illegal_dk_as_dkt,
    illegal_space_omitted,
    illegal_labels_t1w_on_dwi,
    monkeypatch,
    tmp_path: Path,
) -> None:
    calls: list[object] = []

    def _must_not_hand_to_workbench(*_args, **_kwargs):
        calls.append((_args, _kwargs))
        raise AssertionError("G must not hand REJECT/ABSTAIN/FAIL to neuroworkbench")

    monkeypatch.setattr(_SUBMIT_MOD, "workbench_submit", _must_not_hand_to_workbench)
    cases = (
        (illegal_dk_as_dkt, "scicap_decision", "REJECT"),
        (illegal_space_omitted, "scicap_decision", "ABSTAIN"),
        (illegal_labels_t1w_on_dwi, "sciguard_status", "FAIL"),
    )
    for fixture, field, expected in cases:
        poster = PostRecorder()
        result = submit(
            fixture,
            arm="G",
            approve=True,
            poster=poster,
            kernel="workbench",
            store=tmp_path,
        )
        assert getattr(result, field) == expected
        assert result.posted is False
        assert result.workbench is None
        assert poster.posts == []
    assert calls == []
    assert_execution_not_loaded()


def test_evaluate_recorded_stays_not_paper6_primary() -> None:
    score = evaluate_recorded(NAB_TASK, NAB_RUN)
    assert score["paper6_primary"] is False
    assert score["owner"] == "neuroagentbench"
    assert "%" not in str(score)


def test_wave6_trace_does_not_invent_percentages() -> None:
    text = METHODS_TRACE.read_text(encoding="utf-8")
    assert "Wave 6" in text
    assert "paper6_primary: false" in text
    assert "neuroworkbench.submit" in text
    assert "%" not in text
    assert "annotators" in text.lower()
