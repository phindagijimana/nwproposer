"""CyberNeuro Planner ≠ Dispatcher (protocol only).

Cite: CyberNeuro, arXiv:2607.28841.
No Linux git found. Do not wrap WandaMind. Dispatcher is existing submit, not an agent.
Planner writes a propose_request. Dispatcher does not execute and does not
import backend.execution.
"""

from __future__ import annotations

import sys
from typing import Any, Mapping

from proposer.canonicalize import canonicalize
from proposer.forbidden import assert_execution_not_loaded
from proposer.propose import propose

CITATION = "arXiv:2607.28841"
SHELL_KEYS = ("command", "shell", "bash", "argv", "claw-shell", "claw_shell")


def _reject_shell(document: Mapping[str, Any], *, role: str) -> None:
    hits = [key for key in SHELL_KEYS if key in document]
    if hits:
        raise ValueError(f"{role} accepts a propose_request, not a shell command: {hits}")


def plan(intent: Mapping[str, Any]) -> dict[str, Any]:
    """Planner writes a propose_request. Not a shell command. Does not execute."""
    assert_execution_not_loaded()
    _reject_shell(intent, role="Planner")
    request = propose(intent)
    request["kind"] = "propose_request"
    request["planner"] = "cyberneuro_protocol"
    request["citation"] = CITATION
    notes = dict(request.get("notes") or {})
    notes["not_a_shell_command"] = True
    notes["dispatcher_is_existing_submit"] = True
    notes["agent_may_not_execute"] = True
    request["notes"] = notes
    return request


def is_propose_request(document: Mapping[str, Any]) -> bool:
    if any(key in document for key in SHELL_KEYS):
        return False
    required = ("plugin_id", "image_digest", "inputs", "backend", "network")
    return all(field in document for field in required)


def dispatch(
    request: Mapping[str, Any],
    *,
    approve: bool = False,
) -> dict[str, Any]:
    """Existing-submit stub. Does not execute. Does not load backend.execution.

    SciCap/SciGuard are not applied here — those are Paper 6 Validator residual.
    """
    assert_execution_not_loaded()
    _reject_shell(request, role="Dispatcher")
    if not is_propose_request(request):
        raise ValueError("Dispatcher accepts a propose_request, not a shell command")
    if "backend.execution" in sys.modules:
        raise RuntimeError("Dispatcher must not load backend.execution")

    from adapters.neuroinsight.job import to_job_payload

    job = to_job_payload(request, canonical=canonicalize(request))
    return {
        "role": "dispatcher",
        "implemented_as": "existing_submit_stub",
        "executed": False,
        "posted": False,
        "imported_backend_execution": False,
        "backend_execution_loaded": "backend.execution" in sys.modules,
        "handed_to": "existing_submit",
        "approve": bool(approve),
        "job": job,
        "citation": CITATION,
    }
