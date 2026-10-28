"""Compute ground-truth answers for evals/questions.jsonl. Ticket: SEC-8.

Read the RAW files directly (not agent.data.load_secom) so a loader bug can't
hide in both the agent and the answers. Writes `expected` back into questions.jsonl.
TODO(SEC-8)
"""
