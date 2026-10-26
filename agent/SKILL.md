# nwproposer

Call `from nwproposer import propose`. Write the same job a human would send to neuroworkbench.

`submit(..., arm="G", approve=True, kernel="workbench")` is fail-closed. Do not execute.

Optional after a recorded tree: `evaluate_recorded` (NeuroAgentBench owns that score; `paper6_primary: false`).

No execute tool. No MCP. No chat UI. G is not a NeuroClaw wrap. U is unconstrained.
