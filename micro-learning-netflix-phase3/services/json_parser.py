import json
import re


def parse_llm_json(text):

    DEFAULT_KEYS = {
        "topic": "",
        "summary": "",
        "key_ideas": [],
        "facts": [],
        "numbers": [],
        "quotes": []
    }

    try:

        # Remove common wrappers
        text = text.strip()

        text = text.replace(
            "MODEL RESPONSE",
            ""
        ).strip()

        # Extract largest JSON block
        match = re.search(
            r"\{[\s\S]*\}",
            text
        )

        if not match:

            return {
                **DEFAULT_KEYS,
                "raw_output": text,
                "parse_error": True
            }

        json_text = match.group()

        data = json.loads(
            json_text
        )

        # Ensure required keys exist
        if isinstance(data, dict):

            for key, default_value in DEFAULT_KEYS.items():

                data.setdefault(
                    key,
                    default_value
                )

        return data

    except Exception as e:

        print("\n" + "=" * 100)
        print("JSON PARSE FAILED")
        print(text)
        print("=" * 100 + "\n")

        return {
            **DEFAULT_KEYS,
            "raw_output": text,
            "parse_error": True,
            "error": str(e)
        }