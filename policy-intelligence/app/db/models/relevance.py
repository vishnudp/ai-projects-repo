from dataclasses import dataclass


@dataclass
class RelevanceScore:
    """
    Explainable document relevance.

    Scores are normalized between 0.0 and 1.0.
    """

    overall: float = 0.0
    policy_relevance: float = 0.0
    country_relevance: float = 0.0
    novelty: float = 0.0
    evidence_quality: float = 0.0

    def validate(self) -> None:
        values = {
            "overall": self.overall,
            "policy_relevance": self.policy_relevance,
            "country_relevance": self.country_relevance,
            "novelty": self.novelty,
            "evidence_quality": self.evidence_quality,
        }

        for name, value in values.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"{name} must be between 0.0 and 1.0"
                )
