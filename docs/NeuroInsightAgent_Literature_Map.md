# NeuroInsight Agent literature map

**Paper 6 — proposer on the existing NeuroInsight job API**  
Scoping map · 26 October 2026 · search cutoff 26 October 2026

**Status.** Planning-stage claim-setting. Not a PRISMA review and not a finding that a gated proposer works. No evaluation numbers are claimed. Re-check licenses and whether CyberNeuro or NeuroPilot have published a cloneable Linux repository before any copy-paste. This is not legal advice.

**Bottom line.** NeuroClaw, CyberNeuro, NeuroPilot, Neurodesk coding-agent remotes, Coala, and Paper2Agent already occupy agentic neuroimaging workbenches, coding agents inside a container desktop, CWL→MCP transport, and papers-as-agents. Paper 6 must not write “first agent workbench.” The residual that still looks testable is a **proposer-only adapter on this product’s job API**, with **job equality versus the human UI path** and **incorrect-submission / silent-success numbers for arms H / G / U**.

Source inventory for the three closest agentic MRI systems: [`Public_Prior_Art_Reuse.md`](Public_Prior_Art_Reuse.md). Locked protocol: [`NeuroInsightAgent_Methods.md`](NeuroInsightAgent_Methods.md).

---

## 1. Search protocol

### 1.1 Sources queried on 26 October 2026

Web search over arXiv, publisher sites, official product docs, and GitHub, starting from `Public_Prior_Art_Reuse.md` and snowballing the 2026 agentic-science hits already mapped for Papers 1 and 5.

| Cluster | Query family | What it was meant to catch |
|---|---|---|
| A | NeuroClaw / NeuroDiscovery + NeuroBench + skill | Agentic MRI harness with public git |
| B | CyberNeuro / NeuroPilot / Wanda / wanda-cyberbench | Local agent workbenches; approval and no-egress protocols |
| C | Coala + CWL + MCP | Descriptor→MCP adapter (not this paper’s object) |
| D | Paper2Agent + papers as agents + MCP | Paper-to-agent conversion (not this paper’s object) |
| E | Neurodesk + OpenCode / Codex / T3 Code / coding-agent remotes | Agents inside an existing container desktop |
| Extra | Nipoppy MCP, Brain Researcher, Papers 1–5 | Transport, claim cards, libraries this paper calls |

### 1.2 What this map is not

- Not an exhaustive ACM / IEEE / PubMed screen with recorded inclusion counts.
- Not a license opinion. NeuroClaw skills mix MIT-in-project and Proprietary; re-read each header before reuse.
- Not a claim that 2026 preprints will remain the version of record.
- Not a finding. Residual claims below are *testable*, not *shown*.

### 1.3 How to read threat levels

| Level | Meaning for Paper 6 |
|---|---|
| **Blocker** | Already implements the thing Paper 6 would otherwise call novel. Do not claim that object. |
| **High** | Same job, different product. Cite; steal a test or field list; run H/G/U on *this* API. |
| **Must-cite baseline** | Fair comparator even if conceptually older. |
| **Reuse / library** | Call it. Do not republish its confirmatory table as Paper 6. |
| **Adjacent** | Method lesson; different object. |

---

## 2. Residual after the closest systems are granted

```
NeuroClaw / CyberNeuro / NeuroPilot     — agentic MRI workbenches (cite; arm U)
Neurodesk OpenCode / Codex / T3 remotes — coding agents in a container desktop
Coala / Nipoppy MCP                     — CWL/Boutiques → MCP (optional transport)
Paper2Agent                             — a paper becomes MCP tools
Papers 1–5                              — invoke, preflight, oracles, literature, kernel
                    │
                    ▼
Residual: proposer writes THIS NeuroInsight job object
          SciCap + SciGuard + approval before POST
          A2 equality vs the human UI submit
          A3 incorrect-submission and silent-success vs H and U
```

**One-sentence answers**

- NeuroClaw asks whether an **agent can run neuroimaging**. Paper 6 asks whether **this already-shipping workbench** can take an agent as a proposer without bypassing the checks a human already faces.
- CyberNeuro’s Dispatcher is an **agent**. Ours must be the **existing FastAPI submit**.
- Coala asks whether a **CWL tool can be an MCP function**. Paper 6 asks whether an **MCP-or-LLM proposer is still the same job** after SciCap and SciGuard.
- Paper2Agent asks whether a **paper can become tools**. Paper 6 asks whether a **job that should never have been posted** was posted.
- Neurodesk remotes ask whether a **coding agent can live in the desktop**. Paper 6 does not add a chat box as the contribution.

