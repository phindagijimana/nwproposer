"""Sibling SciCap/SciGuard if importable; else recorded mocks. REJECT/FAIL still not POST."""

from __future__ import annotations

from guards.scicap import invoke as scicap_invoke
from guards.scicap import sibling_available as scicap_sibling
from guards.scicap import guard_mode as scicap_mode
from guards.sciguard import sibling_available as sciguard_sibling
from guards.sciguard import guard_mode as sciguard_mode
from guards.sciguard import validate as sciguard_validate
from proposer.submit import PostRecorder, submit


def test_dk_as_dkt_calls_sibling_or_recorded_and_does_not_post(illegal_dk_as_dkt):
    decision = scicap_invoke(illegal_dk_as_dkt)
    assert decision == "REJECT"
    mode = scicap_mode()
    assert mode in {"sibling", "recorded"}
    if scicap_sibling():
        assert mode == "sibling"
    poster = PostRecorder()
    result = submit(illegal_dk_as_dkt, arm="G", approve=True, poster=poster)
    assert result.scicap_decision == "REJECT"
    assert result.posted is False
    assert poster.posts == []
    assert result.guard_mode["scicap"] in {"sibling", "recorded"}


def test_labels_to_dwi_calls_sibling_or_recorded_and_does_not_post(
    illegal_labels_t1w_on_dwi,
):
    status = sciguard_validate(illegal_labels_t1w_on_dwi)
    assert status == "FAIL"
    mode = sciguard_mode()
    assert mode in {"sibling", "recorded"}
    if sciguard_sibling():
        assert mode == "sibling"
    poster = PostRecorder()
    result = submit(illegal_labels_t1w_on_dwi, arm="G", approve=True, poster=poster)
    assert result.sciguard_status == "FAIL"
    assert result.posted is False
    assert poster.posts == []
    assert result.guard_mode["sciguard"] in {"sibling", "recorded"}


def test_space_omitted_calls_sibling_or_recorded_and_does_not_post(
    illegal_space_omitted,
):
    decision = scicap_invoke(illegal_space_omitted)
    assert decision == "ABSTAIN"
    mode = scicap_mode()
    assert mode in {"sibling", "recorded"}
    if scicap_sibling():
        assert mode == "sibling"
    poster = PostRecorder()
    result = submit(illegal_space_omitted, arm="G", approve=True, poster=poster)
    assert result.scicap_decision == "ABSTAIN"
    assert result.posted is False
    assert poster.posts == []
    assert result.guard_mode["scicap"] in {"sibling", "recorded"}
    assert "space" not in (illegal_space_omitted.get("parameters") or {})
