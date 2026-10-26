"""nwproposer public API. Write the same job. Do not execute."""

from proposer.propose import propose
from proposer.submit import submit

__all__ = ["propose", "submit"]
__version__ = "0.1.0"
