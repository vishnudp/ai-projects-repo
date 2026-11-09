from workflows.documentation_workflow import DocumentationWorkflow
from tools.confluence_tool import ConfluenceTool


class PublishWorkflow:

    def run(
        self,
        project_key,
        sprint_id
    ):

        content = DocumentationWorkflow().run(
            project_key,
            sprint_id
        )

        page = ConfluenceTool().create_or_update_page(
            space="SCRUM",
            title=f"{project_key}-Sprint-{sprint_id}",
            body=content
        )

        return page