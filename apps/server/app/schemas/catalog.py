from datetime import date, time

from pydantic import BaseModel, Field, HttpUrl


class CatalogImage(BaseModel):
    """Image associated with an external catalogue event."""

    url: HttpUrl
    ratio: str | None = None
    width: int | None = None
    height: int | None = None
    fallback: bool = False


class CatalogDate(BaseModel):
    """Normalized event date information."""

    local_date: date | None = None
    local_time: time | None = None
    timezone: str | None = None
    date_tba: bool = False
    date_tbd: bool = False
    time_tba: bool = False


class CatalogLocation(BaseModel):
    """Normalized event location information."""

    name: str | None = None
    city: str | None = None
    state: str | None = None
    state_code: str | None = None
    country: str | None = None
    country_code: str | None = None
    postal_code: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class CatalogClassification(BaseModel):
    """Normalized event classification."""

    segment: str | None = None
    genre: str | None = None
    sub_genre: str | None = None
    type: str | None = None
    sub_type: str | None = None


class CatalogEvent(BaseModel):
    """Application representation of an external catalogue event."""

    external_id: str
    provider: str

    title: str
    description: str | None = None

    event_type: str | None = None
    url: HttpUrl | None = None
    locale: str | None = None

    images: list[CatalogImage] = Field(
        default_factory=list,
    )

    date: CatalogDate | None = None
    location: CatalogLocation | None = None
    classification: CatalogClassification | None = None


class CatalogPagination(BaseModel):
    """Pagination information returned by the catalogue."""

    page: int
    size: int
    total_elements: int
    total_pages: int


class CatalogSearchResponse(BaseModel):
    """Paginated catalogue search response."""

    results: list[CatalogEvent]
    pagination: CatalogPagination