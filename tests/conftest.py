import sys
from pathlib import Path

import pytest
import yaml

PAPER_ROOT = Path(__file__).resolve().parents[1]
if str(PAPER_ROOT) not in sys.path:
    sys.path.insert(0, str(PAPER_ROOT))
FIXTURES = PAPER_ROOT / "fixtures"


@pytest.fixture
def paper_root() -> Path:
    return PAPER_ROOT


@pytest.fixture
def human_fastsurfer_job(paper_root: Path) -> Path:
    return paper_root / "fixtures" / "human_fastsurfer_job.json"


@pytest.fixture
def example_propose_fastsurfer(paper_root: Path) -> Path:
    return paper_root / "schema" / "example_propose_fastsurfer.yaml"


@pytest.fixture
def illegal_dk_as_dkt() -> dict:
    return yaml.safe_load((FIXTURES / "illegal_dk_as_dkt.yaml").read_text())


@pytest.fixture
def illegal_labels_t1w_on_dwi() -> dict:
    return yaml.safe_load((FIXTURES / "illegal_labels_t1w_on_dwi.yaml").read_text())


@pytest.fixture
def illegal_space_omitted() -> dict:
    return yaml.safe_load((FIXTURES / "illegal_space_omitted.yaml").read_text())


@pytest.fixture
def silent_success_receipt() -> dict:
    return yaml.safe_load((FIXTURES / "silent_success_receipt.yaml").read_text())


@pytest.fixture
def network_on_request() -> dict:
    return yaml.safe_load((FIXTURES / "network_on.yaml").read_text())


@pytest.fixture
def overwrite_request() -> dict:
    return yaml.safe_load((FIXTURES / "overwrite.yaml").read_text())


@pytest.fixture
def backend_switch_request() -> dict:
    return yaml.safe_load((FIXTURES / "backend_switch.yaml").read_text())


@pytest.fixture
def fastapi_product_jobs(paper_root: Path) -> dict:
    import json

    path = paper_root / "fixtures" / "fastapi_fastsurfer_job.json"
    return json.loads(path.read_text())


@pytest.fixture
def arms() -> dict:
    data = yaml.safe_load((PAPER_ROOT / "evaluation" / "arms.yaml").read_text())
    return data["arms"]
