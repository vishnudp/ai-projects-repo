from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.ingestion.base import RawDocument


# =========================================================
# Result
# =========================================================

@dataclass
class DataflowFilterResult:
    """
    Result of evaluating a single SDMX dataflow.
    """

    document: RawDocument

    score: float

    matched_terms: list[str] = field(
        default_factory=list
    )

    matched_sectors: list[str] = field(
        default_factory=list
    )

    matched_countries: list[str] = field(
        default_factory=list
    )

    reasons: list[str] = field(
        default_factory=list
    )


# =========================================================
# Filter
# =========================================================

class DataflowFilter:
    """
    Lightweight relevance filter for discovered SDMX
    dataflows.

    Responsibilities:

        - Evaluate discovered dataflows
        - Match configurable sector keywords
        - Match configurable country keywords
        - Use country metadata when available
        - Calculate relevance score
        - Rank candidates
        - Limit candidates

    This class does NOT:

        - make HTTP requests
        - retrieve datasets
        - parse observations
        - persist data
        - invoke an LLM
    """

    def __init__(
        self,
        config: dict[str, Any] | None = None,
    ) -> None:

        self.config = config or {}

        # -------------------------------------------------
        # Scoring configuration
        # -------------------------------------------------

        self.min_score = float(
            self.config.get(
                "min_score",
                0.20,
            )
        )

        self.max_candidates = int(
            self.config.get(
                "max_candidates",
                100,
            )
        )

        # -------------------------------------------------
        # Sector configuration
        # -------------------------------------------------

        self.sectors = (
            self._normalize_mapping(
                self.config.get(
                    "sectors",
                    {},
                )
            )
        )

        # -------------------------------------------------
        # Country configuration
        # -------------------------------------------------

        self.countries = (
            self._normalize_mapping(
                self.config.get(
                    "countries",
                    {},
                )
            )
        )

        # -------------------------------------------------
        # General keywords
        # -------------------------------------------------

        self.additional_keywords = (
            self._normalize_list(
                self.config.get(
                    "keywords",
                    [],
                )
            )
        )

    # =====================================================
    # Public API
    # =====================================================

    def filter(
        self,
        documents: list[RawDocument],
        primary_country: str | None = None,
        comparison_countries: list[str] | None = None,
    ) -> list[DataflowFilterResult]:

        comparison_countries = (
            comparison_countries or []
        )

        results: list[
            DataflowFilterResult
        ] = []

        for document in documents:

            result = self._evaluate(
                document=document,
                primary_country=primary_country,
                comparison_countries=(
                    comparison_countries
                ),
            )

            if result.score >= self.min_score:

                results.append(
                    result
                )

        # -------------------------------------------------
        # Highest relevance first
        # -------------------------------------------------

        results.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        return results[
            : self.max_candidates
        ]

    # =====================================================
    # Evaluation
    # =====================================================

    def _evaluate(
        self,
        document: RawDocument,
        primary_country: str | None,
        comparison_countries: list[str],
    ) -> DataflowFilterResult:

        text = self._document_text(
            document
        )

        matched_terms: list[str] = []

        matched_sectors: list[str] = []

        matched_countries: list[str] = []

        reasons: list[str] = []

        score = 0.0

        # -------------------------------------------------
        # Country metadata
        #
        # This will be populated later from SDMX
        # structure/dataset metadata.
        #
        # For now we safely consume it if present.
        # -------------------------------------------------

        document_countries = (
            document.metadata or {}
        ).get(
            "countries",
            [],
        )

        if not isinstance(
            document_countries,
            list,
        ):

            document_countries = []

        # Normalize metadata countries

        normalized_document_countries = [
            self._normalize_country(
                country
            )
            for country
            in document_countries
            if isinstance(
                country,
                str,
            )
        ]

        # -------------------------------------------------
        # Sector matching
        # -------------------------------------------------

        for sector, keywords in (
            self.sectors.items()
        ):

            sector_matched = []

            for keyword in keywords:

                if self._contains(
                    text,
                    keyword,
                ):

                    sector_matched.append(
                        keyword
                    )

                    if (
                        keyword
                        not in matched_terms
                    ):

                        matched_terms.append(
                            keyword
                        )

            if sector_matched:

                matched_sectors.append(
                    sector
                )

                score += min(
                    0.40,
                    0.15
                    * len(
                        sector_matched
                    ),
                )

                reasons.append(
                    f"Sector match: {sector}"
                )

        # -------------------------------------------------
        # Country matching
        # -------------------------------------------------

        requested_countries: list[str] = []

        if primary_country:

            requested_countries.append(
                primary_country
            )

        requested_countries.extend(
            comparison_countries
        )

        # Remove duplicates while preserving order

        requested_countries = list(
            dict.fromkeys(
                requested_countries
            )
        )

        for country in requested_countries:

            if not isinstance(
                country,
                str,
            ):
                continue

            country_key = (
                self._find_mapping_key(
                    country,
                    self.countries,
                )
            )

            country_keywords = (
                self.countries.get(
                    country_key,
                    [country],
                )
            )

            # ---------------------------------------------
            # Match against title / description / content
            # ---------------------------------------------

            text_match = False

            matched_country_keyword = None

            for keyword in country_keywords:

                if self._contains(
                    text,
                    keyword,
                ):

                    text_match = True

                    matched_country_keyword = (
                        keyword
                    )

                    break

            # ---------------------------------------------
            # Match against document country metadata
            # ---------------------------------------------

            normalized_requested_country = (
                self._normalize_country(
                    country
                )
            )

            metadata_match = (
                normalized_requested_country
                in normalized_document_countries
            )

            # ---------------------------------------------
            # Match result
            # ---------------------------------------------

            if (
                text_match
                or metadata_match
            ):

                if (
                    country
                    not in matched_countries
                ):

                    matched_countries.append(
                        country
                    )

                if (
                    matched_country_keyword
                    and
                    matched_country_keyword
                    not in matched_terms
                ):

                    matched_terms.append(
                        matched_country_keyword
                    )

                elif (
                    metadata_match
                    and country
                    not in matched_terms
                ):

                    matched_terms.append(
                        country
                    )

                score += 0.15

                if metadata_match:

                    reasons.append(
                        "Country metadata match: "
                        f"{country}"
                    )

                else:

                    reasons.append(
                        "Country text match: "
                        f"{country}"
                    )

        # -------------------------------------------------
        # General keywords
        # -------------------------------------------------

        keyword_matches = 0

        for keyword in (
            self.additional_keywords
        ):

            if self._contains(
                text,
                keyword,
            ):

                if (
                    keyword
                    not in matched_terms
                ):

                    matched_terms.append(
                        keyword
                    )

                keyword_matches += 1

        if keyword_matches:

            score += min(
                0.30,
                0.05
                * keyword_matches,
            )

            reasons.append(
                "General keyword matches: "
                f"{keyword_matches}"
            )

        # -------------------------------------------------
        # Metadata quality bonus
        # -------------------------------------------------

        if document.title:

            score += 0.05

        if document.content:

            score += 0.05

        # -------------------------------------------------
        # Cap score
        # -------------------------------------------------

        score = min(
            score,
            1.0,
        )

        # -------------------------------------------------
        # Result
        # -------------------------------------------------

        return DataflowFilterResult(
            document=document,

            score=round(
                score,
                4,
            ),

            matched_terms=matched_terms,

            matched_sectors=matched_sectors,

            matched_countries=(
                matched_countries
            ),

            reasons=reasons,
        )

    # =====================================================
    # Document Text
    # =====================================================

    @staticmethod
    def _document_text(
        document: RawDocument,
    ) -> str:

        parts = [
            document.title or "",
            document.content or "",
        ]

        description = (
            document.metadata or {}
        ).get(
            "description",
            "",
        )

        if description:

            parts.append(
                str(description)
            )

        return " ".join(
            parts
        ).lower()

    # =====================================================
    # String Matching
    # =====================================================

    @staticmethod
    def _contains(
        text: str,
        keyword: str,
    ) -> bool:

        if not text:
            return False

        if not keyword:
            return False

        return (
            keyword.lower()
            in text.lower()
        )

    # =====================================================
    # Country Normalization
    # =====================================================

    @staticmethod
    def _normalize_country(
        country: str,
    ) -> str:

        if not isinstance(
            country,
            str,
        ):

            return ""

        return (
            country
            .strip()
            .lower()
            .replace(
                "_",
                " ",
            )
            .replace(
                "-",
                " ",
            )
        )

    # =====================================================
    # Mapping Helpers
    # =====================================================

    @staticmethod
    def _normalize_list(
        values,
    ) -> list[str]:

        if not values:

            return []

        if isinstance(
            values,
            str,
        ):

            values = [
                values
            ]

        return [
            str(value)
            .strip()
            .lower()
            for value in values
            if str(value).strip()
        ]

    @classmethod
    def _normalize_mapping(
        cls,
        mapping,
    ) -> dict[str, list[str]]:

        if not isinstance(
            mapping,
            dict,
        ):

            return {}

        result = {}

        for key, values in (
            mapping.items()
        ):

            normalized_key = (
                str(key)
                .strip()
                .lower()
            )

            result[
                normalized_key
            ] = cls._normalize_list(
                values
            )

        return result

    @staticmethod
    def _find_mapping_key(
        value: str,
        mapping: dict[str, list[str]],
    ) -> str:

        normalized = (
            value
            .strip()
            .lower()
        )

        if normalized in mapping:

            return normalized

        return normalized