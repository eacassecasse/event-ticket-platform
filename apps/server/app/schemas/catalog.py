from pydantic import BaseModel


class CatalogMovie(BaseModel):
    external_id: str
    title: str
    description: str | None = None
    image_url: str | None = None


class CatalogSearchResponse(BaseModel):
    results: list[CatalogMovie]