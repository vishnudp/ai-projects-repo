import re
import json

def extract_json(text):

    match = re.search(
        r'\{.*\}',
        text,
        re.DOTALL
    )

    if not match:
        return None

    json_text = match.group(0)

    return json.loads(json_text)