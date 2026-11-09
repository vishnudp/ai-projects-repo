from tools.jira_tool import JiraTool

class JiraAgent:

    def execute(self, project, sprint):

        jira = JiraTool(
            url="https://testv.atlassian.net/",
            username="vishnubansalcomp@gmail.com",
            token="ATATT3xFfGF0htUGLcfXUEXwI7UGveMWUc72GDxDUMDOQlFtrgksbme93homBtrnVZPXK52Mb99RebagU2aGsYZPKK87Gta1YQnZ6OA4cf8jmhaJVizGhLWWbIFMYFhbc34-nso8DikfJ5RJKFmsJNtSNfI6GQiXvXIyytRlRLOCoc_4B4LIePY=3DCBE909"
        )

        issues = jira.get_sprint_issues(
            project,
            sprint
        )

        print(issues)
        
        return {
            "issues": issues
        }

    def get_completed_issues(self,project_key,sprint_id):
        
        issues = JiraTool(
            url="https://testv.atlassian.net/",
            username="vishnubansalcomp@gmail.com",
            token="ATATT3xFfGF0htUGLcfXUEXwI7UGveMWUc72GDxDUMDOQlFtrgksbme93homBtrnVZPXK52Mb99RebagU2aGsYZPKK87Gta1YQnZ6OA4cf8jmhaJVizGhLWWbIFMYFhbc34-nso8DikfJ5RJKFmsJNtSNfI6GQiXvXIyytRlRLOCoc_4B4LIePY=3DCBE909"
        ).get_completed_issues(
            project_key,
            sprint_id
        )

        return [
            {
                "key": issue.key,
                "summary": issue.fields.summary
            }
            for issue in issues
        ]
    
    def get_open_issues(self,project_key,sprint_id):
        
        issues = JiraTool(
            url="https://testv.atlassian.net/",
            username="vishnubansalcomp@gmail.com",
            token="ATATT3xFfGF0htUGLcfXUEXwI7UGveMWUc72GDxDUMDOQlFtrgksbme93homBtrnVZPXK52Mb99RebagU2aGsYZPKK87Gta1YQnZ6OA4cf8jmhaJVizGhLWWbIFMYFhbc34-nso8DikfJ5RJKFmsJNtSNfI6GQiXvXIyytRlRLOCoc_4B4LIePY=3DCBE909"
        ).get_open_issues(
            project_key,
            sprint_id
        )

        return [
            {
                "key": issue.key,
                "summary": issue.fields.summary
            }
            for issue in issues
        ]