import anthropic
import json

from agent.data import load_secom
from agent.config import MODEL

client = anthropic.Anthropic()

QUESTION = "How many runs failed, and what share of all runs is that?"
TOOLS = [
    {
        "name": "count_runs",
        "description": (
            "Count production runs in the SECOM fab dataset. "
            "status='fail' counts failed runs, 'pass' counts passing runs, 'all' counts every run."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["pass", "fail", "all"],
                    "description": "Which runs to count.",
                }
            },
            "required": ["status"],
        }
    }
]

df = load_secom()

def count_runs(status: str) -> int:
    if status == "all":
        return len(df)
    return int((df["label"] == status).sum())

def main() -> None:
    client = anthropic.Anthropic()

    messages = [{"role": "user", "content": QUESTION}]
    call = 0
    while True:
        call += 1
        response = client.messages.create(
            model=MODEL, max_tokens=1024, tools=TOOLS, messages=messages
        )

        print(
            f"\n--- LOOP {call}: stop_reason={response.stop_reason} "
            f"input_tokens={response.usage.input_tokens} "
            f"output_tokens={response.usage.output_tokens}"
        )
        for block in response.content:
            if block.type == "text":
                print(f"text: {block.text}")
            elif block.type == "tool_use":
                print(f"tool_use: {block.name}({json.dumps(block.input)})  id={block.id}")

        if response.stop_reason != "tool_use":
            print("[LOOP BREAK] - Not 'tool_use' breaking the loop!")
            break

        messages.append({"role": "assistant", "content": response.content})

        results = []
        for block in response.content:
            if block.type == "tool_use":
                value = count_runs(**block.input)
                print(f"tool_result for {block.id}: {value}")
                results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": str(value)}
                )
        messages.append({"role": "user", "content": results})

if __name__ == "__main__":
    main()
