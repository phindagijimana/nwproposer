"""A2: canonicalize a propose_request / job document on locked equality fields."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

import yaml

EQUALITY_FIELDS_FALLBACK = (
    "plugin_id",
    "image_digest",
    "inputs",
    "backend",
    "network",
)


def paper_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_equality_fields(schema_path: Path | None = None) -> list[str]:
    path = schema_path or paper_root() / "schema" / "propose_request.yaml"
    data = yaml.safe_load(path.read_text())
    fields = data.get("equality_fields") or list(EQUALITY_FIELDS_FALLBACK)
    return list(fields)


def load_document(source: Mapping[str, Any] | str | Path) -> dict[str, Any]:
    if isinstance(source, Mapping):
        return dict(source)
    path = Path(source)
    text = path.read_text()
    if path.suffix == ".json":
        loaded = json.loads(text)
    else:
        loaded = yaml.safe_load(text)
    if not isinstance(loaded, dict):
        raise ValueError(f"{path} did not contain a mapping")
    return loaded


def _normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _normalize(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    if isinstance(value, str):
        return value.strip()
    return value


def normalize_network(value: Any) -> str:
    """YAML 1.1 loads `off`/`on` as booleans; the job API stores strings."""
    if value in (False, "off", "false", "False", 0, None):
        return "off"
    if value in (True, "on", "true", "True", 1):
        return "on"
    return str(value).strip()


def canonicalize(
    source: Mapping[str, Any] | str | Path,
    *,
    equality_fields: list[str] | None = None,
) -> dict[str, Any]:
    """Return only equality_fields, with nested keys sorted and strings stripped."""
    document = load_document(source)
    fields = equality_fields or load_equality_fields()
    missing = [field for field in fields if field not in document]
    if missing:
        raise ValueError(f"document missing equality fields: {missing}")
    canonical: dict[str, Any] = {}
    for field in fields:
        value = document[field]
        if field == "network":
            canonical[field] = normalize_network(value)
        else:
            canonical[field] = _normalize(value)
    return canonical
