"""Map a propose_request onto the inspected NeuroInsight FastAPI job fields.

Inspected product (2026-10-26, private repo not cloned): desktop + FastAPI +
YAML plugins (`plugins/fastsurfer.yaml`, fMRIPrep, QSIPrep, …) and
Docker/Slurm backends. A submit object carries plugin + image digest +
inputs + backend (docker or slurm) + network.

This adapter is a **contract map**, not a dump or clone of
`neuroinsight_research`. Equality vs a human UI job is defined only on
`equality_fields`: plugin_id, image_digest, inputs, backend, network.
"""

from __future__ import annotations

from typing import Any, Mapping

from proposer.canonicalize import normalize_network

EQUALITY_FIELDS = (
    "plugin_id",
    "image_digest",
    "inputs",
    "backend",
    "network",
)

# Inspected FastAPI submit vocabulary → propose_request backend enum.
BACKEND_FROM_PRODUCT = {
    "docker": "local_docker",
    "local_docker": "local_docker",
    "remote_docker": "remote_docker",
    "slurm": "slurm",
}

PRODUCT_SHAPE_NOTES = (
    "Hand-authored FastAPI job shape from the 2026-10-26 product inspection: "
    "plugin{id,version,descriptor=plugins/<name>.yaml} + image{digest,container} "
    "+ backend{kind: docker|slurm} + inputs + network. "
    "Not exported from neuroinsight_research; that repo is not vendored here."
)


def _backend_from_product(raw: Any) -> Any:
    if isinstance(raw, Mapping):
        kind = raw.get("kind") or raw.get("type") or raw.get("name")
        return BACKEND_FROM_PRODUCT.get(str(kind), kind)
    if raw in BACKEND_FROM_PRODUCT:
        return BACKEND_FROM_PRODUCT[str(raw)]
    return raw


def from_product_job(product: Mapping[str, Any]) -> dict[str, Any]:
    """Extract locked equality fields from a product-shaped FastAPI job."""
    plugin = product.get("plugin") if isinstance(product.get("plugin"), Mapping) else {}
    image = product.get("image") if isinstance(product.get("image"), Mapping) else {}
    return {
        "plugin_id": plugin.get("id") or product.get("plugin_id"),
        "image_digest": image.get("digest") or product.get("image_digest"),
        "inputs": product.get("inputs"),
        "backend": _backend_from_product(product.get("backend")),
        "network": normalize_network(product.get("network", "off")),
    }


def to_product_job(request: Mapping[str, Any]) -> dict[str, Any]:
    """Emit the inspected FastAPI shape from a propose_request (contract only)."""
    backend = request.get("backend")
    kind = "slurm" if backend == "slurm" else "docker"
    plugin_id = request["plugin_id"]
    return {
        "plugin": {
            "id": plugin_id,
            "version": request.get("plugin_version"),
            "descriptor": f"plugins/{plugin_id}.yaml",
        },
        "image": {
            "digest": request["image_digest"],
            "container": "docker" if kind == "docker" else "slurm",
        },
        "backend": {"kind": kind},
        "inputs": request["inputs"],
        "network": normalize_network(request.get("network", "off")),
    }


def to_job_payload(
    request: Mapping[str, Any],
    *,
    canonical: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    fields = canonical or {
        "plugin_id": request["plugin_id"],
        "image_digest": request["image_digest"],
        "inputs": request["inputs"],
        "backend": request["backend"],
        "network": normalize_network(request.get("network", "off")),
    }
    payload = {
        "plugin_id": fields["plugin_id"],
        "image_digest": fields["image_digest"],
        "inputs": fields["inputs"],
        "backend": fields["backend"],
        "network": fields["network"],
        "plugin_version": request.get("plugin_version"),
        "parameters": dict(request.get("parameters") or {}),
        "proposer": request.get("proposer", "agent"),
    }
    if request.get("workflow") or request.get("workflow_id"):
        payload["workflow_id"] = request.get("workflow_id") or request.get("plugin_id")
    return payload
