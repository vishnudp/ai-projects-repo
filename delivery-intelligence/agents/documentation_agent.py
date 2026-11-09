import os
from google import genai


class DocumentationAgent:

    def execute(
        self,
        sprint_data,
        metrics,
        risk,
        summary
    ):

        prompt = f"""
You are a Release Manager.

Create:

1. Executive Summary
2. Release Notes
3. Deployment Guide

Sprint Metrics:
{metrics}

Risk:
{risk}

Summary:
{summary}

Issues:
{sprint_data}
"""

        client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        try:

            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt
            )

            ai_content = response.text

        except Exception as e:

            print("Gemini Error:", e)

            ai_content = f"""
            <h2>Executive Summary</h2>

            <p>
            Sprint Completion:
            {metrics.get('completion_rate', 0)}%
            </p>

            <p>
            Risk:
            {risk.get('risk', 'UNKNOWN')}
            </p>

            <p>
            Reasons:
            {", ".join(risk.get('reasons', []))}
            </p>

            <p>
            AI analysis unavailable because Gemini quota was exceeded.
            </p>
            """

        html = f"""
        <h1>Sprint Delivery Intelligence Report</h1>

        <h2>AI Analysis</h2>

        {ai_content}

        <h2>Sprint Metrics</h2>

        <table border="1">
            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Total Issues</td>
                <td>{metrics.get('total', 0)}</td>
            </tr>
            <tr>
                <td>Completed Issues</td>
                <td>{metrics.get('completed', 0)}</td>
            </tr>
            <tr>
                <td>Completion Rate</td>
                <td>{metrics.get('completion_rate', 0)}%</td>
            </tr>
            <tr>
                <td>Risk</td>
                <td>{risk.get('risk', 'UNKNOWN')}</td>
            </tr>
        </table>
        """

        html += self.build_issue_table(
            sprint_data
        )

        html += self.build_release_notes(
            sprint_data
        )

        html += self.build_deployment_guide()

        return html

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
        issues = sprint_data.get("issues", [])
        for issue in issues:

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
        issues = sprint_data.get("issues", [])
        for issue in issues:

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

    def build_deployment_guide(
        self
    ):

        return """
        <h2>Deployment Guide</h2>

        <table border="1">
            <tr>
                <th>Step</th>
                <th>Description</th>
            </tr>

            <tr>
                <td>1</td>
                <td>Deploy application package</td>
            </tr>

            <tr>
                <td>2</td>
                <td>Run DB migrations</td>
            </tr>

            <tr>
                <td>3</td>
                <td>Restart services</td>
            </tr>

            <tr>
                <td>4</td>
                <td>Execute smoke tests</td>
            </tr>

            <tr>
                <td>5</td>
                <td>Validate Jira stories marked Done</td>
            </tr>

            <tr>
                <td>6</td>
                <td>Execute regression suite</td>
            </tr>

            <tr>
                <td>7</td>
                <td>Business sign-off</td>
            </tr>

        </table>
        """