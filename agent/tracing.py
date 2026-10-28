"""Write one JSONL trace file per run. Ticket: SEC-7.

Spec: FR-6. A trace must be enough to replay the run without new API calls.
"""
from pathlib import Path
from typing import Any


class Trace:
    """TODO(SEC-7): one event per line in runs/<run_id>.jsonl:
    run_start, api_call (tokens, latency), tool_call, tool_result, run_end (status, cost, latency)."""

    def __init__(self, question: str, model: str) -> None:
        raise NotImplementedError

    def log(self, event: str, **fields: Any) -> None:
        raise NotImplementedError

    @property
    def path(self) -> Path:
        raise NotImplementedError
