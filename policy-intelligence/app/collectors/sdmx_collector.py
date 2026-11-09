import json
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

import requests

from app.collectors.base import BaseCollector
from app.collectors.errors import (
    CollectorHTTPError,
    CollectorNetworkError,
    CollectorValidationError,
)
from app.ingestion.base import RawDocument


class SDMXCollector(BaseCollector):
    """
    Collector for SDMX-based sources.

    Phase 1:
        Discover available dataflows and represent
        each discovered dataflow as a RawDocument.

    This collector does NOT yet download every observation
    from every dataset.

    That will be handled as a later enrichment/data-artifact
    stage.

    Supported initially:
        - OECD
        - IMF
    """

    DEFAULT_TIMEOUT = 30
    DEFAULT_RETRIES = 2

    # ---------------------------------------------------------
# Country extraction
# ---------------------------------------------------------

    def _extract_country_hints_from_text(
        self,
        *values: str | None,
    ) -> list[str]:

        text = " ".join(
            value or ""
            for value in values
        ).lower()

        country_terms = {
            "india": "India",
            "australia": "Australia",
            "united states": "United States",
            "usa": "United States",
            "united kingdom": "United Kingdom",
            "uk": "United Kingdom",
            "canada": "Canada",
            "germany": "Germany",
            "france": "France",
            "japan": "Japan",
            "china": "China",
            "brazil": "Brazil",
            "south africa": "South Africa",
            "global": "Global",
            "world": "Global",
        }

        countries = []

        for keyword, country in country_terms.items():

            if keyword in text and country not in countries:

                countries.append(country)

        return countries

    def collect(self) -> list[RawDocument]:

        collection_config = self.config.get(
            "collection",
            {},
        )

        discovery_url = collection_config.get(
            "sdmx_discovery_url"
        )

        if not discovery_url:

            raise CollectorValidationError(
                message=(
                    "No sdmx_discovery_url configured "
                    f"for source {self.source_id}"
                ),
                source_id=self.source_id,
            )

        timeout = int(
            collection_config.get(
                "timeout",
                self.DEFAULT_TIMEOUT,
            )
        )

        retries = int(
            collection_config.get(
                "retries",
                self.DEFAULT_RETRIES,
            )
        )

        content, content_type = self._fetch(
            discovery_url,
            timeout,
            retries,
        )

        documents = self._parse_dataflows(
            content=content,
            content_type=content_type,
            discovery_url=discovery_url,
        )

        return self._validate_documents(
            documents
        )

    # ---------------------------------------------------------
    # HTTP
    # ---------------------------------------------------------

    def _fetch(
        self,
        url: str,
        timeout: int,
        retries: int,
    ) -> tuple[bytes, str]:

        last_error = None

        headers = {
            "User-Agent": (
                "GlobalPolicyIntelligence/0.1"
            ),
            "Accept": (
                "application/vnd.sdmx.structure+xml;"
                "version=2.1, "
                "application/xml, "
                "application/json, "
                "text/xml, "
                "*/*"
            ),
        }

        for attempt in range(
            1,
            retries + 1,
        ):

            try:

                response = requests.get(
                    url,
                    timeout=timeout,
                    headers=headers,
                )

                if response.status_code >= 400:

                    retryable = (
                        response.status_code >= 500
                    )

                    error = CollectorHTTPError(
                        message=(
                            "SDMX request failed: "
                            f"{response.status_code}"
                        ),
                        source_id=self.source_id,
                        retryable=retryable,
                    )

                    if not retryable:
                        raise error

                    last_error = error

                    if attempt < retries:
                        time.sleep(
                            0.5 * attempt
                        )

                    continue

                return (
                    response.content,
                    response.headers.get(
                        "content-type",
                        "",
                    ),
                )

            except CollectorHTTPError:

                raise

            except requests.RequestException as exc:

                last_error = exc

                if attempt == retries:

                    raise CollectorNetworkError(
                        message=(
                            "Failed to fetch SDMX "
                            f"endpoint: {url}"
                        ),
                        source_id=self.source_id,
                    ) from exc

                time.sleep(
                    0.5 * attempt
                )

        raise CollectorNetworkError(
            message=(
                "Failed to fetch SDMX endpoint "
                f"after {retries} attempts: {url}"
            ),
            source_id=self.source_id,
        ) from last_error

    # ---------------------------------------------------------
    # Parser
    # ---------------------------------------------------------

    def _parse_dataflows(
        self,
        content: bytes,
        content_type: str,
        discovery_url: str,
    ) -> list[RawDocument]:

        documents = []

        stripped = content.lstrip()

        # -------------------------------------------------
        # JSON
        # -------------------------------------------------

        if (
            "json" in content_type.lower()
            or stripped.startswith(b"{")
            or stripped.startswith(b"[")
        ):

            try:

                payload = json.loads(
                    content.decode(
                        "utf-8"
                    )
                )

            except (
                UnicodeDecodeError,
                json.JSONDecodeError,
            ) as exc:

                raise CollectorValidationError(
                    message=(
                        "SDMX JSON response "
                        "could not be parsed"
                    ),
                    source_id=self.source_id,
                ) from exc

            documents.extend(
                self._dataflows_from_json(
                    payload,
                    discovery_url,
                )
            )

            return documents

        # -------------------------------------------------
        # XML
        # -------------------------------------------------

        try:

            root = ET.fromstring(
                content
            )

        except ET.ParseError as exc:

            raise CollectorValidationError(
                message=(
                    "SDMX response could not "
                    "be parsed as XML"
                ),
                source_id=self.source_id,
            ) from exc

        documents.extend(
            self._dataflows_from_xml(
                root,
                discovery_url,
            )
        )

        return documents

    # ---------------------------------------------------------
    # XML
    # ---------------------------------------------------------

    def _dataflows_from_xml(
        self,
        root: ET.Element,
        discovery_url: str,
    ) -> list[RawDocument]:

        documents = []

        # SDMX namespaces vary by implementation.
        # Therefore we intentionally inspect local names.
        for element in root.iter():

            if self._local_name(
                element.tag
            ) != "Dataflow":
                continue

            dataflow_id = (
                element.attrib.get("id")
                or element.attrib.get(
                    "ID"
                )
            )

            agency_id = (
                element.attrib.get(
                    "agencyID"
                )
                or element.attrib.get(
                    "agencyId"
                )
                or ""
            )

            version = (
                element.attrib.get(
                    "version"
                )
                or ""
            )

            name = self._find_text(
                element,
                "Name",
            )

            description = self._find_text(
                element,
                "Description",
            )

            if not dataflow_id:

                continue

            title = (
                name
                or dataflow_id
            )

            external_id = (
                f"{self.source_id}:"
                f"{agency_id}:"
                f"{dataflow_id}:"
                f"{version}"
            )

            documents.append(
                self._build_document(
                    external_id=external_id,
                    title=title,
                    description=description,
                    dataflow_id=dataflow_id,
                    agency_id=agency_id,
                    version=version,
                    discovery_url=discovery_url,
                )
            )

        return documents

    # ---------------------------------------------------------
    # JSON
    # ---------------------------------------------------------

    def _dataflows_from_json(
        self,
        payload,
        discovery_url: str,
    ) -> list[RawDocument]:

        documents = []

        dataflows = []

        if isinstance(
            payload,
            dict,
        ):

            # Common SDMX-JSON structure
            dataflows = (
                payload.get(
                    "dataflows",
                    []
                )
                or payload.get(
                    "Dataflows",
                    []
                )
            )

            # Some APIs wrap structures.
            if not dataflows:

                structures = payload.get(
                    "structures",
                    {}
                )

                if isinstance(
                    structures,
                    dict,
                ):

                    dataflows = (
                        structures.get(
                            "dataflows",
                            []
                        )
                    )

        if not isinstance(
            dataflows,
            list,
        ):

            return documents

        for dataflow in dataflows:

            if not isinstance(
                dataflow,
                dict,
            ):
                continue

            dataflow_id = (
                dataflow.get(
                    "id"
                )
                or dataflow.get(
                    "ID"
                )
            )

            if not dataflow_id:
                continue

            agency_id = (
                dataflow.get(
                    "agencyID"
                )
                or dataflow.get(
                    "agencyId"
                )
                or ""
            )

            version = (
                dataflow.get(
                    "version"
                )
                or ""
            )

            name = self._extract_json_text(
                dataflow.get(
                    "name"
                )
            )

            description = (
                self._extract_json_text(
                    dataflow.get(
                        "description"
                    )
                )
            )

            title = (
                name
                or dataflow_id
            )

            external_id = (
                f"{self.source_id}:"
                f"{agency_id}:"
                f"{dataflow_id}:"
                f"{version}"
            )

            documents.append(
                self._build_document(
                    external_id=external_id,
                    title=title,
                    description=description,
                    dataflow_id=dataflow_id,
                    agency_id=agency_id,
                    version=version,
                    discovery_url=discovery_url,
                )
            )

        return documents

    def _extract_countries(
        self,
        title: str | None,
        description: str | None,
    ) -> list[str]:

        text = " ".join(
            [
                title or "",
                description or "",
            ]
        ).lower()

        countries = []

        country_aliases = {
            "india": ["india", "ind"],
            "australia": ["australia", "aus"],
            "canada": ["canada", "can"],
            "united states": [
                "united states",
                "usa",
                "us",
                "united states of america",
            ],
            "united kingdom": [
                "united kingdom",
                "uk",
                "great britain",
            ],
            "germany": ["germany", "deu"],
            "france": ["france", "fra"],
            "japan": ["japan", "jpn"],
            "china": ["china", "chn"],
            "brazil": ["brazil", "bra"],
            "south africa": [
                "south africa",
                "zaf",
            ],
        }

        for country, aliases in country_aliases.items():

            if any(
                alias in text
                for alias in aliases
            ):
                countries.append(country)

        return countries

    # ---------------------------------------------------------
    # RawDocument
    # ---------------------------------------------------------

    def _build_document(
        self,
        external_id: str,
        title: str,
        description: str | None,
        dataflow_id: str,
        agency_id: str,
        version: str,
        discovery_url: str,
        countries: list[str] | None = None,
        country_scope: str = "unknown",
    ) -> RawDocument:

        content_parts = [
            f"SDMX Dataflow: {title}",
            f"Dataflow ID: {dataflow_id}",
        ]

        if agency_id:
            content_parts.append(
                f"Agency: {agency_id}"
            )

        if version:
            content_parts.append(
                f"Version: {version}"
            )

        if description:
            content_parts.append(
                description
            )

        return RawDocument(
            external_id=external_id,
            title=title,
            source_url=discovery_url,
            source_id=self.source_id,
            source_name=self.config.get(
                "name",
                self.source_id,
            ),
            content="\n".join(content_parts),
            metadata={
                "collector": "sdmx",
                "discovery_url": discovery_url,
                "dataflow_id": dataflow_id,
                "agency_id": agency_id,
                "version": version,
                "artifact_type": "sdmx_dataflow",

                # -----------------------------------------
                # Country metadata
                # -----------------------------------------

                "countries": (
                    countries
                    if countries is not None
                    else []
                ),

                "country_scope": country_scope,
            },
        )
    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _local_name(
        tag: str,
    ) -> str:

        return tag.split(
            "}",
            1
        )[-1]

    @classmethod
    def _find_text(
        cls,
        element: ET.Element,
        local_name: str,
    ) -> str | None:

        for child in element.iter():

            if cls._local_name(
                child.tag
            ) == local_name:

                if child.text:

                    value = child.text.strip()

                    if value:
                        return value

        return None

    @staticmethod
    def _extract_json_text(
        value,
    ) -> str | None:

        if isinstance(
            value,
            str,
        ):
            return value.strip()

        if isinstance(
            value,
            list,
        ):

            for item in value:

                if isinstance(
                    item,
                    str,
                ):
                    return item.strip()

                if isinstance(
                    item,
                    dict,
                ):

                    if item.get(
                        "value"
                    ):
                        return str(
                            item["value"]
                        ).strip()

        if isinstance(
            value,
            dict,
        ):

            if value.get(
                "value"
            ):
                return str(
                    value["value"]
                ).strip()

        return None