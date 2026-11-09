import json
import os

FILE_PATH = "data/case_studies.json"


def load_repository():

    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, "r") as f:
        return json.load(f)


def save_case(case_json):

    data = load_repository()

    data.append(case_json)

    with open(FILE_PATH, "w") as f:
        json.dump(
            data,
            f,
            indent=2
        )