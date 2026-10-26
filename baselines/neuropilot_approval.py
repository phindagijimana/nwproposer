"""NeuroPilot consequential-approval list (protocol only).

Cite: Chen et al., NeuroPilot, arXiv:2608.07541.
No research git. The VS Code repo VSC-NeuroPilot/neuropilot is unrelated.
This is the paper's field list, not a vendored skill pack.
"""

from __future__ import annotations

from typing import Any, Mapping

from proposer.canonicalize import normalize_network

CITATION = "arXiv:2608.07541"
UNRELATED_VSCODE = "VSC-NeuroPilot/neuropilot is an unrelated VS Code extension"

# Locked list from the NeuroPilot paper / propose_request.yaml.
CONSEQUENTIAL_FIELDS = (
    "overwrite",
    "delete",
    "slurm_array",
    "backend_switch",
    "network_on",
    "fallback_plugin",
)


def _truthy(value: Any) -> bool:
    return value not in (None, False, "", 0, "off", "false", "False")


def _lookup(request: Mapping[str, Any], *names: str) -> bool:
    pools = (
        request,
        request.get("parameters") or {},
        request.get("approval") or {},
        request.get("actions") or {},
    )
    for name in names:
        for pool in pools:
            if isinstance(pool, Mapping) and name in pool and _truthy(pool[name]):
                return True
    return False


def consequential_triggers(request: Mapping[str, Any]) -> list[str]:
    """Return which locked consequential fields are present. Atlas/space are not in this list."""
    triggers: list[str] = []
    if normalize_network(request.get("network")) == "on":
        triggers.append("network_on")
    if _lookup(request, "overwrite"):
        triggers.append("overwrite")
    if _lookup(request, "delete"):
        triggers.append("delete")
    array_flag = request.get("array")
    if _lookup(request, "slurm_array", "array_job") or array_flag is True:
        triggers.append("slurm_array")
    previous = request.get("previous_backend")
    current = request.get("backend")
    if _lookup(request, "backend_switch") or (
        previous and current and previous != current
    ):
        triggers.append("backend_switch")
    if _lookup(request, "fallback_plugin", "fallback"):
        triggers.append("fallback_plugin")
    return triggers


def review_approval(
    request: Mapping[str, Any],
    *,
    already_approved: bool | None = None,
) -> dict[str, Any]:
    """Return whether the NeuroPilot list requires approve.

    ``requires_approve`` is true iff a locked consequential field is present.
    Already-approved jobs with no such field need no extra approve.
    Atlas/space mismatches are not in this list (SciCap/SciGuard residual).
    """
    triggers = consequential_triggers(request)
    approval = request.get("approval") or {}
    if already_approved is None:
        already_approved = bool(approval.get("execution")) or request.get(
            "proposer"
        ) == "human"
    requires_approve = bool(triggers)
    return {
        "requires_approve": requires_approve,
        "triggers": triggers,
        "already_approved": bool(already_approved),
        "extra_approve": requires_approve and not already_approved,
        "citation": CITATION,
        "unrelated_vscode": UNRELATED_VSCODE,
    }
