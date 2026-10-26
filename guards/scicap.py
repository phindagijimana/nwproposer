"""SciCap invoke gate (Paper 1). Sibling package if importable, else recorded mock.

REJECT on DK declared as DKT or a demonstrated atlas/modality contradiction.
ABSTAIN when space evidence is omitted. ALLOW otherwise.
REJECT must still not POST (see proposer.submit).
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Callable, Mapping

GUARD_MODE_RECORDED = "recorded"
GUARD_MODE_SIBLING = "sibling"

_WORKSPACE = Path(__file__).resolve().parents[2]
_SCICAP_CORE = _WORKSPACE / "01_SciCap" / "packages" / "scicap-core"
_SCICAP_CAPABILITY = (
    _WORKSPACE
    / "01_SciCap"
    / "packages"
    / "scicap-neuro"
    / "capabilities"
    / "neuro.t1.hippocampal_volumes.yaml"
)
_SHARED_DK_AS_DKT = (
    _WORKSPACE / "shared" / "fixtures" / "invalid" / "dk_as_dkt" / "instance.json"
)

_guard_mode = GUARD_MODE_RECORDED
_sibling_invoke: Callable[..., Any] | None | bool = False


def guard_mode() -> str:
    return _guard_mode


def _load_sibling_invoke() -> Callable[..., Any] | None:
    global _sibling_invoke
    if _sibling_invoke is not False:
        return _sibling_invoke if callable(_sibling_invoke) else None

    invoke_fn: Callable[..., Any] | None = None
    try:
        from scicap_core.invoke import invoke as invoke_fn  # type: ignore
    except ImportError:
        invoke_fn = None

    if invoke_fn is None and (_SCICAP_CORE / "__init__.py").is_file():
        if "scicap_core" not in sys.modules:
            spec = importlib.util.spec_from_file_location(
                "scicap_core",
                _SCICAP_CORE / "__init__.py",
                submodule_search_locations=[str(_SCICAP_CORE)],
            )
            if spec is not None and spec.loader is not None:
                module = importlib.util.module_from_spec(spec)
                sys.modules["scicap_core"] = module
                try:
                    spec.loader.exec_module(module)
                except Exception:
                    sys.modules.pop("scicap_core", None)
                    invoke_fn = None
                else:
                    invoke_fn = getattr(module, "invoke", None)
        else:
            invoke_fn = getattr(sys.modules["scicap_core"], "invoke", None)

    if invoke_fn is None:
        try:
            import scicap  # type: ignore

            invoke_fn = getattr(scicap, "invoke", None)
        except ImportError:
            invoke_fn = None

    _sibling_invoke = invoke_fn
    return invoke_fn


def sibling_available() -> bool:
    return _load_sibling_invoke() is not None and _SCICAP_CAPABILITY.is_file()


def _is_dk_as_dkt(request: Mapping[str, Any]) -> bool:
    parameters = request.get("parameters") or {}
    if parameters.get("illegal_family") == "dk_as_dkt":
        return True
    declared = parameters.get("atlas_declared")
    actual = parameters.get("atlas_actual")
    return bool(declared and actual and declared != actual)


def _instance_for_request(request: Mapping[str, Any]) -> dict[str, Any] | Path:
    parameters = request.get("parameters") or {}
    inputs = request.get("inputs") or {}
    if _SHARED_DK_AS_DKT.is_file() and _is_dk_as_dkt(request):
        return _SHARED_DK_AS_DKT
    instance: dict[str, Any] = {
        "modality": parameters.get("modality") or "T1w",
        "space": parameters.get("space") or "subject_native",
        "atlas": parameters.get("atlas_declared") or parameters.get("atlas"),
        "label_set": parameters.get("atlas_actual") or parameters.get("label_set"),
        "path": inputs.get("labels") or inputs.get("T1w"),
    }
    return instance


def _recorded_invoke(request: Mapping[str, Any]) -> str:
    parameters = request.get("parameters") or {}
    declared = parameters.get("atlas_declared")
    actual = parameters.get("atlas_actual")
    if declared and actual and declared != actual:
        return "REJECT"
    if parameters.get("illegal_family") == "dk_as_dkt":
        return "REJECT"
    if parameters.get("wrong_modality"):
        return "REJECT"
    if parameters.get("space_omitted") or parameters.get("illegal_family") == "missing_space":
        return "ABSTAIN"
    return "ALLOW"


def invoke(request: Mapping[str, Any]) -> str:
    """Return ALLOW / REJECT / ABSTAIN. Sets guard_mode to sibling or recorded."""
    global _guard_mode
    sibling = _load_sibling_invoke()
    if sibling is not None and _is_dk_as_dkt(request) and _SCICAP_CAPABILITY.is_file():
        try:
            result = sibling(_SCICAP_CAPABILITY, _instance_for_request(request))
            decision = str(result.get("decision", ""))
        except Exception:
            decision = ""
        if decision in {"ALLOW", "REJECT", "ABSTAIN"}:
            _guard_mode = GUARD_MODE_SIBLING
            return decision
    _guard_mode = GUARD_MODE_RECORDED
    return _recorded_invoke(request)
