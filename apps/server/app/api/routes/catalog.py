import httpx
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import require_role, get_http_client
from app.models import User, UserRole
from app.schemas.catalog import (
    CatalogSearchResponse,
    CatalogEvent
)
from app.services.catalog import CatalogService


router = APIRouter(
    prefix="/catalog",
    tags=["Catalogue"],
)


def get_catalog_service(
          http_client: Annotated[
                    httpx.AsyncClient,
                    Depends(get_http_client),
                ]
        ) -> CatalogService:
        return CatalogService(http_client)

@router.get(
    "/events",
    response_model=CatalogSearchResponse,
)
async def search_events(
    _: Annotated[
        User,
        Depends(
            require_role(UserRole.ORGANIZER),
        ),
    ],
    service: Annotated[
        CatalogService,
        Depends(get_catalog_service)
        ],
    keyword: str | None = None,
    page: int = Query(
        default=0,
        ge=0,
    ),
    size: int = Query(
        default=20,
        ge=1,
        le=50,
    ),
    city: list[str] | None = Query(
        default=None,
    ),
    country_code: str | None = None,
    classification_name: list[str] | None = Query(
        default=None,
    ),
    start_date_time: str | None = None,
    end_date_time: str | None = None,
) -> CatalogSearchResponse:

    try:
        return await service.search_events(
            keyword=keyword,
            page=page,
            size=size,
            city=city,
            country_code=country_code,
            classification_name=classification_name,
            start_date_time=start_date_time,
            end_date_time=end_date_time,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                "External catalogue is currently unavailable."
            ),
        ) from exc

@router.get(
    "/events/{external_id}",
    response_model=CatalogEvent,
)
async def get_catalog_event(
    external_id: str,
    _: Annotated[
        User,
        Depends(
            require_role(UserRole.ORGANIZER),
        ),
    ],
    service: Annotated[
        CatalogService,
        Depends(get_catalog_service)
    ],
) -> CatalogEvent:

    try:
        event = await service.get_event(
            external_id,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                "External catalogue is currently unavailable."
            ),
        ) from exc

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Catalogue event not found.",
        )

    return event