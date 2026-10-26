"""A2: human UI job vs gated-proposer job on equality_fields."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from proposer.canonicalize import canonicalize


def jobs_equal(
    left: Mapping[str, Any] | str | Path,
    right: Mapping[str, Any] | str | Path,
    *,
    equality_fields: list[str] | None = None,
) -> bool:
    return canonicalize(left, equality_fields=equality_fields) == canonicalize(
        right, equality_fields=equality_fields
    )
