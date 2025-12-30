from schemas.input import AdvisoryInput
from schemas.output import ToolSuggestion, AdvisoryWarning


def apply_rules(input: AdvisoryInput):
    suggestions = []
    warnings = []
    explanation_parts = []
    if not input.all_available_mcp_tools_with_client:
        warnings.append(
            AdvisoryWarning(
                code="NO_TOOLS",
                message="No tools provided; advisory confidence is low.",
                severity="high",
            )
        )
        explanation_parts.append("No tools were available to evaluate.")

        return suggestions, warnings, " ".join(explanation_parts)

    # naive demo rule
    first_tool = input.all_available_mcp_tools_with_client[0]

    suggestions.append(
        ToolSuggestion(
            tool_name=first_tool,
            confidence=0.6,
            rationale="Default-first-tool heuristic (Phase 1 demo rule).",
        )
    )

    explanation_parts.append(
        "Applied Phase 1 heuristic: suggest first available tool."
    )

    return suggestions, warnings, " ".join(explanation_parts)
