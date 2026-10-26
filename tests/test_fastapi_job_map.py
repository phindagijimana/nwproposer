"""Contract test: equality fields vs a hand-authored FastAPI product job.

Not a clone of neuroinsight_research. Private repo stays outside this folder.
"""

from __future__ import annotations

from adapters.neuroinsight.job import (
    EQUALITY_FIELDS,
    PRODUCT_SHAPE_NOTES,
    from_product_job,
    to_job_payload,
    to_product_job,
)
from proposer.canonicalize import canonicalize, load_document, load_equality_fields
from proposer.equality import jobs_equal
from proposer.propose import propose
from proposer.submit import PostRecorder, submit


def test_equality_fields_match_schema_and_adapter():
    assert tuple(load_equality_fields()) == EQUALITY_FIELDS
    assert EQUALITY_FIELDS == (
        "plugin_id",
        "image_digest",
        "inputs",
        "backend",
        "network",
    )
    assert "not a dump" in PRODUCT_SHAPE_NOTES.lower() or "not exported" in PRODUCT_SHAPE_NOTES.lower()
    assert "neuroinsight_research" in PRODUCT_SHAPE_NOTES


def test_hand_authored_product_job_is_not_a_private_clone(fastapi_product_jobs):
    assert fastapi_product_jobs["private_repo_cloned"] is False
    assert fastapi_product_jobs["source"] == "hand_authored_not_cloned_private_repo"
    docker = fastapi_product_jobs["docker_job"]
    slurm = fastapi_product_jobs["slurm_job"]
    assert docker["plugin"]["descriptor"] == "plugins/fastsurfer.yaml"
    assert docker["backend"]["kind"] == "docker"
    assert slurm["backend"]["kind"] == "slurm"
    assert docker["inputs"]["T1w"].startswith("bids:")
    assert slurm["inputs"] == docker["inputs"]


def test_product_docker_job_equals_human_on_equality_fields(
    fastapi_product_jobs, human_fastsurfer_job
):
    extracted = from_product_job(fastapi_product_jobs["docker_job"])
    human = load_document(human_fastsurfer_job)
    assert jobs_equal(extracted, human)
    assert extracted["plugin_id"] == "fastsurfer"
    assert extracted["backend"] == "local_docker"
    assert extracted["network"] == "off"


def test_product_slurm_job_maps_backend_kind(fastapi_product_jobs):
    extracted = from_product_job(fastapi_product_jobs["slurm_job"])
    assert extracted["plugin_id"] == "fastsurfer"
    assert extracted["image_digest"] == "sha256:PENDING"
    assert extracted["backend"] == "slurm"
    assert extracted["inputs"]["T1w"] == "bids:sub-01/anat/sub-01_T1w.nii.gz"
    assert set(extracted) == set(EQUALITY_FIELDS)


def test_gated_propose_matches_product_docker_equality(
    fastapi_product_jobs, human_fastsurfer_job
):
    human = load_document(human_fastsurfer_job)
    request = propose(
        {
            "plugin_id": human["plugin_id"],
            "plugin_version": human["plugin_version"],
            "image_digest": human["image_digest"],
            "inputs": human["inputs"],
            "parameters": human["parameters"],
            "backend": human["backend"],
            "network": human["network"],
            "approval": {"execution": True},
        }
    )
    product = from_product_job(fastapi_product_jobs["docker_job"])
    assert canonicalize(request) == canonicalize(product)
    poster = PostRecorder()
    result = submit(request, arm="G", approve=True, poster=poster)
    assert result.posted is True
    assert jobs_equal(product, result.job)
    payload = to_job_payload(request)
    assert {field: payload[field] for field in EQUALITY_FIELDS} == canonicalize(product)


def test_round_trip_propose_request_to_product_shape(human_fastsurfer_job):
    human = load_document(human_fastsurfer_job)
    product = to_product_job(human)
    assert product["plugin"]["id"] == "fastsurfer"
    assert product["plugin"]["descriptor"] == "plugins/fastsurfer.yaml"
    assert product["backend"]["kind"] == "docker"
    assert from_product_job(product) == canonicalize(human)
