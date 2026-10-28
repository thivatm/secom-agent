"""Tool schemas and handlers. Tickets: SEC-5 (run_python), SEC-6 (describe_data, final_answer).

Spec: FR-3, FR-4, FR-5 and Technical design -> Tool interfaces.
"""
from dataclasses import dataclass, field
from typing import Any

# TODO(SEC-6): exactly three tool definitions: describe_data, run_python, final_answer.
# Each: {"name": ..., "description": ..., "input_schema": {JSON Schema}}.
# Descriptions are prompts - write them carefully.
TOOLS: list[dict[str, Any]] = []


@dataclass
class RunState:
    """Per-run state the handlers need, e.g. for the FR-4 code-backed check."""
    successful_code_runs: list[str] = field(default_factory=list)
    final_answer: dict[str, Any] | None = None


def handle_tool(name: str, tool_input: dict[str, Any], state: RunState) -> tuple[str, bool]:
    """Execute one tool call. Return (content for tool_result, is_error).

    Never raise for model mistakes - return an error message with is_error=True (FR-3).
    TODO(SEC-5, SEC-6)
    """
    raise NotImplementedError
