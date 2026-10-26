# nwproposer

Writes the same job a human would submit to **neuroworkbench**. Does not execute.

Pip: **`nwproposer`**. No CLI. No `neuroinsight-agent`. Separate from `neuroinsight_research`.

## Go

```bash
pip install git+https://github.com/phindagijimana/nwproposer.git
pip install git+https://github.com/phindagijimana/neuroworkbench.git
pip install git+https://github.com/phindagijimana/scicap.git
pip install git+https://github.com/phindagijimana/sciguard.git
```

```python
from nwproposer import propose, submit

req = propose({
    "plugin_id": "fastsurfer_anatomical",
    "plugin_version": "0.1.0",
    "image_digest": "sha256:PENDING",
    "inputs": {"t1w": "bids:sub-01/anat/sub-01_T1w.nii.gz"},
    "backend": "local_container",
    "parameters": {"modality": "T1w", "space": "subject_native"},
})
submit(req, arm="G", approve=True, kernel="workbench")
# optional, recorded tree only:
# from nwproposer import evaluate_recorded
```

G is blocked on SciCap REJECT / ABSTAIN, SciGuard FAIL, or missing approve — those jobs are not handed to neuroworkbench. U skips gates (incorrect_submission) and is an unconstrained stub, not a NeuroClaw wrap. H/G must match on plugin, digest, inputs, backend, network.

If a public T1w is already on disk under `shared/data/external` (not in git), a legal H/G FastSurfer job is pointed at that path and dry-run through neuroworkbench.submit. Pytest does not download. Annex pointers are treated as absent. When those bytes are absent, fixture jobs remain.

Public tools: SciCap, SciGuard, neuroworkbench, NeuroPilot approval list, CyberNeuro Planner ≠ Dispatcher. No chat UI. Stub U-vs-G counts are not evaluation percentages.

```bash
pytest tests
```

[Methods](docs/NeuroInsightAgent_Methods.md) · Apache-2.0
