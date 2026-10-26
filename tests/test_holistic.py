"""Same propose_request fixtures through public protocol and Paper 6 stubs.

Behavioral assertions only. No fabricated U-vs-G percentages.
Silent success is Paper 5 N2, not a Paper 6 result.
"""

from __future__ import annotations

from baselines.cyberneuro_split import dispatch, plan
from baselines.neuropilot_approval import review_approval
from proposer.canonicalize import load_document
from proposer.equality import jobs_equal
from proposer.forbidden import forbidden_imports_found
from proposer.propose import propose
from proposer.score import item_score, platform_silent_success
from proposer.submit import PostRecorder, incorrect_submission_rate, submit

_VENDORED_DIR_NAMES = {
    "neuroinsight_research",
    "neuroclaw",
    "neurodiscovery",
    "claw-shell",
    "claw_shell",
    "wandamind",
}


def _intent_from(document: dict) -> dict:
    return {
        "plugin_id": document["plugin_id"],
        "plugin_version": document["plugin_version"],
        "image_digest": document["image_digest"],
        "inputs": document["inputs"],
        "parameters": document.get("parameters") or {},
        "backend": document["backend"],
        "network": document.get("network", "off"),
        "approval": document.get("approval") or {"execution": True},
        **(
            {"workflow": True, "workflow_id": document.get("workflow_id")}
            if document.get("workflow") or document.get("workflow_id")
            else {}
        ),
    }


def test_human_fastsurfer_public_and_paper6(human_fastsurfer_job, arms):
    human = load_document(human_fastsurfer_job)
    review = review_approval(human, already_approved=True)
    assert review["requires_approve"] is False
    assert review["extra_approve"] is False

    planned = plan(_intent_from(human))
    protocol = dispatch(planned)
    assert protocol["executed"] is False
    assert jobs_equal(human, planned)

    h_poster = PostRecorder()
    h_result = submit(human, arm="H", approve=True, poster=h_poster)
    assert h_result.posted is True
    g_request = propose(_intent_from(human))
    g_poster = PostRecorder()
    g_result = submit(g_request, arm="G", approve=True, poster=g_poster)
    assert g_result.posted is True
    assert jobs_equal(human, g_result.job)
    assert set(arms) == {"H", "G", "U"}


def test_dk_as_dkt_public_and_paper6(illegal_dk_as_dkt):
    review = review_approval(illegal_dk_as_dkt)
    assert "atlas" not in review["triggers"]
    assert review["requires_approve"] is False
    protocol = dispatch(illegal_dk_as_dkt)
    assert protocol["executed"] is False

    poster = PostRecorder()
    result = submit(illegal_dk_as_dkt, arm="G", approve=True, poster=poster)
    assert result.scicap_decision == "REJECT"
    assert result.posted is False
    assert poster.posts == []


def test_labels_to_dwi_public_and_paper6(illegal_labels_t1w_on_dwi):
    review = review_approval(illegal_labels_t1w_on_dwi)
    assert "space" not in review["triggers"]
    assert review["requires_approve"] is False
    protocol = dispatch(illegal_labels_t1w_on_dwi)
    assert protocol["executed"] is False

    poster = PostRecorder()
    result = submit(illegal_labels_t1w_on_dwi, arm="G", approve=True, poster=poster)
    assert result.sciguard_status == "FAIL"
    assert result.posted is False
    assert poster.posts == []


def test_network_on_public_and_paper6(network_on_request):
    review = review_approval(network_on_request)
    assert review["requires_approve"] is True
    protocol = dispatch(network_on_request)
    assert protocol["executed"] is False

    poster = PostRecorder()
    result = submit(network_on_request, arm="G", approve=False, poster=poster)
    assert result.posted is False
    assert result.reason == "approval_required"
    assert poster.posts == []


def test_overwrite_and_backend_switch_public_and_paper6(
    overwrite_request, backend_switch_request
):
    for request, trigger in (
        (overwrite_request, "overwrite"),
        (backend_switch_request, "backend_switch"),
    ):
        review = review_approval(request)
        assert review["requires_approve"] is True
        assert trigger in review["triggers"]
        protocol = dispatch(request)
        assert protocol["executed"] is False
        poster = PostRecorder()
        result = submit(request, arm="G", approve=False, poster=poster)
        assert result.posted is False
        assert result.reason == "approval_required"
        assert poster.posts == []


def test_qc_skipped_is_paper5_n2_field_not_paper6_result(silent_success_receipt, arms):
    assert platform_silent_success(silent_success_receipt) is True
    for arm in arms:
        score = item_score(
            item_id="qc_skipped_reported_complete",
            arm=arm,
            posted=True,
            receipt=silent_success_receipt,
        )
        assert score["platform_silent_success"] is True
        assert score["arm"] == arm


def test_u_incorrect_submission_gt_g_is_stub_count_not_a_result(
    illegal_dk_as_dkt, illegal_labels_t1w_on_dwi
):
    fixtures = [illegal_dk_as_dkt, illegal_labels_t1w_on_dwi]
    g_results = [submit(row, arm="G", approve=True, poster=PostRecorder()) for row in fixtures]
    u_results = [submit(row, arm="U", approve=True, poster=PostRecorder()) for row in fixtures]
    assert all(not row.posted for row in g_results)
    assert all(row.posted and row.incorrect_submission for row in u_results)
    # Existing stub inequality only. Not an evaluation result and not a percentage.
    assert incorrect_submission_rate(u_results) > incorrect_submission_rate(g_results)


def test_g_is_not_a_neuroclaw_wrap_on_public_and_stubs(paper_root):
    hits = forbidden_imports_found()
    claw = [
        hit
        for hit in hits
        if any(name in hit[1] for name in ("neuroclaw", "claw_shell", "neurodiscovery"))
    ]
    assert claw == []
    submit_text = (paper_root / "proposer" / "submit.py").read_text()
    assert "not a NeuroClaw wrap" in submit_text


def test_a5_reuse_is_imports_not_reimplementation(paper_root):
    submit_text = (paper_root / "proposer" / "submit.py").read_text()
    score_text = (paper_root / "proposer" / "score.py").read_text()
    assert "from guards.scicap import invoke as scicap_invoke" in submit_text
    assert "from guards.sciguard import is_workflow, validate as sciguard_validate" in submit_text
    assert "Paper 5 N2" in score_text
    mcp_modules = [
        path
        for path in paper_root.rglob("*.py")
        if path.is_file() and "mcp" in path.name.lower()
    ]
    assert mcp_modules == []


def test_private_repo_and_neuroclaw_not_vendored(paper_root):
    names = {path.name.lower() for path in paper_root.iterdir()}
    assert names.isdisjoint(_VENDORED_DIR_NAMES)
    for path in paper_root.rglob("*"):
        if path.is_dir() and path.name.lower() in _VENDORED_DIR_NAMES:
            raise AssertionError(f"vendored tree present: {path}")
