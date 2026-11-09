import json
from typing import Any


def parse_json_object(
    content: str,
) -> dict[str, Any]:

    content = content.strip()

    if content.startswith("```"):
        lines = content.splitlines()

        if len(lines) >= 2:
            lines = lines[1:-1]

        content = "\n".join(lines).strip()

    value = json.loads(content)

    if not isinstance(value, dict):
        raise ValueError(
            "LLM output must be a JSON object"
        )

    return value