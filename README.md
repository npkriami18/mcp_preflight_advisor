# MCP Preflight Advisor

An MCP server that provides deterministic, explainable advice to AI agents
about tool usage — without executing tools, enforcing decisions, or using ML.

## Why This Exists

LLM-based agents frequently make poor tool choices:

- tools are selected inconsistently
- missing evidence is replaced with confident guesses
- prior failures are forgotten
- tool-selection logic is opaque and uninspectable

This project externalizes part of that decision-making into a
deterministic, auditable system that can advise — but not control — agents.

## What This Server Does

The MCP Preflight Advisor runs *before* tool execution and:

- evaluates a task description and available tools
- suggests tool sequences (advisory only)
- assigns confidence scores with explicit uncertainty
- emits warnings when evidence is weak or negative
- explains why advice was given
- references similar past tasks when available

## What This Server Does Not Do

- execute tools
- block or enforce agent behavior
- train or run ML models
- make autonomous decisions

## Design Philosophy

- Advisory, not authoritarian  
- Evidence-first, not answer-first  
- Explainable logic over clever models  
- Guardrails over autonomy  
- Determinism over novelty  

The advisor is designed to say:
“I am not confident, and here is why.”

## How It Works (High Level)

1. Deterministic rules generate an initial tool suggestion.
2. Historical outcomes adjust confidence conservatively.
3. Negative evidence produces explicit warnings.
4. Similar past tasks are surfaced when possible.
5. A structured advisory response is returned to the agent.

All reasoning is logged and inspectable.

## Why No Machine Learning

This project intentionally avoids ML models.

Instead, it uses:
- deterministic rules
- simple mathematical scoring
- historical statistics
- conservative thresholds

The goal is:
- explainability
- debuggability
- predictable behavior
- engineering clarity

ML may be explored in future phases, but it is not foundational.

## What This Project Demonstrates

- understanding of MCP beyond syntax
- system design under uncertainty
- separation of policy from execution
- state and persistence design
- observability for decision-making
- engineering restraint

## Status

This is a working demo with:
- MCP server integration
- advisory rules
- confidence scoring
- outcome-aware warnings
- similarity-lite matching
- persistent institutional memory (SQLite)

Future work may include:
- richer similarity metrics
- configurable policies
- production-grade persistence

## Failure Injection Example

To demonstrate uncertainty handling, the advisor can be seeded
with repeated failures for a given tool sequence.

When the same task is evaluated again:
- confidence is reduced
- warnings are elevated
- negative history is surfaced explicitly

This behavior is deterministic and explainable.
