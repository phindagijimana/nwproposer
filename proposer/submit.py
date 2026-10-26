"""Dry-run submit through the public neuroworkbench kernel only if G gates pass.

Arm G is not a NeuroClaw wrap. REJECT / ABSTAIN / FAIL never reach neuroworkbench.
Arm U is an unconstrained stub (not a NeuroClaw wrap) that skips gates.
Kernel is neuroworkbench (Paper 5), not neuroinsight_research.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from pathlib import Path

from adapters.neuroinsight.job import to_job_payload
from adapters.neuroworkbench.request import workbench_available, workbench_submit
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
    workbench: dict[str, Any] | None = None
    execute_called: bool = False


_BLOCKING_SCICAP = frozenset({"REJECT", "ABSTAIN"})
_BLOCKING_SCIGUARD = frozenset({"FAIL"})


def _illegal_for_score(scicap_decision: str, sciguard_status: str) -> bool:
    return scicap_decision in _BLOCKING_SCICAP or sciguard_status in _BLOCKING_SCIGUARD


def _gate_block_reason(scicap_decision: str, sciguard_status: str) -> str | None:
    """Reason G/H must not hand this request to neuroworkbench, or None."""
    if scicap_decision in _BLOCKING_SCICAP:
        return f"scicap_{scicap_decision.lower()}"
    if sciguard_status in _BLOCKING_SCIGUARD:
        return "sciguard_fail"
    return None


def _modes() -> dict[str, str]:
    return {"scicap": scicap_guard_mode(), "sciguard": sciguard_guard_mode()}


def submit(
    request: Mapping[str, Any],
    *,
    arm: str,
    approve: bool = False,
    poster: PostRecorder | None = None,
    kernel: str = "recorder",
    store: Path | None = None,
) -> SubmitResult:
    """POST only on arm G when SciCap/SciGuard allow and approval is set.

    NeuroPilot consequential fields (network: on, overwrite, backend switch)
    still require the explicit approve flag. Arm U posts without gates.
    kernel='workbench' uses public neuroworkbench.submit (dry-run).
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
        # Unconstrained stub: skip gates and the workbench kernel. Not NeuroClaw.
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
            workbench=None,
        )

    blocked = _gate_block_reason(scicap_decision, sciguard_status)
    if blocked:
        return SubmitResult(
            arm=arm,
            posted=False,
            reason=blocked,
            scicap_decision=scicap_decision,
            sciguard_status=sciguard_status,
            incorrect_submission=False,
            guard_mode=modes,
            workbench=None,
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
            workbench=None,
        )

    job = to_job_payload(request, canonical=canonicalize(request))
    workbench_result = None
    execute_called = False
    reason = "dry_run_existing_submit"
    if kernel == "workbench":
        if not workbench_available():
            return SubmitResult(
                arm=arm,
                posted=False,
                reason="workbench_unavailable",
                scicap_decision=scicap_decision,
                sciguard_status=sciguard_status,
                incorrect_submission=False,
                job=job,
                guard_mode=modes,
                workbench=None,
            )
        workbench_result = workbench_submit(
            request,
            approve=approve,
            store=store or Path(".nwproposer_store"),
        )
        execute_called = bool(workbench_result.get("execute_called"))
        if workbench_result.get("status") == "rejected":
            return SubmitResult(
                arm=arm,
                posted=False,
                reason=str(workbench_result.get("reason") or "workbench_rejected"),
                scicap_decision=scicap_decision,
                sciguard_status=sciguard_status,
                incorrect_submission=False,
                job=job,
                guard_mode=modes,
                workbench=workbench_result,
                execute_called=execute_called,
            )
        reason = "dry_run_neuroworkbench"
    recorder.post(job)
    return SubmitResult(
        arm=arm,
        posted=True,
        reason=reason,
        scicap_decision=scicap_decision,
        sciguard_status=sciguard_status,
        incorrect_submission=False,
        job=job,
        guard_mode=modes,
        workbench=workbench_result,
        execute_called=execute_called,
    )


def incorrect_submission_rate(results: list[SubmitResult]) -> float:
    if not results:
        return 0.0
    return sum(1 for result in results if result.incorrect_submission) / len(results)
