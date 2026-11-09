class MetricsAgent:

    def execute(self, sprint_data):

        issues = sprint_data["issues"]

        total = len(issues)

        completed = len([
            i for i in issues
            if i["status"] == "Done"
        ])

        completion_rate = (
            completed / total * 100
        ) if total else 0

        return {
            "total": total,
            "completed": completed,
            "completion_rate":
                round(completion_rate, 2)
        }