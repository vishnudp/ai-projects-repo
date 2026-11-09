from fastapi import FastAPI
from agents.jira_agent import JiraAgent
from workflows.query_workflow import (
    QueryWorkflow
)

from workflows.sprint_report import (
    SprintReportWorkflow
)

from workflows.documentation_workflow import (
    DocumentationWorkflow
)

from workflows.publish_workflow import PublishWorkflow

app = FastAPI()


@app.get("/sprint-report/{project_key}/{sprint_id}")
def report(
    project_key: str,
    sprint_id: int
):


    return SprintReportWorkflow().run(
        project_key,
        sprint_id
    )


@app.get("/sprint-report/{project_key}/{sprint_id}/completed")
def completed(
    project_key: str,
    sprint_id: int
):
    return JiraAgent().get_completed_issues(
        project_key,
        sprint_id
    )


@app.get("/sprint-report/{project_key}/{sprint_id}/open")
def open_items(
    project_key: str,
    sprint_id: int
):
    return JiraAgent().get_open_issues(
        project_key,
        sprint_id
    )

@app.get("/ask")
def ask(
    question: str,
    project_key: str,
    sprint_id: int
):
    return QueryWorkflow().run(
        question,
        project_key,
        sprint_id
    )

@app.get(
    "/generate-docs/{project_key}/{sprint_id}"
)
def generate_docs(
    project_key: str,
    sprint_id: int
):

    return DocumentationWorkflow().run(
        project_key,
        sprint_id
    )

@app.get(
    "/sprint-report/{project_key}/{sprint_id}/publish"
)
def publish(
    project_key: str,
    sprint_id: int
):

    return PublishWorkflow().run(
        project_key,
        sprint_id
    )
