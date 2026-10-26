"""NeuroPilot approve gates: network:on, overwrite, backend switch. Not posted without approve."""

from __future__ import annotations

from baselines.neuropilot_approval import review_approval
from proposer.submit import PostRecorder, submit


def test_network_on_not_posted_without_approve(network_on_request):
    review = review_approval(network_on_request)
    assert review["requires_approve"] is True
    assert "network_on" in review["triggers"]
    poster = PostRecorder()
    result = submit(network_on_request, arm="G", approve=False, poster=poster)
    assert result.posted is False
    assert result.reason == "approval_required"
    assert poster.posts == []


def test_overwrite_not_posted_without_approve(overwrite_request):
    review = review_approval(overwrite_request)
    assert review["requires_approve"] is True
    assert "overwrite" in review["triggers"]
    poster = PostRecorder()
    result = submit(overwrite_request, arm="G", approve=False, poster=poster)
    assert result.posted is False
    assert result.reason == "approval_required"
    assert poster.posts == []


def test_backend_switch_not_posted_without_approve(backend_switch_request):
    review = review_approval(backend_switch_request)
    assert review["requires_approve"] is True
    assert "backend_switch" in review["triggers"]
    poster = PostRecorder()
    result = submit(backend_switch_request, arm="G", approve=False, poster=poster)
    assert result.posted is False
    assert result.reason == "approval_required"
    assert poster.posts == []


def test_consequential_jobs_post_on_g_when_approved(
    network_on_request, overwrite_request, backend_switch_request
):
    for request in (network_on_request, overwrite_request, backend_switch_request):
        poster = PostRecorder()
        result = submit(request, arm="G", approve=True, poster=poster)
        assert result.posted is True
        assert result.reason == "dry_run_existing_submit"
        assert len(poster.posts) == 1
