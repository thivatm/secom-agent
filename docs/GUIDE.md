# Build guide — Fab Data Analyst Agent

The spec says **what** to build. This guide says **in what order and how**, one ticket at a time.
Each ticket: learn first → do → done when → review.

## How work flows (same as on a team)

1. Pick the next ticket in the spec's Milestones table and set its Status to **In progress**.
2. Branch: `git checkout -b sec-2-data-loader`
3. Build until the ticket's acceptance criteria pass. Write the tests with the code, not after.
4. Check: `ruff check . && pytest`
5. Push and open a PR titled `SEC-2: Data loader and data notes`. Set Status to **In review**.
6. Tell Claude: **"SEC-2 ready for review"**. I read the branch and give review comments.
7. Fix, merge to `main`, set Status to **Done**.

Rule: ask for hints and reviews, not full solutions. In an interview you must explain every line.

---

## Where to start: SEC-1 (about 20 min left)

Done already: data downloaded, venv created, `.env` filled in.

1. `source .venv/bin/activate`
2. `pip install -r requirements.txt -r requirements-dev.txt`
3. Docker smoke test:
   `docker run --rm --network none python:3.11-slim python -c "print('sandbox ok')"`
4. `git init && git add . && git status`
   Confirm `.env`, `data/secom.*` and `.venv/` are **not** listed. Stop if they are.
5. `git commit -m "SEC-1: project skeleton"`, create a private GitHub repo `secom-agent`, push `main`.

**Done when:** the repo is on GitHub with no secrets and no data files in it.

---

## Day 1 — a working, sandboxed agent

### SEC-2 — Data loader and data notes (1.5 h)

**Learn first:** `pd.read_csv(path, sep=r"\s+", header=None)`, `pd.to_datetime(..., format=...)`,
`df.isna().mean()`, `df.nunique()`.

**Do:**
1. Read `data/secom.names` (5 min). Real projects start with the data's documentation.
2. Implement `load_secom()` in `agent/data.py` as its docstring says.
3. Write `tests/test_data.py`: 1,567 rows; labels only `pass`/`fail`; 104 fails;
   `timestamp` is a datetime; sensor columns named `sensor_000`, ...
4. In a scratch script, measure each fact in `data/DATA_NOTES.md` and fill it in.

**Done when:** tests pass and `DATA_NOTES.md` has real numbers.
**Interview question:** why measure data quality before building the agent?

### SEC-3 — Tool-use spike (1 h)

**Learn first:** [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview), [How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works), [How to implement tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use). The whole mechanism:
1. Send `messages` + `tools` (name, description, JSON Schema input).
2. Response has `stop_reason == "tool_use"` and one or more `tool_use` blocks (`id`, `name`, `input`).
3. You run the tool. Append Claude's full response as an `assistant` message, then ONE `user`
   message with a `tool_result` block per call (matching `tool_use_id`).
4. Call again. Stop at `stop_reason == "end_turn"`.

**Do:** in `hello_tools.py`, one tool `count_runs(status: "pass" | "fail" | "all")`.
Ask: *"How many runs failed, and what share of all runs is that?"* Print every tool call,
tool result, the final answer and `response.usage` for each API call.

**Done when:** Claude calls `count_runs` with `fail`, gets 104, answers about 6.6%.
**Answer before review:** (1) Did it call once or twice, in one response or two?
(2) What error do you get if you skip appending the assistant message? (3) Why did input
tokens grow on the second call?

### SEC-4 — Agent loop (2 h)

**Learn first:** Anthropic's "Building effective agents" post; the SDK's error classes and its
built-in `max_retries` option.

**Do:**
1. Implement `run_agent()` in `agent/loop.py` (see the docstring).
2. Stop conditions: accepted `final_answer` → `completed`; `MAX_STEPS` → `step_limit`;
   input tokens over `INPUT_TOKEN_BUDGET` → `budget_exceeded`.
3. Retries with backoff on rate-limit, overload and 5xx errors. Decide between the SDK's
   built-in retries and your own; explain the choice in the PR.
