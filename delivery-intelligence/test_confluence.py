from atlassian import Confluence
from dotenv import load_dotenv
import os

load_dotenv()

confluence = Confluence(
    url=os.getenv("CONFLUENCE_URL"),
    username=os.getenv("CONFLUENCE_EMAIL"),
    password=os.getenv("CONFLUENCE_TOKEN")
)

spaces = confluence.get_all_spaces()

for s in spaces["results"]:
    print(
        s["key"],
        s["name"]
    )