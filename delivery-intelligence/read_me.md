Yesterday 11:56 AM



"Given one Jira sprint, generate a Delivery Intelligence Report using Jira data + basic statistical analysis + AI summary."

At the end of the week, you should be able to ask:

"What is the sprint health and delivery risk?"

and get a useful answer.

POC Scope(1 Sprint Only)
Input

One Jira sprint:

Example:

Project: PAY
Sprint: Sprint - 45
Duration: 2 weeks
Issues: ~50

Collect:

Stories
Bugs
Tasks
Status changes
Assignee
Priority
Story points
Created date
Completed date
Comments
Blockers
Target Output

Generate a report like:

Sprint: Sprint - 45

Delivery Health: 78 %

  Completed:
32 issues

Remaining:
12 issues

Blocked:
6 issues


Key Risks:

1. 3 critical bugs still open
2. 5 stories moved from previous sprint
3. Average cycle time increased by 25 %


  Prediction:

Sprint likely to complete with 2 - 3 carryover items.
Week Plan
Day 1 — Jira Data Extraction
Goal:

Get sprint data into your system.

  Architecture:

Jira
  |
  Jira REST API
    |
    Node.js Script
      |
      JSON / PostgreSQL
Create Jira API access

Need:

Jira URL
Email
API Token
Project Key
Sprint ID
Extract sprint issues

Use JQL:

project = PAY
AND sprint = 45

Collect:

issueKey
summary
type
status
priority
storyPoints
assignee
created
updated
resolutionDate

Store:

Option 1(fast):

sprint.json

Option 2:

PostgreSQL
Day 2 — Calculate Sprint Metrics

Build a simple analytics service.

No AI yet.

  Calculate:

1. Completion Rate

Formula:

Completed Issues
-----------------
  Total Sprint Issues

Example:

32 / 50

Completion:
64 %
  2. Story Point Completion

Example:

Committed:
80 points

Completed:
62 points

Velocity:
77 %
  3. Carryover Analysis

Find:

Issues added from previous sprint

Example:

Carryover:
8 issues

Risk:
High
4. Cycle Time

Calculate:

Done Date - In Progress Date

Example:

Average cycle time:

5.2 days
5. Blocker Analysis

Find:

Status = Blocked

Output:

Blocked Issues:

PAY - 101
PAY - 115
PAY - 122
Day 3 — Build Risk Rules

Create simple statistical rules.

  Example:

if (carryOverPercentage > 20) {
  risk = "HIGH"
}

Rules:

Rule 1
IF
open critical bugs > 0

THEN
release risk HIGH
Rule 2
IF
carryover issues > 15 %

  THEN
delivery risk HIGH
Rule 3
IF
average cycle time increased

THEN
delivery risk MEDIUM

Output:

{
  "risk": "HIGH",
    "reason": [
      "5 blocked issues",
      "3 critical bugs",
      "25% carryover"
    ]
}
Day 4 — Add AI Summary Layer

Now add an LLM.

  Architecture:

Sprint Data
  |
  Metrics Engine
    |
    Risk JSON
      |
      AI
      |
      Human Report

Give AI only the calculated data.

Example prompt:

You are a delivery manager.

Analyze this sprint:

Completion: 64 %
  Carryover: 25 %
    Blocked issues: 5
Critical bugs: 3

Generate:
1. Sprint summary
2. Risks
3. Recommendations

AI output:

Sprint is at high risk.

Main contributors:

- High carryover
  - Critical bugs
    - Dependency blockers

Recommendation:

Run defect triage.
Review unfinished stories.
  Day 5 — Create Simple UI / API

Create one endpoint:

GET / sprint - report / 45

Response:

{
  "sprint": "Sprint-45",
    "health": "78%",
      "risk": "Medium",
        "summary": "..."
}

Optional UI:

Simple:

React page
Streamlit
Grafana dashboard

Display:

-----------------------
  Sprint Health
78 %
  -----------------------

    Completed
32

Blocked
5

Risk
MEDIUM
-----------------------
  Day 6 — Add Confluence Context(Optional)

Only add one or two documents.

  Example:

Confluence:

Sprint Goal Document
Release Plan
Architecture Notes