4. `tests/test_loop.py` with a **stub client** (a fake `messages.create` returning scripted
   responses, no network): two parallel `tool_use` blocks → one user message with two
   `tool_result` blocks; the step limit stops the run.

**Done when:** the loop tests pass with no API key set.
**Interview question:** why does the loop, not the model, enforce the limits?

### SEC-5 — Sandbox and `run_python` (2 h)

**Learn first:** `docker run` flags `--network none`, `--read-only`, `--tmpfs /tmp`,
`-v <dir>:/data:ro`, `--user`, `--cpus`, `--memory`, `--pids-limit`; the Docker SDK's
`containers.run(...)`, `container.wait(timeout=...)` and `container.kill()`.

**Do:**
1. Write `sandbox/Dockerfile` and `sandbox/secom.py` (see the TODOs). Copy the loader into the
   image so host and sandbox read the data the same way.
   Build: `docker build -t secom-sandbox sandbox/`
2. Implement `run_code()` in `agent/sandbox.py` with every limit in the spec table.
3. Wire `run_python` into `handle_tool()`.
4. `tests/test_sandbox.py`: the 7 security cases from the spec, marked `@pytest.mark.docker`.

**Done when:** all 7 security tests pass locally.
**Interview question:** what doesn't Docker protect against, and what would you use for
stronger isolation?

### SEC-6 — `describe_data`, `final_answer`, code-backed check (1.5 h)

**Do:**
1. Fill in `TOOLS` with the three schemas. Treat descriptions as prompts.
2. `describe_data` returns the facts from `DATA_NOTES.md` as JSON.
3. `final_answer`: validate the input; apply the FR-4 check (a numeric answer needs a successful
   `run_python` earlier in the run, tracked in `RunState`); reject with `is_error=True`.
4. Write `SYSTEM_PROMPT` in `agent/loop.py`.
5. `tests/test_tools.py`: the FR-4 rejection; input validation.

**Done when:** both unanswerable example questions abstain in 3 of 3 runs.

### SEC-7 — Tracing and CLI (1 h)

**Do:** implement `Trace` in `agent/tracing.py`; fill `PRICES` in `agent/config.py` from the
official pricing page; implement `agent/cli.py`.

**Done when:** `python -m agent.cli ask "How many runs failed?"` prints all six items and writes
`runs/<run_id>.jsonl`. **Day 1 is complete.**

---

## Day 2 — measure, then improve

### SEC-8 — Question set and ground truth (2 h)

**Do:**
1. Write 30 questions in `evals/questions.jsonl` following the spec's category mix
   (one example line is there). State the answer format in each question.
2. `evals/compute_answers.py`: compute every `expected` from the **raw files**, not from
   `load_secom()`, so a loader bug can't hide in both places.
3. Hand-check 5 answers. Mark 20 as `dev` and 10 as `held_out`, spread across categories.

**Done when:** 30 lines, every `expected` filled by the script.

### SEC-9 — Eval runner and baseline (2 h)

**Do:** implement `evals/run.py`: questions × repeats → `run_agent` → grade → metrics → report
built from the saved traces. Run 5 questions first and check the cost before running all 90.
Then run the dev and held-out baselines and copy the numbers into the README.

**Done when:** both baseline reports exist with every metric from the spec.

### SEC-10 — Error analysis and one fix (2.5 h)

**Do:**
1. Read every failing trace. Write one line per failure in your own words in
   `evals/reports/error_analysis.md`.
2. Check the expected answer first; your ground truth can be wrong.
3. Group the lines into categories and count them.
4. Fix only the largest category. Re-run dev, then held-out once.

**Done when:** a before/after table for dev and held-out.

### SEC-11 — Write-up and demo (1.5 h)

**Do:** README with the architecture diagram, how to run, results table, "what failed" and
"what I'd do next"; a 2-minute screen recording; a GitHub Action running `ruff` and
`pytest -m "not docker"`.

**Done when:** a stranger can clone, run and understand the results.

---

## Getting unstuck

- Stuck more than 30 minutes: send me the error, what you expected, and what you tried.
- Ask "what's a hint for X?" before "how do I do X?".
