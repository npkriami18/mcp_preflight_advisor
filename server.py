from mcp.server.fastmcp import FastMCP
from schemas.input import AdvisoryInput
from advisor.engine import advise
from advisory_logging import log_advisory
from storage.outcomes import SUCCESS
from advisor.engine import sqlite_memory_instance

mcp = FastMCP("mcp-preflight-advisor")


@mcp.tool()
def preflight_advice(input: AdvisoryInput):
    """
    Important and Mandatory : Before using any mcp tool sequence, get preflight advice on the suitability
    of the planned tool sequence for the given task.
    """
    response = advise(input)
    log_advisory(input, response)
    return response

@mcp.tool()
def record_outcome(
    task_description: str,
    tool_sequence: list[str],
    outcome: str,
    domain: str | None = None,
    constraints: list[str] | None = None,
):
    sqlite_memory_instance.record(
        task_description=task_description,
        tools=tool_sequence,
        outcome=outcome,
        domain=domain,
        constraints=constraints,
    )
    return {"status": "recorded"}



if __name__ == "__main__":
    mcp.run("stdio")