Flow:

Sprint Metrics
  +
  Confluence Context
    |
    AI
    |
    Better Explanation

Example:

Without Confluence:

API story delayed

With Confluence:

API story delayed because payment gateway migration dependency is pending.
  Day 7 — Demo Scenario

Prepare 5 questions:

Question 1

"How healthy is Sprint-45?"

Answer:

Health: 78 %
  Risk: Medium
Question 2

"Why are we delayed?"

Answer:

Main reasons:

1. 5 blocked stories
2. Increased cycle time
3. QA delay
Question 3

"Which items need attention?"

Answer:

PAY - 101
PAY - 115
PAY - 122
Question 4

"Can this sprint finish on time?"

Answer:

Probability:
65 %

  Risk:
Medium
Question 5

"Prepare manager summary"

Output:

Sprint executive summary...
POC Technology Stack

Keep it simple:

Component	Technology
Backend	Node.js
Jira Integration	Jira REST API
Database	PostgreSQL / JSON
Analytics	JavaScript
AI	OpenAI API / Azure OpenAI
UI	React / Streamlit
Deployment	Local Docker
Do NOT build in this POC

This is a strong POC because it stays focused on a real delivery-management problem instead of trying to build a generic "AI for Jira" solution.

For an engineering leadership, Associate Architect, or AI Solutions Engineer interview, I would refine it slightly so that it demonstrates:

Data Engineering
Analytics
AI Reasoning
Business Impact

rather than just Jira extraction.

Recommended Architecture
                    +-------------------+
                    |      Jira API     |
                    +---------+---------+
                              |
                              v
                 +------------------------+
                 | Jira Data Ingestion    |
                 | Node.js Service        |
                 +-----------+------------+
                             |
                             v
                 +------------------------+
                 | Sprint Analytics Engine|
                 +-----------+------------+
                             |
        +--------------------+------------------+
        |                                       |
        v                                       v

+-------------------+            +----------------------+
| Statistical Rules |            | Historical Metrics   |
| Risk Engine       |            | Trend Analysis       |
+---------+---------+            +----------+-----------+
          |                                 |
          +---------------+-----------------+
                          |
                          v

               +----------------------+
               | Delivery Context JSON|
               +----------+-----------+
                          |
                          v

               +----------------------+
               | LLM Summary Engine   |
               | GPT / Azure OpenAI   |
               +----------+-----------+
                          |
                          v

               +----------------------+
               | Delivery Report API  |
               +----------------------+
What Makes This More Valuable

Instead of only reporting:

{
  "completed": 32,
  "blocked": 6
}

calculate a real Sprint Health Score.

Example:

Health Score =

30% Completion Rate
25% Story Point Velocity
20% Blocker Impact
15% Carryover Impact
10% Critical Defects

Example:

Completion Score      80
Velocity Score        75
Blocker Score         60
Carryover Score       70
Defect Score          90

Final Health Score:

78%

This immediately gives management a single KPI.

Metrics to Calculate
Delivery Metrics
Completion %
Completed Issues
---------------
Total Issues
Velocity %
Completed Story Points
----------------------
Committed Story Points
Scope Change %
Added During Sprint
-------------------
Original Sprint Scope

Very important because many teams fail due to scope creep.

Flow Metrics
Average Cycle Time
Done Date - In Progress Date
Lead Time
Done Date - Created Date
Throughput
Completed Issues / Day
Quality Metrics
Open Critical Bugs
Priority = Highest
Type = Bug
Status != Done
Bug Leakage
Bugs Created During Sprint
Stability Metrics
Carryover %
Issues moved from previous sprint
---------------------------------
Sprint Issues
Reopened %
Reopened Issues
---------------
Completed Issues
Risk Engine Design

Keep this deterministic initially.

Example:

const risks = [];

if (criticalBugs > 0)
    risks.push("Critical defects remain open");

if (carryOverPercent > 15)
    risks.push("High carryover from previous sprint");

if (blockedIssues > 5)
    risks.push("Multiple blocked items affecting flow");

if (cycleTimeGrowth > 20)
    risks.push("Cycle time significantly increased");

