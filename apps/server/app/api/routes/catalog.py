from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import require_role
from app.models import User, UserRole
from app.schemas.catalog import (
    CatalogMovie,
    CatalogSearchResponse,
)
from app.services.catalog import CatalogService


router = APIRouter(
    prefix="/catalog",
    tags=["Catalogue"],
)


@router.get(
    "/movies",
    response_model=CatalogSearchResponse,
)
async def search_movies(
    query: str,
    _: Annotated[
        User,
        Depends(
            require_role(UserRole.ORGANIZER),
        ),
    ],
) -> CatalogSearchResponse:

    service = CatalogService()

    try:
        results = await service.search_movies(query)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="External catalogue is currently unavailable.",
        ) from exc

    movies = [
        CatalogMovie(
            external_id=str(movie["id"]),
            title=movie["name"],
            description=movie.get("description"),
            image_url=(
                f"{movie['images'][1].get('url', '')}"
            ),
        )
        for movie in results
    ]

    return CatalogSearchResponse(results=movies)