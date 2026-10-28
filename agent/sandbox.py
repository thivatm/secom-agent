"""Run model-generated Python inside a locked-down Docker container. Ticket: SEC-5.

Spec: Non-functional requirements -> Sandbox limits for run_python.
"""
from dataclasses import dataclass


@dataclass
class SandboxResult:
    stdout: str
    stderr: str
    exit_code: int | None
    duration_s: float
    timed_out: bool
    truncated: bool


def run_code(code: str) -> SandboxResult:
    """Run `code` in a fresh secom-sandbox container and return its output.

    TODO(SEC-5): apply EVERY limit in the spec table:
      no network, read-only root fs, writable /tmp only, data mounted read-only at /data,
      non-root user, 1 CPU, 512 MB, 64 pids, 30 s wall clock (then kill),
      output truncated to SANDBOX_OUTPUT_LIMIT, no host env vars passed in.
    The container must be removed afterwards, even on timeout or error.
    """
    raise NotImplementedError
