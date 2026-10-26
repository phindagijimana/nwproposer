"""Paper 5 neuroworkbench request map. Public kernel. No private repo."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable, Mapping

from proposer.canonicalize import normalize_network

_WORKSPACE = Path(__file__).resolve().parents[3]
_WORKBENCH_ROOT = _WORKSPACE / "05_NeuroInsight"

BACKEND_TO_WORKBENCH = {
    "local_docker": "local_container",
    "remote_docker": "local_container",
    "docker": "local_container",
    "local_container": "local_container",
    "slurm": "slurm",
}


def to_workbench_request(request: Mapping[str, Any]) -> dict[str, Any]:
    """Emit a neuroworkbench run request. Does not execute."""
    backend = BACKEND_TO_WORKBENCH.get(str(request.get("backend")), request.get("backend"))
    approval = request.get("approval")
    if not isinstance(approval, dict):
        approval = {"execution": bool(approval)}
    return {
        "proposer": request.get("proposer") or "agent",
        "plugin_id": request["plugin_id"],
        "plugin_version": str(request.get("plugin_version") or "0.1.0"),
        "image_digest": request["image_digest"],
        "inputs": dict(request.get("inputs") or {}),
        "parameters": dict(request.get("parameters") or {}),
        "backend": backend,
        "network": normalize_network(request.get("network", "off")),
        "approval": dict(approval) or {"execution": False},
    }


def _load_submit() -> Callable[..., Any] | None:
    try:
        from neuroworkbench import submit as submit_fn

        return submit_fn
    except ImportError:
        pass
    if _WORKBENCH_ROOT.is_dir() and str(_WORKBENCH_ROOT) not in sys.path:
        sys.path.insert(0, str(_WORKBENCH_ROOT))
    try:
        from neuroworkbench import submit as submit_fn

        return submit_fn
    except ImportError:
        return None


def workbench_available() -> bool:
    return _load_submit() is not None


def workbench_submit(
    request: Mapping[str, Any],
    *,
    approve: bool,
    store: Path,
) -> dict[str, Any]:
    """Dry-run through public neuroworkbench.submit. No container start from Paper 6."""
    submit_fn = _load_submit()
    if submit_fn is None:
        raise ImportError("neuroworkbench is not importable; install the public Paper 5 package")
    mapped = to_workbench_request(request)
    return submit_fn(mapped, approve=approve, store=store, dry_run=True)
