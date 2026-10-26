"""Optional Paper 3 score on a recorded tree. Not this paper’s primary. No agent start."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_WORKSPACE = Path(__file__).resolve().parents[2]
_NAB_ROOT = _WORKSPACE / "03_NeuroAgentBench"


def _load_evaluate():
    try:
        from neuroagentbench import evaluate as evaluate_fn

        return evaluate_fn
    except ImportError:
        pass
    if _NAB_ROOT.is_dir() and str(_NAB_ROOT) not in sys.path:
        sys.path.insert(0, str(_NAB_ROOT))
    try:
        from neuroagentbench import evaluate as evaluate_fn

        return evaluate_fn
    except ImportError:
        return None


def nab_available() -> bool:
    return _load_evaluate() is not None


def evaluate_recorded(
    task: str | Path,
    run: str | Path,
    *,
    seed: int | None = None,
) -> dict[str, Any]:
    """Score a recorded run with NeuroAgentBench. Does not start an agent."""
    evaluate_fn = _load_evaluate()
    if evaluate_fn is None:
        raise ImportError("neuroagentbench is not importable; install the public Paper 3 package")
    score = dict(evaluate_fn(task, run, seed=seed))
    score["owner"] = "neuroagentbench"
    # Paper 3 owns this number. Never promote it to a Paper 6 primary.
    score["paper6_primary"] = False
    return score
