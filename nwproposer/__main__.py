"""Library only. No execute command. No MCP."""

import sys

print(
    "nwproposer is a library: from nwproposer import propose\n"
    "agent hook: from nwproposer.agent import call_tool\n"
    "there is no execute command and no MCP server",
    file=sys.stderr,
)
raise SystemExit(2)
