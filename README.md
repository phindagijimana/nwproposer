# nwproposer

Writes the same job a human would submit. Does not execute.

Pip: **`nwproposer`**. No CLI. No `neuroinsight-agent`.

## Go

```bash
pip install git+https://github.com/phindagijimana/nwproposer.git
```

```python
from nwproposer import propose, submit

req = propose({
    "plugin_id": "fastsurfer",
    "plugin_version": "1",
    "image_digest": "sha256:…",
    "inputs": {"t1w": "bids:sub-01/anat/sub-01_T1w.nii.gz"},
    "backend": "docker",
})
submit(req, arm="G", approve=True)  # blocked on SciCap REJECT, SciGuard FAIL, or missing approve
```

Python 3.11+. Does not vendor [neuroinsight_research](https://github.com/phindagijimana/neuroinsight_research). Not a NeuroClaw wrap.

Agent hook: `from nwproposer.agent import call_tool` (propose / dry-run submit; no execute tool). No MCP — that is not this paper.

Workbench: [`neuroworkbench`](https://github.com/phindagijimana/neuroworkbench).

```bash
pytest tests
```

[Methods](docs/NeuroInsightAgent_Methods.md) · Apache-2.0
