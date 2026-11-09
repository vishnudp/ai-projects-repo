from agents.jira_agent import JiraAgent
from agents.metrics_agent import MetricsAgent
from agents.risk_agent import RiskAgent
from agents.summary_agent import SummaryAgent
from agents.documentation_agent import DocumentationAgent


class DocumentationWorkflow:

    def run(
        self,
        project_key,
        sprint_id
    ):

        jira_data = JiraAgent().execute(
            project_key,
            sprint_id
        )

        metrics = MetricsAgent().execute(
            jira_data
        )

        risk = RiskAgent().execute(
            metrics
        )

        summary = SummaryAgent().execute(
            metrics,
            risk
        )

        return DocumentationAgent().execute(
            jira_data,
            metrics,
            risk,
            summary
        )