"""Project settings. Ticket: SEC-1 (used by SEC-4, SEC-5, SEC-7).

Spec: Technical design -> Configuration.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
RUNS_DIR = ROOT / "runs"

MODEL = os.getenv("MODEL", "claude-sonnet-5-5")
MAX_STEPS = 12
INPUT_TOKEN_BUDGET = 200_000
API_TIMEOUT_S = 60

SANDBOX_IMAGE = "secom-sandbox"
SANDBOX_TIMEOUT_S = 30
SANDBOX_MEMORY = "512m"
SANDBOX_CPUS = 1.0
SANDBOX_PIDS_LIMIT = 64
SANDBOX_OUTPUT_LIMIT = 10_000  # characters, stdout + stderr

# USD per million tokens, per model: {"claude-...": {"input": 0.0, "output": 0.0}}
# TODO(SEC-7): fill from the official pricing page. Do not guess these numbers.
PRICES: dict[str, dict[str, float]] = {}