If G is implemented by wrapping NeuroClaw and pointing it at FastSurfer, A1 has failed.

---

## 3. Layer — agentic MRI workbenches (highest blockers)

### 3.1 NeuroClaw / NeuroDiscovery (Wang et al., arXiv:2604.24696)

Public code: [CUHK-AIM-Group/NeuroClaw](https://github.com/CUHK-AIM-Group/NeuroClaw) → NeuroDiscovery. Docs: [cuhk-aim-group.github.io/NeuroClaw](https://cuhk-aim-group.github.io/NeuroClaw/get-started.html). Checked 26 October 2026.

Three-tier skills, BIDS-grounded planning, Docker, audit traces, NeuroBench (T01–T500). Host-agent installer for Cursor / Claude / Codex. This is the strongest “agentic neuroimaging” occupancy.

**May steal (tests / patterns, not a kernel):** arm **U** comparator; `SKILL.md` frontmatter *style* only (SciCap owns scientific fields); JSONL audit / checksum / digest *ideas* re-implemented against NeuroInsight jobs; with-skills vs no-skills contrast as G vs U **on our job API**.

**Must not:** vendor `claw-shell`, the desktop, AutoResearch / NeuroOracle, or the GPT-5.4 NeuroBench rubric (planning 30% / tool 40% / code 30%) as Paper 6 primary. Do not ship “NeuroClaw mode” inside NeuroInsight. Do not copy Proprietary skills (academic-research-hub is marked Proprietary).

**Install for comparator only**, outside this repo:

```text
git clone https://github.com/CUHK-AIM-Group/NeuroDiscovery.git
```

Arm U may be “same model + NeuroClaw skills + shell” *or* “same model + unconstrained tools.” Declare which. **Do not require NeuroClaw to implement G.**

### 3.2 CyberNeuro (arXiv:2607.28841)

Paper + hosted Windows app at [wanda-cyberbench.com](https://wanda-cyberbench.com). Claims FAIR4RS / open source. **No GitHub repo found** on 26 October 2026. Not an installable Linux/Slurm kernel.

**May steal (documented protocols):** Planner / Validator / Dispatcher / Reporter split — Planner = proposer (A1); Validator = SciCap + SciGuard; **Dispatcher = existing NeuroInsight submit, not an agent**; Reporter = Paper 5 receipt + optional NeuroAgentBench. JSON receipt field list (inputs, tool versions, commands, outputs, logs, validation, completion) plus our `qc_did_not_run`. No-egress *test design* copied onto Linux local and Slurm — do not claim their Windows measurement. Workspace confinement as threat model.

**Must not:** WandaMind or the Windows/WSL bundle as a dependency; wrap wanda-cyberbench.com as an API; inherit their NeuroBench-vs-NeuroClaw accuracy number.

### 3.3 NeuroPilot (Chen et al., arXiv:2608.07541)

Paper + same host. **No research GitHub.** [VSC-NeuroPilot/neuropilot](https://github.com/VSC-NeuroPilot/neuropilot) is an unrelated VS Code extension. Named skills exist only as paper descriptions (`dcm2bids-skill`, `neuroimage-pre-skill`, `qc-agent-skill`).

**May steal:** consequential-approval list locked on NeuroInsight submit — overwrite, delete, Slurm array, backend switch, `network: on`, fallback plugin. G cannot skip `--approve` on that list. Source data read-only; derivatives elsewhere. Append-only ledger *idea* maps to Paper 5 receipt + correction history. Idempotent retry is a platform feature; G must not “fix” by silently posting a different digest (A2). QC flags; `qc_did_not_run` ≠ pass.

**Must not:** treat their 17-cohort / 123k-subject claims as our results; implement `qc-agent-skill` as Paper 6 novelty; use the unrelated VS Code extension.

---

## 4. Layer — adjacent agent surfaces (not this job API)

### 4.1 Coala (Hu et al., *Bioinformatics*, 26 August 2026)

DOI: [10.1093/bioinformatics/btag641](https://doi.org/10.1093/bioinformatics/btag641). Site: [coala.info](https://coala.info). Code: [coala-info/coala](https://github.com/coala-info/coala).

CWL descriptors → MCP schemas; containerized execution via a generic MCP server. **Blocker for “we added MCP.”** Optional transport later (with Nipoppy). Paper 6 does not implement or claim a CWL→MCP adapter.

### 4.2 Paper2Agent (Miao et al., *Nature*, 16 September 2026)

DOI: [10.1038/s41586-026-11044-y](https://doi.org/10.1038/s41586-026-11044-y). Code: [jmiao24/Paper2Agent](https://github.com/jmiao24/Paper2Agent).

A paper becomes a validated MCP server. **Blocker for “papers-as-agents” and for Nature-family positioning of a chat wrapper.** Different object from a proposer on a shipping job API.

### 4.3 Neurodesk coding-agent remotes (2026)

Neurodesk already occupies accessible reproducible environments (*Nature Methods*; cite the platform paper at submission — do not invent a DOI here). 2026 product remotes put coding agents *inside* that desktop:

| Release | What shipped | Source |
|---|---|---|
| 2026-04-28 | OpenCode, Codex, Claude agent apps | [Release history](https://neurodesk.org/overview/release-history/) |
| 2026-09-23 | T3 Code remote server; OpenCode and Codex providers | same |

Docs: [OpenCode](https://neurodesk.org/getting-started/agents/opencode/), [Codex](https://neurodesk.org/getting-started/agents/codex/), [T3 Code](https://neurodesk.org/getting-started/agents/t3-code/).

**Positioning.** Agents in a container desktop, not NeuroInsight’s plugin/job API, not fail-closed submit, not H/G/U incorrect-submission. Do not rebuild Neurodesk remotes. Unconstrained tool-calling against Neurodesk images is a feature gap, not a method.

### 4.4 Nipoppy MCP, Brain Researcher

Nipoppy MCP exposes Boutiques descriptors over MCP — optional catalog/transport, not a fail-closed NeuroInsight submit. Brain Researcher (named in the limitations memo) uses claim cards on a live analysis; cite if a stable bibliographic record is locked, do not clone. Neither is this paper’s job object.

---

## 5. Layer — libraries this paper calls (not inventions)

| Call | Owner | Paper 6 may |
|---|---|---|
| `scicap invoke` ALLOW / REJECT / ABSTAIN | Paper 1 | Gate G before POST |
| `sciguard validate` PASS / FAIL / UNKNOWN | Paper 2 | Gate multi-step G before POST |
| `neuroagentbench evaluate` | Paper 3 | Optional after-run score; not primary |
| EvidenceGraph `workflow_run` | Paper 4 | Optional pointer |
| Kernel, receipt, N2 silent success, boundary | Paper 5 / `neuroinsight_research` | Submit path; reuse N2 field |

Do not republish M1–M4, G1–G5, B1–B7, E1–E5, or N1–N6 as Paper 6 results.

---

## 6. Field / object coverage

| Paper 6 object | Occupied by | Residual on *this* product |
|---|---|---|
| Agentic MRI workbench | NeuroClaw, CyberNeuro, NeuroPilot | **No. Do not claim.** |
| Coding agent in a desktop | Neurodesk remotes | **No.** |
| CWL/Boutiques → MCP | Coala, Nipoppy MCP | Optional transport only |
| Papers as agents | Paper2Agent | Different object |
| Skill packs / NeuroBench rubric | NeuroClaw | Arm U comparator; score with NeuroAgentBench |
| Planner / validate / dispatch | CyberNeuro | Planner = proposer; dispatch = existing submit |
| Consequential approval | NeuroPilot | Approval object = NeuroInsight job |
| Job equality vs human UI | — | **Yes — A2 on this API** |
| Incorrect-submission of posted jobs | — | **Yes — A3; not NAB false success** |
| Silent success by arm | Paper 5 N2 definition | **Yes — count N2 under H/G/U** |
| Proposer cannot import executor | Paper 5 N1 planned | **Yes — A1 on the shipping product** |

---

## 7. Five literature updates (this refresh)

1. **NeuroClaw (arXiv:2604.24696, public git) is the workbench occupancy.** Paper 6’s residual is a proposer on **this** job API plus H/G/U safety numbers — not a second harness. Arm U may use a separate NeuroDiscovery clone. **G is not a NeuroClaw wrap.**
2. **CyberNeuro (arXiv:2607.28841) is protocol, not a kernel.** No Linux repo found (26 October 2026). Steal Planner ≠ Dispatcher and the receipt field list. Their Dispatcher is an agent; ours must not be.
3. **NeuroPilot (arXiv:2608.07541) supplies the consequential-approval list**, not a skill pack to vendor. Overwrite, delete, Slurm array, backend switch, `network: on`, fallback plugin require `--approve`. The unrelated VS Code “NeuroPilot” extension is out of scope.
4. **Coala (Hu et al., *Bioinformatics* 2026, [10.1093/bioinformatics/btag641](https://doi.org/10.1093/bioinformatics/btag641)) occupies CWL→MCP.** Paper 6 does not claim an MCP adapter and does not treat Coala as the contribution.
5. **Paper2Agent (Miao et al., *Nature* 2026, [10.1038/s41586-026-11044-y](https://doi.org/10.1038/s41586-026-11044-y)) occupies papers-as-agents; Neurodesk 2026-04-28 / 2026-09-23 remotes occupy OpenCode / Codex / T3 coding agents in a container desktop.** Both kill “first agent workbench” and a Nature-family chat-wrapper story. Residual remains incorrect-submission and equality on the NeuroInsight job object.

---

## 8. What would not be novel (do not write these sentences)

- “We introduce the first agentic neuroimaging workbench.”
- “We add a chat box to NeuroInsight.”
- “We wrap NeuroClaw / claw-shell around FastSurfer.”
- “We expose neuroimaging tools to agents via MCP.” (Coala, Nipoppy MCP)
- “We turn papers into agents.” (Paper2Agent)
- “We put a coding agent in the desktop.” (Neurodesk remotes)
- “The agent is faster” as the primary claim.
- Republishing Papers 1–5 confirmatory tables as this paper’s invention.

---

## 9. Remaining testable claim

**Primary (keep).** On the shipping NeuroInsight job API, a proposer that can only write an approved job request — gated by SciCap and SciGuard — matches the human path on locked equality fields and does not raise incorrect submissions or platform silent success versus an unconstrained agent.

**Necessary controls**

1. Same plugins, same S0 fixtures, same token/time budget across H / G / U.
2. G cannot POST on SciCap REJECT/ABSTAIN or SciGuard FAIL.
3. Proposer process cannot import `backend.execution`, open a shell, or start a container.
4. Equality on `plugin_id`, `image_digest`, `inputs`, `backend`, `network` (and receipt format when Paper 5 receipts exist).
5. Incorrect-submission ≠ NeuroAgentBench false success. Paper 3 scores the artifact; Paper 6 scores whether a job that should never have been posted was posted.
6. Time-to-valid-job is secondary. A speed win that raises (1) or silent success is a no-go.

**Go / no-go** remain those in methods §5. Chat wrapper only → JOSS or fold into Paper 5 secondary. Not a Nature paper.

---

## 10. Sources (seed; re-check before submission)

1. Wang et al. NeuroClaw technical report. arXiv:2604.24696. Code: https://github.com/CUHK-AIM-Group/NeuroClaw  
2. CyberNeuro. arXiv:2607.28841. Product: https://wanda-cyberbench.com  
3. Chen et al. NeuroPilot. arXiv:2608.07541. Product: https://wanda-cyberbench.com  
4. NeuroClaw get-started: https://cuhk-aim-group.github.io/NeuroClaw/get-started.html  
5. Hu et al. (2026). Coala. *Bioinformatics* 42(9): btag641. https://doi.org/10.1093/bioinformatics/btag641 — https://coala.info  
6. Miao et al. (2026). Paper2Agent. *Nature*. https://doi.org/10.1038/s41586-026-11044-y — https://github.com/jmiao24/Paper2Agent  
7. Neurodesk release history (2026-04-28; 2026-09-23 remotes): https://neurodesk.org/overview/release-history/  
8. Neurodesk OpenCode / Codex / T3 Code: https://neurodesk.org/getting-started/agents/opencode/ · https://neurodesk.org/getting-started/agents/codex/ · https://neurodesk.org/getting-started/agents/t3-code/  
9. Papers 1–5 methods in this workspace. Software under test: https://github.com/phindagijimana/neuroinsight_research  

Re-run this search before submission. CyberNeuro’s “open-sourced” claim is not the same as a cloneable Linux repository today.
