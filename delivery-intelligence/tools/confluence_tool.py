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