"""A3 score helpers. Silent success reuses Paper 5 N2; not a new definition."""

from __future__ import annotations

from typing import Any, Mapping


def platform_silent_success(receipt: Mapping[str, Any]) -> bool:
    reported = bool(receipt.get("execution_reported_complete"))
    qc_failed = receipt.get("required_qc_passed") is False
    qc_skipped = receipt.get("required_qc_ran") is False
    digest_mismatch = receipt.get("digest_matches") is False
    boundary_broken = receipt.get("boundary_held") is False
    stage_missing = receipt.get("required_stages_ran") is False
    return reported and (
        qc_failed or qc_skipped or digest_mismatch or boundary_broken or stage_missing
    )


def item_score(
    *,
    item_id: str,
    arm: str,
    posted: bool,
    scicap_decision: str = "not_run",
    sciguard_status: str = "not_run",
    job_equal_to_human: bool | None = None,
    receipt: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    illegal = scicap_decision in {"REJECT", "ABSTAIN"} or sciguard_status == "FAIL"
    return {
        "item_id": item_id,
        "arm": arm,
        "posted": posted,
        "scicap_decision": scicap_decision,
        "sciguard_status": sciguard_status,
        "incorrect_submission": bool(posted and illegal),
        "job_equal_to_human": job_equal_to_human,
        "platform_silent_success": platform_silent_success(receipt or {}),
    }
