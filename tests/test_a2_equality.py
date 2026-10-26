"""A2: human-recorded FastSurfer job equals gated-proposer job on equality_fields."""

from __future__ import annotations

from proposer.canonicalize import canonicalize, load_document, load_equality_fields
from proposer.equality import jobs_equal
from proposer.propose import propose
from proposer.submit import PostRecorder, submit


def test_equality_fields_are_locked_in_schema():
    assert load_equality_fields() == [
        "plugin_id",
        "image_digest",
        "inputs",
        "backend",
        "network",
    ]


def test_human_fastsurfer_job_is_recorded(human_fastsurfer_job):
    human = load_document(human_fastsurfer_job)
    assert human["proposer"] == "human"
    assert human["plugin_id"] == "fastsurfer"
    assert human["source"] == "stub_not_cloned_private_repo"


def test_g_equals_human_on_equality_fields(human_fastsurfer_job, example_propose_fastsurfer):
    assert jobs_equal(human_fastsurfer_job, example_propose_fastsurfer)


def test_propose_from_same_intent_matches_human(human_fastsurfer_job):
    human = load_document(human_fastsurfer_job)
    request = propose(
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
    assert jobs_equal(human, request)
    poster = PostRecorder()
    result = submit(request, arm="G", approve=True, poster=poster)
    assert result.posted is True
    assert jobs_equal(human, result.job)


def test_canonicalize_drops_non_equality_fields(human_fastsurfer_job):
    human = load_document(human_fastsurfer_job)
    canonical = canonicalize(human)
    assert set(canonical) == set(load_equality_fields())
    assert "job_id" not in canonical
    assert "proposer" not in canonical


def test_digest_or_plugin_mismatch_is_not_equal(human_fastsurfer_job):
    human = load_document(human_fastsurfer_job)
    other = dict(human)
    other["image_digest"] = "sha256:DIFFERENT"
    assert jobs_equal(human, other) is False
    other = dict(human)
    other["plugin_id"] = "qsiprep"
    assert jobs_equal(human, other) is False
    other = dict(human)
    other["network"] = "on"
    assert jobs_equal(human, other) is False
