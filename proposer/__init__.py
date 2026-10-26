"""Paper 6 proposer stubs. This folder is the project. Do not execute.

Do not import submit here: proposer.submit imports proposer.* and that
cycle would load the dry-run kernel at package import.
"""

from proposer.canonicalize import canonicalize, load_equality_fields
from proposer.equality import jobs_equal
from proposer.external import (
    find_public_t1w,
    is_real_nifti_bytes,
    legal_s0_job,
    t1w_blocker,
    workbench_job_for_t1w,
)
from proposer.forbidden import assert_no_forbidden_imports
from proposer.propose import propose

__all__ = [
    "canonicalize",
    "load_equality_fields",
    "jobs_equal",
    "find_public_t1w",
    "is_real_nifti_bytes",
    "legal_s0_job",
    "t1w_blocker",
    "workbench_job_for_t1w",
    "assert_no_forbidden_imports",
    "propose",
]
