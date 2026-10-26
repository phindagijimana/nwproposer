# Agent instructions — NeuroInsight Agent (Paper 6)

Read [`docs/NeuroInsightAgent_Methods.md`](docs/NeuroInsightAgent_Methods.md) first.

You are **not** rebuilding NeuroInsight. You are adding a **proposer** that writes the same job the existing UI submits.

## Software under test

Private repo (do not vendor it into Agentic_research):

```text
git@github.com:phindagijimana/neuroinsight_research.git
https://github.com/phindagijimana/neuroinsight_research
```

Clone separately. Implement the adapter there as `agents/proposer/` (or equivalent), and keep the research protocol in this folder.

Inspected baseline (2026-10-26): desktop + FastAPI + YAML plugins (`plugins/fastsurfer.yaml`, fMRIPrep, QSIPrep, …), Docker/Slurm backends. No LLM job proposer. “Pennsieve agent” is unrelated.

## Mission

Gated proposer → SciCap invoke → SciGuard validate (if workflow) → existing NeuroInsight submit → optional NeuroAgentBench score.

If the proposer can execute a job, Paper 6 has failed.

## Do not

- Rewrite `frontend/`, `desktop/`, or the plugin registry.
- Claim first agent workbench.
- Call external model APIs with image bytes.
- Import `backend.execution` from the proposer.
- Republish Papers 1–5 confirmatory tables as this paper’s results.
- Name the NeuroInsight product binary `neuroinsight-agent`.

## Reuse

| Package | Role |
|---|---|
| `scicap invoke` | Single-plugin gate (Paper 1) |
| `sciguard validate` | Multi-step workflow gate (Paper 2) |
| `neuroagentbench evaluate` | After-run score (Paper 3) |
| EvidenceGraph | Optional `workflow_run` pointer (Paper 4) |
| NeuroInsight FastAPI submit | Kernel (Paper 5 / git repo) |

Public substrate: same as Papers 1–5 (Boutiques/pybids, BIDS Validator, Docker/Apptainer). The workbench itself is the private repo.

What we may take from NeuroClaw / CyberNeuro / NeuroPilot is listed in [`docs/Public_Prior_Art_Reuse.md`](docs/Public_Prior_Art_Reuse.md). Short version:

- **NeuroClaw (public git):** arm **U** comparator; skill-metadata *pattern*; NeuroBench scenarios scored with **our** oracle. Do not vendor `claw-shell` or the GPT-5.4 rubric.
- **CyberNeuro (paper; no Linux repo found):** receipt field list; Planner ≠ Dispatcher; no-egress *test* on Linux/Slurm.
- **NeuroPilot (paper; no research git):** consequential-approval list; source read-only; append-only ledger *idea*.

Do not implement G by wrapping NeuroClaw.

## Target (in the git repo, not here)

```text
agents/proposer/
  propose.py      # NL or structured intent → propose_request.yaml
  submit.py       # POST existing job API only if guards pass and approval is set
  forbidden.py    # tests: cannot import backend.execution
```

This folder:

```text
schema/propose_request.yaml
schema/example_propose_fastsurfer.yaml
schema/score.schema.json
evaluation/arms.yaml
docs/NeuroInsightAgent_Methods.md
docs/NeuroInsightAgent_Limitations_to_Methods.md
tests/test_a1_no_execute.py
```

## First vertical slice

1. Map `schema/propose_request.yaml` onto one existing plugin (`fastsurfer`) job payload.
2. Human-recorded job JSON vs gated-proposer JSON: equality on `equality_fields`.
3. SciCap REJECT (DK as DKT or wrong modality) → `submit.py` does not POST.
4. Proposer process cannot import `backend.execution`.

Dry-run submit is enough. Do not run FastSurfer to prove A1.

## Done when

- Three arms (H, G, U) can be *declared* on the same fixture.
- G cannot execute on SciCap REJECT / SciGuard FAIL.
- Equality test exists for FastSurfer.
- No MRI bytes and no model required for those tests.

Stop. Do not add a chat UI until A1–A3 tests are green.
