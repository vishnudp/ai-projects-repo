from jira import JIRA

class JiraTool:

    def __init__(self, url, username, token):
        self.client = JIRA(
            server=url,
            basic_auth=(username, token)
        )

    def get_sprint_issues(self, project, sprint_id):

        jql = f"project={project} and sprint={sprint_id}"

        issues = self.client.search_issues(
            jql,
            maxResults=500
        )

        result = []

        for issue in issues:

            result.append({
                "key": issue.key,
                "summary": issue.fields.summary,
                "status": issue.fields.status.name,
                "priority": issue.fields.priority.name
                if issue.fields.priority else None,
                "assignee":
                    issue.fields.assignee.displayName
                    if issue.fields.assignee else None,
                "created": str(issue.fields.created),
                "resolutionDate":
                    str(issue.fields.resolutiondate)
            })

        return result
    
    def get_completed_issues(self, project_key, sprint_id):
        jql = f"project = {project_key} AND sprint = {sprint_id} AND statusCategory = Done"

        return self.client.search_issues(
            jql,
            maxResults=100
        )

    def get_open_issues(self,project_key,sprint_id):

        jql = f"project = {project_key} AND sprint = {sprint_id} AND statusCategory != Done"

        return self.client.search_issues(
            jql,
            maxResults=100
        )
    