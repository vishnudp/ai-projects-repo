from nlp.semantic_matcher import SemanticMatcher
from agents.jira_agent import JiraAgent
from workflows.sprint_report import SprintReportWorkflow


class QueryWorkflow:

    def __init__(self):
        self.matcher = SemanticMatcher()

    def run(
        self,
        question,
        project_key,
        sprint_id
    ):

        result = self.matcher.classify(question)

        print("Intent:", result)

        intent = result["intent"]

        if intent == "completed_issues":
            return JiraAgent().get_completed_issues(
                project_key,
                sprint_id
            )

        elif intent == "open_issues":
            return JiraAgent().get_open_issues(
                project_key,
                sprint_id
            )

        elif intent == "sprint_health":
            return SprintReportWorkflow().run(
                project_key,
                sprint_id
            )

        return {
            "message": "Unsupported query"
        }