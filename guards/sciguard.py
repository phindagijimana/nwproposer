"""SciGuard validate gate (Paper 2). Sibling package if importable, else recorded mock.

labels in T1w space wired to DWI with no transform is a demonstrated mismatch → FAIL.
Missing transform evidence on an otherwise unspecified edge would be UNKNOWN;
Paper 6's locked illegal fixture is the known-illegal labels→DWI wiring.
FAIL must still not POST (see proposer.submit).
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable, Mapping

GUARD_MODE_RECORDED = "recorded"
GUARD_MODE_SIBLING = "sibling"

_WORKSPACE = Path(__file__).resolve().parents[2]
_SCIGUARD_ROOT = _WORKSPACE / "02_SciGuard"

_guard_mode = GUARD_MODE_RECORDED
_sibling_check: Callable[..., Any] | None | bool = False


def guard_mode() -> str:
    return _guard_mode


def is_workflow(request: Mapping[str, Any]) -> bool:
    return bool(
        request.get("workflow")
        or request.get("workflow_id")
        or request.get("kind") == "workflow"
    )


def _load_sibling_check() -> Callable[..., Any] | None:
    global _sibling_check
    if _sibling_check is not False:
        return _sibling_check if callable(_sibling_check) else None

    check_fn: Callable[..., Any] | None = None
    try:
        from validation.check import check_workflow as check_fn  # type: ignore
    except ImportError:
        check_fn = None

    if check_fn is None and _SCIGUARD_ROOT.is_dir():
        if str(_SCIGUARD_ROOT) not in sys.path:
            sys.path.insert(0, str(_SCIGUARD_ROOT))
        try:
            from validation.check import check_workflow as check_fn  # type: ignore
        except ImportError:
            check_fn = None

    if check_fn is None:
        try:
            import sciguard  # type: ignore

            check_fn = getattr(sciguard, "check_workflow", None) or getattr(
                sciguard, "validate", None
            )
        except ImportError:
            check_fn = None

    _sibling_check = check_fn
    return check_fn


def sibling_available() -> bool:
    return _load_sibling_check() is not None


def _transform_missing(inputs: Mapping[str, Any]) -> bool:
    if "transform" not in inputs:
        return True
    transform = inputs.get("transform")
    if transform in (None, "", "omitted", "missing"):
        return True
    if isinstance(transform, dict) and not transform.get("verified"):
        return True
    return False


def _labels_t1w_on_dwi(inputs: Mapping[str, Any]) -> bool:
    labels = inputs.get("labels")
    dwi = inputs.get("dwi") or inputs.get("reference")
    if not isinstance(labels, dict) or dwi is None:
        return False
    label_space = str(labels.get("space", "")).lower()
    return "t1w" in label_space and _transform_missing(inputs)


def _is_labels_to_dwi(request: Mapping[str, Any]) -> bool:
    parameters = request.get("parameters") or {}
    if parameters.get("illegal_family") == "labels_t1w_on_dwi":
        return True
    return _labels_t1w_on_dwi(request.get("inputs") or {})


def _request_to_workflow(request: Mapping[str, Any]) -> dict[str, Any]:
    """Map a Paper 6 propose_request onto SciGuard's declared-DAG schema."""
    inputs = request.get("inputs") or {}
    labels = inputs.get("labels") if isinstance(inputs.get("labels"), dict) else {}
    dwi = inputs.get("dwi") if isinstance(inputs.get("dwi"), dict) else {}
    if not dwi and isinstance(inputs.get("reference"), dict):
        dwi = inputs["reference"]
    edges: list[dict[str, Any]] = [
        {
            "id": "labels→map1",
            "from": "labels",
            "to": "map1.labels",
            "artifact": {
                "kind": labels.get("kind") or "parcellation",
                "modality": labels.get("modality") or "T1w",
                "space": labels.get("space") or "subject_T1w",
                "atlas": labels.get("atlas"),
                "value_type": labels.get("value_type") or "discrete_labels",
            },
        },
        {
            "id": "ref→map1",
            "from": "tractogram",
            "to": "map1.reference",
            "artifact": {
                "kind": dwi.get("kind") or "diffusion_reference",
                "modality": dwi.get("modality") or "dwi",
                "space": dwi.get("space") or "subject_DWI",
            },
        },
    ]
    transform = inputs.get("transform")
    if isinstance(transform, dict) and not _transform_missing(inputs):
        edges.append(
            {
                "id": "xfm→map1",
                "from": "transform",
                "to": "map1.transform",
                "artifact": {
                    "kind": "spatial_transform",
                    "from_space": transform.get("from_space"),
                    "to_space": transform.get("to_space"),
                    "same_subject": transform.get("same_subject", True),
                    "verified": transform.get("verified", True),
                },
            }
        )
    return {
        "schema_version": "0.1",
        "workflow_id": str(
            request.get("workflow_id") or request.get("plugin_id") or "paper6-request"
        ),
        "operations": [
            {
                "id": "map1",
                "contract": "map_labels_to_diffusion",
                "interpolation": "nearest_neighbor",
            }
        ],
        "edges": edges,
    }


def _status_from_report(report: Mapping[str, Any]) -> str | None:
    edges = report.get("edges") or []
    statuses = {str(item.get("status")) for item in edges if isinstance(item, dict)}
    graph = str(report.get("graph_status") or "")
    if "FAIL" in statuses or graph == "reject":
        return "FAIL"
    if "UNKNOWN" in statuses or graph == "not_auto_accepted":
        return "UNKNOWN"
    if statuses <= {"PASS"} and edges:
        return "PASS"
    raw = report.get("status")
    if raw in {"FAIL", "PASS", "UNKNOWN"}:
        return str(raw)
    return None


def _recorded_validate(request: Mapping[str, Any]) -> str:
    if not is_workflow(request):
        return "not_applicable"
    parameters = request.get("parameters") or {}
    inputs = request.get("inputs") or {}
    if parameters.get("illegal_family") == "labels_t1w_on_dwi" or _labels_t1w_on_dwi(
        inputs
    ):
        return "FAIL"
    if _transform_missing(inputs):
        return "UNKNOWN"
    return "PASS"


def validate(request: Mapping[str, Any]) -> str:
    """Return PASS / FAIL / UNKNOWN / not_applicable. Sets guard_mode."""
    global _guard_mode
    if not is_workflow(request):
        _guard_mode = GUARD_MODE_RECORDED
        return "not_applicable"

    sibling = _load_sibling_check()
    if sibling is not None:
        try:
            report = sibling(_request_to_workflow(request))
            status = _status_from_report(report) if isinstance(report, Mapping) else None
        except Exception:
            status = None
        if status in {"PASS", "FAIL", "UNKNOWN"}:
            _guard_mode = GUARD_MODE_SIBLING
            return status

    _guard_mode = GUARD_MODE_RECORDED
    return _recorded_validate(request)
