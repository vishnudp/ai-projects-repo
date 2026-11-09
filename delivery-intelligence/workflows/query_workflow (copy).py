# from agents.intent_agent import IntentAgent
# from agents.jira_agent import JiraAgent
# from workflows.sprint_report import SprintReportWorkflow


# class QueryWorkflow:

#     def run(
#         self,
#         question,
#         project_key,
#         sprint_id
#     ):

#         intent = IntentAgent().execute(question)
#         action = intent["action"]
#         print("Intent:", intent)

#         if action == "completed_issues":
#             return JiraAgent().get_completed_issues(
#                 project_key,
#                 sprint_id
#             )

#         elif action == "open_issues":
#             return JiraAgent().get_open_issues(
#                 project_key,
#                 sprint_id
#             )

#         elif action == "bugs":
#             return JiraAgent().get_open_bugs(
#                 project_key,
#                 sprint_id
#             )
        
#         elif action == "sprint_health":
#             return SprintReportWorkflow().run(
#                 project_key,
#                 sprint_id
#             )

#         return {
#             "message": "Intent not supported"
#         }

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

        result = self.matcher.classify(
            question
        )

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