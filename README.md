# nwproposer

Writes the same job a human would submit. Does not execute.

Pip: **`nwproposer`**. No CLI. No `neuroinsight-agent`.

## Go

```bash
git clone https://github.com/phindagijimana/nwproposer.git
cd nwproposer && pip install -e .
python -c "from proposer.propose import propose; print('ok')"
```

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
submit(req)  # blocked on SciCap REJECT, SciGuard FAIL, or missing approve
```

Python 3.11+. Does not vendor [neuroinsight_research](https://github.com/phindagijimana/neuroinsight_research). Not a NeuroClaw wrap.

```bash
pytest tests
```

Workbench: [`neuroworkbench`](https://github.com/phindagijimana/neuroworkbench).

[Methods](docs/NeuroInsightAgent_Methods.md) · Apache-2.0