Risk Scoring:

riskScore =
    criticalBugWeight +
    blockerWeight +
    carryoverWeight +
    cycleTimeWeight;

Output:

{
  "healthScore": 78,
  "riskLevel": "MEDIUM",
  "riskReasons": [
    "3 critical bugs",
    "6 blocked issues",
    "20% carryover"
  ]
}
AI Layer (Important)

The biggest mistake is sending raw Jira tickets to the LLM.

Instead send only:

{
  "completionRate": 64,
  "velocity": 77,
  "carryover": 25,
  "blocked": 5,
  "criticalBugs": 3,
  "cycleTimeIncrease": 25
}

Prompt:

You are a Delivery Manager.

Analyze the sprint metrics below.

Provide:

1. Executive Summary
2. Delivery Risks
3. Likely Outcome
4. Recommendations

Return concise management-friendly output.

This reduces:

Cost
Hallucination
Token usage
Privacy concerns
API Design
Sprint Report
GET /api/sprints/45/report

Response:

{
  "sprintId": 45,
  "healthScore": 78,
  "risk": "MEDIUM",
  "completionRate": 64,
  "velocity": 77,
  "blockedIssues": 5,
  "criticalBugs": 3,
  "carryover": 25,
  "prediction": "2-3 items likely to spill over",
  "summary": "Sprint progressing with moderate risk..."
}
Executive Dashboard

Instead of a generic React page, show:

----------------------------------
SPRINT HEALTH
78%
----------------------------------

Completion Rate     64%
Velocity            77%
Carryover           25%
Blocked Items        5
Critical Bugs        3

Risk Level      MEDIUM

Prediction:
2-3 items may spill over
----------------------------------
What Would Impress Leadership More

Add a simple prediction model.

Using previous sprint history:

Sprint 41 -> 70%
Sprint 42 -> 74%
Sprint 43 -> 68%
Sprint 44 -> 72%

Estimate:

Probability of completion:
65%

Even a basic regression or weighted average is enough for a POC.

This elevates the solution from a reporting dashboard to a Delivery Intelligence Platform.

Final POC Deliverables
Jira data ingestion service (Node.js)
Sprint analytics engine
Rule-based risk engine
AI-generated delivery summary
Sprint Health Score (0–100)
Completion prediction
REST API (/sprint-report/{id})
Lightweight dashboard

That is a realistic 1-week POC and aligns well with a Forward Deployed Engineer / AI Solutions Engineer / Associate Architect profile because it combines integration, analytics, AI orchestration, and executive-level insights rather than being just another Jira reporting tool.

how to get the project name

This is actually good news — it means your Confluence integration is working and the page was already created successfully.

The error:

A page with this title already exists

means you're trying to create:

Sprint 2 Delivery Report

again in the same Confluence space.

Option 1: Update Existing Page (Recommended)

Instead of:

confluence.create_page(
    space="SCRUM",
    title=title,
    body=content
)

use:

existing = confluence.get_page_by_title(
    space="SCRUM",
    title=title
)

if existing:

    confluence.update_page(
        page_id=existing["id"],
        title=title,
        body=content
    )

    return {
        "message": "Page Updated",
        "page_id": existing["id"]
    }

else:

    page = confluence.create_page(
        space="SCRUM",
        title=title,
        body=content
    )

    return {
        "message": "Page Created",
        "page_id": page["id"]
    }
Option 2: Auto Version the Title

Generate unique titles:

from datetime import datetime

title = (
    f"Sprint {sprint_id} Delivery Report - "
    f"{datetime.now().strftime('%Y%m%d-%H%M%S')}"
)

Example:

Sprint 2 Delivery Report - 20260720-154500

This creates a new page every time.

Best Enterprise Approach

For your Delivery Intelligence POC, I'd recommend:

Sprint 2 Delivery Report

always stays the same page and gets updated.

Benefits:

Single source of truth
Latest metrics always visible
Release notes get refreshed
Leadership bookmark never changes
Update your PublishWorkflow

In workflows/publish_workflow.py:

title = f"Sprint {sprint_id} Delivery Report"

existing = self.confluence.get_page_by_title(
    space="SCRUM",
    title=title
)

