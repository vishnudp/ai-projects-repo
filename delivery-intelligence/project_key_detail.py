from jira import JIRA

print("Step 1: Starting")

try:
    jira = JIRA(
        server="https://testv.atlassian.net/",
        basic_auth=("vishnubansalcomp@gmail.com", "ATATT3xFfGF0htUGLcfXUEXwI7UGveMWUc72GDxDUMDOQlFtrgksbme93homBtrnVZPXK52Mb99RebagU2aGsYZPKK87Gta1YQnZ6OA4cf8jmhaJVizGhLWWbIFMYFhbc34-nso8DikfJ5RJKFmsJNtSNfI6GQiXvXIyytRlRLOCoc_4B4LIePY=3DCBE909")
    )

    
    print(jira.myself())
    print("Step 2: Connected")

    projects = jira.projects()

    print("Step 3: Projects fetched")
    print(projects)
    

except Exception as e:
    print("ERROR:")
    print(str(e))

try:
    issue = jira.issue("SCRUM-1")

    print(issue.key)
    print(issue.fields.summary)

except Exception as e:
    print("ERROR:", e)

for board in jira.boards():
    print(f"Board: {board.id} - {board.name}")

    try:
        sprints = jira.sprints(board.id)

        for sprint in sprints:
            print(
                f"  Sprint ID={sprint.id}, "
                f"Name={sprint.name}, "
                f"State={sprint.state}"
            )

    except Exception as e:
        print(e)