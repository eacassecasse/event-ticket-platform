from typing import Any

import httpx
from app.core.config import get_settings
from app.schemas.catalog import (
    CatalogClassification,
    CatalogDate,
    CatalogEvent,
    CatalogImage,
    CatalogLocation,
    CatalogPagination,
    CatalogSearchResponse,
)


class CatalogService:
    """Service for interacting with the external event catalogue."""

    BASE_URL = (
        "https://app.ticketmaster.com/discovery/v2"
    )

    PROVIDER = "ticketmaster"

    def __init__(
            self,
            http_client: httpx.AsyncClient
            ) -> None:
        self.settings = get_settings()
        self.http_client = http_client

    def _build_params(
        self,
        *,
        keyword: str | None = None,
        page: int = 0,
        size: int = 20,
        sort: str = "relevance,desc",
        city: list[str] | None = None,
        country_code: str | None = None,
        classification_name: list[str] | None = None,
        start_date_time: str | None = None,
        end_date_time: str | None = None,
    ) -> dict[str, Any]:
        """Build only the Ticketmaster parameters we need."""

        params: dict[str, Any] = {
            "apikey": self.settings.TICKETMASTER_API_KEY,
            "page": page,
            "size": size,
            "sort": sort,
            "includeTest": "no",
        }

        optional_params = {
            "keyword": keyword,
            "city": city,
            "countryCode": country_code,
            "classificationName": classification_name,
            "startDateTime": start_date_time,
            "endDateTime": end_date_time,
        }

        params.update(
            {
                key: value
                for key, value in optional_params.items()
                if value is not None
            }
        )

        return params

    @staticmethod
    def _map_images(
        event: dict[str, Any],
    ) -> list[CatalogImage]:

        return [
            CatalogImage(
                url=image["url"],
                ratio=image.get("ratio"),
                width=image.get("width"),
                height=image.get("height"),
                fallback=image.get(
                    "fallback",
                    False,
                ),
            )
            for image in event.get("images", [])
            if image.get("url")
        ]

    @staticmethod
    def _map_date(
        event: dict[str, Any],
    ) -> CatalogDate | None:

        dates = event.get("dates")

        if not dates:
            return None

        start = dates.get("start", {})

        local_date = start.get("localDate")
        local_time = start.get("localTime")

        return CatalogDate(
            local_date=local_date,
            local_time=local_time,
            timezone=dates.get("timezone"),
            date_tba=(
                start.get("dateTBA", False)
            ),
            date_tbd=(
                start.get("dateTBD", False)
            ),
            time_tba=(
                start.get("timeTBA", False)
            ),
        )

    @staticmethod
    def _map_location(
        event: dict[str, Any],
    ) -> CatalogLocation | None:

        venues = (
            event.get("_embedded", {})
            .get("venues", [])
        )

        if not venues:
            return None

        venue = venues[0]

        city = venue.get("city", {})
        state = venue.get("state", {})
        country = venue.get("country", {})
        address = venue.get("address", {})
        location = venue.get("location", {})

        return CatalogLocation(
            name=venue.get("name"),
            city=city.get("name"),
            state=state.get("name"),
            state_code=state.get("stateCode"),
            country=country.get("name"),
            country_code=country.get("countryCode"),
            postal_code=venue.get("postalCode"),
            address=address.get("line1"),
            latitude=location.get("latitude"),
            longitude=location.get("longitude"),
        )

    @staticmethod
    def _map_classification(
        event: dict[str, Any],
    ) -> CatalogClassification | None:

        classifications = event.get(
            "classifications",
            [],
        )

        if not classifications:
            return None

        classification = classifications[0]

        segment = classification.get(
            "segment",
            {},
        )

        genre = classification.get(
            "genre",
            {},
        )

        sub_genre = classification.get(
            "subGenre",
            {},
        )

        event_type = classification.get(
            "type",
            {},
        )

        sub_type = classification.get(
            "subType",
            {},
        )

        return CatalogClassification(
            segment=segment.get("name"),
            genre=genre.get("name"),
            sub_genre=sub_genre.get("name"),
            type=event_type.get("name"),
            sub_type=sub_type.get("name"),
        )

    def _map_event(
        self,
        event: dict[str, Any],
    ) -> CatalogEvent:

        return CatalogEvent(
            external_id=str(event["id"]),
            provider=self.PROVIDER,
            title=event["name"],
            description=event.get("description"),
            event_type=event.get("type"),
            url=event.get("url"),
            locale=event.get("locale"),
            images=self._map_images(event),
            date=self._map_date(event),
            location=self._map_location(event),
            classification=self._map_classification(event),
        )

    async def search_events(
        self,
        *,
        keyword: str | None = None,
        page: int = 0,
        size: int = 20,
        sort: str = "relevance,desc",
        city: list[str] | None = None,
        country_code: str | None = None,
        classification_name: list[str] | None = None,
        start_date_time: str | None = None,
        end_date_time: str | None = None,
    ) -> CatalogSearchResponse:

        if not self.settings.TICKETMASTER_API_KEY:
            raise RuntimeError(
                "Ticketmaster API key is not configured."
            )

        params = self._build_params(
            keyword=keyword,
            page=page,
            size=size,
            sort=sort,
            city=city,
            country_code=country_code,
            classification_name=classification_name,
            start_date_time=start_date_time,
            end_date_time=end_date_time,
        )

        async with self.http_client as client:

            response = await client.get(
                f"{self.BASE_URL}/events.json",
                params=params,
            )

            response.raise_for_status()

        data = response.json()

        events = (
            data
            .get("_embedded", {})
            .get("events", [])
        )

        pagination = data.get(
            "page",
            {},
        )

        return CatalogSearchResponse(
            results=[
                self._map_event(event)
                for event in events
            ],
            pagination=CatalogPagination(
                page=pagination.get("number", page),
                size=pagination.get("size", size),
                total_elements=pagination.get(
                    "totalElements",
                    0,
                ),
                total_pages=pagination.get(
                    "totalPages",
                    0,
                ),
            ),
        )

    async def get_event(
        self,
        external_id: str,
    ) -> CatalogEvent | None:

        if not self.settings.TICKETMASTER_API_KEY:
            raise RuntimeError(
                "Ticketmaster API key is not configured."
            )

        params = {
            "apikey": self.settings.TICKETMASTER_API_KEY,
            "id": external_id,
            "size": 1,
        }

        async with self.http_client as client:

            response = await client.get(
                f"{self.BASE_URL}/events.json",
                params=params,
            )

            response.raise_for_status()

        events = (
            response.json()
            .get("_embedded", {})
            .get("events", [])
        )

        if not events:
            return None

        return self._map_event(events[0])