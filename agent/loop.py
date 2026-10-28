"""The hand-written agent loop. Ticket: SEC-4 (system prompt in SEC-6).

Spec: FR-2. No agent frameworks.
"""
from dataclasses import dataclass
from typing import Any

SYSTEM_PROMPT = """TODO(SEC-6): role, where the data is, use run_python for every number,
call final_answer with status cannot_answer when the data cannot answer."""


@dataclass
class RunResult:
    run_id: str
    status: str  # completed | step_limit | budget_exceeded | error
    answer: dict[str, Any] | None
    steps: int
    input_tokens: int
    output_tokens: int
    cost_usd: float
    latency_s: float


def run_agent(question: str, client: Any = None) -> RunResult:
    """Answer one question. `client` is injectable so tests can pass a stub.

    TODO(SEC-4):
      - send messages + TOOLS; on tool_use run EVERY tool_use block via handle_tool
      - append the assistant content, then ONE user message with all tool_result blocks
      - stop on accepted final_answer, MAX_STEPS, or INPUT_TOKEN_BUDGET
      - retry rate-limit / overload / 5xx errors with backoff
      - log every API call and tool call to the trace (SEC-7)
    """
    raise NotImplementedError
