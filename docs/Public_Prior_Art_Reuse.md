# Public prior art we can build on

NeuroInsight Agent / Paper 6 · 26 October 2026 · inventory, not a license opinion

Paper 6 is built on **NeuroInsight** (`neuroinsight_research`) plus SciCap / SciGuard / NeuroAgentBench. NeuroClaw, CyberNeuro, and NeuroPilot are **comparators and protocol sources**, not a second kernel to fork.

Checked 26 October 2026. Re-check licenses and whether CyberNeuro/NeuroPilot code has appeared on GitHub before any copy-paste. This is not legal advice.

**Rule.** Steal a *test*, a *field list*, or an *arm*. Do not steal a harness and call it NeuroInsight Agent.

---

## 1. What is actually public

| System | Paper | Code / product | Usable as |
|---|---|---|---|
| **NeuroClaw** (now NeuroDiscovery) | [arXiv:2604.24696](https://arxiv.org/abs/2604.24696) | **Yes.** [CUHK-AIM-Group/NeuroClaw](https://github.com/CUHK-AIM-Group/NeuroClaw) → NeuroDiscovery. Docs: [cuhk-aim-group.github.io/NeuroClaw](https://cuhk-aim-group.github.io/NeuroClaw/get-started.html) | Arm **U** comparator; skill-metadata *pattern*; audit/JSONL *ideas*. Not our executor. |
| **CyberNeuro** | [arXiv:2607.28841](https://arxiv.org/abs/2607.28841) | **Paper + hosted app.** Claims FAIR4RS / open source. Product: [wanda-cyberbench.com](https://wanda-cyberbench.com). **No GitHub repo found** on this date. Windows-only in the paper. | Receipt fields; no-egress *test protocol*; Planner ≠ Dispatcher split. Not an installable Linux kernel. |
| **NeuroPilot** | [arXiv:2608.07541](https://arxiv.org/abs/2608.07541) | **Paper + same host.** Also [wanda-cyberbench.com](https://wanda-cyberbench.com). **No research GitHub.** [VSC-NeuroPilot/neuropilot](https://github.com/VSC-NeuroPilot/neuropilot) is an unrelated VS Code extension. | Approval taxonomy; read-only source; idempotent retry; append-only ledger *idea*. Not a skill pack we can vendor. |

Individual NeuroClaw `SKILL.md` files mix **MIT-in-project** and **Proprietary**. Read `LICENSE` and each skill header before any reuse. Academic-research-hub is marked Proprietary — do not copy it.

---

## 2. NeuroClaw — what we have

Public tree (compatibility names kept): `core/agent`, `core/skill_loader`, `skills/*/SKILL.md`, `neurobench/` (T01–T500), `installer/install_agent_integration.py`, `neuroclaw_environment.json`, host-agent skill `neuroclaw`, MCP names `neuroclaw_academic_*`.

### 2.1 May use

| Artifact | How Paper 6 uses it |
|---|---|
| Host-agent installer (Cursor / Claude / Codex) | Pattern only: a host agent **enters a mode** and writes actions. Our mode writes a NeuroInsight `propose_request`, not `claw-shell`. |
| `SKILL.md` YAML frontmatter (`layer`, `skill_type`, `dependencies`) | Optional annotation style on NeuroInsight plugins. **SciCap owns the scientific fields.** Do not adopt NeuroClaw skills as contracts. |
| `harness-core` ideas: JSONL audit, checkpoints, expected-artifact checks, NaN/Inf, checksum, digest | Field *ideas* for Paper 5 receipts / Paper 6 score. Re-implement against NeuroInsight jobs. Do not import their Python as our kernel. |
| NeuroBench task list (`neurobench/`, `task.md`, `task_atlas.json`) | **Arm U** or shared illegal/legal *scenarios* after license check. Score with **NeuroAgentBench** (B1–B3), not their GPT-5.4 rubric. |
| With-skills vs no-skills contrast | Maps to our **G vs U**. Cite their finding; run it on *our* job API. |
| Three-tier split (user / orchestrate / tool) | Maps to: human or LLM propose → guards → NeuroInsight execute. We keep execute inside the existing backend. |

### 2.2 Must not use as Paper 6

- Their executor, `claw-shell`, desktop, or AutoResearch / NeuroOracle as the product.
- `--score-benchmark` GPT-5.4 rubric (planning 30% / tool 40% / code 30%) as primary. That is NeuroBench’s weakness and Paper 3’s non-scope.
- Shipping “NeuroClaw mode” inside NeuroInsight.
- Copying Proprietary skills.

**Install for comparator only** (separate clone, not vendored here):

```text
git clone https://github.com/CUHK-AIM-Group/NeuroDiscovery.git
# or https://github.com/CUHK-AIM-Group/NeuroClaw.git
```

Arm U may be “same model + NeuroClaw skills + shell” *or* “same model + unconstrained tools.” Declare which. Do not require NeuroClaw to implement G.

---

## 3. CyberNeuro — what we have

No cloneable kernel found. The paper is the source. Hosted binary at wanda-cyberbench.com is Windows-local; not our Slurm/Linux product.

### 3.1 May use (documented protocols)

| Protocol in the paper | How we use it |
|---|---|
| Four stages: Planner, Validator, Dispatcher, Reporter | **Planner = proposer (A1).** Validator = SciCap + SciGuard. **Dispatcher = existing NeuroInsight submit.** Reporter = receipt + optional NAB score. Their Dispatcher is an agent. Ours must not be. |
| MCP bridge + pinned execution layer | Transport optional (Coala/Nipoppy). Pin = plugin `image_digest`. |
| JSON receipt: inputs, tool versions, commands, outputs, logs, validation, completion | Align Paper 5 `receipt.yaml` / Paper 6 score. Add `qc_did_not_run` (they under-specify that). |
| No-egress tests: host + WSL traffic capture; disconnected-host | **Copy the test design** onto Linux local and Slurm (Paper 5 N6 / Paper 6 illegal network request). Do not claim their Windows measurement. |
| Workspace confinement, path canonicalization, allowlisted skills | Already in NeuroInsight + N6. Cite as the threat model. |
| Human verification panel | Our `--approve` and UI Submit. Not a new panel. |
| NeuroBench comparison vs NeuroClaw | Cite as related eval; do not treat 69% domain accuracy as a number we inherit. |

### 3.2 Must not use

- WandaMind or their Windows/WSL bundle as a dependency.
- Claiming CyberNeuro is our privacy layer.
- Treating wanda-cyberbench.com as an API we wrap.

If they later publish a real git repo, re-run this inventory before importing anything.

---

## 4. NeuroPilot — what we have

No research code found. Three named skills exist only as paper descriptions: `dcm2bids-skill`, `neuroimage-pre-skill`, `qc-agent-skill`.

### 4.1 May use (documented protocols)

| Protocol in the paper | How we use it |
|---|---|
| Escalate to a human at **consequential** steps | Lock the list on NeuroInsight submit: overwrite, delete, Slurm array, backend switch, `network: on`, fallback plugin. G cannot skip `--approve` on that list. |
| Source data stay **read-only**; derivatives elsewhere | Encode in the job: inputs not writable by the proposer. |
| Append-only ledger of detect → propose → approve → fix → verify | Maps to Paper 5 receipt + correction history. Do not invent a second log format if NeuroInsight audit already appends. |
| Idempotent resubmit of failed nodes | Platform feature (Paper 5 / existing Slurm scripts). Paper 6 must not let G “fix” by posting a different digest silently (A2). |
| QC as a skill that **flags**, not a silent pass | `qc_did_not_run` ≠ pass; silent success (N2) still applies. |
| One `pipeline.env` for site portability | Optional later. Not v0. |

### 4.2 Must not use

- Their 17-cohort / 123k-subject claims as our results.
- Implementing `qc-agent-skill` as Paper 6 novelty (QC is NeuroInsight + optional NAB L4).
- The unrelated VS Code “NeuroPilot” extension.

---

## 5. Mapping onto Paper 6 (what we actually build)

```text
                    NeuroClaw / CyberNeuro / NeuroPilot
                    (cite; steal tests and field lists)
                                    │
NeuroInsight job API  ←── G proposer ──→ SciCap + SciGuard
(the kernel)                 │
                             └── A2 equality vs human UI
                             └── A3 vs arm U (NeuroClaw-style unconstrained)
```

| Paper 6 object | Borrowed from | Implemented on |
|---|---|---|
| `propose_request` | CyberNeuro Planner output; NeuroClaw skill *intent* | NeuroInsight plugin/workflow ids |
| Guards before POST | CyberNeuro Validator; NeuroPilot approve list | SciCap + SciGuard |
| Submit | CyberNeuro Dispatcher — **but human/kernel, not agent** | Existing FastAPI |
| Receipt / score | CyberNeuro JSON receipt; NeuroClaw JSONL; NeuroPilot ledger | Paper 5 receipt + `schema/score.schema.json` |
| No-egress fixture | CyberNeuro §3.4 | Linux/Slurm, not Windows |
| Arm U | NeuroClaw with-skills / direct agent | Same model, tools/shell, **or** NeuroClaw clone |
| Primary scorer | — | Incorrect-submission + equality; **not** GPT-5.4 |

---

## 6. What we will not vendor

- `CUHK-AIM-Group/NeuroDiscovery` as a submodule of NeuroInsight.
- wanda-cyberbench binaries.
- NeuroClaw `claw-shell` as a fallback executor.
- Any skill marked Proprietary.

If G is implemented by wrapping NeuroClaw and pointing it at FastSurfer, Paper 6 has failed A1.

---

## 7. First practical steps

1. Cite the three papers in Paper 6 related work (mandatory).
2. Copy CyberNeuro’s disconnected-host *checklist* into `05`/`06` tests (Linux).
3. Copy NeuroPilot’s consequential-approval *list* into `schema/propose_request.yaml` / NeuroInsight submit policy.
4. Optionally clone NeuroDiscovery **outside** this repo to run arm U on 5–10 overlapping scenarios.
5. Align receipt keys with CyberNeuro’s list + our `qc_did_not_run`.
6. Do not install NeuroClaw skills into the NeuroInsight desktop.

---

## 8. Sources (seed)

- Wang et al. NeuroClaw technical report. arXiv:2604.24696. Code: https://github.com/CUHK-AIM-Group/NeuroClaw
- CyberNeuro. arXiv:2607.28841. Product: https://wanda-cyberbench.com
- Chen et al. NeuroPilot. arXiv:2608.07541. Product: https://wanda-cyberbench.com
- NeuroClaw get-started: https://cuhk-aim-group.github.io/NeuroClaw/get-started.html

Re-run this search before submission. CyberNeuro’s “open-sourced” claim is not the same as a cloneable Linux repository today.
