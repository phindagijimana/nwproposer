"""A1: proposer must not import the executor or grow a second path."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

FORBIDDEN_MODULES = (
    "backend.execution",
    "claw_shell",
    "neuroclaw",
    "neurodiscovery",
)

FORBIDDEN_ROOTS = (
    "subprocess",
    "docker",
    "podman",
    "apptainer",
)


def proposer_package_root() -> Path:
    return Path(__file__).resolve().parent


def research_stub_roots() -> tuple[Path, ...]:
    paper = proposer_package_root().parent
    return (
        paper / "proposer",
        paper / "guards",
        paper / "adapters",
        paper / "baselines",
        paper / "nwproposer",
    )


def _python_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.py") if path.is_file())


def imported_module_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
            for alias in node.names:
                names.add(f"{node.module}.{alias.name}")
    return names


def forbidden_imports_found(roots: tuple[Path, ...] | None = None) -> list[tuple[Path, str]]:
    hits: list[tuple[Path, str]] = []
    for root in roots or research_stub_roots():
        if not root.exists():
            continue
        for path in _python_files(root):
            for name in imported_module_names(path):
                if name in FORBIDDEN_MODULES or name.split(".")[0] in FORBIDDEN_ROOTS:
                    hits.append((path, name))
    return hits


def assert_no_forbidden_imports() -> None:
    hits = forbidden_imports_found()
    if hits:
        rendered = ", ".join(f"{path.name}:{name}" for path, name in hits)
        raise AssertionError(f"A1 violated: forbidden imports in research stubs: {rendered}")


def assert_execution_not_loaded() -> None:
    if "backend.execution" in sys.modules:
        raise RuntimeError("A1 violated: backend.execution is loaded in this process")
