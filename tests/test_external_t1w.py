"""Wave 5: G=H on a public T1w path when bytes exist; never download.

If shared/data/external has no T1w, fixture jobs remain and the blocker
is recorded. Not an evaluation. No fabricated U-vs-G percentages.
"""

from __future__ import annotations

from pathlib import Path

from proposer.canonicalize import load_document, paper_root
from proposer.equality import jobs_equal
from proposer.external import (
    find_public_t1w,
    legal_s0_job,
    t1w_blocker,
    workbench_job_for_t1w,
)
from proposer.forbidden import assert_execution_not_loaded, imported_module_names
from proposer.propose import propose
from proposer.submit import PostRecorder, submit

ROOT = paper_root()
HUMAN = ROOT / "fixtures" / "workbench_human.yaml"
EXTERNAL_PY = ROOT / "proposer" / "external.py"
METHODS_TRACE = ROOT / "docs" / "METHODS_TRACE.md"


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


def test_discovery_source_does_not_download() -> None:
    text = EXTERNAL_PY.read_text(encoding="utf-8")
    assert "urlretrieve" not in text
    assert "urlopen" not in text
    assert "fetch_public_bytes" not in text
    assert "Never download" in text


def test_discovery_does_not_call_network(monkeypatch) -> None:
    def _boom(*_args, **_kwargs):
        raise AssertionError("pytest must not download a T1w")

    monkeypatch.setattr("urllib.request.urlretrieve", _boom)
    path = find_public_t1w()
    blocker = t1w_blocker()
    assert blocker["download_in_pytest"] is False
    assert blocker["bytes_in_git"] is False
    assert (path is None) == (blocker["present"] is False)


def test_blocker_is_documented_when_bytes_absent() -> None:
    blocker = t1w_blocker()
    trace = METHODS_TRACE.read_text(encoding="utf-8")
    assert "Wave 5" in trace
    assert "Wave 6" in trace
    assert "shared/data/external" in trace
    assert "does not download" in trace
    assert "paper6_primary: false" in trace
    if not blocker["present"]:
        assert "no public T1w" in blocker["reason"]
        assert "fixture jobs remain" in blocker["reason"]
        assert "fixture jobs remain" in trace.lower()


def test_fixture_jobs_remain_g_equals_h(tmp_path: Path) -> None:
    human = load_document(HUMAN)
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
    assert jobs_equal(human, g_result.job)
    assert_execution_not_loaded()


def test_g_equals_h_on_external_t1w_when_present(tmp_path: Path) -> None:
    t1w = find_public_t1w()
    built = legal_s0_job(proposer="human")
    if t1w is None:
        blocker = t1w_blocker()
        assert blocker["present"] is False
        assert blocker["download_in_pytest"] is False
        assert blocker["paper6_primary"] is False
        assert built is None
        assert Path(HUMAN).is_file()
        return

    human = built or workbench_job_for_t1w(t1w, proposer="human")
    assert human["inputs"]["t1w"] == str(t1w.resolve())
    assert human["notes"]["s0_used"] is True
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
    assert jobs_equal(human, g_result.job)
    assert g_result.reason == "dry_run_neuroworkbench"
    assert g_result.workbench is not None
    assert g_result.workbench["status"] == "accepted"
    assert g_result.workbench["receipt"]["dry_run"] is True
    assert_execution_not_loaded()


def test_job_builder_rewrites_inputs_to_given_path(tmp_path: Path) -> None:
    fake = tmp_path / "sub-01_T1w.nii.gz"
    fake.write_bytes(b"")
    job = workbench_job_for_t1w(fake, proposer="human")
    assert job["inputs"]["t1w"] == str(fake.resolve())
    assert job["plugin_id"] == "fastsurfer_anatomical"
    proposed = propose(_intent(job))
    assert jobs_equal(job, proposed)


def test_g_still_refuses_illegal_after_external_lookup(
    illegal_dk_as_dkt, illegal_space_omitted, illegal_labels_t1w_on_dwi
) -> None:
    find_public_t1w()
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
        )
        assert getattr(result, field) == expected
        assert result.posted is False
        assert result.workbench is None
        assert poster.posts == []


def test_u_stays_unconstrained_not_neuroclaw(illegal_dk_as_dkt) -> None:
    result = submit(illegal_dk_as_dkt, arm="U", approve=True, kernel="workbench")
    assert result.posted is True
    assert result.incorrect_submission is True
    assert result.reason == "unconstrained"
    assert result.workbench is None


def test_proposer_init_does_not_import_submit() -> None:
    init = ROOT / "proposer" / "__init__.py"
    names = imported_module_names(init)
    assert "proposer.submit" not in names
    assert "submit" not in names
    text = init.read_text(encoding="utf-8")
    assert "from proposer.submit" not in text
    assert "from .submit" not in text
    from proposer import __all__ as public

    assert "submit" not in public
