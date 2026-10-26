# NeuroWorkbench proposer

Gated **proposer** for the workbench. Writes the same job a human would submit. Does not execute.

Pip name: **`neuroworkbench-proposer`**. No console command. No `neuroinsight-agent`.

The shipping UI remains [neuroinsight_research](https://github.com/phindagijimana/neuroinsight_research). This repo does not vendor it. G is not a NeuroClaw wrap.

## Install

```bash
pip install -e .
```

Python 3.11+. No model API required for the stubs.

## Use

```python
from proposer.propose import propose
from proposer.submit import submit

req = propose({
    "plugin_id": "fastsurfer",
    "plugin_version": "1",
    "image_digest": "sha256:…",
    "inputs": {"t1w": "bids:sub-01/anat/sub-01_T1w.nii.gz"},
    "backend": "docker",
})
result = submit(req)  # not POSTed if SciCap REJECT, SciGuard FAIL, or no approve
```

Arms: **H** human UI, **G** this proposer, **U** unconstrained comparator.

## Tests

```bash
pytest tests
```

## Docs

- [Methods](docs/NeuroInsightAgent_Methods.md) (A1–A5)
- [Prior art reuse](docs/Public_Prior_Art_Reuse.md)
- [Methods trace](docs/METHODS_TRACE.md)

Apache-2.0.
