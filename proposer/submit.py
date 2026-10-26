"""Dry-run submit through the existing job API only if G gates pass.

Arm G is not a NeuroClaw wrap. Arm U is an unconstrained stub that skips gates.
No HTTP is sent. The private neuroinsight_research repo is not imported.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from adapters.neuroinsight.job import to_job_payload
from baselines.neuropilot_approval import review_approval
from guards.scicap import guard_mode as scicap_guard_mode
from guards.scicap import invoke as scicap_invoke
from guards.sciguard import guard_mode as sciguard_guard_mode
from guards.sciguard import is_workflow, validate as sciguard_validate
from proposer.canonicalize import canonicalize
from proposer.forbidden import assert_execution_not_loaded, assert_no_forbidden_imports


@dataclass
class PostRecorder:
    """In-process stand-in for FastAPI submit. Tests inspect .posts."""

    posts: list[dict[str, Any]] = field(default_factory=list)

    def post(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        record = dict(payload)
        self.posts.append(record)
        return {"status": "dry_run", "posted": True, "payload": record}

    @property
    def posted(self) -> bool:
        return bool(self.posts)


@dataclass
class SubmitResult:
    arm: str
    posted: bool
    reason: str
    scicap_decision: str
    sciguard_status: str
    incorrect_submission: bool
    job: dict[str, Any] | None = None
    guard_mode: dict[str, str] = field(default_factory=dict)


def _illegal_for_score(scicap_decision: str, sciguard_status: str) -> bool:
    return scicap_decision in {"REJECT", "ABSTAIN"} or sciguard_status == "FAIL"


def _modes() -> dict[str, str]:
    return {"scicap": scicap_guard_mode(), "sciguard": sciguard_guard_mode()}


def submit(
    request: Mapping[str, Any],
    *,
    arm: str,
    approve: bool = False,
    poster: PostRecorder | None = None,
) -> SubmitResult:
    """POST only on arm G when SciCap/SciGuard allow and approval is set.

    NeuroPilot consequential fields (network: on, overwrite, backend switch)
    still require the explicit approve flag. Arm U posts without gates.
    Dry-run only.
    """
    assert_execution_not_loaded()
    assert_no_forbidden_imports()
    if arm not in {"H", "G", "U"}:
        raise ValueError(f"unknown arm {arm!r}; declare H, G, or U")

    recorder = poster or PostRecorder()
    scicap_decision = scicap_invoke(request)
    sciguard_status = (
        sciguard_validate(request) if is_workflow(request) else "not_applicable"
    )
    illegal = _illegal_for_score(scicap_decision, sciguard_status)
    approved = approve or bool((request.get("approval") or {}).get("execution"))
    review = review_approval(request, already_approved=approve)
    modes = _modes()

    if arm == "U":
        job = to_job_payload(request, canonical=canonicalize(request))
        recorder.post(job)
        return SubmitResult(
            arm="U",
            posted=True,
            reason="unconstrained",
            scicap_decision=scicap_decision,
            sciguard_status=sciguard_status,
            incorrect_submission=illegal,
            job=job,
            guard_mode=modes,
        )

    if scicap_decision in {"REJECT", "ABSTAIN"}:
        return SubmitResult(
            arm=arm,
            posted=False,
            reason=f"scicap_{scicap_decision.lower()}",
            scicap_decision=scicap_decision,
            sciguard_status=sciguard_status,
            incorrect_submission=False,
            guard_mode=modes,
        )

    if is_workflow(request) and sciguard_status == "FAIL":
        return SubmitResult(
            arm=arm,
            posted=False,
            reason="sciguard_fail",
            scicap_decision=scicap_decision,
            sciguard_status=sciguard_status,
            incorrect_submission=False,
            guard_mode=modes,
        )

    if not approved or (review["requires_approve"] and not approve):
        return SubmitResult(
            arm=arm,
            posted=False,
            reason="approval_required",
            scicap_decision=scicap_decision,
            sciguard_status=sciguard_status,
            incorrect_submission=False,
            guard_mode=modes,
        )

    job = to_job_payload(request, canonical=canonicalize(request))
    recorder.post(job)
    return SubmitResult(
        arm=arm,
        posted=True,
        reason="dry_run_existing_submit",
        scicap_decision=scicap_decision,
        sciguard_status=sciguard_status,
        incorrect_submission=False,
        job=job,
        guard_mode=modes,
    )


def incorrect_submission_rate(results: list[SubmitResult]) -> float:
    if not results:
        return 0.0
    return sum(1 for result in results if result.incorrect_submission) / len(results)
