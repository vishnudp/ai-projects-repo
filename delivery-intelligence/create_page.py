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

for space in spaces["results"]:
    print(
        f"KEY={space['key']} NAME={space['name']}"
    )
    
page = confluence.create_page(
    space="SCRUM",
    title="Sprint 2 Delivery Report",
    body="""
<h1>Sprint Health</h1>
<p>Completion: 50%</p>
<p>Risk: HIGH</p>
"""
)

print(page)