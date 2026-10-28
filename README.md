# secom-agent

A data-analyst agent that answers questions about real semiconductor fab sensor data
(UCI SECOM) by writing and running Python in a locked-down Docker sandbox, graded
automatically on a 30-question eval set.

The agent loop is hand-written against the Claude API; no agent framework.

- Spec (requirements, design, tickets): see the project spec doc
- Build guide (order and how-to for each ticket): [docs/GUIDE.md](docs/GUIDE.md)

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
curl -L -o data/secom.zip https://archive.ics.uci.edu/static/public/179/secom.zip
unzip data/secom.zip -d data
cp .env.example .env            # add your ANTHROPIC_API_KEY
docker build -t secom-sandbox sandbox/
python -m agent.cli ask "How many runs failed?"
```

## Tickets

| ID | Ticket | Day |
|---|---|---|
| SEC-1 | Project setup | 1 |
| SEC-2 | Data loader and data notes | 1 |
| SEC-3 | Tool-use spike | 1 |
| SEC-4 | Agent loop | 1 |
| SEC-5 | Sandbox and run_python | 1 |
| SEC-6 | describe_data, final_answer, code-backed check | 1 |
| SEC-7 | Tracing and CLI | 1 |
| SEC-8 | Question set and ground truth | 2 |
| SEC-9 | Eval runner and baseline | 2 |
| SEC-10 | Error analysis and one fix | 2 |
| SEC-11 | Write-up and demo | 2 |

## Results
_(SEC-9 and SEC-10)_

| Version | Split | Pass rate | All-3-correct | Avg steps | Cost / question | p95 latency |
|---|---|---|---|---|---|---|
| Baseline | dev | | | | | |
| Baseline | held-out | | | | | |
| After fix | dev | | | | | |
| After fix | held-out | | | | | |

## What failed
_(SEC-10)_

## Data
UCI SECOM dataset (CC BY 4.0), McCann & Johnston.
https://archive.ics.uci.edu/dataset/179/secom
