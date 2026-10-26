# Methods trace — NeuroInsight Agent (Paper 6)

Planning-stage correspondence · 26 October 2026 · no results claimed

This traces locked methods A1–A5 onto the public protocol tools in `baselines/` and the Wave 1 research stubs. It does not replace [`NeuroInsightAgent_Methods.md`](NeuroInsightAgent_Methods.md). There is no A6. There is no MCP adapter (Coala owns CWL→MCP). There are no fabricated U-vs-G percentages.

Residual: **job equality and incorrect-submission on the public neuroworkbench job API.** Not a first agent workbench. Not `neuroinsight_research`.

---

## Locked methods A1–A5

| Method | Public tool reused | Literature residual | Test |
|---|---|---|---|
| A1 | CyberNeuro Planner≠Dispatcher (`baselines/cyberneuro_split.py`) | proposer-only; no execute | `tests/test_a1_no_execute.py` |
| A2 | existing job object (`adapters/neuroinsight/job.py`) | G equals H on plugin/digest/inputs/backend/network | `tests/test_a2_equality.py` |
| A3 | SciCap/SciGuard sibling if importable, else `guard_mode: recorded` (`guards/`) | illegal not POSTed; U incorrect-submission > G (stub counts, not a result) | `tests/test_a3_illegal_not_posted.py` |
| A4 | NeuroClaw as U only | H/G/U declared; G is not NeuroClaw | `tests/test_a1_no_execute.py` |
| A5 | Papers 1–3 + Paper 5 | reuse invoke/validate/score; do not reimplement | `guards/`, `adapters/neuroworkbench/`, `proposer/evaluate.py` |

Public protocol tests: `tests/test_public_protocol.py`. Same fixtures through both stacks: `tests/test_holistic.py`.

---

## What the public tools already own

**NeuroPilot consequential list** (`baselines/neuropilot_approval.py`; Chen et al., [arXiv:2608.07541](https://arxiv.org/abs/2608.07541)). Overwrite, delete, Slurm array, backend switch, `network: on`, fallback plugin → `requires_approve: true`. The VS Code repo `VSC-NeuroPilot/neuropilot` is unrelated. Atlas and space are not in this list.

**CyberNeuro Planner ≠ Dispatcher** (`baselines/cyberneuro_split.py`; [arXiv:2607.28841](https://arxiv.org/abs/2607.28841)). Planner writes a `propose_request`, not a shell command. Dispatcher is the existing submit *role*, implemented here as a stub that does not execute and does not import `backend.execution`. No Linux git; protocol only. Their Dispatcher is an agent; ours must not be.

**Existing job object.** Human UI submit and gated proposal are the same fields. Public protocol does not invent a second payload.

---

## Literature residual (cite; do not reimplement)

### NeuroClaw / NeuroDiscovery (Wang et al., [arXiv:2604.24696](https://arxiv.org/abs/2604.24696))

Public git: [CUHK-AIM-Group/NeuroClaw](https://github.com/CUHK-AIM-Group/NeuroClaw). Occupies the agentic MRI workbench. **Arm U only.** G is not a NeuroClaw wrap. Do not vendor `claw-shell`, the desktop, or the GPT-5.4 NeuroBench rubric. Do not clone that git into this folder.

### CyberNeuro ([arXiv:2607.28841](https://arxiv.org/abs/2607.28841))

Protocol source for Planner ≠ Dispatcher and the receipt field list. No cloneable Linux repository found (26 October 2026). Residual: Dispatcher = existing NeuroInsight submit, not an agent. Do not wrap WandaMind.

### NeuroPilot (Chen et al., [arXiv:2608.07541](https://arxiv.org/abs/2608.07541))

Protocol source for the consequential-approval list. Residual: approval object = this job request; atlas/space refusals stay with SciCap/SciGuard. Do not vendor a skill pack. Do not use the unrelated VS Code extension.

### Coala (Hu et al., *Bioinformatics* 2026, [10.1093/bioinformatics/btag641](https://doi.org/10.1093/bioinformatics/btag641))

Owns CWL→MCP. Paper 6 does not add MCP and does not treat Coala as the contribution.

### Paper2Agent (Miao et al., *Nature* 2026, [10.1038/s41586-026-11044-y](https://doi.org/10.1038/s41586-026-11044-y))

Owns papers-as-agents. Different object from a proposer on a shipping job API. Blocks a Nature-family chat-wrapper story.

### Neurodesk coding-agent remotes (2026-04-28 / 2026-09-23)

OpenCode / Codex / T3 Code inside a container desktop. Not this plugin/job API. Do not rebuild those remotes.

### Papers 1–5

| Call | Owner | Paper 6 |
|---|---|---|
| `scicap invoke` | Paper 1 | Gate G before POST |
| `sciguard validate` | Paper 2 | Gate multi-step G before POST |
| `neuroagentbench evaluate` | Paper 3 | Optional after-run score |
| EvidenceGraph `workflow_run` | Paper 4 | Optional pointer |
| Kernel, receipt, N2 silent success | Paper 5 | Submit path; reuse N2 field |

Do not republish M1–M4, G1–G5, B1–B7, E1–E5, or N1–N6 as Paper 6 results. QC-skipped + reported complete is the Paper 5 N2 field counted by arm, not a Paper 6 confirmatory table.

---

## What this document is not

- Not A6 and not an MCP adapter.
- Not a claim of first agent workbench.
- Not an evaluation: U-vs-G incorrect-submission is a Wave 1 stub inequality, not a percentage.
- Not a vendor of `neuroinsight_research`. The private repo stays outside this folder.

---

## Wave 3 residual (protocol + stubs)

Sibling `01_SciCap` / `02_SciGuard` are called on DK-as-DKT and labels→DWI when those packages import; otherwise guards stay recorded. FastAPI equality is a hand-authored product-shape contract (`fixtures/fastapi_fastsurfer_job.json`), not a clone. NeuroPilot still requires approve on `network: on`, overwrite, and backend switch. A1 still scans `baselines/` and `adapters/` for `backend.execution`. G is not NeuroClaw.

---

## Sources (seed; re-check before submission)

1. Wang et al. NeuroClaw technical report. arXiv:2604.24696. Code: https://github.com/CUHK-AIM-Group/NeuroClaw
2. CyberNeuro. arXiv:2607.28841. Product: https://wanda-cyberbench.com
3. Chen et al. NeuroPilot. arXiv:2608.07541. Product: https://wanda-cyberbench.com
4. Hu et al. (2026). Coala. *Bioinformatics* 42(9): btag641. https://doi.org/10.1093/bioinformatics/btag641
5. Miao et al. (2026). Paper2Agent. *Nature*. https://doi.org/10.1038/s41586-026-11044-y
6. Neurodesk release history (2026-04-28; 2026-09-23 remotes): https://neurodesk.org/overview/release-history/
7. Locked protocol: [`NeuroInsightAgent_Methods.md`](NeuroInsightAgent_Methods.md)
8. Inventory: [`Public_Prior_Art_Reuse.md`](Public_Prior_Art_Reuse.md)
