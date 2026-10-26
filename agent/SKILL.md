# nwproposer

Call `from nwproposer import propose`. Write the same job a human would send to neuroworkbench.

`submit(..., arm="G", approve=True, kernel="workbench")` is fail-closed. Do not execute.

Optional after a recorded tree: `evaluate_recorded` (NeuroAgentBench owns that score).

No execute tool. No MCP. Not a NeuroClaw wrap.
