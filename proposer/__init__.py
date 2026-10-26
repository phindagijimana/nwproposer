"""Research stub for Paper 6. Production adapter lives in neuroinsight_research."""

from proposer.canonicalize import canonicalize, load_equality_fields
from proposer.equality import jobs_equal
from proposer.forbidden import assert_no_forbidden_imports
from proposer.propose import propose
from proposer.submit import submit

__all__ = [
    "canonicalize",
    "load_equality_fields",
    "jobs_equal",
    "assert_no_forbidden_imports",
    "propose",
    "submit",
]