if existing:

    self.confluence.update_page(
        page_id=existing["id"],
        title=title,
        body=content
    )

    return {
        "status": "updated",
        "page_id": existing["id"]
    }

page = self.confluence.create_page(
    space="SCRUM",
    title=title,
    body=content
)

return {
    "status": "created",
    "page_id": page["id"]
}

Also, one important security note: you've previously pasted a live Atlassian API token in this chat. You should revoke that token and create a new one, then move it into .env rather than keeping it hardcoded in jira_agent.py and Confluence code.

update this

from atlassian import Confluence
from dotenv import load_dotenv
import os

load_dotenv()


class ConfluenceTool:

    def __init__(self):

        self.client = Confluence(
            url=os.getenv("CONFLUENCE_URL"),
            username=os.getenv("CONFLUENCE_EMAIL"),
            password=os.getenv("CONFLUENCE_TOKEN")
        )

    def list_spaces(self):

        spaces = self.client.get_all_spaces()

        for space in spaces["results"]:
            print(
                f"KEY={space['key']} "
                f"NAME={space['name']}"
            )

        return spaces

    def create_page(
        self,
        space,
        title,
        body
    ):

        return self.client.create_page(
            space=space,
            title=title,
            body=body
        )

    def update_page(
        self,
        page_id,
        title,
        body
    ):

        return self.client.update_page(
            page_id=page_id,
            title=title,
            body=body
        )

Update your ConfluenceTool so it can:

Check whether a page already exists.
Create if it doesn't exist.
Update if it already exists.
from atlassian import Confluence
from dotenv import load_dotenv
import os

load_dotenv()


class ConfluenceTool:

    def __init__(self):

        self.client = Confluence(
            url=os.getenv("CONFLUENCE_URL"),
            username=os.getenv("CONFLUENCE_EMAIL"),
            password=os.getenv("CONFLUENCE_TOKEN")
        )

    def list_spaces(self):

        spaces = self.client.get_all_spaces()

        for space in spaces["results"]:
            print(
                f"KEY={space['key']} "
                f"NAME={space['name']}"
            )

        return spaces

    def get_page_by_title(
        self,
        space,
        title
    ):

        return self.client.get_page_by_title(
            space=space,
            title=title
        )

    def create_page(
        self,
        space,
        title,
        body
    ):

        return self.client.create_page(
            space=space,
            title=title,
            body=body
        )

    def update_page(
        self,
        page_id,
        title,
        body
    ):

        return self.client.update_page(
            page_id=page_id,
            title=title,
            body=body
        )

    def create_or_update_page(
        self,
        space,
        title,
        body
    ):

        existing_page = self.get_page_by_title(
            space,
            title
        )

        if existing_page:

            page_id = existing_page["id"]

            self.update_page(
                page_id,
                title,
                body
            )

            return {
                "status": "updated",
                "page_id": page_id,
                "title": title
            }

        page = self.create_page(
            space,
            title,
            body
        )

        return {
            "status": "created",
            "page_id": page["id"],
            "title": title
        }

Then in your PublishWorkflow, replace:

confluence.create_page(
    space="SCRUM",
    title=title,
    body=content
)

with:

result = confluence.create_or_update_page(
    space="SCRUM",
    title=title,
    body=content
)

return result

This will ensure that:

First publish → creates the page.
Subsequent publishes → update the same Confluence page.
No more "A page with this title already exists" errors.

You can also enhance it later to create pages under a parent page such as:

Delivery Intelligence
 ├── Sprint 1 Report
 ├── Sprint 2 Report
 ├── Sprint 3 Report

which is a common enterprise Confluence structure.

DATA: : {'issues': [{'key': 'SCRUM-2', 'summary': 'Task 2', 'status': 'Done', 'priority': None, 'assignee': None, 'created': '2026-07-20T13:09:00.645+0530', 'resolutionDate': 'None'}, {'key': 'SCRUM-1', 'summary': 'Task 1', 'status': 'To Do', 'priority': None, 'assignee': None, 'created': '2026-07-20T13:08:59.822+0530', 'resolutionDate': 'None'}]}

