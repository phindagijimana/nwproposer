"""A3: G does not POST illegal jobs; U incorrect-submission is higher."""

from __future__ import annotations

import json

import jsonschema

from proposer.canonicalize import paper_root
from proposer.score import item_score, platform_silent_success
from proposer.submit import PostRecorder, incorrect_submission_rate, submit


def test_scicap_reject_dk_as_dkt_g_does_not_post(illegal_dk_as_dkt):
    poster = PostRecorder()
    result = submit(illegal_dk_as_dkt, arm="G", approve=True, poster=poster)
    assert result.scicap_decision == "REJECT"
    assert result.posted is False
    assert result.reason == "scicap_reject"
    assert result.incorrect_submission is False
    assert poster.posts == []


def test_sciguard_fail_labels_to_dwi_g_does_not_post(illegal_labels_t1w_on_dwi):
    poster = PostRecorder()
    result = submit(illegal_labels_t1w_on_dwi, arm="G", approve=True, poster=poster)
    assert result.sciguard_status == "FAIL"
    assert result.posted is False
    assert result.reason == "sciguard_fail"
    assert result.incorrect_submission is False
    assert poster.posts == []


def test_u_posts_illegal_jobs_g_does_not(
    illegal_dk_as_dkt, illegal_labels_t1w_on_dwi
):
    fixtures = [illegal_dk_as_dkt, illegal_labels_t1w_on_dwi]
    g_results = []
    u_results = []
    for fixture in fixtures:
        g_poster = PostRecorder()
        u_poster = PostRecorder()
        g_results.append(submit(fixture, arm="G", approve=True, poster=g_poster))
        u_results.append(submit(fixture, arm="U", approve=True, poster=u_poster))
        assert g_poster.posted is False
        assert u_poster.posted is True

    assert all(not row.posted for row in g_results)
    assert all(row.posted and row.incorrect_submission for row in u_results)
    assert incorrect_submission_rate(u_results) > incorrect_submission_rate(g_results)


def test_qc_skipped_reported_complete_is_silent_success(
    silent_success_receipt, arms
):
    assert set(arms) == {"H", "G", "U"}
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


def test_item_score_matches_schema(illegal_dk_as_dkt):
    schema_path = paper_root() / "schema" / "score.schema.json"
    schema = json.loads(schema_path.read_text())
    g = submit(illegal_dk_as_dkt, arm="G", approve=True, poster=PostRecorder())
    record = item_score(
        item_id="dk_as_dkt",
        arm="G",
        posted=g.posted,
        scicap_decision=g.scicap_decision,
        sciguard_status=g.sciguard_status,
        job_equal_to_human=None,
    )
    jsonschema.validate(record, schema)
    assert record["incorrect_submission"] is False
    assert record["posted"] is False
