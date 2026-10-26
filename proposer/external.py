"""Locate a public S0 T1w under shared/data/external. Never download.

Pytest must not fetch OpenNeuro bytes. When those bytes are already on
disk (gitignored), point a neuroworkbench FastSurfer job at that path.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from proposer.canonicalize import load_document, normalize_network, paper_root

_MANIFEST_REL = Path("ds000003") / "sub-01" / "anat" / "sub-01_T1w.nii.gz"
_FETCH = "shared/scripts/fetch_s0.py --i-accept-public-data"
_ABSENT_REASON = (
    "shared/data/external has no public T1w bytes; "
    "pytest does not download; fixture jobs remain"
)


def workspace_root() -> Path:
    return paper_root().parent


def external_root() -> Path:
    return workspace_root() / "shared" / "data" / "external"


def manifest_t1w_path() -> Path:
    return external_root() / _MANIFEST_REL


def _is_nifti(path: Path) -> bool:
    name = path.name.lower()
    return name.endswith(".nii.gz") or name.endswith(".nii")


def _looks_t1w(path: Path) -> bool:
    return "t1w" in path.name.lower()


def is_real_nifti_bytes(path: Path) -> bool:
    """True only for gzip/NIfTI magic and size >> 1 KB.

    Git-annex / LFS pointers (tiny ASCII, often starting with ``..``) are
    absent. Wave 6 requires this check before pointing a job at the path.
    """
    try:
        size = path.stat().st_size
        head = path.read_bytes()[:8]
    except OSError:
        return False
    if size < 1024:
        return False
    if head.startswith(b"..") or head.startswith(b"<") or head.startswith(b"version"):
        return False
    if head.startswith(b"\x1f\x8b"):
        return True
    if head[:2] in (b"\x5c\x01", b"\x6c\x01"):
        return True
    return False


def _is_real_nifti_bytes(path: Path) -> bool:
    return is_real_nifti_bytes(path)


def find_public_t1w() -> Path | None:
    """Return an on-disk public T1w, or None. Does not download."""
    preferred = manifest_t1w_path()
    if preferred.is_file() and _is_real_nifti_bytes(preferred):
        return preferred.resolve()
    root = external_root()
    if not root.is_dir():
        return None
    hits = [
        path.resolve()
        for path in root.rglob("*")
        if path.is_file()
        and _is_nifti(path)
        and _looks_t1w(path)
        and _is_real_nifti_bytes(path)
    ]
    return sorted(hits)[0] if hits else None


def t1w_blocker() -> dict[str, Any]:
    """Record why a live-path job is or is not available. Not an evaluation."""
    path = find_public_t1w()
    present = path is not None
    preferred = manifest_t1w_path()
    gzip_magic = False
    annex_pointer = False
    size = 0
    if preferred.is_file():
        try:
            size = preferred.stat().st_size
            head = preferred.read_bytes()[:8]
            gzip_magic = head.startswith(b"\x1f\x8b")
            annex_pointer = head.startswith(b"..") or size < 1024
        except OSError:
            pass
    return {
        "present": present,
        "path": str(path) if path is not None else None,
        "reason": "public T1w present under shared/data/external" if present else _ABSENT_REASON,
        "bytes_in_git": False,
        "download_in_pytest": False,
        "fetch": _FETCH,
        "accession": "ds000003",
        "gzip_magic": gzip_magic,
        "annex_pointer_rejected": annex_pointer and not present,
        "size_bytes": size,
        "paper6_primary": False,
    }


def workbench_job_for_t1w(
    t1w: Path,
    *,
    proposer: str = "human",
    template: Path | None = None,
) -> dict[str, Any]:
    """Human-shaped neuroworkbench FastSurfer request pointed at ``t1w``."""
    source = template or paper_root() / "fixtures" / "workbench_human.yaml"
    job = load_document(source)
    job["proposer"] = proposer
    job["network"] = normalize_network(job.get("network", "off"))
    job["inputs"] = {**dict(job.get("inputs") or {}), "t1w": str(Path(t1w).resolve())}
    notes = dict(job.get("notes") or {})
    notes["source"] = "shared/data/external"
    notes["bytes_in_git"] = False
    notes["s0_used"] = True
    notes["paper6_primary"] = False
    job["notes"] = notes
    return job


def legal_s0_job(*, proposer: str = "human") -> dict[str, Any] | None:
    """Legal FastSurfer job pointed at on-disk S0 T1w, or None if bytes absent."""
    t1w = find_public_t1w()
    if t1w is None:
        return None
    return workbench_job_for_t1w(t1w, proposer=proposer)
