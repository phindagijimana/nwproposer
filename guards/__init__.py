"""Guard wiring. Sibling SciCap/SciGuard if importable; else recorded mocks."""

from guards.scicap import invoke as scicap_invoke
from guards.sciguard import validate as sciguard_validate

__all__ = ["scicap_invoke", "sciguard_validate"]
