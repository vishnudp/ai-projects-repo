from dataclasses import dataclass, field


@dataclass
class DocumentClassification:
    """
    Document-level classification.

    Classification is independent of source scope and may
    contain multiple values in every dimension.
    """

    countries: list[str] = field(default_factory=list)

    sectors: list[str] = field(default_factory=list)

    policy_domains: list[str] = field(default_factory=list)

    topics: list[str] = field(default_factory=list)
