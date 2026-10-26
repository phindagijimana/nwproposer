# Agent instructions — NeuroInsight Agent (Paper 6)

Read [`docs/NeuroInsightAgent_Methods.md`](docs/NeuroInsightAgent_Methods.md) first.

This folder **is** the project. You are **not** implementing inside `neuroinsight_research`. You are adding a **proposer** that writes the same job public `neuroworkbench` submits.

## Software under test

| Package | Role |
|---|---|
| [`nwproposer`](https://github.com/phindagijimana/nwproposer) | This paper: propose / gated submit |
| [`neuroworkbench`](https://github.com/phindagijimana/neuroworkbench) | Paper 5 kernel (dry-run) |
| [`scicap`](https://github.com/phindagijimana/scicap) | Paper 1 invoke |
| [`sciguard`](https://github.com/phindagijimana/sciguard) | Paper 2 validate |

`neuroinsight_research` is a separate product. Do not clone or vendor it.

## Mission

Gated proposer → SciCap invoke → SciGuard validate (if workflow) → `neuroworkbench.submit --approve` → optional NeuroAgentBench score.

If the proposer can execute a job, Paper 6 has failed.

## Do not

- Rewrite a desktop, FastAPI, or plugin registry.
- Claim first agent workbench.
- Call external model APIs with image bytes.
- Import `backend.execution` from the proposer.
- Wrap NeuroClaw as arm G.
- Add MCP (holistic test forbids `mcp` modules).
- Name a binary `neuroinsight-agent`.

## Reuse

Public substrate: SciCap, SciGuard, neuroworkbench, NeuroPilot approval list, CyberNeuro Planner ≠ Dispatcher. NeuroClaw is arm **U** only.

## Done when

- H / G / U declared on the same fixture.
- G equals H on a neuroworkbench FastSurfer request.
- G does not hand SciCap REJECT / SciGuard FAIL to the workbench.
- U can still post an illegal job (incorrect_submission).
- No MRI bytes and no model required.

Stop. Do not add a chat UI.
