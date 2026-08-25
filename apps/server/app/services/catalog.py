from typing import Any

import httpx

from app.core.config import get_settings


class CatalogService:
    """Client for the external movie catalogue."""

    BASE_URL = "https://app.ticketmaster.com/discovery/v2/"

    def __init__(self) -> None:
        self.settings = get_settings()

    async def search_movies(
        self,
        query: str,
    ) -> list[dict[str, Any]]:
        """Search movies in Tickemaster."""

        if not self.settings.TICKETMASTER_API_KEY:
            raise RuntimeError(
                "Ticketmaster API key is not configured."
            )

        params = {
            "api_key": self.settings.TICKETMASTER_API_KEY,
            "query": query,
            "language": "pt-PT",
            "include_adult": False,
        }

        async with httpx.AsyncClient(
            timeout=10.0,
        ) as client:
            response = await client.get(
                f"{self.BASE_URL}/events",
                params=params,
            )

        response.raise_for_status()

        data = response.json()

        return data["_embedded"].get("events", [])