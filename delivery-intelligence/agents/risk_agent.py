class RiskAgent:

    def execute(self, metrics):

        reasons = []

        risk = "LOW"

        if metrics["completion_rate"] < 70:
            risk = "HIGH"
            reasons.append(
                "Completion below threshold"
            )

        return {
            "risk": risk,
            "reasons": reasons
        }