def build_issue_table(
        self,
        sprint_data
    ):

        print("TYPE:", type(sprint_data))
        print("DATA:", sprint_data)

        html = """
        <h2>Jira Tickets</h2>

        <table border="1">
            <tr>
                <th>Key</th>
                <th>Summary</th>
                <th>Status</th>
                <th>Assignee</th>
                <th>Priority</th>
            </tr>
        """

        for issue in sprint_data:

            if not isinstance(issue, dict):
                print("Skipping invalid issue:", issue)
                continue

            html += f"""
            <tr>
                <td>{issue.get('key', '')}</td>
                <td>{issue.get('summary', '')}</td>
                <td>{issue.get('status', '')}</td>
                <td>{issue.get('assignee', '')}</td>
                <td>{issue.get('priority', '')}</td>
            </tr>
            """

        html += "</table>"

        return html

    def build_release_notes(
        self,
        sprint_data
    ):

        html = """
        <h2>Release Notes</h2>

        <table border="1">
            <tr>
                <th>Ticket</th>
                <th>Feature</th>
                <th>Status</th>
            </tr>
        """

        for issue in sprint_data:

            if not isinstance(issue, dict):
                continue

            status = str(
                issue.get("status", "")
            ).lower()

            if status in [
                "done",
                "closed",
                "completed",
                "resolved"
            ]:

                html += f"""
                <tr>
                    <td>{issue.get('key', '')}</td>
                    <td>{issue.get('summary', '')}</td>
                    <td>Released</td>
                </tr>
                """

        html += "</table>"

        return html


Your debug output shows the root cause:

sprint_data = {
    "issues": [
        {...},
        {...}
    ]
}

But your methods are doing:

for issue in sprint_data:

which iterates over the dictionary keys:

"issues"

instead of the actual issue list.

That's why your code either skips everything or produces empty tables.

Fix build_issue_table

Replace:

for issue in sprint_data:

with:

issues = sprint_data.get("issues", [])

for issue in issues:

Full version:

def build_issue_table(self, sprint_data):

    issues = sprint_data.get("issues", [])

    html = """
    <h2>Jira Tickets</h2>

    <table border="1">
        <tr>
            <th>Key</th>
            <th>Summary</th>
            <th>Status</th>
            <th>Assignee</th>
            <th>Priority</th>
        </tr>
    """

    for issue in issues:

        html += f"""
        <tr>
            <td>{issue.get('key', '')}</td>
            <td>{issue.get('summary', '')}</td>
            <td>{issue.get('status', '')}</td>
            <td>{issue.get('assignee') or 'Unassigned'}</td>
            <td>{issue.get('priority') or 'Medium'}</td>
        </tr>
        """

    html += "</table>"

    return html
Fix build_release_notes

Replace:

for issue in sprint_data:

with:

issues = sprint_data.get("issues", [])

for issue in issues:

Full version:

def build_release_notes(self, sprint_data):

    issues = sprint_data.get("issues", [])

    html = """
    <h2>Release Notes</h2>

    <table border="1">
        <tr>
            <th>Ticket</th>
            <th>Feature</th>
            <th>Status</th>
        </tr>
    """

    for issue in issues:

        status = str(
            issue.get("status", "")
        ).lower()

        if status in [
            "done",
            "closed",
            "completed",
            "resolved"
        ]:

            html += f"""
            <tr>
                <td>{issue.get('key')}</td>
                <td>{issue.get('summary')}</td>
                <td>Released</td>
            </tr>
            """

    html += "</table>"

    return html
Better long-term fix

Instead of returning:

{
    "issues": [...]
}

from JiraAgent.execute(), return the list directly:

return issues

Then all your agents become simpler:

for issue in sprint_data:

However, if your MetricsAgent and RiskAgent already depend on:

jira_data["issues"]

keep the current structure and use:

issues = sprint_data.get("issues", [])

inside the documentation agent.

After this change, your Confluence page should show:

Key	Summary	Status
SCRUM-2	Task 2	Done
SCRUM-1	Task 1	To Do

and Release Notes should contain:

Ticket	Feature	Status
SCRUM-2	Task 2	Released

because only SCRUM-2 is in Done status.