from mcp.server.fastmcp import FastMCP
from schemas.input import AdvisoryInput
from advisor.engine import advise
from advisory_logging import log_advisory
from storage.outcomes import SUCCESS
from advisor.engine import memory

mcp = FastMCP("mcp-preflight-advisor")


@mcp.tool()
def preflight_advice(input: AdvisoryInput):
    """
    Provide advisory guidance on tool usage.
    This tool does not execute tools or enforce decisions.
    """
    response = advise(input)
    log_advisory(input, response)
    return response

@mcp.tool()
def record_outcome(tool_sequence: list[str], outcome: str):
    """
    Demo-only: record the outcome of a tool sequence.
    """
    memory.record(tool_sequence, outcome)
    return {"status": "recorded"}


if __name__ == "__main__":
    mcp.run("stdio")
